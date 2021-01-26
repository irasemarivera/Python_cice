# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 21:28:38 2020

@author: Irasema
"""

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client['prueba2']
tweets = db['tweets']

## Indicamos que queremos que se muestren los tweets de gabrimmarin y solo texto
## _id: 0 indica que no queremos que se muestre el identificador.

tweet = tweets.find_one({"usuario.nick": 'gabrimarin'}, {'text': 1, '_id': 1})
print (tweet)  

## Si en lugar de un tweet queremos tratar todos los que cumplan unas condiciones
## indicadas, usaremos directamente find

for t in tweets.find({'usuario.nick': "gabrimarin", 'mentions': "herminia"}):
    print(t)

for t in tweets.find({'mentions': "herminia"}):
    print(t)

## Otra fórmula, pero no menos eficiente (leo todo, y busco -- procesado)

for t in tweets.find():
    if t['usuario']['nick']=="gabrimarin" and "herminia" in t['mentions']:
        print(t['text'])
