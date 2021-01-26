# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 21:08:06 2020

@author: Irasema
"""

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client['prueba2']
tweets = db ['tweets']
tweets.drop()

tweet = {'_id': 2, 'usuario': {'nick': "herminia", 'seguidores': 5320}, 'texto':"RT: @herminia: hoy, excursión a la sierra con @pedro", 'menciones': ["herminia", "pedro"], 'RT': True, 'origen': 1}

insertado = tweets.insert_one(tweet)
print(insertado.inserted_id)

