# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

url="https://www1.sedecatastro.gob.es/CYCBienInmueble/OVCBusqueda.aspx"

driver.get(url)

coord = driver.find_element_by_id("tabcoords")
coord.click()

## Ejecutar hasta aquí... Y luego el resto.

lat = driver.find_element_by_id("ctl00_Contenido_txtLatitud")
lon = driver.find_element_by_id("ctl00_Contenido_txtLongitud")

latitud = "28.2723368"
longitud = "-16.6600606"
lat.send_keys(latitud)
lon.send_keys(longitud)

cart = driver.find_element_by_id("ctl00_Contenido_btnNuevaCartografia")
cart.click()


html = driver.find_element_by_xpath("/html")
print(html.text)

head = driver.find_element_by_xpath("/html/head")
body = driver.find_element_by_xpath("/html/body")
html2 = body.find_element_by_xpath("/html")

hijos = driver.find_elements_by_xpath("/html/body/*")
for element in hijos:
    print(element.tag_name)
