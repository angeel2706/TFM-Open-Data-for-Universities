from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import re
from geopy.geocoders import Nominatim #latitud, longitud
from pandas import DataFrame
import pandas as pd
from unicodedata import normalize


elim_tildes = dict.fromkeys(map(ord, u'\u0301\u0308'), None) #Para eliminar tildes


driver_path = 'C:\\Users\\sanch\\Downloads\\chromedriver.exe'

option = Options()    
option.add_argument('--headless') #ocultar pestaña navegador


#CENTROS
url = 'https://www.educacion.gob.es/ruct/consultacentros.action?actual=centros'
driver = webdriver.Chrome(driver_path, options=option)
driver.get(url)

uni = driver.find_elements_by_xpath('//*[@id="codigoUniversidad"]')
uni[0].click()
UPM = driver.find_elements_by_xpath('//*[@id="codigoUniversidad"]/option[79]')
UPM[0].click()
buscar = driver.find_elements_by_xpath('//*[@id="consultacentros_listacentros"]')
buscar[0].click()
cod_centro = list()
nombre_centro = list()
ciudad_centro = list()
campus_centro = list()
cod_tipo_centro = list() 
des_tipo_centro = list() #propio, adscrito, vinculado ...
cod_naturaleza_centro = list()
des_naturaleza_centro = list() #publico, privado ...
cod_situacion_centro = list()
des_situacion_centro = list()
latitud_centro = list()
longitud_centro = list()

#PAGINA 1
centros = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr')
links = len(driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[4]/a'))

for centro in centros:
	cod_centro.append(centro.find_elements_by_xpath('.//td[3]')[0].text)
	nombre_centro.append(centro.find_elements_by_xpath('.//td[4]/a')[0].text)

for link in range(0, links):
	centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[4]/a')
	centro[link].click()

	ciudad_centro.append(driver.find_elements_by_xpath('//*[@id="centro"]/fieldset/label[7]/span[2]')[0].text)
	ciudad = driver.find_elements_by_xpath('//*[@id="centro"]/fieldset/label[7]/span[2]')[0].text #localidad
	geolocator = Nominatim(user_agent="Angel")
	location = geolocator.geocode(ciudad)
	latitud_centro.append(location.latitude)
	longitud_centro.append(location.longitude)
	if 'E.T.S.' and 'Ciudad Universitaria' in driver.find_elements_by_xpath('//*[@id="centro"]/fieldset/label[5]/span[2]')[0].text:
		campus_centro.append('Campus Ciudad Universitaria')
	else:
		campus = driver.find_elements_by_xpath('//*[@id="centro"]/fieldset/label[5]/span[2]')[0].text
		campus = campus.split(',')[0]
		campus = campus.split('.')[0]
		campus_centro.append(campus)
	des_tipo_centro.append('Centro ' + driver.find_elements_by_xpath('//*[@id="centro"]/fieldset/label[4]/span[2]')[0].text)
	des_naturaleza_centro.append(driver.find_elements_by_xpath('//*[@id="centro"]/fieldset/label[3]/span[2]')[0].text)

	driver.back()

#PAGINA 2
pagina2 = driver.find_elements_by_xpath('//*[@id="ver"]/span[2]/a[1]')
pagina2[0].click()
centros = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr')
links = len(driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[4]/a'))

for centro in centros:
	cod_centro.append(centro.find_elements_by_xpath('.//td[3]')[0].text)
	nombre_centro.append(centro.find_elements_by_xpath('.//td[4]/a')[0].text)

for link in range(0, links):
	centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[4]/a')
	centro[link].click()

	ciudad_centro.append(driver.find_elements_by_xpath('//*[@id="centro"]/fieldset/label[7]/span[2]')[0].text) #localidad
	ciudad = driver.find_elements_by_xpath('//*[@id="centro"]/fieldset/label[7]/span[2]')[0].text
	geolocator = Nominatim(user_agent="Angel")
	location = geolocator.geocode(ciudad)
	latitud_centro.append(location.latitude)
	longitud_centro.append(location.longitude)
	if 'E.T.S.' and 'Ciudad Universitaria' in driver.find_elements_by_xpath('//*[@id="centro"]/fieldset/label[5]/span[2]')[0].text:
		campus_centro.append('Campus Ciudad Universitaria')
	else:
		campus = driver.find_elements_by_xpath('//*[@id="centro"]/fieldset/label[5]/span[2]')[0].text
		campus = campus.split(',')[0]
		campus = campus.split('.')[0]
		campus_centro.append(campus)
	des_tipo_centro.append('Centro ' + driver.find_elements_by_xpath('//*[@id="centro"]/fieldset/label[4]/span[2]')[0].text)
	des_naturaleza_centro.append(driver.find_elements_by_xpath('//*[@id="centro"]/fieldset/label[3]/span[2]')[0].text)

	driver.back()

#PAGINA 3
pagina3 = driver.find_elements_by_xpath('//*[@id="ver"]/span[2]/a[4]')
pagina3[0].click()
centros = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr')
links = len(driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[4]/a'))

for centro in centros:
	cod_centro.append(centro.find_elements_by_xpath('.//td[3]')[0].text)
	nombre_centro.append(centro.find_elements_by_xpath('.//td[4]/a')[0].text)

for link in range(0, links):
	centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[4]/a')
	centro[link].click()

	ciudad_centro.append(driver.find_elements_by_xpath('//*[@id="centro"]/fieldset/label[7]/span[2]')[0].text) #localidad
	ciudad = driver.find_elements_by_xpath('//*[@id="centro"]/fieldset/label[7]/span[2]')[0].text
	geolocator = Nominatim(user_agent="Angel")
	location = geolocator.geocode(ciudad)
	latitud_centro.append(location.latitude)
	longitud_centro.append(location.longitude)
	if 'E.T.S.' and 'Ciudad Universitaria' in driver.find_elements_by_xpath('//*[@id="centro"]/fieldset/label[5]/span[2]')[0].text:
		campus_centro.append('Campus Ciudad Universitaria')
	else:
		campus = driver.find_elements_by_xpath('//*[@id="centro"]/fieldset/label[5]/span[2]')[0].text
		campus = campus.split(',')[0]
		campus = campus.split('.')[0]
		campus_centro.append(campus)
	des_tipo_centro.append('Centro ' + driver.find_elements_by_xpath('//*[@id="centro"]/fieldset/label[4]/span[2]')[0].text)
	des_naturaleza_centro.append(driver.find_elements_by_xpath('//*[@id="centro"]/fieldset/label[3]/span[2]')[0].text)

	driver.back()


#Codigos para las 3 paginas
for tipo, naturaleza in zip(des_tipo_centro, des_naturaleza_centro):
	if 'Centro Propio' in tipo:
		cod_tipo_centro.append('C1')
	elif 'Centro Adscrito' in tipo:
		cod_tipo_centro.append('C2')
	elif 'Centro Centro asociado/vinculado' in tipo:
		cod_tipo_centro.append('C3')
	elif 'Instituto universitario de investigación' in tipo:
		cod_tipo_centro.append('O1')
	elif 'Escuela de doctorado' in tipo:
		cod_tipo_centro.append('O2')
	elif 'Hospital' in tipo:
		cod_tipo_centro.append('O3')
	elif 'Fundación' in tipo:
		cod_tipo_centro.append('O4')
	elif 'Otros' in tipo:
		cod_tipo_centro.append('XX')
	else:
		cod_tipo_centro.append('None')


	if 'Público' in naturaleza:
		cod_naturaleza_centro.append('1')
	elif 'Privado' in naturaleza:
		cod_naturaleza_centro.append('2')
	elif 'Privado de la Iglesia' in naturaleza:
		cod_naturaleza_centro.append('3')
	elif 'Mixto' in naturaleza:
		cod_naturaleza_centro.append('4')
	else:
		cod_naturaleza_centro.append('None')

print(len(cod_centro), cod_centro)
for i in range(len(cod_centro)):
	cod_situacion_centro.append('1')
	des_situacion_centro.append('Activo')

print(ciudad_centro)
#CODIGO CIUDAD
cod_ciudad_centro = list()
ciudades_df = pd.read_csv('municipios/UPM-centros.csv', sep=';', skiprows = 2)
for ciudad in ciudad_centro:
	ciudad = normalize('NFKC', normalize('NFKD', ciudad).translate(elim_tildes))
	for index, row in ciudades_df.iterrows():
		if ciudad == row[3]:
			cod_ciudad_centro.append(int(row[1]))




#CENTROS DATASET

curso_academico = ['2020-21'] * len(cod_centro)
cod_universidad = ['025'] * len(cod_centro)
des_universidad = ['Universidad Politécnica de Madrid'] * len(cod_centro)
cod_centro = cod_centro 
des_centro = nombre_centro 
cod_municipio = cod_ciudad_centro #no se donde encontrarlo. No es codigo postal
des_municipio = ciudad_centro
cod_campus = [' '] * len(cod_centro) #no se donde encontrarlo
des_campus = campus_centro
cod_tipo_centro = cod_tipo_centro
des_tipo_centro = des_tipo_centro
cod_naturaleza_centro = cod_naturaleza_centro
des_naturaleza_centro = des_naturaleza_centro
cod_situacion_centro = cod_situacion_centro
des_situacion_centro = des_situacion_centro
fecha_desde_situacion_centro = [' '] * len(cod_centro)
latitud = latitud_centro
longitud = longitud_centro

'''
print(len(curso_academico),len(cod_universidad),len(des_universidad),len(cod_centro),len(des_centro),len(cod_municipio),
	len(des_municipio),len(cod_campus),len(des_campus),len(cod_tipo_centro),len(des_tipo_centro),len(cod_naturaleza_centro),
	len(des_naturaleza_centro),len(cod_situacion_centro),len(des_situacion_centro),len(fecha_desde_situacion_centro),len(latitud),len(longitud))
'''

print('Codigo municipio', cod_municipio)

data = {'curso_academico':curso_academico,
		'cod_universidad':cod_universidad,
		'des_universidad':des_universidad,
		'cod_centro':cod_centro,
		'des_centro':des_centro, 
		'cod_municipio':cod_municipio,
		'des_municipio':des_municipio,
		'cod_campus':cod_campus,
		'des_campus':des_campus,
		'cod_tipo_centro':cod_tipo_centro,
		'des_tipo_centro':des_tipo_centro,
		'cod_naturaleza_centro':cod_naturaleza_centro,
		'des_naturaleza_centro':des_naturaleza_centro,
		'cod_situacion_centro':cod_situacion_centro,
		'des_situacion_centro':des_situacion_centro,
		'fecha_desde_situacion_centro':fecha_desde_situacion_centro,
		'latitud':latitud,
		'longitud':longitud
}

centros_df = DataFrame(data)
centros_df.to_csv('UPM-centros.csv')
print('Done')