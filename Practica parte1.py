# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 19:38:17 2020

@author: Irasema
"""
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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
time.sleep(4)
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
lista = []
#Recorre los resultados de la consulta hasta que el boton Siguiente se deshabilite
while True:
    time.sleep(2)
    div = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/md-content/div/div/div[2]')
    consultas = div.find_elements_by_class_name('item')    
    for consulta in consultas:
        c = consulta.find_element_by_class_name('label-text')
        print(index, c.text)
        lista.append(c.text)
        index += 1
    
    siguiente = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/md-content/div/div/div[2]/trends-widget/ng-include/widget/div/div/ng-include/div/div[6]/pagination/div/button[2]')
    if siguiente.is_enabled() == False:
        break
    else:
        siguiente.click()
print("Total de resultados Google Trends:", len(lista))
print("Fin")