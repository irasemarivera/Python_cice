# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 18:44:33 2020

@author: Irasema
"""

from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client['Sales']
customers = db['Customers']
customers.drop()

#Insertamos los documentos
customers.insert_many([{'customernumber': 103, 'customername': 'Atelier graphique', 
                        'contactlastname': 'Schmitt', 'contactfirstname': 'Carine', 
                        'phone': '40.32.2555', 'addressline1' : '54, rue Royale', 
                        'addressline2' : None, 'city' : 'Nantes', 'postalcode': '44000', 
                        'state': None, 'country': 'France', 'salesrepemployeenumber' : 1370,
                        'creditlimit': 21000},
                       {'customernumber': 112, 'customername': 'Signal gift Stores', 
                        'contactlastname': 'King', 'contactfirstname': 'Sue', 
                        'phone': '7025551838', 'addressline1' : '8489 Strong St.', 
                        'addressline2' : None, 'city' : 'Las Vegas', 
                        'state': 'NV', 'postalcode': '83030', 
                        'country': 'USA', 'salesrepemployeenumber' : 1166,
                        'creditlimit': 71800},
                       {'customernumber': 114, 'customername': 'Australian Collectors, Co.', 
                        'contactlastname': 'Ferguson', 'contactfirstname': 'Peter', 
                        'phone': '03 9520 4555', 'addressline1' : '636 St Kilda Road', 
                        'addressline2' : 'Level 3', 'city' : 'Melbourne', 
                        'state': 'Victoria', 'postalcode': '3004', 
                        'country': 'Australia', 'salesrepemployeenumber' : 1611,
                        'creditlimit': 117300},
                       {'customernumber': 119, 'customername': 'La Rochelle gifts', 
                        'contactlastname': 'Labrune', 'contactfirstname': 'Janine', 
                        'phone': '40.67.8555', 'addressline1' : '67, rue des Cinquante Otages', 
                        'addressline2' : None, 'city' : 'Nantes', 'postalcode': '44000', 
                        'state': None, 'country': 'France', 'salesrepemployeenumber' : 1370,
                        'creditlimit': 118200}                    
])

#Realiza una query para que devuelva la dirección completa
#("ADDRESSLINE1", "ADDRESSLINE2", "CITY", "STATE", "POSTALCODE")
#de todos los documentos de la colección
def notNull(x):
    if x == None:
        return ""
    else:
        return x

for t in customers.find():
    print(notNull(t['addressline1']), notNull(t['addressline2']), notNull(t['city']), notNull(t['state']), notNull(t['postalcode']))

#Actualiza la clave "CREDITLIMIT" de todos los documentos de la colección
#atendiendo a la siguiente regla: Si el límite de crédito es menor o igual
#de 21 000 euros lo incrementaremos en 100 euros. Si es superior a 21 000
#euros e inferior a 75 000 euros lo incrementaremos en 200 euros. Si es igual
#o mayor a 75 000 euros lo decrementaremos en 100 euros

for t in customers.find():
    print("id: ", t['_id'])
    if t['creditlimit'] <= 21000:
        customers.update_one({'_id': t['_id']}, {'$set': {'creditlimit': t['creditlimit']+100}})
    elif t['creditlimit'] > 21000 and t['creditlimit'] < 75000:
        customers.update_one({'_id': t['_id']}, {'$set': {'creditlimit': t['creditlimit']+200}})
    else:
        customers.update_one({'_id': t['_id']}, {'$set': {'creditlimit': t['creditlimit']-100}})
