#!/usr/bin/env python3
"""
Created on 20210128
Update on 20210201
@author: Sandro Regis Cardoso
"""

from redis.exceptions import RedisError
import logging

log = logging.getLogger("Order Book")

class NoxTrading(object):
    '''
    @Description: ....
    @author: Sandro Regis Cardoso | Software Eng.
    @TODO: Run performance tests overall methods
           Split this class to NoxTradingAsks and NoxTradingBids
    '''
    
    _name = "nox.trading"
    
    __ASKSPRICELIST = []
    __BIDPRICESLIST = []
    
    def __init__(self):
        log.debug("Creating NoxTrading class object")
        #self.__objRedisService = RedisService()
        """
        self.sellingOffers = __RedisService.getBTCSellings()
        sleep(0.007)
        #self.purchaseOffers = __RedisService.getBTCPurchases()
        #sleep(0.007)
        self.__mountListOfAsksBidsPrices()
        sleep(0.007)
        self.__calcAverageAskMarket()
        """
    
    
    
    def __mountListOfAsksBidsPrices(self) -> list:
        try:
            asksPriceList = []
            bidsPriceList = []  # @UnusedVariable
            for vals in self.sellingOffers:
                asksPriceList.append(vals[0])
            
            self.__ASKSLIST = asksPriceList
            #self.__BIDSLIST = bidsPriceList
            #return self.__ASKSPRICELIST, self.__BIDPRICESLIST
            return self.__ASKSPRICELIST
        except:
            log.critical("Method __mountListOfAsks exception %s" %Exception)
            raise Exception
    
    
    
    def __registerOrder(self, orderType:str, btcAmount:float = 0.0, btcQty:float = 0.0) -> bool:
        #@Descritpion: This should be an implementation of abstract method
        try:
            pass
        except:
            log.critical("Method __registerMarketOrder exception %s" %RedisError)
            raise Exception
    
    
    
    def __calcAverageAskMarket(self):
        try:
            __sumAsksPrice = 0
            __sumAsksQty   = 0
            for asks in self.sellingOffers:
                __sumAsksPrice =+ asks[0]
                __sumAsksQty =+ asks[1]
                del(asks)
            average = (__sumAsksQty / __sumAsksPrice)
            log.info("AVERAGE BITCOIN SELLING PRICE %s" %average)
        except:
            log.exception("Method __calcAverageAskMarket exception %s" %BaseException)
            raise BaseException
    
    
    
    def __calcAverageBidMarket(self):
        try:
            __sumBidsPrice = 0
            __sumBidsQty   = 0
            for bids in self.purchaseOffers:
                __sumBidsPrice =+ bids[0]
                __sumBidsQty =+ bids[1]
                del(bids)
            average = (__sumBidsQty / __sumBidsPrice)
            log.info("AVERAGE BITCOIN PURCHASE PRICE %s" %average)
        except:
            log.exception("Method __calcAverageBidMarket exception %s" %BaseException)
            raise BaseException
    
    
    
    def checkRequestForSaleOffer(self, btcAmount:float = 0.0, btcQty:float = 0.0) -> bool:
        #Check if bitcoin is equal or higher valid ask
        NotImplemented
    
    
    
    def __setBTCSaleOffer(self, btcAmount:float = 0.0, btcQty:float = 0.0) -> list:
        try:
            _asks = self.__splitJsonResponseByTag("asks")
            
            for idx, lst in enumerate(_asks):
                #Basic validation of values from external sources
                __isValid = self.__checkDataIntegrity(lst, idx)
                if __isValid == False:
                    #@TODO: NOTIFY SUPPORT
                    pass
                else:
                    self.__REDIS_SERVICE.rpush("btc_asks", "%s"%lst)
                
                del(idx)
                del(lst)
            
            
            log.debug("Selling Offers (Queue %s) %s" %("asks", self.__REDIS_SERVICE.lrange('btc_asks', 0, -1)))
            redis_key = self.__REDIS_SERVICE.lrange('btc_asks', 0, -1)
            return redis_key
        except:
            log.error("Method testChargeBTCAsksQueue exception %s" %RedisError)
            raise RedisError
    
    
    
    def checkRequestForByuOffer(self, btcAmount:float = 0.0, btcQty:float = 0.0) -> bool:
        NotImplemented
    
    
    
    def findSellingByMatchPrice(self, bid:float)->bool:
        try:            
            for ask in self.sellingOffers:
                if bid.__eq__(ask[0]):
                    log.debug("MATCH DE OFERTA DE VENDA: $%s" %bid)
                    log.debug("ESTE VALOR CORRESPONDE A COMPRA DE: %s %s" %(ask[1], "Bitcoins"))
                    #print("\n\nMATCH DE OFERTA DE VENDA: $%s" %bid)
                    #print("ESTE VALOR CORRESPONDE A COMPRA DE: %s %s" %(ask[1], "Bitcoins"))
                    del(ask)
                    del(bid)
                    return True
                elif not bid.__eq__(ask[0]):
                    #log.debug("SEM MATCH DE OFERTA DE VENDA PARA: $%s" %bid)
                    #print("SEM MATCH DE OFERTA DE VENDA PARA: $%s" %bid)
                    del(ask)
                    pass
        except:
            log.debug("Exception: %s" %BaseException)
            raise BaseException
    
    
    
    def findSellingByMatchQuantity(self, qty:float)->bool:
        try:
            for ask in self.sellingOffers:
                if qty.__eq__(ask[1]):
                    log.debug("MATCH DE OFERTA DE VENDA: %s" %qty)
                    log.debug("A QTD. DESEJA PODE SER ADQUIRIDA PELO VALOR: %s" %ask[0])
                    #print("\n\nMATCH DE OFERTA DE VENDA: %s" %qty)
                    #print("A QTD. DESEJA PODE SER ADQUIRIDA PELO VALOR: %s" %ask[0])
                    del(ask)
                    del(qty)
                    return True
                elif not qty.__eq__(ask[1]):
                    #log.debug("SEM MATCH DE OFERTA DE VENDA PARA: %s" %qty)
                    #print("SEM MATCH DE OFERTA DE VENDA PARA: %s" %qty)
                    del(ask)
                    pass
        except:
            log.debug("Exception: %s" %BaseException)
            raise BaseException
        
    
    
    def __findClosest(self, param:float) -> float:
        NotImplemented
    
    
    
    def findUpperClosestAsk(self, _givenBid:float) -> float:
        #@TODO: Unify this calculation in __findClosest
        try:
            __givenBid = _givenBid
            _knowAsksList = self.sellingOffers.copy()
            # @fix: Pass a list only with float values [0.1, 0.2, 0.3]
            _computedCloser = lambda __unknowValue : abs(__unknowValue + __givenBid)
            _closestUpperValue = max(_knowAsksList, key=_computedCloser)
            return _closestUpperValue
        except:
            log.debug("Exception: %s" %BaseException)
            raise Exception
    
    
    
    def __findLowerClosestAsk(self, _givenBid:float) -> float:
        #@TODO: Unify this calculation in __findClosest
        try:
            __givenBid = _givenBid
            _knowAsksList = self.sellingOffers.copy()
            _computedCloser = lambda __unknowValue : float(__unknowValue - [__givenBid])
            _closestUpperValue = max(_knowAsksList, key=_computedCloser)
            return _closestUpperValue
        except:
            log.debug("Exception: %s" %BaseException)
            raise Exception





