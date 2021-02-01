from rest_framework.utils import json
import yaml
import logging

log = logging.getLogger("Order Book")
class Utils(object):
    '''
    classdocs
    '''
    _name = "utils"
    _description = "Class with generic methods"
    
    
    def readJsonFile(self, filePath, fileName):
        """
        Decription: Method to read json file
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
            log.error(Exception)
    
    
    
    def load_system_config(self, texto, app_name, config_file):
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
    
    
    
    
    
    
    
    
        