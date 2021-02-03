#!/usr/bin/env python3
"""
Created on 20210128
Update on 20210131
@author: Sandro Regis Cardoso
"""

from django.test import TestCase

import logging
from nox_bitcoin_orders.api_models.RedisService import RedisService

from time import sleep


log = logging.getLogger("Order Book")

class TestNoxTrading(TestCase):
    '''
    classdocs
    '''
    _name = "test.noxtrading"
    _description = "Class to process trading ops"
    
    @classmethod
    def setUpClass(cls):
        log.debug("Initializing Test on NoxTrading class")
        super(TestNoxTrading, cls).setUpClass()
        
        redisConf = {'queue_server': {'db': 0, 'host': '127.0.0.1', 'password': '05250310', 'port': '6379'}}
        redisConf = redisConf.get("queue_server")
        
        dsConfig = {'datasources': [{'name': 'MercadoBitcoin', 'status': True, 'tipo': 'BTC', 
                                        'launch': {'status': True}, 
                                        'remote': {'url': 'https://www.mercadobitcoin.net/api/BTC/orderbook/', 
                                                   'alternative_url': 'https://api.cryptowat.ch/markets/kraken/btcusd/orderbook',
                                                   'arquivo_dados_erro': './datasources/excessao.json', 
                                                   'max_tentativas': 3, 
                                                   'smtp': [{'name': 'Alerta Critico | Sev 0', 
                                                             'destinatarios': {'copia': ['contato@noxbitcoin.com.br'], 
                                                                               'nome_principal': 'Sandro Regis Cardoso'}, 
                                                             'remetente': {'email': 'projetaty@gmail.com', 'nome': 'Nox Orders Book'}, 
                                                             'server': {'autenticacao': {'senha': '', 'usuario': ''}, 
                                                                        'host': 'mx.noxbitcoin.com.br', 'port': 25}, 
                                                             'subject': 'Problemas com BTC Datasource'}]}}]}
        ds = dsConfig.get("datasources")[0]
        dsEndpoint = ds['remote']['url']
        alternativeUrl = ds['remote']['alternative_url']
        
        cls.__objRedisService = RedisService()
        queues = cls.__objRedisService.initializeRedisAskBidQueues(redisConf, dsEndpoint, alternativeUrl)
        
        cls.sellingOffers = queues[0]
        cls.purchaseOffers = queues[1]
    
    def testDummy(self):
        log.info("NoxTrading %s" %self.sellingOffers)
        sleep(10)
        
        log.info("NoxTrading %s" %self.purchaseOffers)
        sleep(10)
        
    
    
    
    
    