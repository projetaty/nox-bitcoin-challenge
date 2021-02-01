#!/usr/bin/env python3
"""
Created on 20210129
Update on 20210201
@author: Sandro Regis Cardoso
"""

import requests
import logging
import json
from nox_utils.Utils import Utils  # @UnusedImport

log = logging.getLogger("Order Book")

class BtcOrderBook(object):
    '''
    @Description: ....
    @author: Sandro Regis Cardoso | Software Eng.
    @TODO: Run performance tests overall methods
           Change this class name to BtcAtivities
    '''
    
    _name = "btc.bookorders"
    
    
    def __getApiHeader(self):
        """
        @TODO: Read this infos from config
        @author: Sandro Regis Cardoso | Software Eng.
        """
        try:
            headers   = {
                'Accept': 'application/json',
                'Authorization': 'Basic'
            }
            return headers
        except:
            log.error("Method __getApiHeader exception.......%s" %Exception)
            #raise Exception
    
    
    
    def getBtcOrderBook(self, url:str = None, alternativeUrl:str=None) -> dict:
        try:
            response = self.__retrieveExternalEndpointData(url)
            return response
        except:
            log.error("Method getBtcOrderBook exception.......%s" %Exception)
            log.warning("Trying to read alternative BTC data source after fails.......");
            response = self.readAlternativeBtcDataSource(alternativeUrl)
            if len(response).__gt__(0):
                return response
            else:
                log.critical("No data source for order book found. Exception.......%s" %Exception)
                log.warning("Nox Trading Service will be halted")
                #@TODO: SEND MAIL ALERT TO NOTIFY SEV. 0 very critical problem
                #raise Exception
            quit()
    
    
    
    def getBtcTicker(self, url:str) -> dict:
        #See: https://www.mercadobitcoin.com.br/api-doc/
        #Sample bellow:
        #{
        #    "ticker": {
        #        "high":"192100.00000000",
        #        "low":"182000.00000000",
        #        "vol":"217.89391458",
        #        "last":"186410.01471000", not in order book
        #        "buy":"186410.01571000", not in order book
        #        "sell":"186999.79780000", not in order book
        #        "open":"188800.07001000",
        #        "date":1612032260
        #    }
        #}
        NotImplemented
    
    
    
    def getBtcTrade(self, url:str) -> dict:
        #See: https://www.mercadobitcoin.com.br/api-doc/
        NotImplemented
    
    
    
    def getBtcTradeSince(self, url:str) -> dict:
        #See: https://www.mercadobitcoin.com.br/api-doc/
        NotImplemented
    
    
    
    def getBtcTradeFrom(self, url:str, date:str) -> dict:
        #See: https://www.mercadobitcoin.com.br/api-doc/
        #@Note: date in timestamp
        NotImplemented
    
    
    
    def getBtcTradeFromTo(self, url:str, startDate:str, endDate:str) -> dict:
        #See: https://www.mercadobitcoin.com.br/api-doc/
        #@Note: startDate/endDate in timestamp
        NotImplemented
    
    
    
    def getBtcDaySumary(self, url:str, year:str, month:str, day:str) -> dict:
        #See: https://www.mercadobitcoin.com.br/api-doc/
        #@Note: startDate/endDate in timestamp
        #@Sample: https://www.mercadobitcoin.net/api/BTC/day-summary/2013/6/20/
        NotImplemented
    
    
    
    def __parseDatasourceResponse(self, data:dict) -> dict:
        try:
            listOfResponseKeys = [*data]
            if listOfResponseKeys[0].__eq__("asks") and listOfResponseKeys[1].__eq__("bids"):
                return data
            else:
                for idx, v in enumerate(listOfResponseKeys):
                    nestedDict = data.get(v)
                    res = [*nestedDict]
                    if res[idx].__eq__("asks") and res[idx+1].__eq__("bids"):
                        del(res)
                        del(v)
                        del(idx)
                        return nestedDict
                    
                    del(res)
                    del(nestedDict)
                    del(v)
                    del(idx)
        except:
            log.error("Method __parseDatasourceResponse exception.......%s" %Exception)
            #raise Exception
    
    
    
    def __retrieveExternalEndpointData(self, url):
        """
        @TODO: Implement method to read dict keys and find the asks and bids position
                in reason of different response format from data sources
        @sample: return [*dict] list only dict keys
        @author: Sandro Regis Cardoso | Software Eng.
        """
        try:
            header = self.__getApiHeader()
            response = requests.get(url, header)
            response = json.loads(response.text)
            del(header)
            del(url)
            return self.__parseDatasourceResponse(response)
        except:
            log.error("Method __retrieveExternalEndpointData exception.......%s" %Exception)
            #pass
            #raise Exception
    
    
    
    def __readAlternativeBtcDataSource(self, __alternativeUrl:str=None) -> dict:
        """
        @Description: This method intend to lookup data from alternative data source
        @method_type: protected
        @TODO: Pick up from config alternative BTC data source
        @author: Sandro Regis Cardoso | Software Eng.
        """
        try:
            __response = None
            if __alternativeUrl != None:
                __response = self.__retrieveExternalEndpointData(__alternativeUrl)
            
            return __response
        except:
            log.error("Method __readAlternativeBtcDataSource exception.......%s" %Exception)
            #raise Exception
    
    
    
    def readAlternativeBtcDataSource(self, alternativeUrl:str = None) -> dict:
        """
        @Description: This method intend to lookup data from alternative data source
        @method_type: public
        @TODO: Pick up from config alternative BTC data source
        @author: Sandro Regis Cardoso | Software Eng.
        """
        try:
            response = self.__readAlternativeBtcDataSource(alternativeUrl)
            return response
        except:
            log.critical("Method readAlternativeBtcDataSource exception.......%s" %Exception)
            #raise Exception
    














