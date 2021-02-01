#!/usr/bin/env python3
"""
Created on 20210128
Update on 
@author: Sandro Regis Cardoso
"""
import argparse

from nox_bitcoin_orders.__init__ import __version__ as VERSION
from nox_bitcoin_orders.__init__ import __data_deploy__ as DATA_DEPLOY
from nox_bitcoin_orders.__init__ import __status__ as STATUS
from nox_utils.Utils import Utils


def main(*args, **kwargs):
    try:
        utils = Utils()
        parser_val = argparse.ArgumentParser(description='Arquivo de configuracao de Order Book')
        parser_val.add_argument('-c', '--config_consulta',
                                help='Config file for Nox Trading processing orders', required=False,
                                default='./config/logging.yaml')
        
        args = parser_val.parse_args([])
        dados_config_file, log = utils.load_system_config(texto='Nox Bitcoin Challenge {0}'.format(VERSION), 
                                                    app_name='Order Book', config_file=args.config_consulta)
        
        log.info('Nox Bitcoin Trading Program Copyright: Nox Bitcoin {0}'.format(DATA_DEPLOY))
        log.info('Status {0}'.format(STATUS))
        
        #Sequency to start services
        try:
            log.debug("Config data %s" %dados_config_file)
        except:
            log.erro(Exception)
    except:
        log.erro(Exception)


if __name__ == "__main__":
    main()






