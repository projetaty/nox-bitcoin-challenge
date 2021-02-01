#!/usr/bin/env python3
"""
Created on 20210128
Update on 
@author: Sandro Regis Cardoso
"""

from django.test import TestCase

import logging
from nox_bitcoin_orders.api_models.main import main


log = logging.getLogger("Order Book")

class TestMainProgram(TestCase):
    '''
    @description: TestCase for MainProgram
    '''
    _name = "test.main"
    
    @classmethod
    def setUpClass(cls):
        log.debug("setUpClass Test Method initialized.......")
        super(TestMainProgram, cls).setUpClass()
        cls.Main = main()
        return
    
    
    def testLoadNoxTradingServices(self):
        log.debug("Running testLoadNoxTradingServices.......")
        pass


























