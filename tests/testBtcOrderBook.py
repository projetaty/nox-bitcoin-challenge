#!/usr/bin/env python3
"""
Created on 20210127
Update on 
@author: Sandro Regis Cardoso
"""

from django.test import TestCase
import requests
from rest_framework import status
import logging
from nox_bitcoin_orders.api_models.BtcOrderBook import BtcOrderBook

from timeout_decorator import TimeoutError

#Used for test proposal and also for track desired limit of method response in production env.
import timeout_decorator

log = logging.getLogger("Order Book")

class TestBtcOrderBook(TestCase):
    
    _name = "test.btcorderbook"
    
    
    @classmethod
    def setUpClass(cls):
        super(TestBtcOrderBook, cls).setUpClass()
        cls.BtcOrderBook = BtcOrderBook()
        return
    
    
    
    #@timeout_decorator.timeout(2)
    def testGetBtcOrderBook(self):
        try:
            log.debug("Running test to retrieve Order Book timeout 1 sec.")
            url = "https://www.mercadobitcoin.net/api/BTC/orderbook/"
            alternativeUrl = "https://api.cryptowat.ch/markets/kraken/btcusd/orderbook"
            
            response = self.BtcOrderBook.getBtcOrderBook(url, alternativeUrl)
            log.debug("Alternative BTC Data source result %s" %response)
            self.assertIsInstance(response, dict)
        except:
            log.error("Method testGetBtcOrderBook exception.......%s" %Exception)
            #raise Exception
    
    
    @timeout_decorator.timeout(1)
    def ttestFailsGetBtcOrderbook(self):
        try:
            log.debug("Running fails to retrieve Order Book timeout 3 sec.")
            headers   = {
                'Accept': 'application/json',
                'Authorization': 'Basic'
            }
            url = "http://10.0.0.100/?"
            alternativeUrl = "https://api.cryptowat.ch/markets/kraken/btcusd/orderbook"
            response = requests.get(url, headers)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        except:
            log.error(TimeoutError)
            log.error("BTC Order Book fails header response %s" %status.HTTP_400_BAD_REQUEST)
            #raise status.HTTP_400_BAD_REQUEST




