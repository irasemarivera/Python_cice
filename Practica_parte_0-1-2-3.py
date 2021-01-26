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
from bs4 import BeautifulSoup

''' PARTE 0. Extraer las tendencias en Google de 2019 y 2018'''
print(datetime.datetime.now(), "Inicia webscraping de Google Trends, tendencias 2019")
#Activamos opciones adicionales para el webscraping
options = webdriver.ChromeOptions()
options.add_argument('--incognito')  #para entrar en modo incógnito
#options.add_argument('--headless') #para realizar webscraping sin abrir un navegador
driver = webdriver.Chrome(r"C:/chromedriver/chromedriver.exe", options=options)
driver.implicitly_wait(5)

#Accedemos a la web
url = "https://trends.google.es/trends/?geo=ES"
driver.get(url)

#Clic en el icono de menú
driver.find_element_by_xpath('//*[@id="sidenav-menu-btn"]').click()
time.sleep(6)

#Clic en "El año en búsquedas", para acceder a lo más destacado de años anteriores
driver.find_element_by_xpath('//*[@id="sidenav-list-group-trends"]/md-item[4]/md-item-content/a').click()
time.sleep(6)

#Queremos que sea visible toda la información posible, por lo que clicamos todos los botones
# de "Mostrar más" mediante la siguiente función
def clic_mostrar_mas():
    mostrar_mas = driver.find_elements_by_class_name("show-more")
    for i in range(len(mostrar_mas)):
          driver.execute_script("arguments[0].click();", mostrar_mas[i])
          time.sleep(1)
          
clic_mostrar_mas()

#Ahora que se muestra toda la info, recopilamos los datos
page_source = driver.page_source #Aquí se guarda todo el código html de la página

#Creamos la sopa de donde exteaer la info
soup = BeautifulSoup(page_source, "html.parser")

#Creamos la BD GoogleTrends y la colección Tendencias2019
client = MongoClient('localhost', 27017)
db = client['GoogleTrends']
tendencias2019 = db['Tendencias2019']
tendencias2019.drop()

#en este diccionario iremos recopilando los datos que nos interesan para luego pasarlos 
#a la base de datos de MongoDB
cat = {} 

#Empezamos la búsqueda mediante loops
#Creamos una función cuyo parametro indica en qué colección recopilar los datos
def recolecta_datos(coleccion):
    #Las tendencias del año pasado se diferencian por 6 categorías
    grid = soup.find('div', class_='grid-container')#Este grid es el contenedor principal de las 6 categorías
    cells = grid.find_all('div', class_='grid-cell')
    a = 0
    b = 10
    for cell in cells:
        category = cell.find('div', class_='expandable-list-header-text')
        busquedas = soup.find_all('a', class_='fe-expandable-item-text')
        lista = []
        for busqueda in busquedas:
            #El texto de la búsqueda tiene saltos de línea y espacios por delante y detrás que no nos sirven, por lo que
            # los quitamos con el método replace()
            lista.append(busqueda.text.replace("\n", "").replace("      ", "").replace("    ", ""))
        #Guardamos en formato JSON para pasarlo a MongoDB
        cat = {'categoria': category.text, 'busquedas': lista[a:b]}
        a += 10
        b += 10
        #Pasamos los datos recopilados a MongoDB
        coleccion.insert_one(cat)
        
recolecta_datos(tendencias2019)

#A partir de aquí se realiza el mismo proceso pero con el año 2018
print(datetime.datetime.now(), "Inicia webscraping de Google Trends, tendencias 2018")

#Clic para cambiar de año
driver.find_element_by_xpath('/html/body/div[2]/div[2]/header/div/div[3]/ng-transclude/ng-include/div/div[1]/yis-year-picker/div/span').click()
time.sleep(6)
#Clic para seleccionar el año 2018
driver.find_element_by_xpath('//*[@id="dialogContent_1"]/div/ul/li[2]').click()
time.sleep(6)

#Reutilizamos la función para clicar todos los botones que muestran más info
clic_mostrar_mas()

#Guardamos el código html de la nueva página
page_source = driver.page_source

#Creamos otra sopa de donde exteaer la info
soup = BeautifulSoup(page_source, "html.parser")

#Para 2018 las tendencias se clasifican de forma similar a 2019 por lo que podemos reusar 
#la función recolecta_datos(), cambiando el parametro
tendencias2018 = db['Tendencias2018'] #Creamos la coleccion Tendencias2018
tendencias2018.drop()
recolecta_datos(tendencias2018)


''' PARTE 1. Extrar las consultas mas buscadas de los últimoms 30 días en España '''
print(datetime.datetime.now(), "Inicia webscraping de Google Trends")
driver.implicitly_wait(5)

url = "https://trends.google.es/trends/?geo=ES"
driver.get(url)

#Clic en el icono de menú
driver.find_element_by_xpath('//*[@id="sidenav-menu-btn"]').click()
time.sleep(2)

#Clic en 'Explorar'
driver.find_element_by_xpath('//*[@id="sidenav-list-group-trends"]/md-item[2]').click()
time.sleep(2)

#Clic en 'Todo el mundo'
driver.find_element_by_xpath('//*[@id="compare-pickers-wrapper"]/div/hierarchy-picker[1]/ng-include/div[1]').click()
time.sleep(6)

#Escribir 'España' y seleccionar la opción sugerida
driver.find_element_by_xpath('//*[@id="input-15"]').send_keys("España")
driver.find_element_by_xpath('//*[@id="input-15"]').send_keys(Keys.ARROW_DOWN)
driver.find_element_by_xpath('//*[@id="input-15"]').send_keys(Keys.ENTER)
time.sleep(2)

#Clic en 'Ultimos 12 meses'
driver.find_element_by_xpath('//*[@id="compare-pickers-wrapper"]/div/custom-date-picker').click()
time.sleep(2)

#Seleccionar 30 días de la lista desplegable
driver.find_element_by_xpath('//*[@id="select_option_25"]').click()
index = 0
lista_gt = []

#Recorrer los resultados de la tabla 'Buscar consultas' hasta que el boton Siguiente se deshabilite
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

#Guardamos los resultados en MongoDB, creamos una nueva colección
tendencias_30_dias = db['Tendencias_30_dias']
tendencias_30_dias.drop()
g_trends = {'Búsquedas destacadas': lista_gt}
tendencias_30_dias.insert_one(g_trends)
print(datetime.datetime.now(), "Termina web scraping de Google Trends")


''' PARTE 2. Extraer los trending topics de Twitter''' 

print(datetime.datetime.now(), "Inicia busqueda de Trending topics de twitter")
consumer_key = "6i6JAMqVnXym9kF33fK6U4MIE"
consumer_secret = "hJTsiq4bUbrbEupzonxIGgv8DyYexL5kQT06uvM2ICiFHRmMVx"
access_token = "1324422374377328643-klos5jxHQNblSJwtVwv1MBwgfB5lHM"
access_secret = "2M7lLj3UwxR8gMpsXsRdFh3MsqdrC9b6ve2sZyuiy7NrE"

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
escuchando activamente durante X minutos guardando en MongoDB los tuits escuchados

print(datetime.datetime.now(), "Inicia Streaming")
MINUTOS_ESCUCHA = 2 #Ej. 2 significa que haremos streaming durante 2 min por cada TT
TEMAS_ESCUCHA = 5 #Ej. 5, significaría los primero 5 trending topics o 5 primeras consultas de google
#Total de tiempo de escucha = TEMAS_ESCUCHA x MINUTOS_ESCUCHA x 2 (Twitter y Google)

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
print(datetime.datetime.now(), "Termina Streaming")'''

''' PARTR 4. Graficar -- Hacer esto en Jupyter'''
