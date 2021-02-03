#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from nox_utils.Utils import Utils
from bin.RunQueue import RunQueue
import logging
from bin.RunClient import RunClient

log = logging.getLogger("Order Book")

def runBackendServices(*args, **kwargs):
    try:
        utils = Utils()
        dados_config_file = utils.boot()
        #Sequency to start services
        RunQueue().run(dados_config_file)
        RunClient().clientSession()
        #welcomeMsg = "Olá bem vindo a Nox Bitcoin, qual a operação que deseja operar?"
        #print("%s\n" %welcomeMsg)
            #raise Exception
    except:
        #log.error(Exception)
        raise Exception

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nox_bitcoin_challenger.settings')
    try:
        from django.core.management import execute_from_command_line
        
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
    runBackendServices()

if __name__ == '__main__':
    main()
