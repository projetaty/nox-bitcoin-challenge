#!/usr/bin/python3
"""
Created on 20210129
Update on 20210201
@author: Sandro Regis Cardoso
"""
import logging
from nox_bitcoin_orders.api_models.RedisService import RedisService
import threading

log = logging.getLogger("Order Book")

class RunQueue(object):
    _name = "run.queue"
    
    
    def __init__(self):
        try:
            log.info("RunQueue object.......")
            self.__objRedisService = RedisService()
            """redisConf = self.__getConfigData("queue_server", config)
            self.__objRedisService = RedisService(redisConf)"""
        except:
            raise Exception
    
    
    
    def __getConfigData(self, nodeName:str, fullConf:dict) -> dict:
        try:
            confData = fullConf.get(nodeName)
            return confData
        except:
            raise Exception
    
    
    
    def startRedisServices(self, redisConf:str):
        try:
            self.__objRedisService.createRedisServiceInstance(redisConf)
        except:
            raise Exception
    
    
    
    def chargeRedisQueues(self, url:str, alternativeUrl:str):
        try:
            self.__objRedisService.chargeBTCAsksToQueue(url, alternativeUrl)
            self.__objRedisService.chargeBTCBidsToQueue(url, alternativeUrl)
            return
        except:
            raise Exception
    
    
    
    def run(self, config:dict):
        try:
            info = {'stop': False}
            
            redisConf = self.__getConfigData("queue_server", config)
            threadRedis = threading.Thread(target = self.startRedisServices(redisConf), args=(info,))
            threadRedis.start()
            threadRedis.join()
            
            dataSources = self.__getConfigData("datasources", config)[0]
            url = dataSources['remote']['url']
            alternativeUrl = dataSources['remote']['alternative_url']
            threadQueues = threading.Thread(target = self.chargeRedisQueues(url, alternativeUrl), args=(info,))
            threadQueues.start()
            threadQueues.join()
        except:
            raise Exception
    
    
    
    
    
    







