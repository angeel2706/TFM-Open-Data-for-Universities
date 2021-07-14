from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pandas import DataFrame


driver_path = 'C:\\Users\\sanch\\Downloads\\chromedriver.exe'

option = Options()    
option.add_argument('--headless') #ocultar pestaña navegador


#CENTROS
url = 'https://www.upm.es/UPM/Centros'
driver = webdriver.Chrome(driver_path, options=option)
driver.get(url)

campus = list()
centros = list()
departamentos = list() #list of lists
ciudad_departamento = list()

#CAMPUS CIUDAD UNIVERSITARIA
centros_campus = driver.find_elements_by_xpath('//*[@id="subcanales"]/li[1]/ul/li')
links = len(driver.find_elements_by_xpath('//*[@id="subcanales"]/li[1]/ul/li/a'))
print('len centros', len(centros_campus), 'len links', links)

for centro in centros_campus:
	centros.append(centro.find_elements_by_xpath('.//a')[0].text)

for link in range(0, links):
	centro = driver.find_elements_by_xpath('//*[@id="subcanales"]/li[1]/ul/li/a')
	centro[link].click()
	campus.append(driver.find_elements_by_xpath('//*[@id="directorio-03"]/div/h2')[0].text)
	'''
	ciudad_link = driver.find_elements_by_xpath('//*[@id="map"]/div/div/div[15]/div[2]/div[2]/a')
	print('ciudad link', ciudad_link)	
	ciudad_link[0].click()
	'''
	departamentos_centro = driver.find_elements_by_xpath('//*[@id="directorio-03"]/div/div')
	print('   DEPART_centro', len(departamentos_centro))
	departamentos_i = list()
	for depart in departamentos_centro:
		try:
			departamentos_i.append(depart.find_elements_by_xpath('.//a')[0].text)
		except:
			departamentos_i.append(depart.find_elements_by_xpath('.//div/div')[0].text)

	departamentos.append(departamentos_i)
	driver.back()

print('Centros', len(centros))
print('Campus', len(campus))
print('Departamentos', len(departamentos)) 

#CAMPUS MADRID CIUDAD 
centros_campus = driver.find_elements_by_xpath('//*[@id="subcanales"]/li[2]/ul/li')
links = len(driver.find_elements_by_xpath('//*[@id="subcanales"]/li[2]/ul/li/a'))
print('len centros', len(centros_campus), 'len links', links)

for centro in centros_campus:
	centros.append(centro.find_elements_by_xpath('.//a')[0].text)

for link in range(0, links):
	centro = driver.find_elements_by_xpath('//*[@id="subcanales"]/li[2]/ul/li/a')
	centro[link].click()
	campus.append(driver.find_elements_by_xpath('//*[@id="directorio-03"]/div/h2')[0].text)

	departamentos_centro = driver.find_elements_by_xpath('//*[@id="directorio-03"]/div/div')
	print('   DEPART_centro', len(departamentos_centro))
	departamentos_i = list()
	for depart in departamentos_centro:
		try:
			departamentos_i.append(depart.find_elements_by_xpath('.//a')[0].text)
		except:
			departamentos_i.append(depart.find_elements_by_xpath('.//div/div')[0].text)

	departamentos.append(departamentos_i)
	driver.back()

print('Centros', len(centros))
print('Campus', len(campus))
print('Departamentos', len(departamentos)) 

#CAMPUS MONTEGANCEDO
centros_campus = driver.find_elements_by_xpath('//*[@id="subcanales"]/li[3]/ul/li')
links = len(driver.find_elements_by_xpath('//*[@id="subcanales"]/li[3]/ul/li/a'))
print('len centros', len(centros_campus), 'len links', links)

for centro in centros_campus:
	centros.append(centro.find_elements_by_xpath('.//a')[0].text)

for link in range(0, links):
	centro = driver.find_elements_by_xpath('//*[@id="subcanales"]/li[3]/ul/li/a')
	centro[link].click()
	campus.append(driver.find_elements_by_xpath('//*[@id="directorio-03"]/div/h2')[0].text)

	departamentos_centro = driver.find_elements_by_xpath('//*[@id="directorio-03"]/div/div')
	print('   DEPART_centro', len(departamentos_centro))
	departamentos_i = list()
	for depart in departamentos_centro:
		try:
			departamentos_i.append(depart.find_elements_by_xpath('.//a')[0].text)
		except:
			departamentos_i.append(depart.find_elements_by_xpath('.//div/div')[0].text)

	departamentos.append(departamentos_i)
	driver.back()

print('Centros', len(centros))
print('Campus', len(campus))
print('Departamentos', len(departamentos)) 

#CAMPUS SUR
centros_campus = driver.find_elements_by_xpath('//*[@id="subcanales"]/li[4]/ul/li')
links = len(driver.find_elements_by_xpath('//*[@id="subcanales"]/li[4]/ul/li/a'))
print('len centros', len(centros_campus), 'len links', links)

for centro in centros_campus:
	centros.append(centro.find_elements_by_xpath('.//a')[0].text)

for link in range(0, links):
	centro = driver.find_elements_by_xpath('//*[@id="subcanales"]/li[4]/ul/li/a')
	centro[link].click()
	campus.append(driver.find_elements_by_xpath('//*[@id="directorio-03"]/div/h2')[0].text)

	departamentos_centro = driver.find_elements_by_xpath('//*[@id="directorio-03"]/div/div')
	print('   DEPART_centro', len(departamentos_centro))
	departamentos_i = list()
	for depart in departamentos_centro:
		try:
			departamentos_i.append(depart.find_elements_by_xpath('.//a')[0].text)
		except:
			departamentos_i.append(depart.find_elements_by_xpath('.//div/div')[0].text)

	departamentos.append(departamentos_i)
	driver.back()


#RESULTADOS LEN = Nº CENTROS = 29
print('Centros', len(centros))
print('Campus', len(campus))
print('Departamentos', len(departamentos)) 


centros_departamentos = list()
campus_departamentos = list()
for i in range(0, len(centros)):
	centros_departamentos.append([centros[i]] * len(departamentos[i]))
	campus_departamentos.append([campus[i]] * len(departamentos[i]))

departamentos = sum(departamentos, []) #flat list
centros_departamentos = sum(centros_departamentos, []) #flat list
campus_departamentos = sum(campus_departamentos, []) #flat list

#RESULTADOS LEN = Nº DEPARTAMENTOS = 95
print(len(centros_departamentos), len(departamentos), len(campus_departamentos))





'''
#GRADO
url = 'https://www.upm.es/Estudiantes/Estudios_Titulaciones/EstudiosOficialesGrado'
driver = webdriver.Chrome(driver_path, options=option)
driver.get(url)

#TECNOLOGÍAS AGROFORESTALES Y MEDIOAMBIENTALES (TAM)
grado_TAM_nombre = list()
grado_TAM_centro = list()
grado_TAM = driver.find_elements_by_xpath('.//*[@id="central"]/div/div[1]/div/div/div[1]/table/tbody/tr')
for grado in grado_TAM:
	grado_TAM_nombre_i = grado.find_elements_by_xpath('.//td/a/strong') or grado.find_elements_by_xpath('.//td/strong')
	grado_TAM_nombre.append(grado_TAM_nombre_i[0].text)
	centro = grado.find_elements_by_xpath('.//td')[0].text
	grado_TAM_centro.append(centro.partition('\n')[2])

#print(grado_TAM_nombre)
#print(grado_TAM_centro)

#TECNOLOGÍAS DE LA ARQUITECTURA E INGENIERÍA DE CAMINOS Y CIVIL
grado_TAICC_nombre = list()
grado_TAICC_centro = list()
grado_TAICC = driver.find_elements_by_xpath('.//*[@id="central"]/div/div[1]/div/div/div[2]/table/tbody/tr')
for grado in grado_TAICC:
	grado_TAICC_nombre_i = grado.find_elements_by_xpath('.//td/a/strong') or grado.find_elements_by_xpath('.//td/strong')
	grado_TAICC_nombre.append(grado_TAICC_nombre_i[0].text)
	centro = grado.find_elements_by_xpath('.//td')[0].text
	grado_TAICC_centro.append(centro.partition('\n')[2])

#print(grado_TAICC_nombre)
#print(grado_TAICC_centro)


#TECNOLOGÍAS INDUSTRIALES
grado_TI_nombre = list()
grado_TI_centro = list()
grado_TI = driver.find_elements_by_xpath('.//*[@id="central"]/div/div[1]/div/div/div[3]/table/tbody/tr')
for grado in grado_TI:
	grado_TI_nombre_i = grado.find_elements_by_xpath('.//td/a/strong') or grado.find_elements_by_xpath('.//td/strong')
	grado_TI_nombre.append(grado_TI_nombre_i[0].text)
	centro = grado.find_elements_by_xpath('.//td')[0].text
	grado_TI_centro.append(centro.partition('\n')[2])

#print(grado_TI_nombre)
#print(grado_TI_centro)

#TECNOLOGÍAS DE LA INFORMACIÓN Y LAS COMUNICACIONES
grado_TIC_nombre = list()
grado_TIC_centro = list()
grado_TIC = driver.find_elements_by_xpath('.//*[@id="central"]/div/div[1]/div/div/div[4]/table/tbody/tr')
for grado in grado_TIC:
	grado_TIC_nombre_i = grado.find_elements_by_xpath('.//td/a/strong') or grado.find_elements_by_xpath('.//td/strong')
	grado_TIC_nombre.append(grado_TIC_nombre_i[0].text)
	centro = grado.find_elements_by_xpath('.//td')[0].text
	grado_TIC_centro.append(centro.partition('\n')[2])

#print(grado_TIC_nombre)
#print(grado_TIC_centro)

#DEPORTE
grado_DEPORTE_nombre = list()
grado_DEPORTE_centro = list()
grado_DEPORTE = driver.find_elements_by_xpath('.//*[@id="central"]/div/div[1]/div/div/div[5]/table/tbody/tr')
for grado in grado_DEPORTE:
	grado_DEPORTE_nombre_i = grado.find_elements_by_xpath('.//td/a/strong') or grado.find_elements_by_xpath('.//td/strong')
	grado_DEPORTE_nombre.append(grado_DEPORTE_nombre_i[0].text)
	centro = grado.find_elements_by_xpath('.//td')[0].text
	grado_DEPORTE_centro.append(centro.partition('\n')[2])

#print(grado_DEPORTE_nombre)
#print(grado_DEPORTE_centro)

#DISEÑO Y MODA
grado_DYM_nombre = list()
grado_DYM_centro = list()
grado_DYM = driver.find_elements_by_xpath('.//*[@id="central"]/div/div[1]/div/div/div[6]/table/tbody/tr')
for grado in grado_DYM:
	grado_DYM_nombre_i = grado.find_elements_by_xpath('.//td/a/strong') or grado.find_elements_by_xpath('.//td/strong')
	grado_DYM_nombre.append(grado_DYM_nombre_i[0].text)
	centro = grado.find_elements_by_xpath('.//td')[0].text
	grado_DYM_centro.append(centro.partition('\n')[2])

#print(grado_DYM_nombre)
#print(grado_DYM_centro)

#NUEVOS GRADOS
grado_NG_nombre = list()
grado_NG_centro = list()
grado_NG = driver.find_elements_by_xpath('.//*[@id="central"]/div/div[1]/div/div/table/tbody/tr')

for grado in grado_NG:
	grado_NG_nombre_i = grado.find_elements_by_xpath('.//td/a/strong') or grado.find_elements_by_xpath('.//td/strong')
	grado_NG_nombre.append(grado_NG_nombre_i[0].text)
	centro = grado.find_elements_by_xpath('.//td')[0].text
	grado_NG_centro.append(centro.partition('\n')[2])

#print(grado_NG_nombre)
#print(grado_NG_centro)

grado_nombre = grado_TAM_nombre + grado_TAICC_nombre + grado_TI_nombre + grado_TIC_nombre + grado_DEPORTE_nombre + grado_DYM_nombre + grado_NG_nombre
grado_centro = grado_TAM_centro + grado_TAICC_centro + grado_TI_centro + grado_TIC_centro + grado_DEPORTE_centro + grado_DYM_centro + grado_NG_centro

print('Len grado_nombre/centro', len(grado_nombre), len(grado_centro))



#MASTER 
url = 'https://www.upm.es/Estudiantes/Estudios_Titulaciones/Estudios_Master/Programas?filtro=todos&orden=centro'

driver.get(url)

master = driver.find_elements_by_xpath('//*[@id="masteres_lista"]/div')
master_centro = list()
master_nombre = list()

for centro in master:
	#print(centro.find_elements_by_xpath('.//h3')[0].text)
	master = centro.find_elements_by_xpath('.//ul/li')
	
	master_centro.append([centro.find_elements_by_xpath('.//h3')[0].text] * len(master)) #list of lists
	#print('Nº masters', len(master))

	for masters in master:

		master = masters.find_elements_by_xpath('.//a')
		#print(master[0].text)
		master_nombre.append(master[0].text)

master_centro = sum(master_centro, []) #flat list
print('Len master_nombre/centro', len(master_centro), len(master_nombre))


#MASTER 
url = 'https://www.upm.es/Estudiantes/Estudios_Titulaciones/Estudios_Doctorado/Programas_de_Doctorado?orden=centro'

driver.get(url)

doctorado = driver.find_elements_by_xpath('//*[@id="masteres_lista"]/div')
doctorado_centro = list()
doctorado_nombre = list()

for centro in doctorado:
	#print(centro.find_elements_by_xpath('.//h3')[0].text)
	doctorado = centro.find_elements_by_xpath('.//ul/li')
	
	doctorado_centro.append([centro.find_elements_by_xpath('.//h3')[0].text] * len(doctorado)) #list of lists
	#print('Nº doctorados', len(doctorado))

	for doctorados in doctorado:

		doctorado = doctorados.find_elements_by_xpath('.//a')
		#print(master[0].text)
		doctorado_nombre.append(doctorado[0].text)
		
doctorado_centro = sum(doctorado_centro, []) #flat list
print('Len doctorado_nombre/centro', len(doctorado_centro), len(doctorado_nombre))


'''


#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#DEPARTAMENTOS DATASET

curso_academico = ['202021'] * len(departamentos) #2020-2021
cod_universidad = ['025'] * len(departamentos)
des_universidad = ['Universidad Politécnica de Madrid'] * len(departamentos)
cod_departamento = ['xx'] * len(departamentos) #no se donde encontrarlo
des_departamento = departamentos 
cod_municipio = ['xx'] * len(departamentos) #no se donde encontrarlo. No es codigo postal
des_municipio = ['xx'] * len(departamentos) #no se obtener de la web upm
cod_campus = ['xx'] * len(departamentos) #no se donde encontrarlo
des_campus = campus_departamentos #no hay departamentos en RUCT. Solo en UPM web
cod_situacion_departamento = ['xx'] * len(departamentos) 
des_situacion_departamento = ['xx'] * len(departamentos)
fecha_desde_situacion_departamento = ['xx'] * len(departamentos)

data = {'curso_academico':curso_academico,
		'codigo_universidad':cod_universidad,
		'nombre_universidad':des_universidad,
		'codigo_departamento':cod_departamento,
		'nombre_departamento':des_departamento, 
		'codigo_municipio':cod_municipio,
		'nombre_municipio':des_municipio,
		'codigo_campus':cod_campus,
		'descripcion_campus':des_campus,
		'codigo_situacion_departamento':cod_situacion_departamento,
		'descripcion_situacion_departamento':des_situacion_departamento,
		'fecha_desde_situacion_departamento':fecha_desde_situacion_departamento,
}

departamentos_df = DataFrame(data)
departamentos_df.to_csv('UPM-departamentos.csv')