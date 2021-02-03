from rest_framework.utils import json
import yaml
import logging
import argparse

from nox_bitcoin_orders.__init__ import __version__ as VERSION
from nox_bitcoin_orders.__init__ import __data_deploy__ as DATA_DEPLOY
from nox_bitcoin_orders.__init__ import __status__ as STATUS


class Utils(object):
    '''
    classdocs
    '''
    _name = "utils"
    _description = "Class with generic methods"
    
    
    def readJsonFile(self, filePath, fileName):
        """
        @Decription: Method to read json file for development agile
        @param: filePath
        @param: fileName
        @author: Sandro Regis Cardoso
        @return: json format
        """
        try:
            with open("%s/%s" %(filePath, fileName), "r") as jsonFile:
                result = json.load(jsonFile)
                jsonFile.close()
                return result
        except:
            raise Exception
    
    
    
    def boot(self):
        try:
            parser_val = argparse.ArgumentParser(description='Arquivo de configuracao de Order Book')
            parser_val.add_argument('-c', '--config_consulta',
                                    help='Config file for Nox Trading processing orders', required=False,
                                    default='./config/logging.yaml')
            
            args = parser_val.parse_args([])
            dados_config_file, log = self.__load_system_config(texto='Nox Bitcoin Challenge {0}'.format(VERSION), 
                                                        app_name='Order Book', config_file=args.config_consulta)
            
            log.info('Nox Bitcoin Trading Program Copyright: Nox Bitcoin {0}'.format(DATA_DEPLOY))
            log.info('Status {0}'.format(STATUS))
            
            #Config data to start services
            return dados_config_file
        except:
            log.error(Exception)
            raise Exception
    
    
    
    def __load_system_config(self, texto, app_name, config_file):
        try:
            with open(config_file, 'r') as stream:
                global_config = yaml.load(stream)
                logging.config.dictConfig(global_config['logging'])
                log = logging.getLogger(app_name)
                log.info('Initializing %s, loading setup file: %s', texto, config_file)
                return global_config, log
        except yaml.YAMLError as exc:
            log.error('File: {0}, Error: {1}'.format(config_file, repr(exc)))
    
        except Exception as exp:
            log.error('File: {0}, General Error: {1}'.format(config_file, repr(exp)))
    
        quit()
    
    
    
    
    
    
    
    
        