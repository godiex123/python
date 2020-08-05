#!/usr/bin/python
#-*- coding: utf-8 -*-
import os
from art import *
import json


class Modeler:

    def __init__(self, file):
        with open(file + ".json") as content:
            datos = json.load(content)

            try:
                for k in datos.items():
                    print(k)
            except AttributeError:
                for k in datos.keys():
                    print(k)


    def parametros(self):

        pass








if __name__ == '__main__':
    
    ''' Menu del cliente '''
    print(text2art( "J-XTRAC"))
    print('\033[1m\x1b[6;32;40m' + 'Simple information extraction from json files' + '\x1b[0m\033[0;0m')
    print()
    print("Your actual location: {}".format(os.getcwd()))
    print()
    file = str(input("JSON File location: "))
    

    app = Modeler(file)

