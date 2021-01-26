# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 18:39:32 2020

@author: gabriel.marin
"""

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client['astronomia']
estelar = db['estelar']

estelar.drop()

estelar.insert_many([{'_id': 1, 'nombre': "Sirio", 'tipo': "estrella", 'espectro': "A1V"}, 
                     {'_id': 2, 'nombre': "Saturno", 'tipo': "planeta"}, 
                     {'_id': 3, 'nombre': "Plutón", 'tipo': "planeta",}])

## buscamos Plutón y reemplazamos el tipo de objeto

pluton = estelar.find_one({'_id': 3})
pluton ['tipo'] = "planeta enano"
estelar.replace_one({'_id': pluton['_id']}, pluton)

## Hemos cargado el documento a modificar mediante find_one, lo modificamos, y lo devolvemos a la BD con replace_one.

## Si queremos hacer un Update parcial, indicando solo los cambios a realizar.

estelar.update_one({'nombre': "Plutón"}, {'$set': {'tipo': "planeta enano2"}})
estelar.update_one({'nombre': "Plutón"}, {'$set': {'tipo': "planeta enano"}})


## Si se quieren modificar todos los documentos que cumplen con una determinada condición se utiliza updatemany

estelar.update_many({}, {'$currentDate': {'fecha': True}})

## Otro operador de interés puede ser rename

estelar.update_many({}, {'$rename': {'tipo': "clase"}})

## Por último, es de interés el operador $unset que permite eliminar claves existentes.
## Vamos a eliminar la clave "espectro" del documento asociado a Sirio

estelar.update_one({'nombre': "Sirio"}, {'$unset': {'espectro': True}})

## Para eliminar documentos lo podemos hacer con la sentencia remove

estelar.remove({'clase': "planeta enano"})

