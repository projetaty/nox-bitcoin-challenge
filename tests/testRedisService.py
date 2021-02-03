#!/usr/bin/env python3
"""
Created on 20210127
Update on 
@author: Sandro Regis Cardoso
"""

from django.test import TestCase

import logging
from nox_bitcoin_orders.api_models.RedisService import RedisService
import redis

log = logging.getLogger("Order Book")

class TestRedisService(TestCase):

    @classmethod
    def setUpClass(cls):
        log.debug("Running TestRedisService Case.......")
        super(TestRedisService, cls).setUpClass()
        cls.RedisService = RedisService()
        return
    
    
    
    def testCreateRedisServiceInstance(self):
        try:
            log.debug("Asking for Redis Service Instance.......")
            redis_conf = {'queue_server': {'db': 0, 'host': '127.0.0.1', 'password': '05250310', 'port': '6379'}}
            instance = self.RedisService.createRedisServiceInstance(redis_conf.get("queue_server"))
            instance.client_setname("ds_mercadobitcoin")
            self.assertEqual(instance.client_getname(), "ds_mercadobitcoin")
            self.assertIsInstance(instance, redis.Redis)
            self.assertTrue(instance.ping())
            log.info("Redis instance name %s" %instance.client_getname())
        except:
            log.error("Exception on testGetRedisServiceInstance %s" %Exception)
            raise Exception
    


    def testInitializeRedisAskBidQueues(self):
        try:
            log.debug("Test for Charge Redis Asks and Bids Queues.......")
            
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
            log.debug("ENDPOINT %s" %dsEndpoint)
            res = self.RedisService.initializeRedisAskBidQueues(redisConf, dsEndpoint, alternativeUrl)
            
            self.assertLessEqual(len(res[0]), 1000)
            self.assertLessEqual(len(res[1]), 1000)
        except:
            log.error("Exception on testInitializeRedisAskBidQueues %s" %Exception)
            raise Exception
    
    
    def testNext(self):
        NotImplemented

