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
    @Description: TestCase for MainProgram
    '''
    _name = "test.main"
    
    @classmethod
    def setUpClass(cls):
        log.debug("setUpClass Test Method initialized.......")
        super(TestMainProgram, cls).setUpClass()
        cls.Main = main()
        return
    
    
    @classmethod
    def testLoadNoxTradingServices(cls):
        dataForTrading = {}
        log.debug("Running testLoadNoxTradingServices.......")
        optionSale = "Para Venda de seus Bitcoins digite 1"
        optionBuy  = "Para Comprar mais ou iniciar sua carteira digite 2"
        userInput  = "Por favor, digite sua opção aqui:"
        saleOffer = "Qual a quantidade que deseja vender de sua carteira?"
        purchaseOffer = "Qual a quantidade que deseja adquirir para sua carteira?"
        
        userChoice = int(input("%s\n%s\n%s: " %(optionSale, optionBuy, userInput)))
        qtyForTrade = 0.0
        if userChoice == 1:
            qtyForTrade = float(input("%s: " %(saleOffer)))
            dataForTrading['ask'] = qtyForTrade
        elif userChoice == 2:
            qtyForTrade = float(input("%s: " %(purchaseOffer)))
            dataForTrading['bids'] = qtyForTrade
        else:
            print("Informe uma opção válida por favor...")
            return cls.testLoadNoxTradingServices()
        
        return dataForTrading

























