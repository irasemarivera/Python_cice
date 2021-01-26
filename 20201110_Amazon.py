# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 19:38:17 2020

@author: Irasema
"""

#Ejercicio 2, obtener un listado de productos de un sitio de compras en español
import time
from selenium import webdriver

chromedriver_location = 'C:/chromedriver/chromedriver.exe'
driver = webdriver.Chrome(chromedriver_location)

url = "https://www.amazon.es/"
driver.get(url)

busqueda = input("Producto a buscar: ")
driver.find_element_by_xpath('//*[@id="twotabsearchtextbox"]').send_keys(busqueda)
driver.find_element_by_xpath('//*[@id="nav-search-submit-text"]/input').click()
time.sleep(2)
#Orden de precio ascendente
driver.find_element_by_xpath('//*[@id="s-result-sort-select"]/option[2]').click()
time.sleep(2)
resultados = driver.find_elements_by_xpath('//span[contains(@class, "SEARCH_RESULTS")]')
print("Total de productos encontrados en Página 1:", len(resultados))
i = 1
for resultado in resultados:
    productos = resultado.find_elements_by_class_name("a-size-base-plus.a-color-base.a-text-normal")
    for producto in productos:
        nombre = producto.text
    precios = resultado.find_elements_by_class_name("a-size-base.a-link-normal.a-text-normal")
    for precio in precios:
        precio = precio.text.replace("\n"," ")
    print("Producto {}: {}, Precio: {}".format(i, nombre, precio))
    i += 1
print("Fin")