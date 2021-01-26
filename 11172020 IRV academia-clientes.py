# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 16:15:24 2020

@author: Irasema
"""

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client['movilmongo']
clientes = db['clientes']
clientes.drop()

#Insertamos los documentos
clientes.insert_many([{'dni': '111', 'nombre': 'pepe', 'telefono': '1111', 'direccion': 'Madrid', 'edad': None},
                      {'dni': '222', 'nombre': 'ana', 'telefono': '2222', 'direccion': 'Barcelona', 'edad': 27},
                      {'dni': '333', 'nombre': 'juan', 'telefono': '3333', 'direccion': None, 'edad': None},
                      {'dni': '444', 'nombre': 'maria', 'telefono': '4444', 'direccion': None, 'edad': 38}                
])

#Mostrar todos los dni, nombre de cada documento en la base de datos (sin visualizar el campo "id" ni el documento entero)
for c in clientes.find({}, {'_id':0, 'dni': 1, 'nombre': 1}):
    print(c)
    
#Mostrar todos lo documentos cuyos telefonos sean 1111 o 4444, o bien su nombre sea maria o bien su edad sea menor o igual que 30
for c in clientes.find({"$or":[{"telefono":"1111"}, {"telefono": "4444"}, {"nombre": "maria"}, {"edad": {"$lte": 30}}]}):
    print(c)

#pepe tiene 2 telefonos más (uno para casa: 1112 y otro para trabajo: 1113). Inserta en el documento de pepe un campo llamado
#adicionales que contenga un array de documentos embebidos. Cada documento tendrá 2 claves casa y trabajo
adic_pepe = [{'casa': '1112'}, {'trabajo': '1113'}]
pepe = clientes.find_one({"nombre": 'pepe'})
clientes.update_one({"nombre": 'pepe'}, {'$set': {'adicionales': adic_pepe}})

#añade un campo antigüedad para ana inicializado a cero. A continuación, incrementalo en 1
clientes.update_one({"nombre": 'ana'}, {'$set': {'antiguedad': 0}})
clientes.update_one({"nombre": 'ana'}, {'$inc': {'antiguedad': 1}})


'''
    Realiza las siguientes operaciones:
    - Crea una base de datos llamada academia y una colección llamada alumnos
'''
db = client['academia']
alumnos = db['alumnos']
alumnos.drop()

'''
    Añade la información de dos alumnos de nombre Ana y Juan cuyas edades son 19 y 18
'''
lista_alumnos = [{'nombre': 'Ana', 'edad': 19},
           {'nombre': 'Juan', 'edad': 18}]

alumnos.insert_many(lista_alumnos)

'''
    Añade una clave llamada lengua a la información de Ana que sea un array cuyos valores sean 6, 7 y 9.
    Haz lo mismo con Juan para añadir información de lengua (con notas 6, 7 y 8) y matematicas (con notas 6, 7 y 8)
'''

notas_lengua_ana = [6, 7, 9]
notas_lengua_juan = [6, 7, 8]
notas_mate_juan = [6, 7, 8]

alumnos.update_one({"nombre": 'Ana'}, {'$set': {'lengua': notas_lengua_ana}})
alumnos.update_one({"nombre": 'Juan'}, {'$set': {'lengua': notas_lengua_juan}})
alumnos.update_one({"nombre": 'Juan'}, {'$set': {'matematicas': notas_mate_juan}})

'''
    Realizar las siguientes consultas:
        Sólo el nombre de todos los alumnos que han sacado un 8 en un examen de lengua
'''
for a in alumnos.find({'lengua' : 8}, {'_id': 0, 'nombre': 1}):
    print(a)

''' Solo el nombre de todo los alumnos que han sacado un 8 en algun examen '''

for a in alumnos.find({"$or":[{'lengua' : 8}, {'matematicas': 8}]}, {'_id': 0, 'nombre': 1}):
    print(a) 

#Anade un 10 a las notas de Ana
notas_lengua_ana.append(10)
alumnos.update_one({"nombre": 'Ana'}, {'$set': {'lengua': notas_lengua_ana}})

'''Ana se ha dado de baja de la academia. Sustituye su información (con una única instrucción) por la de Javier de edad 22
y con notas en lengua de 5 y 6 '''
alumnos.replace_one({'nombre': 'Ana'}, {'nombre': 'Javier', 'edad': 22, 'lengua': [5, 6]})


'''
Crea la base de datos exoplaneta y la coleccion especies
'''
db = client['exoplaneta']
especies = db['especies']
especies.drop()

#Insertamos los documentos
especies.insert_many([{'codigo': 111, 'especie_parecida': 'hipopótamo', 'tamaño': 15, 'habitat' : 'Marino', 'esperanza_vida': None},
                      {'codigo': 222, 'especie_parecida': 'abeja', 'tamaño': 2, 'habitat' : None, 'esperanza_vida': 2},
                      {'codigo': 333, 'especie_parecida': 'gato', 'tamaño': 33, 'habitat' : 'Marino', 'esperanza_vida': 1400},
                      {'codigo': 444, 'especie_parecida': 'caballo', 'tamaño': None, 'habitat' : None, 'esperanza_vida': 328}               
])

for e in especies.find({}, {'_id': 0, 'codigo': 1, 'especie_parecida': 1}):
    print(e)
    
''' Todos los codigos de animales que sean parecidos a hipopótamos o caballos, o bien sean marinos o bien su esperanza de vida
sea mayor o igual que 500'''
for e in especies.find({"$or":[{"especie_parecida":"hipopótamo"}, {"especie_parecida": "caballo"}, {"habitat": "Marino"}, {"Esperanza_vida": {"$gte": 500}}]}, {'_id': 0, 'codigo': 1}):
    print(e)
    
'''
La especie 111 se parece a dos animales más (rinoceronte y jirafa en grado 0.8 y 0.9 respectivamente). Inserta en el documento 111 un campo
llamado adicionales que contenga un array de documentos embebidos. Cada documento embebido tendrá dos claves: rinoceronte y jirafa y sus
correspondientes grados como valores
'''
adic_111 = [{'jirafa': '0.8'},{'rinoceronte': '0.9'}]
especies.update_one({"codigo": 111}, {'$set': {'adicionales': adic_111}})

