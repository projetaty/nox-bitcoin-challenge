#!/usr/bin/env python3
"""
Created on 20210128
Update on 20210201
@author: Sandro Regis Cardoso
"""
import sys # @UnusedImport
import redis
from redis.exceptions import ConnectionError, ExecAbortError, DataError
from nox_utils.Utils import Utils # @UnusedImport
import logging # @UnusedImport
from time import sleep  # @UnusedImport

from nox_bitcoin_orders.api_models.BtcOrderBook import BtcOrderBook
from nox_bitcoin_orders.api_models.RedisSingleton import RedisServer

log = logging.getLogger("Order Book")


class RedisServiceSingleton(type):
    _name = "redisservice.singleton"
    _instances = {}
    
    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super(RedisServiceSingleton, self).__call__(*args, **kwargs)
        return self._instances[self]

class RedisService(object):
    '''
    @Description: Class for store BTC data retrieved from external data source and for stores customers trading 
                  selling and purchase offers
    @author: Sandro Regis Cardoso | Software Eng.
    @TODO: Create Timer for update Redis Queue;
           Run performance tests overall methods;
    '''
    _name = "redis.service"
    __metaclass__   =   RedisServiceSingleton
    
    global _SELLING_OFFERS
    global _PURCHASE_OFFERS
    global _REDIS_QUEUE_SERVICE
    
    
    def __createRedisService(self, __boot_config) -> redis:
        try:
            _redisConn = RedisServer().setConnection(
                                    __boot_config['host'], 
                                    __boot_config['port'], 
                                    __boot_config['db'], 
                                    __boot_config['password'])
            ping = _redisConn.ping()
            if ping:
                _redisConn.flushdb(asynchronous=True) #for development only
                return _redisConn
        except:
            log.error("Exception to create Redis Service %s" %ConnectionError)
            raise ConnectionError
    
    
    
    def chargeBTCAsksToQueue(self, url:str, alternativeUrl:str=None) -> list:
        try:
            log.debug("Charging BTC Asks Queues.......")
            global _SELLING_OFFERS
            _SELLING_OFFERS = self.__chargeBTCAsksToQueue(url, alternativeUrl)
            return _SELLING_OFFERS
        except:
            log.error("Exception on chargeBTCAsksToQueue %s" %ExecAbortError)
            raise ExecAbortError
    
    
    
    def chargeBTCBidsToQueue(self, url:str, alternativeUrl:str=None) -> list:
        """
        @Description: Charge Asks and Bids to Redis Queue
        """
        try:
            global _PURCHASE_OFFERS
            _PURCHASE_OFFERS = self.__chargeBTCBidsToQueue(url, alternativeUrl)
            return _PURCHASE_OFFERS
        except:
            log.error("Exception on chargeBTCBidsToQueue %s" %ExecAbortError)
            raise ExecAbortError
    
    
    
    def createRedisServiceInstance(self, config:dict) -> bool:
        """
        @Description: Open Redis Connection
        """
        try:
            log.debug("Create Redis Service instance.......")
            global _REDIS_QUEUE_SERVICE
            _REDIS_QUEUE_SERVICE = self.__createRedisService(config)
            return _REDIS_QUEUE_SERVICE
        except:
            log.error("Exception on createRedisServiceInstance %s" %ExecAbortError)
            raise ExecAbortError
    
    
    
    def getRedisQueueInstance(self) -> redis:
        """
        @Description: Return existing Redis Connection
        """
        try:
            log.debug("Return Redis Service instance.......")
            instance = _REDIS_QUEUE_SERVICE
            return instance
        except:
            log.error("Exception on getRedisServiceInstance %s" %ExecAbortError)
            raise ExecAbortError
    
    
    
    def __checkDataIntegrity(self, lst:list, idx:int) -> bool:
        """
        @Description: Check for data integrity before add to Redis Queue
        """
        try:
            __zero  = 0.0
            __empty = ""
            if __zero in lst:
                #@TODO: NOTIFY SUPPORT
                log.warning("0.0 value Not allowed value Exception at list index %s" %idx)
                return False
            if __empty in lst:
                #@TODO: NOTIFY SUPPORT
                log.warning("Empty value Not allowed value Exception at list index %s" %idx)
                return False
        except:
            log.error("Method __checkDataIntegrity exception %s" %DataError)
            raise DataError
    
    
    
    def __chargeBtcAsksBidsToQueue(self, asks:list, bids:list):
        #@Note: This method will replace both methods bellow
        NotImplemented
    
    
    
    def __chargeBTCAsksToQueue(self, url:str, alternativeUrl:str=None) -> list:
        try:
            __orderBook = BtcOrderBook()
            _response = __orderBook.getBtcOrderBook(url, alternativeUrl)
            
            if _response is not None:
                #pointer for test only
                pointer = 0
                
                #Revert the list for calculations
                _asksOrders = _response.get("asks")[::-1]
                for idx, lst in enumerate(_asksOrders):
                    #Basic validation of values from external sources
                    _isValid = self.__checkDataIntegrity(lst, idx)
                    if _isValid == False:
                        #@TODO: NOTIFY SUPPORT
                        pass
                    else:
                        _REDIS_QUEUE_SERVICE.rpush("btc_asks", "%s"%lst)
                        pointer += 1
                        if pointer == 250:
                            sleep(0.07)
                            pointer = 0
                    
                    del(idx)
                    del(lst)
                
                sellings = _REDIS_QUEUE_SERVICE.lrange('btc_asks', 0, -1)
                return sellings
        except:
            log.error("Method __chargeBTCAsksQueue exception %s" %DataError)
            raise DataError
    
    
    
    def __chargeBTCBidsToQueue(self, url:str, alternativeUrl:str=None) -> list:
        try:
            __orderBook = BtcOrderBook()
            _response = __orderBook.getBtcOrderBook(url, alternativeUrl)
            
            if _response is not None:
                #pointer for test only
                pointer = 0
                
                #Revert the list for calculations
                _bidsOrders = _response.get("bids")[::-1]
                
                for idx, lst in enumerate(_bidsOrders):
                    #Basic validation of values from external sources
                    _isValid = self.__checkDataIntegrity(lst, idx)
                    if _isValid == False:
                        #@TODO: NOTIFY SUPPORT
                        pass
                    else:
                        _REDIS_QUEUE_SERVICE.rpush("btc_bids", "%s"%lst)
                        pointer += 1
                        if pointer == 250:
                            sleep(0.07)
                            pointer = 0
                    
                    del(idx)
                    del(lst)
                
                purchases = _REDIS_QUEUE_SERVICE.lrange('btc_bids', 0, -1)
                return purchases
        except:
            log.error("Method __chargeBTCBidsToQueue exception %s" %DataError)
            raise DataError
    
    
    
    def getBTCSellings(self) -> list:
        try:
            sellingOffers = _SELLING_OFFERS
            return sellingOffers
        except:
            log.error("Method getBTCSellings exception %s" %DataError)
            raise DataError
    
    
    
    def getBTCPurchases(self) -> list:
        try:
            purchaseOffers = _PURCHASE_OFFERS
            return purchaseOffers
        except:
            log.error("Method getBTCPurchases exception %s" %DataError)
            raise DataError































