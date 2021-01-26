# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 14:47:28 2020

@author: Irasema
"""
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client['astronomia']
planetas = db['Planetas']
planetas.drop()

#Insertamos los documentos
planetas.insert_many([{'id': 1, 'nombre': 'P111', 'masa': 1.9, 'volumen': 3, 'composicion': 'H', 'perihelio': 0.5, 'afelio': None},
                       {'id': 2, 'nombre': 'P222', 'masa': 3.1, 'volumen': 4.5, 'composicion': 'O', 'perihelio': 0.07, 'afelio': None},
                       {'id': 3, 'nombre': 'S111', 'masa': 0.2, 'volumen': None, 'composicion': None, 'perihelio': None, 'afelio': None},
                       {'id': 4, 'nombre': 'S222', 'masa': 0.3, 'volumen': 1.1, 'composicion': None, 'perihelio': None, 'afelio': None},
                       {'id': 5, 'nombre': 'S333', 'masa': None, 'volumen': 0.02, 'composicion': None, 'perihelio': None, 'afelio': None},
                       {'id': 6, 'nombre': 'C111', 'masa': 0.05, 'volumen': None, 'composicion': 'H', 'perihelio': 0.01, 'afelio': 25},
                       {'id': 2, 'nombre': 'P333', 'masa': 3.8, 'volumen': 4.9, 'composicion': 'He', 'perihelio': None, 'afelio': None}                 
])

#Estos son satelites
s111 = planetas.find_one({"nombre": 'S111'})
s222 = planetas.find_one({"nombre": 'S222'})
s333 = planetas.find_one({"nombre": 'S333'})

#actualizamos el planeta con sus satelites
planetas.update_one({'nombre': "P222"}, {'$set': {'satelites': [s111, s222, s333]}})

#muestra en pantalla los nombres de aquellos objetos que tengan en la composición H o N o bien su masa sea mayor que 3.2
for p in planetas.find({"$or":[{"composicion":"H"}, {"composicion": "N"}, {"masa": {"$gt": 3.2}}]}):
    print(p["nombre"], p["composicion"], p["masa"])
    
#actualiza el nombre de C111 a Z111
planetas.update_one({'nombre': "C111"}, {'$set': {'nombre': 'Z111'}})