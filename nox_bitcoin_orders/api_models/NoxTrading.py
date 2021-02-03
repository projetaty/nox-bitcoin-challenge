#!/usr/bin/env python3
"""
Created on 20210128
Update on 20210201
@author: Sandro Regis Cardoso
"""

from redis.exceptions import RedisError
import logging
from nox_bitcoin_orders.api_models.RedisService import RedisService
import ast
from time import sleep

log = logging.getLogger("Order Book")


class NoxTrading(object):
    '''
    @Description: ....
    @author: Sandro Regis Cardoso | Software Eng.
    @TODO: Run performance tests overall methods
           Split this class to NoxTradingAsks and NoxTradingBids
    '''
    
    _name = "nox.trading"
    
    _ASKSPRICELIST = []
    _BIDPRICESLIST = []
    _AVERAGEASKPRICE = 0.0
    _AVERAGEBIDPRICE = 0.0
    _AVAILABLEBTC = 0.0
    
    def __init__(self):
        log.debug("Creating NoxTrading class object")
        self.__objRedisService = RedisService()
        self.__mountListOfAsksBidsPrices()
        self.__calcTotalAsksOffer()
        self.__calcAverageBidMarket()
    
    
    
    def __mountListOfAsksBidsPrices(self) -> list:
        try:
            log.debug("Running __mountListOfAsksBidsPrices")
            asksPriceList = []
            bidsPriceList = []
            
            _sellingOffers = self.__objRedisService.getBTCSellings()
            for askVals in _sellingOffers:
                asksPriceList.append(ast.literal_eval(askVals))
            
            self._ASKSLIST = asksPriceList
            sleep(0.007)
            
            _purchaseOffers = self.__objRedisService.getBTCPurchases()
            for bidVals in _purchaseOffers:
                bidsPriceList.append(ast.literal_eval(bidVals))
            
            self._BIDPRICESLIST = bidsPriceList
        except:
            log.critical("Method __mountListOfAsks exception %s" %Exception)
            raise Exception
    
    
    
    def __calcTotalAsksOffer(self):
        try:
            _sumAsksPrice = 0
            _sumAsksQty   = 0
            for asks in self._ASKSLIST:
                _sumAsksPrice += asks[0]
                _sumAsksQty += asks[1]
                del(asks)
            
            self._AVAILABLEBTC = _sumAsksQty
            self._AVERAGEASKPRICE = (_sumAsksPrice / len(self._ASKSLIST))
            log.info("AVERAGE OF BITCOINS PRICE FOR SELLING %s" %self._AVERAGEASKPRICE)
            log.info("TOTAL OF BITCOINS FOR SELLING %s" %_sumAsksQty)
        except:
            log.exception("Method __calcAverageAskMarket exception %s" %Exception)
            raise Exception
    
    
    
    def __calcAverageBidMarket(self):
        try:
            _sumBidsPrice = 0
            _sumBidsQty   = 0
            for bids in self._BIDPRICESLIST:
                _sumBidsPrice += bids[0]
                _sumBidsQty += bids[1]
                del(bids)
            
            self._AVERAGEBIDPRICE = (_sumBidsPrice / len(self._BIDPRICESLIST))
            log.info("AVERAGE OF BITCOINS PRICE FOR PURCHASE %s" %self._AVERAGEBIDPRICE)
            log.info("TOTAL OF BITCOINS PURCHASE REQUESTS %s" %_sumBidsQty)
        except:
            log.exception("Method __calcAverageBidMarket exception %s" %Exception)
            raise Exception
    
    
    
    def calcOrder(self, orderType:str, btcQty:float = 0.0) -> bool:
        #@Descritpion: This should be an implementation of abstract method
        try:
            if orderType == "ask":
                maxSalePrice = float(self._BIDPRICESLIST[0][0])
                transactionAmount = (maxSalePrice * float(btcQty))
            elif orderType == "bid":
                maxPurchasePrice = float(self._ASKSLIST[0][0])
                log.info("preço %s" %float(self._ASKSLIST[0][0]))
                transactionAmount = (maxPurchasePrice * float(btcQty))
            
            self.addTradingToNoxQueue(orderType, btcQty=float(btcQty))
            return transactionAmount
        except:
            log.critical("Method calcOrder exception %s" %Exception)
            raise Exception
    
    
    
    def checkRequestForSaleOffer(self, btcAmount:float = 0.0, btcQty:float = 0.0) -> bool:
        #Check if bitcoin is equal or higher valid ask
        NotImplemented
    
    
    
    
    def addTradingToNoxQueue(self, orderType:str, customerID="000001", btcQty:float=0.0):
        try:
            lst = [customerID, btcQty]
            _redidConn = self.__objRedisService.getRedisQueueInstance()
            _redidConn.rpush("nox_btc_%s"%orderType, "%s"%lst)
            
            added = _redidConn.lrange("nox_btc_%s"%orderType, 0, -1)
            log.debug("Added Trading %s" %added)
        except:
            raise RedisError
    
    
    
    
    def checkBtcQtyAvailable(self, btcQty:float) -> bool:
        """
        @Description: This method do some security calculation for trading having base on 30% of total amount of available BTC in market
                      It is a dummy validation which may doesn't apply to reality
        @TODO: Create input for agreement on proposed quantity
        """
        try:
            if (self._AVAILABLEBTC * 0.3) > float(btcQty):
                return True
            elif (self._AVAILABLEBTC * 0.3) < float(btcQty):
                print("Não existe esta quantidade de %s bitcoins disponíveis para compra." %btcQty)
                print("Ou a quantidade desejada excede nosso limite possível para hoje.")
                print("Podemos lhe assegurar a aquisição de %s do total de bitcoins disponíveis hoje no mercado" %"30%")
                print("Estimativa do total para aquisão hoje é de: %s %s" %((self._AVAILABLEBTC * 0.3), "BTC"))
                print("Preço total estimatdo para esta aquisição é de: R$%s" %(self.calcOrder("bid", (self._AVAILABLEBTC * 0.3))))
        except:
            raise Exception
    
    
    
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
            log.debug("Exception: %s" %Exception)
            raise Exception
    
    
    
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
            log.debug("Exception: %s" %Exception)
            raise Exception
    
    
    
    def __findClosest(self, param:float) -> float:
        NotImplemented
    
    
    
    def findUpperClosestAsk(self, _givenBid:float) -> float:
        #@TODO: Unify this calculation in __findClosest. Need to validate calculation
        try:
            __givenBid = _givenBid
            _knowAsksList = self.sellingOffers.copy()
            # @fix: Pass a list only with float values [0.1, 0.2, 0.3]
            _computedCloser = lambda __unknowValue : abs(__unknowValue + __givenBid)
            _closestUpperValue = max(_knowAsksList, key=_computedCloser)
            return _closestUpperValue
        except:
            log.debug("Exception: %s" %Exception)
            raise Exception
    
    
    
    def __findLowerClosestAsk(self, _givenBid:float) -> float:
        #@TODO: Unify this calculation in __findClosest. Need to validate calculation
        try:
            __givenBid = _givenBid
            _knowAsksList = self.sellingOffers.copy()
            _computedCloser = lambda __unknowValue : float(__unknowValue - [__givenBid])
            _closestUpperValue = max(_knowAsksList, key=_computedCloser)
            return _closestUpperValue
        except:
            log.debug("Exception: %s" %Exception)
            raise Exception





