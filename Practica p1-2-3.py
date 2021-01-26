# -*- coding: utf-8 -*-
"""
Created on Sat Nov 21 12:35:44 2020

@author: Irasema
"""
import time
import tweepy
import json
import datetime

from pymongo import MongoClient
from tweepy import Stream
from tweepy.streaming import StreamListener
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

''' PARTE 1n Extrar las consultas mas buscadas de los últimoms 30 días en España '''
print(datetime.datetime.now(), "Inicia webscraping de Google Trends")
chromedriver_location = 'C:/chromedriver/chromedriver.exe'
driver = webdriver.Chrome(chromedriver_location)
driver.implicitly_wait(5)

url = "https://trends.google.es/trends/?geo=ES"
driver.get(url)
#Hacer clic en el icono de la hamburguesa
driver.find_element_by_xpath('//*[@id="sidenav-menu-btn"]').click()
time.sleep(2)
#Clic en Explorar
driver.find_element_by_xpath('//*[@id="sidenav-list-group-trends"]/md-item[2]').click()
time.sleep(2)
#Clic en Todo el mundo
driver.find_element_by_xpath('//*[@id="compare-pickers-wrapper"]/div/hierarchy-picker[1]/ng-include/div[1]').click()
time.sleep(5)
#Escribir España y seleccionar la opción sugerida
driver.find_element_by_xpath('//*[@id="input-15"]').send_keys("España")
driver.find_element_by_xpath('//*[@id="input-15"]').send_keys(Keys.ARROW_DOWN)
driver.find_element_by_xpath('//*[@id="input-15"]').send_keys(Keys.ENTER)
time.sleep(2)
#Hacer clic en Ultimos 12 meses
driver.find_element_by_xpath('//*[@id="compare-pickers-wrapper"]/div/custom-date-picker').click()
time.sleep(2)
#Seleccionar 30 días
driver.find_element_by_xpath('//*[@id="select_option_25"]').click()
index = 0
lista_gt = []
#Recorre los resultados de la consulta hasta que el boton Siguiente se deshabilite
while True:
    time.sleep(2)
    div = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/md-content/div/div/div[2]')
    consultas = div.find_elements_by_class_name('item')    
    for consulta in consultas:
        c = consulta.find_element_by_class_name('label-text')
        print(index, c.text)
        lista_gt.append(c.text)
        index += 1
    
    siguiente = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/md-content/div/div/div[2]/trends-widget/ng-include/widget/div/div/ng-include/div/div[6]/pagination/div/button[2]')
    if siguiente.is_enabled() == False:
        break
    else:
        siguiente.click()
print("Total de resultados Google Trends:", len(lista_gt))
print(datetime.datetime.now(), "Termina web scraping de Google Trends")


''' PARTE 2. Extraer los trending topics de Twitter''' 

print(datetime.datetime.now(), "Inicia busqueda de Trending topics de twitter")
consumer_key = "xxxxxxxxxxxx"
consumer_secret = "xxxxxxxxxxxx"
access_token = "xxxxxxxxxxxx"
access_secret = "xxxxxxxxxxxx"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# Where On Earth ID para España es 23424950.
SPAIN_WOEID = 23424950
sp_trends = api.trends_place(SPAIN_WOEID)
trends = json.loads(json.dumps(sp_trends, indent=1))
index = 0 
lista_tw = []
for trend in trends[0]["trends"]:
    print(index, trend["name"])
    lista_tw.append(trend["name"])
    index += 1
print("Total de Trending Topics de Twitter: ", len(lista_tw))
print("Termina busqueda de Trending topics de twitter", datetime.datetime.now())

''' PARTE 3. Escuchar en Twitter los primeros N temas de Google Trends y los primeros N de Twitter
escuchando activamente durante X minutos guardando en MongoDB los tuits escuchados'''

print(datetime.datetime.now(), "Inicia Streaming")
MINUTOS_ESCUCHA = 2 #Ej. 2 significa que haremos streaming durante 2 min por cada TT
TEMAS_ESCUCHA = 5 #Ej. 5, significaría los primero 5 trending topics o 5 primeras consultas de google
#TOtal de tiempo de escucha = TEMAS_ESCUCHA x MINUTOS_ESCUCHA x 2 (Twitter y Google)

client = MongoClient('localhost', 27017)
db = client['twitter']

class MyListener (StreamListener):
    
    def on_status(self, status):
        #print("Tweet id", status.id)
        tt.insert_one(status._json)
        now = datetime.datetime.now()
        if now >= end_date:
            return False
            
    def on_error(self, status):
        print(status)
        return True
    
api = tweepy.API(auth)
twitter_stream = Stream (auth, MyListener())

#Escuchar los temas de Google Trends
print("Streaming de los primeros {} Trends de Google...".format(TEMAS_ESCUCHA))
i = 0
while (i < TEMAS_ESCUCHA):
    end_date = datetime.datetime.now() + timedelta(minutes = MINUTOS_ESCUCHA)
    #Creamos la coleccion de forma dinámica por cada tema escuchado
    tt = db['GoogleTrends{}'.format(i+1)]
    #Borramos si tuvieramos algo creado
    tt.drop()
    #el primer registro de cada colección será el nombre del tema
    fila_tema = {"tema": lista_gt[i]}
    tt.insert_one(fila_tema)
    print("Escuchando en Twitter sobre Google Trend", i, lista_gt[i])
    twitter_stream.filter(track=[lista_gt[i]], languages=["es"])
    i += 1
print("Termina Streaming de los Trends de Google")

#Escuchar los temas de twitter
print("Streaming de los primeros {} TTs de Twitter...".format(TEMAS_ESCUCHA))
i = 0
while (i < TEMAS_ESCUCHA):
    end_date = datetime.datetime.now() + timedelta(minutes = MINUTOS_ESCUCHA)
    #Creamos la coleccion de forma dinámica por cada tema escuchado
    tt = db['TrendingTopics{}'.format(i+1)]
    #Borramos si tuvieramos algo creado
    tt.drop()
    #el primer registro de cada colección será el nombre del tema
    fila_tema = {"tema": lista_tw[i]}
    tt.insert_one(fila_tema)
    print("Escuchando en Twitter sobre TT",i, lista_tw[i])
    twitter_stream.filter(track=[lista_tw[i]], languages=["es"])
    i += 1
print("Fin Streaming de TTs de Twitter")
print(datetime.datetime.now(), "Termina Streaming")

''' PARTR 4. Graficar -- Hacer esto en Jupyter'''
