#!/usr/bin/python3
"""
Created on 20210202
Update on 
@author: Sandro Regis Cardoso
"""
import logging
from nox_bitcoin_orders.api_models.NoxTrading import NoxTrading

log = logging.getLogger("Order Book")

class RunClient(object):
    _name = "run.queue"
    
    
    def __init__(self):
        try:
            self.__objNoxTrading = NoxTrading()
            welcomeMsg = "Olá bem vindo a Nox Bitcoin, qual a operação que deseja operar?"
            print("%s\n" %welcomeMsg)
        except:
            raise Exception
    
    
    
    def clientSession(self):
        try:
            optionSale = "Para Venda de seus Bitcoins digite 1"
            optionBuy  = "Para Comprar mais ou iniciar sua carteira digite 2"
            userInput  = "Por favor, digite sua opção aqui: "
            saleOffer = "Qual a quantidade que deseja vender de sua carteira?"
            purchaseOffer = "Qual a quantidade que deseja adquirir para sua carteira?"
            
            
            userChoice = float(input("%s\n%s\n%s" %(optionSale, optionBuy, userInput)))
            btcQty = 0.0
            orderType = ""
            resultMsg = ""
            if int(userChoice) == 1:
                orderType = 'ask'
                btcQty = input("%s: " %(saleOffer))
                btcQty = float(btcQty.replace(",", "."))
                resultMsg = "O valor aproximado da sua venda é de: R$"
            elif int(userChoice) == 2:
                orderType = 'bid'
                btcQty = input("%s: " %(purchaseOffer))
                btcQty = float(btcQty.replace(",", "."))
                resultMsg = "O valor aproximado da sua compra é de: R$"
            else:
                print("Informe uma opção válida por favor...")
                return self.clientSession()
            
            if self.__objNoxTrading.checkBtcQtyAvailable(btcQty) == True:
                result = self.__objNoxTrading.calcOrder(orderType, btcQty)
                print("%s %s" %(resultMsg, result))
        except:
            raise Exception
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    