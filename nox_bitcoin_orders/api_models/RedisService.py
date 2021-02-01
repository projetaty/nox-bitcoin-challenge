#!/usr/bin/env python3
"""
Created on 20210128
Update on 20210201
@author: Sandro Regis Cardoso
"""
import sys # @UnusedImport
import redis
from redis.exceptions import ConnectionError
from nox_utils.Utils import Utils # @UnusedImport
import logging # @UnusedImport
from time import sleep  # @UnusedImport
import ast
from nox_bitcoin_orders.api_models.BtcOrderBook import BtcOrderBook
from nox_bitcoin_orders.api_models.RedisSingleton import RedisServer

log = logging.getLogger("Order Book")

class RedisService(object):
    '''
    @Description: Class for store BTC data retrieved from external data source and for stores customers trading 
                  selling and purchase offers
    @author: Sandro Regis Cardoso | Software Eng.
    @TODO: Run performance tests overall methods
    '''
    _name = "redis.service"
    
    
    __SELLING_OFFERS = []
    __PURCHASE_OFFERS = []
    __REDIS_QUEUE_SERVICE = object
    
    def __init__(self):
        #, config_data:dict=None
        try:
            log.debug("Creating Redis Service class object.......")
        except:
            log.error("Exception on create objects %s" %BaseException)
    
    
    
    def __createRedisService(self, __boot_config):
        try:
            self.__REDIS_QUEUE_SERVICE = RedisServer().setConnection(
                                    __boot_config['host'], 
                                    __boot_config['port'], 
                                    __boot_config['db'], 
                                    __boot_config['password'])
            ping = self.__REDIS_QUEUE_SERVICE.ping()
            if ping:
                self.__REDIS_QUEUE_SERVICE.flushdb(asynchronous=True) #for development only
                return self.__REDIS_QUEUE_SERVICE
        except:
            log.error("Exception to create Redis Service %s" %ConnectionError)
    
    
    
    def createRedisServiceInstance(self, config:dict) -> redis:
        try:
            log.debug("Create Redis Service instance.......")
            instance = self.__createRedisService(config)
            return instance
        except:
            log.error("Exception on getRedisServiceInstance %s" %BaseException)
            #raise ConnectionError
    
    
    
    def getRedisServiceInstance(self) -> redis:
        try:
            log.debug("Return Redis Service instance.......")
            instance = self.__REDIS_QUEUE_SERVICE
            return instance
        except:
            log.error("Exception on getRedisServiceInstance %s" %BaseException)
            #raise ConnectionError
    
    
    
    def __checkDataIntegrity(self, lst:list, idx:int) -> bool:
        try:
            log.debug("Running __checkDataIntegrity")
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
            log.error("Method __checkDataIntegrity exception %s" %BaseException)
    
    
    
    def __chargeBtcAsksBidsToQueue(self, asks:list, bids:list):
        #@Note: This method will replace both methods bellow
        NotImplemented
    
    
    
    def __chargeBTCAsksToQueue(self, url:str, alternativeUrl:str=None) -> list:
        try:
            __orderBook = BtcOrderBook()
            __response = __orderBook.getBtcOrderBook(url, alternativeUrl)
            
            if __response is not None:
                #pointer for test only
                pointer = 0
                
                #Revert the list for calculations
                __asksOrders = __response.get("asks")[::-1]
                log.debug("ASKS ORDER BOOK RESPONSE %s" %__asksOrders)
                
                for idx, lst in enumerate(__asksOrders):
                    #Basic validation of values from external sources
                    __isValid = self.__checkDataIntegrity(lst, idx)
                    if __isValid == False:
                        #@TODO: NOTIFY SUPPORT
                        pass
                    else:
                        self.__REDIS_QUEUE_SERVICE.rpush("btc_asks", "%s"%lst)
                        pointer += 1
                        if pointer == 10:
                            break
                    
                    del(idx)
                    del(lst)
                
                self.__SELLING_OFFERS = self.__REDIS_QUEUE_SERVICE.lrange('btc_asks', 0, -1)
                log.debug("Selling Offers (Queue %s) %s" %("asks", self.__SELLING_OFFERS))
                return self.__SELLING_OFFERS
        except:
            log.error("Method __chargeBTCAsksQueue exception %s" %Exception)
            #raise Exception
    
    
    
    def __chargeBTCBidsToQueue(self, url:str, alternativeUrl:str=None) -> list:
        try:
            __orderBook = BtcOrderBook()
            __response = __orderBook.getBtcOrderBook(url, alternativeUrl)
            
            if __response is not None:
                #pointer for test only
                pointer = 0
                
                #Revert the list for calculations
                __bidsOrders = __response.get("bids")[::-1]
                log.debug("BIDS ORDER BOOK RESPONSE %s" %__bidsOrders)
                
                for idx, lst in enumerate(__bidsOrders):
                    #Basic validation of values from external sources
                    __isValid = self.__checkDataIntegrity(lst, idx)
                    if __isValid == False:
                        #@TODO: NOTIFY SUPPORT
                        pass
                    else:
                        self.__REDIS_QUEUE_SERVICE.rpush("btc_bids", "%s"%lst)
                        pointer += 1
                        if pointer == 10:
                            break
                    
                    del(idx)
                    del(lst)
                
                self.__PURCHASE_OFFERS = self.__REDIS_QUEUE_SERVICE.lrange('btc_bids', 0, -1)
                log.debug("Purchase Offers (Queue %s) %s" %("bids", self.__PURCHASE_OFFERS))
                return self.__PURCHASE_OFFERS
        except:
            log.error("Method __chargeBTCBidsToQueue exception %s" %Exception)
            #raise Exception
    
    
    
    def initializeRedisAskBidQueues(self, redisConf:dict, url:str, alternativeUrl:str = None) -> list:
        try:
            log.debug("Running initializeRedisAskBidQueues")
            #self.__REDIS_QUEUE_SERVICE = self.__createRedisService(redisConf)
            asks = self.__chargeBTCAsksToQueue(url)
            bids = self.__chargeBTCBidsToQueue(url)
            return asks, bids
        except:
            log.error("Method initializeRedisAskBidQueues exception %s" %Exception)
            #raise Exception
    
    
    
    def getBTCSellings(self) -> list:
        try:
            #sellingOffers = []
            sellingOffers = self.__SELLING_OFFERS
            return sellingOffers
            
            for lsts in self.__SELLING_OFFERS:
                sellingOffers.append(ast.literal_eval(lsts.decode('utf-8')))
                del(lsts)
            
            return sellingOffers
        except:
            log.error("Method getBTCSellings exception %s" %Exception)
            #raise Exception

    
    
    



























