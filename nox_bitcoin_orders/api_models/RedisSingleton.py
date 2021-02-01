#!/usr/bin/python3
"""
Created on 20200125
Update on 20210131
@author: Sandro Regis Cardoso
"""
import redis
import logging

log = logging.getLogger("Order Book")

class RedisSingleton(type):
    _name="redis.singleton"
    _instances = {}
    
    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super(RedisSingleton, self).__call__(*args, **kwargs)
        return self._instances[self]

class RedisServer(object):
    _name="redis.server"
    __metaclass__ = RedisSingleton
    __DB_IN_USE = []
    
    #TODO: Revisar processamento para abertura de conexao em multiplos servers:[port]:[db]
    def setConnection(self, redis_host, redis_port, redis_db, redis_pwd):
        if redis_db not in self.__DB_IN_USE:
            self.__DB_IN_USE.append(redis_db)
        
        connection = redis.Redis(host = redis_host, 
                                port =  redis_port, 
                                db = int(redis_db),
                                password = redis_pwd, 
                                decode_responses = True)
        
        return connection

