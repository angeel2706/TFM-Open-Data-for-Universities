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



#----------------------------------------------------------------------------------
des_tipo_estudio = list()
cod_tipo_estudio = list()
cod_interuniversitario = list()
cod_rol_coordinacion = list()

#TITULACIONES - GRADO
url = 'https://www.educacion.gob.es/ruct/consultaestudios?actual=estudios'
driver = webdriver.Chrome(driver_path, options=option)
driver.get(url)
#driver.maximize_window()

uni = driver.find_elements_by_xpath('//*[@id="codigoUniversidad"]')
uni[0].click()
UPM = driver.find_elements_by_xpath('//*[@id="codigoUniversidad"]/option[79]')
UPM[0].click()

nivel_academico = driver.find_elements_by_xpath('//*[@id="codigoTipo"]')
nivel_academico[0].click()
grado = driver.find_elements_by_xpath('//*[@id="codigoTipo"]/option[4]')
grado[0].click()
buscar = driver.find_elements_by_xpath('//*[@id="consultaestudios_listaestudios"]')
buscar[0].click()

cod_grado = list()
nombre_grado = list()
estado_grado = list()
rama_grado = list()
cod_centro_grado = list()
nombre_centro_grado = list()
anio_inicio = list()
des_grado_presencialidad = list()
num_creditos_necesarios = list()
cod_idioma_extranjero = list()
des_idioma_extranjero = list()

#PAGINA 1
grados = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr')
links = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a'))
print('\nNº grados pagina 1: ', len(grados))

for grado in grados:
	cod_grado.append(grado.find_elements_by_xpath('.//td[1]')[0].text)
	nombre_grado.append(grado.find_elements_by_xpath('.//td[2]')[0].text)
	estado_grado.append(grado.find_elements_by_xpath('.//td[5]')[0].text)
	cod_tipo_estudio.append('G')
	des_tipo_estudio.append('Grado')

print('len cod - nombre - estado , grado', len(cod_grado), len(nombre_grado), len(estado_grado))

for link in range(0, links):
	#Un master no tiene rama
	try: 
		titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
		titulo[link].click()
		rama_click = driver.find_elements_by_xpath('//*[@id="ui-id-1"]/span')
		rama_click[0].click()
		rama = driver.find_elements_by_xpath('//*[@id="estudio_descripcionRama"]')[0].text
		rama_grado.append(rama)

		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')
	
		driver.back()

	except:
		rama = 'None'
		rama_grado.append(rama)
		
		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')

		driver.back()


	titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
	titulo[link].click()
	try:
		centros_click = driver.find_elements_by_xpath('//*[@id="tab3"]')
		centros_click[0].click()
		codigo = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[2]')[0].text
		cod_centro_grado.append(codigo)
		centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]/a')[0].text
		nombre_centro_grado.append(centro)
		driver.back()
	except:
		centros_click = driver.find_elements_by_xpath('//*[@id="ui-id-2"]/span')
		centros_click[0].click()
		codigo = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[2]')[0].text
		cod_centro_grado.append(codigo)
		centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]/a')[0].text
		nombre_centro_grado.append(centro)
		driver.back()


links2 = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]'))
print('links2', links2)
for i in range(0, links2):
	try:
		detalle = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]/a')
		detalle[i].click()
		datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
		datos_i = list()
		print('len DATOS', len(datos))
		#Navegando menu 'Datos del titulo'
		for dat in range(0, len(datos)):
			datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
			datos_i.append(datos[dat].text)
			

			#DESCRIPCION DEL TITULO
			if 'Descripción del título' in datos[dat].text:
				datos[dat].click()
				descripcion_click = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/ul/li')
				descripcion_click_i = list()
				print('len DESCRIPCION', len(descripcion_click))

				#Navegando en 'Descripcion del titulo'
				for desc in range(0, len(descripcion_click)):

					#Click en 'Universidades y centros'
					if 'Universidades y centros' in descripcion_click[desc].text:
						
						try:
							descripcion_click_i.append(descripcion_click[desc].text)
							descripcion_click[desc].click()

							centro_uni = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]')
							centro_uni_i = list()
							centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[4]/a')
							participantes = driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[1]')
							participantes_i = list()
							for part in range(0, len(participantes)):
								#Si es = 4, es una universidad española
								participantes_i.append(len(participantes[part].text))
							
							cod_interuniversitario_i = list()
							#Es 'Interuniversitario', comprobar si hay universidades extranjeras
							if len(centro_uni) >= 2: #Centros
								for part in participantes_i:
									if part >= 5:
										cod_interuniversitario_i.append('2')
									if part < 5:
										cod_interuniversitario_i.append('1')

								if '2' in cod_interuniversitario_i:
									cod_interuniversitario.append('2')
								else:
									cod_interuniversitario.append('1')

							#A priori 'No interuniversitario'
							#Comprobacion interuniversitario, sino 'No interuniversitario'
							elif len(centro_uni) < 2:
								if len(participantes) >= 2:
									for part in participantes_i:
										if part >= 5:
											cod_interuniversitario_i.append('2')
										if part < 5:
											cod_interuniversitario_i.append('1')

									if '2' in cod_interuniversitario_i:
										cod_interuniversitario.append('2')
									else:
										cod_interuniversitario.append('1')


								if len(participantes) < 2:
									cod_interuniversitario.append('0')

							print('---------------')
							#Rol Coordinacion 
							print('cod_interuniversitario', cod_interuniversitario[-1])
							print(driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text)
							if cod_interuniversitario[-1] == '1' or cod_interuniversitario[-1] == '2':
								if 'Universidad Politécnica de Madrid' in driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text:
									cod_rol_coordinacion.append('1')
								else:
									cod_rol_coordinacion.append('0')	
							if cod_interuniversitario[-1] == '0':
								cod_rol_coordinacion.append('8')
							print('cod_rol_coordinacion', cod_rol_coordinacion)

							for j in range(0, len(centro_uni)):
								
								centro_uni_i.append(centro_uni[j].text)
								if 'Universidad Politécnica de Madrid' in centro_uni[j].text:

									print('  UPM', centro_uni[j].text)
									centro[j].click()
									try:
										presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_presencial"]')[0].get_attribute('checked')
										semi_presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_semipresencial"]')[0].get_attribute('checked')
										a_distancia = driver.find_elements_by_xpath('//*[@id="datosCentro_virtual"]')[0].get_attribute('checked')
										print('  Try presencialidad')

										#print(presencial, semi_presencial, a_distancia)

										des_grado_presencialidad_i = list()
										if presencial == 'true':
											des_grado_presencialidad_i.append('Estudio presencial')
										if semi_presencial == 'true':
											des_grado_presencialidad_i.append('Estudio semipresencial')
										if a_distancia == 'true':
											des_grado_presencialidad_i.append('Estudio no presencial')
										if len(des_grado_presencialidad_i) >= 2:
											des_grado_presencialidad_i = list()
											des_grado_presencialidad_i.append('Varias modalidades')
										if presencial != 'true' and semi_presencial != 'true' and a_distancia != 'true': #para DOCTORADOS
											des_grado_presencialidad_i.append(' ')

										des_grado_presencialidad.append(des_grado_presencialidad_i[0])

									except:
										des_grado_presencialidad.append(' ')
										print('  Except presencialidad')


									try:
										idiomas = driver.find_elements_by_xpath('//*[@id="lengua"]/tbody/tr/td')
										idiomas_i = list()
										print('  Try idiomas')
										for i in range(0, len(idiomas)):
											idiomas_i.append(idiomas[i].text)

										if len(idiomas_i) == 1 and 'CASTELLANO ' in idiomas_i:
											cod_idioma_extranjero.append('0')
											des_idioma_extranjero.append('No')
										elif len(idiomas_i) == 1 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('1')
											des_idioma_extranjero.append('Ingles')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('2')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en ingles')
										elif len(idiomas_i) == 1 and 'INGLÉS ' not in idiomas_i and 'CASTELLANO ' not in idiomas_i:
											cod_idioma_extranjero.append('3')
											des_idioma_extranjero.append('Otro idioma extranjero')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' not in idiomas_i:
											cod_idioma_extranjero.append('4')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en otro idioma extranjero')
										else:
											cod_idioma_extranjero.append('None')
											des_idioma_extranjero.append('None')

										driver.back()
										driver.back()
										driver.back()
										break

									except:
										cod_idioma_extranjero.append('None')
										des_idioma_extranjero.append('None')
										print('  Except idiomas')
										driver.back()
										driver.back()
										driver.back()
										break


								else:
									print('	 No UPM', centro_uni[j].text, 'seguimos')
									#continue


							#En caso de que no haya 'Universidad Politécnica de Madrid  '
							if 'Universidad Politécnica de Madrid' not in centro_uni_i[-1]:
								print('   ', centro_uni_i)
								des_grado_presencialidad.append(' ')
								cod_idioma_extranjero.append('None')
								des_idioma_extranjero.append('None')
								print('	  No UPM final \n')

						except:
							print('FALLO UNIVERSIDADES')
							descripcion_click_i.pop(-1)
							driver.back()
							driver.back()
							pass


				if 'Universidades y centros' not in descripcion_click_i:
					print('No hay Universidadades y centros')
					des_grado_presencialidad.append(' ')
					cod_idioma_extranjero.append('None')
					des_idioma_extranjero.append('None')
					cod_rol_coordinacion.append(' ')


			if 'Calendario de implantación' in datos_i[-1]:
				datos[dat].click()

				try:
					anio = driver.find_elements_by_xpath('//*[@id="calendarioImplantacion_curso_Inicio"]')[0]
					anio_value = anio.get_attribute('value')
					print('  Try Año inicio', anio_value)
					if anio_value == '0':
						anio_inicio.append('8888')
						driver.back()
					
					else:
						anio_inicio.append(anio_value)
						driver.back()

					
				except:
					print('  Except Año inicio')
					anio_inicio.append('8888')
					driver.back()


		if 'Calendario de implantación' not in datos_i:
			print('      Not anio inicio fin')
			anio_inicio.append('8888')


		#Pagina principal 'Detalle'
		driver.back()


	#Cuando no hay link 'Ver en Detalle'!
	except IndexError as exception:
		print('No detalle')
		des_grado_presencialidad.append(' ')
		cod_idioma_extranjero.append('None')
		des_idioma_extranjero.append('None')
		anio_inicio.append('8888')
		cod_interuniversitario.append(' ')
		cod_rol_coordinacion.append(' ')
		

print('RESUMEN GRADO')
print('rama' ,len(rama_grado))
print(rama_grado)
print('num creditos necesarios', len(num_creditos_necesarios))
print('cod centro grado', len(cod_centro_grado))
print(cod_centro_grado)
print('nombre centro grado', len(nombre_centro_grado))
print('grado presencialidad', len(des_grado_presencialidad))
print('idioma extranjero', len(des_idioma_extranjero))
print('anio inicio', len(anio_inicio))
print(anio_inicio)
print(len(cod_interuniversitario))
print(len(cod_rol_coordinacion))


#PAGINA 2
pagina2 = driver.find_elements_by_xpath('//*[@id="ver"]/span[2]/a[1]')
pagina2[0].click()
grados = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr')
links = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a'))
print('Nº grados pagina 2: ', len(grados))

for grado in grados:
	cod_grado.append(grado.find_elements_by_xpath('.//td[1]')[0].text)
	nombre_grado.append(grado.find_elements_by_xpath('.//td[2]')[0].text)
	estado_grado.append(grado.find_elements_by_xpath('.//td[5]')[0].text)
	cod_tipo_estudio.append('G')
	des_tipo_estudio.append('Grado')

for link in range(0, links):
	#Un master no tiene rama
	try: 
		titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
		titulo[link].click()
		rama_click = driver.find_elements_by_xpath('//*[@id="ui-id-1"]/span')
		rama_click[0].click()
		rama = driver.find_elements_by_xpath('//*[@id="estudio_descripcionRama"]')[0].text
		rama_grado.append(rama)

		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')
	
		driver.back()

	except:
		rama = 'None'
		rama_grado.append(rama)
		
		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')

		driver.back()

	titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
	titulo[link].click()
	centros_click = driver.find_elements_by_xpath('//*[@id="tab3"]')
	centros_click[0].click()
	codigo = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[2]')[0].text
	cod_centro_grado.append(codigo)
	centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]/a')[0].text
	nombre_centro_grado.append(centro)
	driver.back()

links2 = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]'))
print('links2', links2)
for i in range(0, links2):
	try:
		detalle = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]/a')
		detalle[i].click()
		datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
		datos_i = list()
		print('len DATOS', len(datos))
		#Navegando menu 'Datos del titulo'
		for dat in range(0, len(datos)):
			datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
			datos_i.append(datos[dat].text)
			

			#DESCRIPCION DEL TITULO
			if 'Descripción del título' in datos[dat].text:
				datos[dat].click()
				descripcion_click = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/ul/li')
				descripcion_click_i = list()
				print('len DESCRIPCION', len(descripcion_click))

				#Navegando en 'Descripcion del titulo'
				for desc in range(0, len(descripcion_click)):

					#Click en 'Universidades y centros'
					if 'Universidades y centros' in descripcion_click[desc].text:
						
						try:
							descripcion_click_i.append(descripcion_click[desc].text)
							descripcion_click[desc].click()

							centro_uni = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]')
							centro_uni_i = list()
							centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[4]/a')
							participantes = driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[1]')
							participantes_i = list()
							for part in range(0, len(participantes)):
								#Si es = 4, es una universidad española
								participantes_i.append(len(participantes[part].text))
							
							cod_interuniversitario_i = list()
							#Es 'Interuniversitario', comprobar si hay universidades extranjeras
							if len(centro_uni) >= 2: #Centros
								for part in participantes_i:
									if part >= 5:
										cod_interuniversitario_i.append('2')
									if part < 5:
										cod_interuniversitario_i.append('1')

								if '2' in cod_interuniversitario_i:
									cod_interuniversitario.append('2')
								else:
									cod_interuniversitario.append('1')

							#A priori 'No interuniversitario'
							#Comprobacion interuniversitario, sino 'No interuniversitario'
							elif len(centro_uni) < 2:
								if len(participantes) >= 2:
									for part in participantes_i:
										if part >= 5:
											cod_interuniversitario_i.append('2')
										if part < 5:
											cod_interuniversitario_i.append('1')

									if '2' in cod_interuniversitario_i:
										cod_interuniversitario.append('2')
									else:
										cod_interuniversitario.append('1')


								if len(participantes) < 2:
									cod_interuniversitario.append('0')

							print('---------------')
							#Rol Coordinacion 
							print('cod_interuniversitario', cod_interuniversitario[-1])
							print(driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text)
							if cod_interuniversitario[-1] == '1' or cod_interuniversitario[-1] == '2':
								if 'Universidad Politécnica de Madrid' in driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text:
									cod_rol_coordinacion.append('1')
								else:
									cod_rol_coordinacion.append('0')	
							if cod_interuniversitario[-1] == '0':
								cod_rol_coordinacion.append('8')
							print('cod_rol_coordinacion', cod_rol_coordinacion)


							for j in range(0, len(centro_uni)):
								
								centro_uni_i.append(centro_uni[j].text)
								if 'Universidad Politécnica de Madrid' in centro_uni[j].text:

									print('  UPM', centro_uni[j].text)
									centro[j].click()
									try:
										presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_presencial"]')[0].get_attribute('checked')
										semi_presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_semipresencial"]')[0].get_attribute('checked')
										a_distancia = driver.find_elements_by_xpath('//*[@id="datosCentro_virtual"]')[0].get_attribute('checked')
										print('  Try presencialidad')

										#print(presencial, semi_presencial, a_distancia)

										des_grado_presencialidad_i = list()
										if presencial == 'true':
											des_grado_presencialidad_i.append('Estudio presencial')
										if semi_presencial == 'true':
											des_grado_presencialidad_i.append('Estudio semipresencial')
										if a_distancia == 'true':
											des_grado_presencialidad_i.append('Estudio no presencial')
										if len(des_grado_presencialidad_i) >= 2:
											des_grado_presencialidad_i = list()
											des_grado_presencialidad_i.append('Varias modalidades')
										if presencial != 'true' and semi_presencial != 'true' and a_distancia != 'true': #para DOCTORADOS
											des_grado_presencialidad_i.append(' ')

										des_grado_presencialidad.append(des_grado_presencialidad_i[0])

									except:
										des_grado_presencialidad.append(' ')
										print('  Except presencialidad')


									try:
										idiomas = driver.find_elements_by_xpath('//*[@id="lengua"]/tbody/tr/td')
										idiomas_i = list()
										print('  Try idiomas')
										for i in range(0, len(idiomas)):
											idiomas_i.append(idiomas[i].text)

										if len(idiomas_i) == 1 and 'CASTELLANO ' in idiomas_i:
											cod_idioma_extranjero.append('0')
											des_idioma_extranjero.append('No')
										elif len(idiomas_i) == 1 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('1')
											des_idioma_extranjero.append('Ingles')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('2')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en ingles')
										elif len(idiomas_i) == 1 and 'INGLÉS ' not in idiomas_i and 'CASTELLANO ' not in idiomas_i:
											cod_idioma_extranjero.append('3')
											des_idioma_extranjero.append('Otro idioma extranjero')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' not in idiomas_i:
											cod_idioma_extranjero.append('4')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en otro idioma extranjero')
										else:
											cod_idioma_extranjero.append('None')
											des_idioma_extranjero.append('None')

										driver.back()
										driver.back()
										driver.back()
										break

									except:
										cod_idioma_extranjero.append('None')
										des_idioma_extranjero.append('None')
										print('  Except idiomas')
										driver.back()
										driver.back()
										driver.back()
										break


								else:
									print('	 No UPM', centro_uni[j].text, 'seguimos')
									#continue


							#En caso de que no haya 'Universidad Politécnica de Madrid  '
							if 'Universidad Politécnica de Madrid' not in centro_uni_i[-1]:
								print('   ', centro_uni_i)
								des_grado_presencialidad.append(' ')
								cod_idioma_extranjero.append('None')
								des_idioma_extranjero.append('None')
								print('	  No UPM final \n')

						except:
							print('FALLO UNIVERSIDADES')
							descripcion_click_i.pop(-1)
							driver.back()
							driver.back()
							pass


				if 'Universidades y centros' not in descripcion_click_i:
					print('No hay Universidadades y centros')
					des_grado_presencialidad.append(' ')
					cod_idioma_extranjero.append('None')
					des_idioma_extranjero.append('None')
					cod_rol_coordinacion.append(' ')


			if 'Calendario de implantación' in datos_i[-1]:
				datos[dat].click()

				try:
					anio = driver.find_elements_by_xpath('//*[@id="calendarioImplantacion_curso_Inicio"]')[0]
					anio_value = anio.get_attribute('value')
					print('  Try Año inicio', anio_value)
					if anio_value == '0':
						anio_inicio.append('8888')
						driver.back()
					
					else:
						anio_inicio.append(anio_value)
						driver.back()

					
				except:
					print('  Except Año inicio')
					anio_inicio.append('8888')
					driver.back()


		if 'Calendario de implantación' not in datos_i:
			print('      Not anio inicio fin')
			anio_inicio.append('8888')


		#Pagina principal 'Detalle'
		driver.back()


	#Cuando no hay link 'Ver en Detalle'!
	except IndexError as exception:
		print('No detalle')
		des_grado_presencialidad.append(' ')
		cod_idioma_extranjero.append('None')
		des_idioma_extranjero.append('None')
		anio_inicio.append('8888')
		cod_interuniversitario.append(' ')
		cod_rol_coordinacion.append(' ')
		

print('RESUMEN GRADO')
print('rama' ,len(rama_grado))
print(rama_grado)
print('num creditos necesarios', len(num_creditos_necesarios))
print('cod centro grado', len(cod_centro_grado))
print(cod_centro_grado)
print('nombre centro grado', len(nombre_centro_grado))
print('grado presencialidad', len(des_grado_presencialidad))
print('idioma extranjero', len(des_idioma_extranjero))
print('anio inicio', len(anio_inicio))
print(anio_inicio)
print(len(cod_interuniversitario))
print(len(cod_rol_coordinacion))


#PAGINA 3
pagina3 = driver.find_elements_by_xpath('//*[@id="ver"]/span[2]/a[4]')
pagina3[0].click()
grados = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr')
links = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a'))
print('Nº grados pagina 3: ', len(grados))

for grado in grados:
	cod_grado.append(grado.find_elements_by_xpath('.//td[1]')[0].text)
	nombre_grado.append(grado.find_elements_by_xpath('.//td[2]')[0].text)
	estado_grado.append(grado.find_elements_by_xpath('.//td[5]')[0].text)
	cod_tipo_estudio.append('G')
	des_tipo_estudio.append('Grado')

for link in range(0, links):
	#Un master no tiene rama
	try: 
		titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
		titulo[link].click()
		rama_click = driver.find_elements_by_xpath('//*[@id="ui-id-1"]/span')
		rama_click[0].click()
		rama = driver.find_elements_by_xpath('//*[@id="estudio_descripcionRama"]')[0].text
		rama_grado.append(rama)

		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')
	
		driver.back()

	except:
		rama = 'None'
		rama_grado.append(rama)
		
		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')

		driver.back()

	titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
	titulo[link].click()
	centros_click = driver.find_elements_by_xpath('//*[@id="tab3"]')
	centros_click[0].click()
	codigo = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[2]')[0].text
	cod_centro_grado.append(codigo)
	centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]/a')[0].text
	nombre_centro_grado.append(centro)
	driver.back()

links2 = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]'))
print('links2', links2)
for i in range(0, links2):
	try:
		detalle = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]/a')
		detalle[i].click()
		datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
		datos_i = list()
		print('len DATOS', len(datos))
		#Navegando menu 'Datos del titulo'
		for dat in range(0, len(datos)):
			datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
			datos_i.append(datos[dat].text)
			

			#DESCRIPCION DEL TITULO
			if 'Descripción del título' in datos[dat].text:
				datos[dat].click()
				descripcion_click = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/ul/li')
				descripcion_click_i = list()
				print('len DESCRIPCION', len(descripcion_click))

				#Navegando en 'Descripcion del titulo'
				for desc in range(0, len(descripcion_click)):

					#Click en 'Universidades y centros'
					if 'Universidades y centros' in descripcion_click[desc].text:
						
						try:
							descripcion_click_i.append(descripcion_click[desc].text)
							descripcion_click[desc].click()

							centro_uni = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]')
							centro_uni_i = list()
							centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[4]/a')
							participantes = driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[1]')
							participantes_i = list()
							for part in range(0, len(participantes)):
								#Si es = 4, es una universidad española
								participantes_i.append(len(participantes[part].text))
							
							cod_interuniversitario_i = list()
							#Es 'Interuniversitario', comprobar si hay universidades extranjeras
							if len(centro_uni) >= 2: #Centros
								for part in participantes_i:
									if part >= 5:
										cod_interuniversitario_i.append('2')
									if part < 5:
										cod_interuniversitario_i.append('1')

								if '2' in cod_interuniversitario_i:
									cod_interuniversitario.append('2')
								else:
									cod_interuniversitario.append('1')

							#A priori 'No interuniversitario'
							#Comprobacion interuniversitario, sino 'No interuniversitario'
							elif len(centro_uni) < 2:
								if len(participantes) >= 2:
									for part in participantes_i:
										if part >= 5:
											cod_interuniversitario_i.append('2')
										if part < 5:
											cod_interuniversitario_i.append('1')

									if '2' in cod_interuniversitario_i:
										cod_interuniversitario.append('2')
									else:
										cod_interuniversitario.append('1')


								if len(participantes) < 2:
									cod_interuniversitario.append('0')

							print('---------------')
							#Rol Coordinacion 
							print('cod_interuniversitario', cod_interuniversitario[-1])
							print(driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text)
							if cod_interuniversitario[-1] == '1' or cod_interuniversitario[-1] == '2':
								if 'Universidad Politécnica de Madrid' in driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text:
									cod_rol_coordinacion.append('1')
								else:
									cod_rol_coordinacion.append('0')	
							if cod_interuniversitario[-1] == '0':
								cod_rol_coordinacion.append('8')
							print('cod_rol_coordinacion', cod_rol_coordinacion)


							for j in range(0, len(centro_uni)):
								
								centro_uni_i.append(centro_uni[j].text)
								if 'Universidad Politécnica de Madrid' in centro_uni[j].text:

									print('  UPM', centro_uni[j].text)
									centro[j].click()
									try:
										presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_presencial"]')[0].get_attribute('checked')
										semi_presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_semipresencial"]')[0].get_attribute('checked')
										a_distancia = driver.find_elements_by_xpath('//*[@id="datosCentro_virtual"]')[0].get_attribute('checked')
										print('  Try presencialidad')

										#print(presencial, semi_presencial, a_distancia)

										des_grado_presencialidad_i = list()
										if presencial == 'true':
											des_grado_presencialidad_i.append('Estudio presencial')
										if semi_presencial == 'true':
											des_grado_presencialidad_i.append('Estudio semipresencial')
										if a_distancia == 'true':
											des_grado_presencialidad_i.append('Estudio no presencial')
										if len(des_grado_presencialidad_i) >= 2:
											des_grado_presencialidad_i = list()
											des_grado_presencialidad_i.append('Varias modalidades')
										if presencial != 'true' and semi_presencial != 'true' and a_distancia != 'true': #para DOCTORADOS
											des_grado_presencialidad_i.append(' ')

										des_grado_presencialidad.append(des_grado_presencialidad_i[0])

									except:
										des_grado_presencialidad.append(' ')
										print('  Except presencialidad')


									try:
										idiomas = driver.find_elements_by_xpath('//*[@id="lengua"]/tbody/tr/td')
										idiomas_i = list()
										print('  Try idiomas')
										for i in range(0, len(idiomas)):
											idiomas_i.append(idiomas[i].text)

										if len(idiomas_i) == 1 and 'CASTELLANO ' in idiomas_i:
											cod_idioma_extranjero.append('0')
											des_idioma_extranjero.append('No')
										elif len(idiomas_i) == 1 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('1')
											des_idioma_extranjero.append('Ingles')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('2')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en ingles')
										elif len(idiomas_i) == 1 and 'INGLÉS ' not in idiomas_i and 'CASTELLANO ' not in idiomas_i:
											cod_idioma_extranjero.append('3')
											des_idioma_extranjero.append('Otro idioma extranjero')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' not in idiomas_i:
											cod_idioma_extranjero.append('4')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en otro idioma extranjero')
										else:
											cod_idioma_extranjero.append('None')
											des_idioma_extranjero.append('None')

										driver.back()
										driver.back()
										driver.back()
										break

									except:
										cod_idioma_extranjero.append('None')
										des_idioma_extranjero.append('None')
										print('  Except idiomas')
										driver.back()
										driver.back()
										driver.back()
										break


								else:
									print('	 No UPM', centro_uni[j].text, 'seguimos')
									#continue


							#En caso de que no haya 'Universidad Politécnica de Madrid  '
							if 'Universidad Politécnica de Madrid' not in centro_uni_i[-1]:
								print('   ', centro_uni_i)
								des_grado_presencialidad.append(' ')
								cod_idioma_extranjero.append('None')
								des_idioma_extranjero.append('None')
								print('	  No UPM final \n')

						except:
							print('FALLO UNIVERSIDADES')
							descripcion_click_i.pop(-1)
							driver.back()
							driver.back()
							pass


				if 'Universidades y centros' not in descripcion_click_i:
					print('No hay Universidadades y centros')
					des_grado_presencialidad.append(' ')
					cod_idioma_extranjero.append('None')
					des_idioma_extranjero.append('None')
					cod_rol_coordinacion.append(' ')


			if 'Calendario de implantación' in datos_i[-1]:
				datos[dat].click()

				try:
					anio = driver.find_elements_by_xpath('//*[@id="calendarioImplantacion_curso_Inicio"]')[0]
					anio_value = anio.get_attribute('value')
					print('  Try Año inicio', anio_value)
					if anio_value == '0':
						anio_inicio.append('8888')
						driver.back()
					
					else:
						anio_inicio.append(anio_value)
						driver.back()

					
				except:
					print('  Except Año inicio')
					anio_inicio.append('8888')
					driver.back()


		if 'Calendario de implantación' not in datos_i:
			print('      Not anio inicio fin')
			anio_inicio.append('8888')


		#Pagina principal 'Detalle'
		driver.back()


	#Cuando no hay link 'Ver en Detalle'!
	except IndexError as exception:
		print('No detalle')
		des_grado_presencialidad.append(' ')
		cod_idioma_extranjero.append('None')
		des_idioma_extranjero.append('None')
		anio_inicio.append('8888')
		cod_interuniversitario.append(' ')
		cod_rol_coordinacion.append(' ')
		

print('RESUMEN GRADO')
print('rama' ,len(rama_grado))
print(rama_grado)
print('num creditos necesarios', len(num_creditos_necesarios))
print('cod centro grado', len(cod_centro_grado))
print(cod_centro_grado)
print('nombre centro grado', len(nombre_centro_grado))
print('grado presencialidad', len(des_grado_presencialidad))
print('idioma extranjero', len(des_idioma_extranjero))
print('anio inicio', len(anio_inicio))
print(anio_inicio)
print(len(cod_interuniversitario))
print(len(cod_rol_coordinacion))
'''

'''
#----------------------------------------------------------------------------------
'''
'''
#TITULACIONES - MASTER
url = 'https://www.educacion.gob.es/ruct/consultaestudios?actual=estudios'
driver = webdriver.Chrome(driver_path, options=option)
driver.get(url)

uni = driver.find_elements_by_xpath('//*[@id="codigoUniversidad"]')
uni[0].click()
UPM = driver.find_elements_by_xpath('//*[@id="codigoUniversidad"]/option[79]')
UPM[0].click()

nivel_academico = driver.find_elements_by_xpath('//*[@id="codigoTipo"]')
nivel_academico[0].click()
master = driver.find_elements_by_xpath('//*[@id="codigoTipo"]/option[5]')
master[0].click()
buscar = driver.find_elements_by_xpath('//*[@id="consultaestudios_listaestudios"]')
buscar[0].click()

cod_master = list()
nombre_master = list()
estado_master = list()
rama_master = list()
cod_centro_master = list()
nombre_centro_master = list()

#PAGINA 1
masters = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr')
links = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a'))
print('Nº masters pagina 1: ', len(masters))

for master in masters:
	cod_master.append(master.find_elements_by_xpath('.//td[1]')[0].text)
	nombre_master.append(master.find_elements_by_xpath('.//td[2]')[0].text)
	estado_master.append(master.find_elements_by_xpath('.//td[5]')[0].text)
	cod_tipo_estudio.append('M')
	des_tipo_estudio.append('Master')

for link in range(0, links):
	#Un master no tiene rama
	try: 
		titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
		titulo[link].click()
		rama_click = driver.find_elements_by_xpath('//*[@id="ui-id-1"]/span')
		rama_click[0].click()
		rama = driver.find_elements_by_xpath('//*[@id="estudio_descripcionRama"]')[0].text
		rama_master.append(rama)

		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')
	
		driver.back()

	except:
		rama = 'None'
		rama_master.append(rama)
		
		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')

		driver.back()

	titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
	titulo[link].click()
	centros_click = driver.find_elements_by_xpath('//*[@id="tab3"]')
	centros_click[0].click()
	codigo = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[2]')[0].text
	cod_centro_master.append(codigo)
	centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]/a')[0].text
	nombre_centro_master.append(centro)
	driver.back()

links2 = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]'))
print('links2', links2)
for i in range(0, links2):
	try:
		detalle = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]/a')
		detalle[i].click()
		datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
		datos_i = list()
		print('len DATOS', len(datos))
		#Navegando menu 'Datos del titulo'
		for dat in range(0, len(datos)):
			datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
			datos_i.append(datos[dat].text)
			

			#DESCRIPCION DEL TITULO
			if 'Descripción del título' in datos[dat].text:
				datos[dat].click()
				descripcion_click = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/ul/li')
				descripcion_click_i = list()
				print('len DESCRIPCION', len(descripcion_click))

				#Navegando en 'Descripcion del titulo'
				for desc in range(0, len(descripcion_click)):

					#Click en 'Universidades y centros'
					if 'Universidades y centros' in descripcion_click[desc].text:
						
						try:
							descripcion_click_i.append(descripcion_click[desc].text)
							descripcion_click[desc].click()

							centro_uni = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]')
							centro_uni_i = list()
							centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[4]/a')
							participantes = driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[1]')
							participantes_i = list()
							for part in range(0, len(participantes)):
								#Si es = 4, es una universidad española
								participantes_i.append(len(participantes[part].text))
							
							cod_interuniversitario_i = list()
							#Es 'Interuniversitario', comprobar si hay universidades extranjeras
							if len(centro_uni) >= 2: #Centros
								for part in participantes_i:
									if part >= 5:
										cod_interuniversitario_i.append('2')
									if part < 5:
										cod_interuniversitario_i.append('1')

								if '2' in cod_interuniversitario_i:
									cod_interuniversitario.append('2')
								else:
									cod_interuniversitario.append('1')

							#A priori 'No interuniversitario'
							#Comprobacion interuniversitario, sino 'No interuniversitario'
							elif len(centro_uni) < 2:
								if len(participantes) >= 2:
									for part in participantes_i:
										if part >= 5:
											cod_interuniversitario_i.append('2')
										if part < 5:
											cod_interuniversitario_i.append('1')

									if '2' in cod_interuniversitario_i:
										cod_interuniversitario.append('2')
									else:
										cod_interuniversitario.append('1')


								if len(participantes) < 2:
									cod_interuniversitario.append('0')

							print('---------------')
							#Rol Coordinacion 
							print('cod_interuniversitario', cod_interuniversitario[-1])
							print(driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text)
							if cod_interuniversitario[-1] == '1' or cod_interuniversitario[-1] == '2':
								if 'Universidad Politécnica de Madrid' in driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text:
									cod_rol_coordinacion.append('1')
								else:
									cod_rol_coordinacion.append('0')	
							if cod_interuniversitario[-1] == '0':
								cod_rol_coordinacion.append('8')
							print('cod_rol_coordinacion', cod_rol_coordinacion)


							for j in range(0, len(centro_uni)):
								
								centro_uni_i.append(centro_uni[j].text)
								if 'Universidad Politécnica de Madrid' in centro_uni[j].text:

									print('  UPM', centro_uni[j].text)
									centro[j].click()
									try:
										presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_presencial"]')[0].get_attribute('checked')
										semi_presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_semipresencial"]')[0].get_attribute('checked')
										a_distancia = driver.find_elements_by_xpath('//*[@id="datosCentro_virtual"]')[0].get_attribute('checked')
										print('  Try presencialidad')

										#print(presencial, semi_presencial, a_distancia)

										des_grado_presencialidad_i = list()
										if presencial == 'true':
											des_grado_presencialidad_i.append('Estudio presencial')
										if semi_presencial == 'true':
											des_grado_presencialidad_i.append('Estudio semipresencial')
										if a_distancia == 'true':
											des_grado_presencialidad_i.append('Estudio no presencial')
										if len(des_grado_presencialidad_i) >= 2:
											des_grado_presencialidad_i = list()
											des_grado_presencialidad_i.append('Varias modalidades')
										if presencial != 'true' and semi_presencial != 'true' and a_distancia != 'true': #para DOCTORADOS
											des_grado_presencialidad_i.append(' ')

										des_grado_presencialidad.append(des_grado_presencialidad_i[0])

									except:
										des_grado_presencialidad.append(' ')
										print('  Except presencialidad')


									try:
										idiomas = driver.find_elements_by_xpath('//*[@id="lengua"]/tbody/tr/td')
										idiomas_i = list()
										print('  Try idiomas')
										for i in range(0, len(idiomas)):
											idiomas_i.append(idiomas[i].text)

										if len(idiomas_i) == 1 and 'CASTELLANO ' in idiomas_i:
											cod_idioma_extranjero.append('0')
											des_idioma_extranjero.append('No')
										elif len(idiomas_i) == 1 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('1')
											des_idioma_extranjero.append('Ingles')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('2')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en ingles')
										elif len(idiomas_i) == 1 and 'INGLÉS ' not in idiomas_i and 'CASTELLANO ' not in idiomas_i:
											cod_idioma_extranjero.append('3')
											des_idioma_extranjero.append('Otro idioma extranjero')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' not in idiomas_i:
											cod_idioma_extranjero.append('4')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en otro idioma extranjero')
										else:
											cod_idioma_extranjero.append('None')
											des_idioma_extranjero.append('None')

										driver.back()
										driver.back()
										driver.back()
										break

									except:
										cod_idioma_extranjero.append('None')
										des_idioma_extranjero.append('None')
										print('  Except idiomas')
										driver.back()
										driver.back()
										driver.back()
										break


								else:
									print('	 No UPM', centro_uni[j].text, 'seguimos')
									#continue


							#En caso de que no haya 'Universidad Politécnica de Madrid  '
							if 'Universidad Politécnica de Madrid' not in centro_uni_i[-1]:
								print('   ', centro_uni_i)
								des_grado_presencialidad.append(' ')
								cod_idioma_extranjero.append('None')
								des_idioma_extranjero.append('None')
								print('	  No UPM final \n')

						except:
							print('FALLO UNIVERSIDADES')
							descripcion_click_i.pop(-1)
							driver.back()
							driver.back()
							pass


				if 'Universidades y centros' not in descripcion_click_i:
					print('No hay Universidadades y centros')
					des_grado_presencialidad.append(' ')
					cod_idioma_extranjero.append('None')
					des_idioma_extranjero.append('None')
					cod_rol_coordinacion.append(' ')


			if 'Calendario de implantación' in datos_i[-1]:
				datos[dat].click()

				try:
					anio = driver.find_elements_by_xpath('//*[@id="calendarioImplantacion_curso_Inicio"]')[0]
					anio_value = anio.get_attribute('value')
					print('  Try Año inicio', anio_value)
					if anio_value == '0':
						anio_inicio.append('8888')
						driver.back()
					
					else:
						anio_inicio.append(anio_value)
						driver.back()

					
				except:
					print('  Except Año inicio')
					anio_inicio.append('8888')
					driver.back()


		if 'Calendario de implantación' not in datos_i:
			print('      Not anio inicio fin')
			anio_inicio.append('8888')


		#Pagina principal 'Detalle'
		driver.back()


	#Cuando no hay link 'Ver en Detalle'!
	except IndexError as exception:
		print('No detalle')
		des_grado_presencialidad.append(' ')
		cod_idioma_extranjero.append('None')
		des_idioma_extranjero.append('None')
		anio_inicio.append('8888')
		cod_interuniversitario.append(' ')
		cod_rol_coordinacion.append(' ')


print('RESUMEN MASTER')
print('rama' ,len(rama_master))
print(rama_master)
print('num creditos necesarios', len(num_creditos_necesarios))
print('cod centro master', len(cod_centro_master))
print('nombre centro master', len(nombre_centro_master))
print('grado presencialidad', len(des_grado_presencialidad))
print('idioma extranjero', len(des_idioma_extranjero))
print('anio inicio', len(anio_inicio))
print(anio_inicio)
print(len(cod_interuniversitario))
print(len(cod_rol_coordinacion))


#PAGINA 2
pagina2 = driver.find_elements_by_xpath('//*[@id="ver"]/span[2]/a[7]')
pagina2[0].click()
masters = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr')
links = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a'))
print('Nº masters pagina 2: ', len(masters))

for master in masters:
	cod_master.append(master.find_elements_by_xpath('.//td[1]')[0].text)
	nombre_master.append(master.find_elements_by_xpath('.//td[2]')[0].text)
	estado_master.append(master.find_elements_by_xpath('.//td[5]')[0].text)
	cod_tipo_estudio.append('M')
	des_tipo_estudio.append('Master')


for link in range(0, links):
	#Un master no tiene rama
	try: 
		titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
		titulo[link].click()
		rama_click = driver.find_elements_by_xpath('//*[@id="ui-id-1"]/span')
		rama_click[0].click()
		rama = driver.find_elements_by_xpath('//*[@id="estudio_descripcionRama"]')[0].text
		rama_master.append(rama)

		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')
	
		driver.back()

	except:
		rama = 'None'
		rama_master.append(rama)

		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')

		driver.back()

	titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
	titulo[link].click()
	centros_click = driver.find_elements_by_xpath('//*[@id="tab3"]')
	centros_click[0].click()
	codigo = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[2]')[0].text
	cod_centro_master.append(codigo)
	centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]/a')[0].text
	nombre_centro_master.append(centro)
	driver.back()

links2 = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]'))
print('links2', links2)
for i in range(0, links2):
	try:
		detalle = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]/a')
		detalle[i].click()
		datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
		datos_i = list()
		print('len DATOS', len(datos))
		#Navegando menu 'Datos del titulo'
		for dat in range(0, len(datos)):
			datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
			datos_i.append(datos[dat].text)
			

			#DESCRIPCION DEL TITULO
			if 'Descripción del título' in datos[dat].text:
				datos[dat].click()
				descripcion_click = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/ul/li')
				descripcion_click_i = list()
				print('len DESCRIPCION', len(descripcion_click))

				#Navegando en 'Descripcion del titulo'
				for desc in range(0, len(descripcion_click)):

					#Click en 'Universidades y centros'
					if 'Universidades y centros' in descripcion_click[desc].text:
						
						try:
							descripcion_click_i.append(descripcion_click[desc].text)
							descripcion_click[desc].click()

							centro_uni = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]')
							centro_uni_i = list()
							centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[4]/a')
							participantes = driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[1]')
							participantes_i = list()
							for part in range(0, len(participantes)):
								#Si es = 4, es una universidad española
								participantes_i.append(len(participantes[part].text))
							
							cod_interuniversitario_i = list()
							#Es 'Interuniversitario', comprobar si hay universidades extranjeras
							if len(centro_uni) >= 2: #Centros
								for part in participantes_i:
									if part >= 5:
										cod_interuniversitario_i.append('2')
									if part < 5:
										cod_interuniversitario_i.append('1')

								if '2' in cod_interuniversitario_i:
									cod_interuniversitario.append('2')
								else:
									cod_interuniversitario.append('1')

							#A priori 'No interuniversitario'
							#Comprobacion interuniversitario, sino 'No interuniversitario'
							elif len(centro_uni) < 2:
								if len(participantes) >= 2:
									for part in participantes_i:
										if part >= 5:
											cod_interuniversitario_i.append('2')
										if part < 5:
											cod_interuniversitario_i.append('1')

									if '2' in cod_interuniversitario_i:
										cod_interuniversitario.append('2')
									else:
										cod_interuniversitario.append('1')


								if len(participantes) < 2:
									cod_interuniversitario.append('0')

							print('---------------')
							#Rol Coordinacion 
							print('cod_interuniversitario', cod_interuniversitario[-1])
							print(driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text)
							if cod_interuniversitario[-1] == '1' or cod_interuniversitario[-1] == '2':
								if 'Universidad Politécnica de Madrid' in driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text:
									cod_rol_coordinacion.append('1')
								else:
									cod_rol_coordinacion.append('0')	
							if cod_interuniversitario[-1] == '0':
								cod_rol_coordinacion.append('8')
							print('cod_rol_coordinacion', cod_rol_coordinacion)


							for j in range(0, len(centro_uni)):
								
								centro_uni_i.append(centro_uni[j].text)
								if 'Universidad Politécnica de Madrid' in centro_uni[j].text:

									print('  UPM', centro_uni[j].text)
									centro[j].click()
									try:
										presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_presencial"]')[0].get_attribute('checked')
										semi_presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_semipresencial"]')[0].get_attribute('checked')
										a_distancia = driver.find_elements_by_xpath('//*[@id="datosCentro_virtual"]')[0].get_attribute('checked')
										print('  Try presencialidad')

										#print(presencial, semi_presencial, a_distancia)

										des_grado_presencialidad_i = list()
										if presencial == 'true':
											des_grado_presencialidad_i.append('Estudio presencial')
										if semi_presencial == 'true':
											des_grado_presencialidad_i.append('Estudio semipresencial')
										if a_distancia == 'true':
											des_grado_presencialidad_i.append('Estudio no presencial')
										if len(des_grado_presencialidad_i) >= 2:
											des_grado_presencialidad_i = list()
											des_grado_presencialidad_i.append('Varias modalidades')
										if presencial != 'true' and semi_presencial != 'true' and a_distancia != 'true': #para DOCTORADOS
											des_grado_presencialidad_i.append(' ')

										des_grado_presencialidad.append(des_grado_presencialidad_i[0])

									except:
										des_grado_presencialidad.append(' ')
										print('  Except presencialidad')


									try:
										idiomas = driver.find_elements_by_xpath('//*[@id="lengua"]/tbody/tr/td')
										idiomas_i = list()
										print('  Try idiomas')
										for i in range(0, len(idiomas)):
											idiomas_i.append(idiomas[i].text)

										if len(idiomas_i) == 1 and 'CASTELLANO ' in idiomas_i:
											cod_idioma_extranjero.append('0')
											des_idioma_extranjero.append('No')
										elif len(idiomas_i) == 1 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('1')
											des_idioma_extranjero.append('Ingles')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('2')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en ingles')
										elif len(idiomas_i) == 1 and 'INGLÉS ' not in idiomas_i and 'CASTELLANO ' not in idiomas_i:
											cod_idioma_extranjero.append('3')
											des_idioma_extranjero.append('Otro idioma extranjero')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' not in idiomas_i:
											cod_idioma_extranjero.append('4')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en otro idioma extranjero')
										else:
											cod_idioma_extranjero.append('None')
											des_idioma_extranjero.append('None')

										driver.back()
										driver.back()
										driver.back()
										break

									except:
										cod_idioma_extranjero.append('None')
										des_idioma_extranjero.append('None')
										print('  Except idiomas')
										driver.back()
										driver.back()
										driver.back()
										break


								else:
									print('	 No UPM', centro_uni[j].text, 'seguimos')
									#continue


							#En caso de que no haya 'Universidad Politécnica de Madrid  '
							if 'Universidad Politécnica de Madrid' not in centro_uni_i[-1]:
								print('   ', centro_uni_i)
								des_grado_presencialidad.append(' ')
								cod_idioma_extranjero.append('None')
								des_idioma_extranjero.append('None')
								print('	  No UPM final \n')

						except:
							print('FALLO UNIVERSIDADES')
							descripcion_click_i.pop(-1)
							driver.back()
							driver.back()
							pass


				if 'Universidades y centros' not in descripcion_click_i:
					print('No hay Universidadades y centros')
					des_grado_presencialidad.append(' ')
					cod_idioma_extranjero.append('None')
					des_idioma_extranjero.append('None')
					cod_rol_coordinacion.append(' ')


			if 'Calendario de implantación' in datos_i[-1]:
				datos[dat].click()

				try:
					anio = driver.find_elements_by_xpath('//*[@id="calendarioImplantacion_curso_Inicio"]')[0]
					anio_value = anio.get_attribute('value')
					print('  Try Año inicio', anio_value)
					if anio_value == '0':
						anio_inicio.append('8888')
						driver.back()
					
					else:
						anio_inicio.append(anio_value)
						driver.back()

					
				except:
					print('  Except Año inicio')
					anio_inicio.append('8888')
					driver.back()


		if 'Calendario de implantación' not in datos_i:
			print('      Not anio inicio fin')
			anio_inicio.append('8888')


		#Pagina principal 'Detalle'
		driver.back()


	#Cuando no hay link 'Ver en Detalle'!
	except IndexError as exception:
		print('No detalle')
		des_grado_presencialidad.append(' ')
		cod_idioma_extranjero.append('None')
		des_idioma_extranjero.append('None')
		anio_inicio.append('8888')
		cod_interuniversitario.append(' ')
		cod_rol_coordinacion.append(' ')


print('RESUMEN MASTER')
print('rama' ,len(rama_master))
print(rama_master)
print('num creditos necesarios', len(num_creditos_necesarios))
print('cod centro master', len(cod_centro_master))
print('nombre centro master', len(nombre_centro_master))
print('grado presencialidad', len(des_grado_presencialidad))
print('idioma extranjero', len(des_idioma_extranjero))
print('anio inicio', len(anio_inicio))
print(anio_inicio)
print(len(cod_interuniversitario))
print(len(cod_rol_coordinacion))


#PAGINA 3
pagina3 = driver.find_elements_by_xpath('//*[@id="ver"]/span[2]/a[9]')
pagina3[0].click()
masters = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr')
links = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a'))
print('Nº masters pagina 3: ', len(masters))

for master in masters:
	cod_master.append(master.find_elements_by_xpath('.//td[1]')[0].text)
	nombre_master.append(master.find_elements_by_xpath('.//td[2]')[0].text)
	estado_master.append(master.find_elements_by_xpath('.//td[5]')[0].text)
	cod_tipo_estudio.append('M')
	des_tipo_estudio.append('Master')


for link in range(0, links):
	#Un master no tiene rama
	try: 
		titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
		titulo[link].click()
		rama_click = driver.find_elements_by_xpath('//*[@id="ui-id-1"]/span')
		rama_click[0].click()
		rama = driver.find_elements_by_xpath('//*[@id="estudio_descripcionRama"]')[0].text
		rama_master.append(rama)

		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')
	
		driver.back()

	except:
		rama = 'None'
		rama_master.append(rama)
		
		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')

		driver.back()

	titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
	titulo[link].click()
	centros_click = driver.find_elements_by_xpath('//*[@id="tab3"]')
	centros_click[0].click()
	codigo = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[2]')[0].text
	cod_centro_master.append(codigo)
	centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]/a')[0].text
	nombre_centro_master.append(centro)
	driver.back()

links2 = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]'))
print('links2', links2)
for i in range(0, links2):
	try:
		detalle = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]/a')
		detalle[i].click()
		datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
		datos_i = list()
		print('len DATOS', len(datos))
		#Navegando menu 'Datos del titulo'
		for dat in range(0, len(datos)):
			datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
			datos_i.append(datos[dat].text)
			

			#DESCRIPCION DEL TITULO
			if 'Descripción del título' in datos[dat].text:
				datos[dat].click()
				descripcion_click = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/ul/li')
				descripcion_click_i = list()
				print('len DESCRIPCION', len(descripcion_click))

				#Navegando en 'Descripcion del titulo'
				for desc in range(0, len(descripcion_click)):

					#Click en 'Universidades y centros'
					if 'Universidades y centros' in descripcion_click[desc].text:
						
						try:
							descripcion_click_i.append(descripcion_click[desc].text)
							descripcion_click[desc].click()

							centro_uni = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]')
							centro_uni_i = list()
							centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[4]/a')
							participantes = driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[1]')
							participantes_i = list()
							for part in range(0, len(participantes)):
								#Si es = 4, es una universidad española
								participantes_i.append(len(participantes[part].text))
							
							cod_interuniversitario_i = list()
							#Es 'Interuniversitario', comprobar si hay universidades extranjeras
							if len(centro_uni) >= 2: #Centros
								for part in participantes_i:
									if part >= 5:
										cod_interuniversitario_i.append('2')
									if part < 5:
										cod_interuniversitario_i.append('1')

								if '2' in cod_interuniversitario_i:
									cod_interuniversitario.append('2')
								else:
									cod_interuniversitario.append('1')

							#A priori 'No interuniversitario'
							#Comprobacion interuniversitario, sino 'No interuniversitario'
							elif len(centro_uni) < 2:
								if len(participantes) >= 2:
									for part in participantes_i:
										if part >= 5:
											cod_interuniversitario_i.append('2')
										if part < 5:
											cod_interuniversitario_i.append('1')

									if '2' in cod_interuniversitario_i:
										cod_interuniversitario.append('2')
									else:
										cod_interuniversitario.append('1')


								if len(participantes) < 2:
									cod_interuniversitario.append('0')

							print('---------------')
							#Rol Coordinacion 
							print('cod_interuniversitario', cod_interuniversitario[-1])
							print(driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text)
							if cod_interuniversitario[-1] == '1' or cod_interuniversitario[-1] == '2':
								if 'Universidad Politécnica de Madrid' in driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text:
									cod_rol_coordinacion.append('1')
								else:
									cod_rol_coordinacion.append('0')	
							if cod_interuniversitario[-1] == '0':
								cod_rol_coordinacion.append('8')
							print('cod_rol_coordinacion', cod_rol_coordinacion)


							for j in range(0, len(centro_uni)):
								
								centro_uni_i.append(centro_uni[j].text)
								if 'Universidad Politécnica de Madrid' in centro_uni[j].text:

									print('  UPM', centro_uni[j].text)
									centro[j].click()
									try:
										presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_presencial"]')[0].get_attribute('checked')
										semi_presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_semipresencial"]')[0].get_attribute('checked')
										a_distancia = driver.find_elements_by_xpath('//*[@id="datosCentro_virtual"]')[0].get_attribute('checked')
										print('  Try presencialidad')

										#print(presencial, semi_presencial, a_distancia)

										des_grado_presencialidad_i = list()
										if presencial == 'true':
											des_grado_presencialidad_i.append('Estudio presencial')
										if semi_presencial == 'true':
											des_grado_presencialidad_i.append('Estudio semipresencial')
										if a_distancia == 'true':
											des_grado_presencialidad_i.append('Estudio no presencial')
										if len(des_grado_presencialidad_i) >= 2:
											des_grado_presencialidad_i = list()
											des_grado_presencialidad_i.append('Varias modalidades')
										if presencial != 'true' and semi_presencial != 'true' and a_distancia != 'true': #para DOCTORADOS
											des_grado_presencialidad_i.append(' ')

										des_grado_presencialidad.append(des_grado_presencialidad_i[0])

									except:
										des_grado_presencialidad.append(' ')
										print('  Except presencialidad')


									try:
										idiomas = driver.find_elements_by_xpath('//*[@id="lengua"]/tbody/tr/td')
										idiomas_i = list()
										print('  Try idiomas')
										for i in range(0, len(idiomas)):
											idiomas_i.append(idiomas[i].text)

										if len(idiomas_i) == 1 and 'CASTELLANO ' in idiomas_i:
											cod_idioma_extranjero.append('0')
											des_idioma_extranjero.append('No')
										elif len(idiomas_i) == 1 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('1')
											des_idioma_extranjero.append('Ingles')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('2')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en ingles')
										elif len(idiomas_i) == 1 and 'INGLÉS ' not in idiomas_i and 'CASTELLANO ' not in idiomas_i:
											cod_idioma_extranjero.append('3')
											des_idioma_extranjero.append('Otro idioma extranjero')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' not in idiomas_i:
											cod_idioma_extranjero.append('4')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en otro idioma extranjero')
										else:
											cod_idioma_extranjero.append('None')
											des_idioma_extranjero.append('None')

										driver.back()
										driver.back()
										driver.back()
										break

									except:
										cod_idioma_extranjero.append('None')
										des_idioma_extranjero.append('None')
										print('  Except idiomas')
										driver.back()
										driver.back()
										driver.back()
										break


								else:
									print('	 No UPM', centro_uni[j].text, 'seguimos')
									#continue


							#En caso de que no haya 'Universidad Politécnica de Madrid  '
							if 'Universidad Politécnica de Madrid' not in centro_uni_i[-1]:
								print('   ', centro_uni_i)
								des_grado_presencialidad.append(' ')
								cod_idioma_extranjero.append('None')
								des_idioma_extranjero.append('None')
								print('	  No UPM final \n')

						except:
							print('FALLO UNIVERSIDADES')
							descripcion_click_i.pop(-1)
							driver.back()
							driver.back()
							pass


				if 'Universidades y centros' not in descripcion_click_i:
					print('No hay Universidadades y centros')
					des_grado_presencialidad.append(' ')
					cod_idioma_extranjero.append('None')
					des_idioma_extranjero.append('None')
					cod_rol_coordinacion.append(' ')


			if 'Calendario de implantación' in datos_i[-1]:
				datos[dat].click()

				try:
					anio = driver.find_elements_by_xpath('//*[@id="calendarioImplantacion_curso_Inicio"]')[0]
					anio_value = anio.get_attribute('value')
					print('  Try Año inicio', anio_value)
					if anio_value == '0':
						anio_inicio.append('8888')
						driver.back()
					
					else:
						anio_inicio.append(anio_value)
						driver.back()

					
				except:
					print('  Except Año inicio')
					anio_inicio.append('8888')
					driver.back()


		if 'Calendario de implantación' not in datos_i:
			print('      Not anio inicio fin')
			anio_inicio.append('8888')


		#Pagina principal 'Detalle'
		driver.back()


	#Cuando no hay link 'Ver en Detalle'!
	except IndexError as exception:
		print('No detalle')
		des_grado_presencialidad.append(' ')
		cod_idioma_extranjero.append('None')
		des_idioma_extranjero.append('None')
		anio_inicio.append('8888')
		cod_interuniversitario.append(' ')
		cod_rol_coordinacion.append(' ')


print('RESUMEN MASTER')
print('rama' ,len(rama_master))
print(rama_master)
print('num creditos necesarios', len(num_creditos_necesarios))
print('cod centro master', len(cod_centro_master))
print('nombre centro master', len(nombre_centro_master))
print('grado presencialidad', len(des_grado_presencialidad))
print('idioma extranjero', len(des_idioma_extranjero))
print('anio inicio', len(anio_inicio))
print(anio_inicio)
print(len(cod_interuniversitario))
print(len(cod_rol_coordinacion))


#PAGINA 4
pagina4 = driver.find_elements_by_xpath('//*[@id="ver"]/span[2]/a[9]')
pagina4[0].click()
masters = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr')
links = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a'))
print('Nº masters pagina 4: ', len(masters))

for master in masters:
	cod_master.append(master.find_elements_by_xpath('.//td[1]')[0].text)
	nombre_master.append(master.find_elements_by_xpath('.//td[2]')[0].text)
	estado_master.append(master.find_elements_by_xpath('.//td[5]')[0].text)
	cod_tipo_estudio.append('M')
	des_tipo_estudio.append('Master')


for link in range(0, links):
	#Un master no tiene rama
	try: 
		titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
		titulo[link].click()
		rama_click = driver.find_elements_by_xpath('//*[@id="ui-id-1"]/span')
		rama_click[0].click()
		rama = driver.find_elements_by_xpath('//*[@id="estudio_descripcionRama"]')[0].text
		rama_master.append(rama)

		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')
	
		driver.back()

	except:
		rama = 'None'
		rama_master.append(rama)
		
		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')

		driver.back()

	titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
	titulo[link].click()
	centros_click = driver.find_elements_by_xpath('//*[@id="tab3"]')
	centros_click[0].click()
	codigo = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[2]')[0].text
	cod_centro_master.append(codigo)
	centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]/a')[0].text
	nombre_centro_master.append(centro)
	driver.back()

links2 = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]'))
print('links2', links2)
for i in range(0, links2):
	try:
		detalle = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]/a')
		detalle[i].click()
		datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
		datos_i = list()
		print('len DATOS', len(datos))
		#Navegando menu 'Datos del titulo'
		for dat in range(0, len(datos)):
			datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
			datos_i.append(datos[dat].text)
			

			#DESCRIPCION DEL TITULO
			if 'Descripción del título' in datos[dat].text:
				datos[dat].click()
				descripcion_click = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/ul/li')
				descripcion_click_i = list()
				print('len DESCRIPCION', len(descripcion_click))

				#Navegando en 'Descripcion del titulo'
				for desc in range(0, len(descripcion_click)):

					#Click en 'Universidades y centros'
					if 'Universidades y centros' in descripcion_click[desc].text:
						
						try:
							descripcion_click_i.append(descripcion_click[desc].text)
							descripcion_click[desc].click()

							centro_uni = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]')
							centro_uni_i = list()
							centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[4]/a')
							participantes = driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[1]')
							participantes_i = list()
							for part in range(0, len(participantes)):
								#Si es = 4, es una universidad española
								participantes_i.append(len(participantes[part].text))
							
							cod_interuniversitario_i = list()
							#Es 'Interuniversitario', comprobar si hay universidades extranjeras
							if len(centro_uni) >= 2: #Centros
								for part in participantes_i:
									if part >= 5:
										cod_interuniversitario_i.append('2')
									if part < 5:
										cod_interuniversitario_i.append('1')

								if '2' in cod_interuniversitario_i:
									cod_interuniversitario.append('2')
								else:
									cod_interuniversitario.append('1')

							#A priori 'No interuniversitario'
							#Comprobacion interuniversitario, sino 'No interuniversitario'
							elif len(centro_uni) < 2:
								if len(participantes) >= 2:
									for part in participantes_i:
										if part >= 5:
											cod_interuniversitario_i.append('2')
										if part < 5:
											cod_interuniversitario_i.append('1')

									if '2' in cod_interuniversitario_i:
										cod_interuniversitario.append('2')
									else:
										cod_interuniversitario.append('1')


								if len(participantes) < 2:
									cod_interuniversitario.append('0')

							print('---------------')
							#Rol Coordinacion 
							print('cod_interuniversitario', cod_interuniversitario[-1])
							print(driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text)
							if cod_interuniversitario[-1] == '1' or cod_interuniversitario[-1] == '2':
								if 'Universidad Politécnica de Madrid' in driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text:
									cod_rol_coordinacion.append('1')
								else:
									cod_rol_coordinacion.append('0')	
							if cod_interuniversitario[-1] == '0':
								cod_rol_coordinacion.append('8')
							print('cod_rol_coordinacion', cod_rol_coordinacion)


							for j in range(0, len(centro_uni)):
								
								centro_uni_i.append(centro_uni[j].text)
								if 'Universidad Politécnica de Madrid' in centro_uni[j].text:

									print('  UPM', centro_uni[j].text)
									centro[j].click()
									try:
										presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_presencial"]')[0].get_attribute('checked')
										semi_presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_semipresencial"]')[0].get_attribute('checked')
										a_distancia = driver.find_elements_by_xpath('//*[@id="datosCentro_virtual"]')[0].get_attribute('checked')
										print('  Try presencialidad')

										#print(presencial, semi_presencial, a_distancia)

										des_grado_presencialidad_i = list()
										if presencial == 'true':
											des_grado_presencialidad_i.append('Estudio presencial')
										if semi_presencial == 'true':
											des_grado_presencialidad_i.append('Estudio semipresencial')
										if a_distancia == 'true':
											des_grado_presencialidad_i.append('Estudio no presencial')
										if len(des_grado_presencialidad_i) >= 2:
											des_grado_presencialidad_i = list()
											des_grado_presencialidad_i.append('Varias modalidades')
										if presencial != 'true' and semi_presencial != 'true' and a_distancia != 'true': #para DOCTORADOS
											des_grado_presencialidad_i.append(' ')

										des_grado_presencialidad.append(des_grado_presencialidad_i[0])

									except:
										des_grado_presencialidad.append(' ')
										print('  Except presencialidad')


									try:
										idiomas = driver.find_elements_by_xpath('//*[@id="lengua"]/tbody/tr/td')
										idiomas_i = list()
										print('  Try idiomas')
										for i in range(0, len(idiomas)):
											idiomas_i.append(idiomas[i].text)

										if len(idiomas_i) == 1 and 'CASTELLANO ' in idiomas_i:
											cod_idioma_extranjero.append('0')
											des_idioma_extranjero.append('No')
										elif len(idiomas_i) == 1 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('1')
											des_idioma_extranjero.append('Ingles')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('2')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en ingles')
										elif len(idiomas_i) == 1 and 'INGLÉS ' not in idiomas_i and 'CASTELLANO ' not in idiomas_i:
											cod_idioma_extranjero.append('3')
											des_idioma_extranjero.append('Otro idioma extranjero')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' not in idiomas_i:
											cod_idioma_extranjero.append('4')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en otro idioma extranjero')
										else:
											cod_idioma_extranjero.append('None')
											des_idioma_extranjero.append('None')

										driver.back()
										driver.back()
										driver.back()
										break

									except:
										cod_idioma_extranjero.append('None')
										des_idioma_extranjero.append('None')
										print('  Except idiomas')
										driver.back()
										driver.back()
										driver.back()
										break


								else:
									print('	 No UPM', centro_uni[j].text, 'seguimos')
									#continue


							#En caso de que no haya 'Universidad Politécnica de Madrid  '
							if 'Universidad Politécnica de Madrid' not in centro_uni_i[-1]:
								print('   ', centro_uni_i)
								des_grado_presencialidad.append(' ')
								cod_idioma_extranjero.append('None')
								des_idioma_extranjero.append('None')
								print('	  No UPM final \n')

						except:
							print('FALLO UNIVERSIDADES')
							descripcion_click_i.pop(-1)
							driver.back()
							driver.back()
							pass


				if 'Universidades y centros' not in descripcion_click_i:
					print('No hay Universidadades y centros')
					des_grado_presencialidad.append(' ')
					cod_idioma_extranjero.append('None')
					des_idioma_extranjero.append('None')
					cod_rol_coordinacion.append(' ')


			if 'Calendario de implantación' in datos_i[-1]:
				datos[dat].click()

				try:
					anio = driver.find_elements_by_xpath('//*[@id="calendarioImplantacion_curso_Inicio"]')[0]
					anio_value = anio.get_attribute('value')
					print('  Try Año inicio', anio_value)
					if anio_value == '0':
						anio_inicio.append('8888')
						driver.back()
					
					else:
						anio_inicio.append(anio_value)
						driver.back()

					
				except:
					print('  Except Año inicio')
					anio_inicio.append('8888')
					driver.back()


		if 'Calendario de implantación' not in datos_i:
			print('      Not anio inicio fin')
			anio_inicio.append('8888')


		#Pagina principal 'Detalle'
		driver.back()


	#Cuando no hay link 'Ver en Detalle'!
	except IndexError as exception:
		print('No detalle')
		des_grado_presencialidad.append(' ')
		cod_idioma_extranjero.append('None')
		des_idioma_extranjero.append('None')
		anio_inicio.append('8888')
		cod_interuniversitario.append(' ')
		cod_rol_coordinacion.append(' ')


print('RESUMEN MASTER')
print('rama' ,len(rama_master))
print(rama_master)
print('num creditos necesarios', len(num_creditos_necesarios))
print('cod centro master', len(cod_centro_master))
print('nombre centro master', len(nombre_centro_master))
print('grado presencialidad', len(des_grado_presencialidad))
print('idioma extranjero', len(des_idioma_extranjero))
print('anio inicio', len(anio_inicio))
print(anio_inicio)
print(len(cod_interuniversitario))
print(len(cod_rol_coordinacion))


#PAGINA 5
pagina5 = driver.find_elements_by_xpath('//*[@id="ver"]/span[2]/a[9]')
pagina5[0].click()
masters = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr')
links = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a'))
print('Nº masters pagina 5: ', len(masters))

for master in masters:
	cod_master.append(master.find_elements_by_xpath('.//td[1]')[0].text)
	nombre_master.append(master.find_elements_by_xpath('.//td[2]')[0].text)
	estado_master.append(master.find_elements_by_xpath('.//td[5]')[0].text)
	cod_tipo_estudio.append('M')
	des_tipo_estudio.append('Master')


for link in range(0, links):
	#Un master no tiene rama
	try: 
		titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
		titulo[link].click()
		rama_click = driver.find_elements_by_xpath('//*[@id="ui-id-1"]/span')
		rama_click[0].click()
		rama = driver.find_elements_by_xpath('//*[@id="estudio_descripcionRama"]')[0].text
		rama_master.append(rama)

		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')
	
		driver.back()

	except:
		rama = 'None'
		rama_master.append(rama)
		
		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')

		driver.back()

	titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
	titulo[link].click()
	centros_click = driver.find_elements_by_xpath('//*[@id="tab3"]')
	centros_click[0].click()
	codigo = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[2]')[0].text
	cod_centro_master.append(codigo)
	centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]/a')[0].text
	nombre_centro_master.append(centro)
	driver.back()

links2 = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]'))
print('links2', links2)
for i in range(0, links2):
	try:
		detalle = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]/a')
		detalle[i].click()
		datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
		datos_i = list()
		print('len DATOS', len(datos))
		#Navegando menu 'Datos del titulo'
		for dat in range(0, len(datos)):
			datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
			datos_i.append(datos[dat].text)
			

			#DESCRIPCION DEL TITULO
			if 'Descripción del título' in datos[dat].text:
				datos[dat].click()
				descripcion_click = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/ul/li')
				descripcion_click_i = list()
				print('len DESCRIPCION', len(descripcion_click))

				#Navegando en 'Descripcion del titulo'
				for desc in range(0, len(descripcion_click)):

					#Click en 'Universidades y centros'
					if 'Universidades y centros' in descripcion_click[desc].text:
						
						try:
							descripcion_click_i.append(descripcion_click[desc].text)
							descripcion_click[desc].click()

							centro_uni = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]')
							centro_uni_i = list()
							centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[4]/a')
							participantes = driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[1]')
							participantes_i = list()
							for part in range(0, len(participantes)):
								#Si es = 4, es una universidad española
								participantes_i.append(len(participantes[part].text))
							
							cod_interuniversitario_i = list()
							#Es 'Interuniversitario', comprobar si hay universidades extranjeras
							if len(centro_uni) >= 2: #Centros
								for part in participantes_i:
									if part >= 5:
										cod_interuniversitario_i.append('2')
									if part < 5:
										cod_interuniversitario_i.append('1')

								if '2' in cod_interuniversitario_i:
									cod_interuniversitario.append('2')
								else:
									cod_interuniversitario.append('1')

							#A priori 'No interuniversitario'
							#Comprobacion interuniversitario, sino 'No interuniversitario'
							elif len(centro_uni) < 2:
								if len(participantes) >= 2:
									for part in participantes_i:
										if part >= 5:
											cod_interuniversitario_i.append('2')
										if part < 5:
											cod_interuniversitario_i.append('1')

									if '2' in cod_interuniversitario_i:
										cod_interuniversitario.append('2')
									else:
										cod_interuniversitario.append('1')


								if len(participantes) < 2:
									cod_interuniversitario.append('0')

							print('---------------')
							#Rol Coordinacion 
							print('cod_interuniversitario', cod_interuniversitario[-1])
							print(driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text)
							if cod_interuniversitario[-1] == '1' or cod_interuniversitario[-1] == '2':
								if 'Universidad Politécnica de Madrid' in driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text:
									cod_rol_coordinacion.append('1')
								else:
									cod_rol_coordinacion.append('0')	
							if cod_interuniversitario[-1] == '0':
								cod_rol_coordinacion.append('8')
							print('cod_rol_coordinacion', cod_rol_coordinacion)


							for j in range(0, len(centro_uni)):
								
								centro_uni_i.append(centro_uni[j].text)
								if 'Universidad Politécnica de Madrid' in centro_uni[j].text:

									print('  UPM', centro_uni[j].text)
									centro[j].click()
									try:
										presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_presencial"]')[0].get_attribute('checked')
										semi_presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_semipresencial"]')[0].get_attribute('checked')
										a_distancia = driver.find_elements_by_xpath('//*[@id="datosCentro_virtual"]')[0].get_attribute('checked')
										print('  Try presencialidad')

										#print(presencial, semi_presencial, a_distancia)

										des_grado_presencialidad_i = list()
										if presencial == 'true':
											des_grado_presencialidad_i.append('Estudio presencial')
										if semi_presencial == 'true':
											des_grado_presencialidad_i.append('Estudio semipresencial')
										if a_distancia == 'true':
											des_grado_presencialidad_i.append('Estudio no presencial')
										if len(des_grado_presencialidad_i) >= 2:
											des_grado_presencialidad_i = list()
											des_grado_presencialidad_i.append('Varias modalidades')
										if presencial != 'true' and semi_presencial != 'true' and a_distancia != 'true': #para DOCTORADOS
											des_grado_presencialidad_i.append(' ')

										des_grado_presencialidad.append(des_grado_presencialidad_i[0])

									except:
										des_grado_presencialidad.append(' ')
										print('  Except presencialidad')


									try:
										idiomas = driver.find_elements_by_xpath('//*[@id="lengua"]/tbody/tr/td')
										idiomas_i = list()
										print('  Try idiomas')
										for i in range(0, len(idiomas)):
											idiomas_i.append(idiomas[i].text)

										if len(idiomas_i) == 1 and 'CASTELLANO ' in idiomas_i:
											cod_idioma_extranjero.append('0')
											des_idioma_extranjero.append('No')
										elif len(idiomas_i) == 1 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('1')
											des_idioma_extranjero.append('Ingles')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('2')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en ingles')
										elif len(idiomas_i) == 1 and 'INGLÉS ' not in idiomas_i and 'CASTELLANO ' not in idiomas_i:
											cod_idioma_extranjero.append('3')
											des_idioma_extranjero.append('Otro idioma extranjero')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' not in idiomas_i:
											cod_idioma_extranjero.append('4')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en otro idioma extranjero')
										else:
											cod_idioma_extranjero.append('None')
											des_idioma_extranjero.append('None')

										driver.back()
										driver.back()
										driver.back()
										break

									except:
										cod_idioma_extranjero.append('None')
										des_idioma_extranjero.append('None')
										print('  Except idiomas')
										driver.back()
										driver.back()
										driver.back()
										break


								else:
									print('	 No UPM', centro_uni[j].text, 'seguimos')
									#continue


							#En caso de que no haya 'Universidad Politécnica de Madrid  '
							if 'Universidad Politécnica de Madrid' not in centro_uni_i[-1]:
								print('   ', centro_uni_i)
								des_grado_presencialidad.append(' ')
								cod_idioma_extranjero.append('None')
								des_idioma_extranjero.append('None')
								print('	  No UPM final \n')

						except:
							print('FALLO UNIVERSIDADES')
							descripcion_click_i.pop(-1)
							driver.back()
							driver.back()
							pass


				if 'Universidades y centros' not in descripcion_click_i:
					print('No hay Universidadades y centros')
					des_grado_presencialidad.append(' ')
					cod_idioma_extranjero.append('None')
					des_idioma_extranjero.append('None')
					cod_rol_coordinacion.append(' ')


			if 'Calendario de implantación' in datos_i[-1]:
				datos[dat].click()

				try:
					anio = driver.find_elements_by_xpath('//*[@id="calendarioImplantacion_curso_Inicio"]')[0]
					anio_value = anio.get_attribute('value')
					print('  Try Año inicio', anio_value)
					if anio_value == '0':
						anio_inicio.append('8888')
						driver.back()
					
					else:
						anio_inicio.append(anio_value)
						driver.back()

					
				except:
					print('  Except Año inicio')
					anio_inicio.append('8888')
					driver.back()


		if 'Calendario de implantación' not in datos_i:
			print('      Not anio inicio fin')
			anio_inicio.append('8888')


		#Pagina principal 'Detalle'
		driver.back()


	#Cuando no hay link 'Ver en Detalle'!
	except IndexError as exception:
		print('No detalle')
		des_grado_presencialidad.append(' ')
		cod_idioma_extranjero.append('None')
		des_idioma_extranjero.append('None')
		anio_inicio.append('8888')
		cod_interuniversitario.append(' ')
		cod_rol_coordinacion.append(' ')


print('RESUMEN MASTER')
print('rama' ,len(rama_master))
print(rama_master)
print('num creditos necesarios', len(num_creditos_necesarios))
print('cod centro master', len(cod_centro_master))
print('nombre centro master', len(nombre_centro_master))
print('grado presencialidad', len(des_grado_presencialidad))
print('idioma extranjero', len(des_idioma_extranjero))
print('anio inicio', len(anio_inicio))
print(anio_inicio)
print(len(cod_interuniversitario))
print(len(cod_rol_coordinacion))


#PAGINA 6
pagina5 = driver.find_elements_by_xpath('//*[@id="ver"]/span[2]/a[9]')
pagina5[0].click()
masters = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr')
links = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a'))
print('Nº masters pagina 6: ', len(masters))

for master in masters:
	cod_master.append(master.find_elements_by_xpath('.//td[1]')[0].text)
	nombre_master.append(master.find_elements_by_xpath('.//td[2]')[0].text)
	estado_master.append(master.find_elements_by_xpath('.//td[5]')[0].text)
	cod_tipo_estudio.append('M')
	des_tipo_estudio.append('Master')


for link in range(0, links):
	#Un master no tiene rama
	try: 
		titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
		titulo[link].click()
		rama_click = driver.find_elements_by_xpath('//*[@id="ui-id-1"]/span')
		rama_click[0].click()
		rama = driver.find_elements_by_xpath('//*[@id="estudio_descripcionRama"]')[0].text
		rama_master.append(rama)

		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')
	
		driver.back()

	except:
		rama = 'None'
		rama_master.append(rama)
		
		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')

		driver.back()

	titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
	titulo[link].click()
	centros_click = driver.find_elements_by_xpath('//*[@id="tab3"]')
	centros_click[0].click()
	codigo = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[2]')[0].text
	cod_centro_master.append(codigo)
	centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]/a')[0].text
	nombre_centro_master.append(centro)
	driver.back()

links2 = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]'))
print('links2', links2)
for i in range(0, links2):
	try:
		detalle = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]/a')
		detalle[i].click()
		datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
		datos_i = list()
		print('len DATOS', len(datos))
		#Navegando menu 'Datos del titulo'
		for dat in range(0, len(datos)):
			datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
			datos_i.append(datos[dat].text)
			

			#DESCRIPCION DEL TITULO
			if 'Descripción del título' in datos[dat].text:
				datos[dat].click()
				descripcion_click = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/ul/li')
				descripcion_click_i = list()
				print('len DESCRIPCION', len(descripcion_click))

				#Navegando en 'Descripcion del titulo'
				for desc in range(0, len(descripcion_click)):

					#Click en 'Universidades y centros'
					if 'Universidades y centros' in descripcion_click[desc].text:
						
						try:
							descripcion_click_i.append(descripcion_click[desc].text)
							descripcion_click[desc].click()

							centro_uni = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]')
							centro_uni_i = list()
							centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[4]/a')
							participantes = driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[1]')
							participantes_i = list()
							for part in range(0, len(participantes)):
								#Si es = 4, es una universidad española
								participantes_i.append(len(participantes[part].text))
							
							cod_interuniversitario_i = list()
							#Es 'Interuniversitario', comprobar si hay universidades extranjeras
							if len(centro_uni) >= 2: #Centros
								for part in participantes_i:
									if part >= 5:
										cod_interuniversitario_i.append('2')
									if part < 5:
										cod_interuniversitario_i.append('1')

								if '2' in cod_interuniversitario_i:
									cod_interuniversitario.append('2')
								else:
									cod_interuniversitario.append('1')

							#A priori 'No interuniversitario'
							#Comprobacion interuniversitario, sino 'No interuniversitario'
							elif len(centro_uni) < 2:
								if len(participantes) >= 2:
									for part in participantes_i:
										if part >= 5:
											cod_interuniversitario_i.append('2')
										if part < 5:
											cod_interuniversitario_i.append('1')

									if '2' in cod_interuniversitario_i:
										cod_interuniversitario.append('2')
									else:
										cod_interuniversitario.append('1')


								if len(participantes) < 2:
									cod_interuniversitario.append('0')

							print('---------------')
							#Rol Coordinacion 
							print('cod_interuniversitario', cod_interuniversitario[-1])
							print(driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text)
							if cod_interuniversitario[-1] == '1' or cod_interuniversitario[-1] == '2':
								if 'Universidad Politécnica de Madrid' in driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text:
									cod_rol_coordinacion.append('1')
								else:
									cod_rol_coordinacion.append('0')	
							if cod_interuniversitario[-1] == '0':
								cod_rol_coordinacion.append('8')
							print('cod_rol_coordinacion', cod_rol_coordinacion)


							for j in range(0, len(centro_uni)):
								
								centro_uni_i.append(centro_uni[j].text)
								if 'Universidad Politécnica de Madrid' in centro_uni[j].text:

									print('  UPM', centro_uni[j].text)
									centro[j].click()
									try:
										presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_presencial"]')[0].get_attribute('checked')
										semi_presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_semipresencial"]')[0].get_attribute('checked')
										a_distancia = driver.find_elements_by_xpath('//*[@id="datosCentro_virtual"]')[0].get_attribute('checked')
										print('  Try presencialidad')

										#print(presencial, semi_presencial, a_distancia)

										des_grado_presencialidad_i = list()
										if presencial == 'true':
											des_grado_presencialidad_i.append('Estudio presencial')
										if semi_presencial == 'true':
											des_grado_presencialidad_i.append('Estudio semipresencial')
										if a_distancia == 'true':
											des_grado_presencialidad_i.append('Estudio no presencial')
										if len(des_grado_presencialidad_i) >= 2:
											des_grado_presencialidad_i = list()
											des_grado_presencialidad_i.append('Varias modalidades')
										if presencial != 'true' and semi_presencial != 'true' and a_distancia != 'true': #para DOCTORADOS
											des_grado_presencialidad_i.append(' ')

										des_grado_presencialidad.append(des_grado_presencialidad_i[0])

									except:
										des_grado_presencialidad.append(' ')
										print('  Except presencialidad')


									try:
										idiomas = driver.find_elements_by_xpath('//*[@id="lengua"]/tbody/tr/td')
										idiomas_i = list()
										print('  Try idiomas')
										for i in range(0, len(idiomas)):
											idiomas_i.append(idiomas[i].text)

										if len(idiomas_i) == 1 and 'CASTELLANO ' in idiomas_i:
											cod_idioma_extranjero.append('0')
											des_idioma_extranjero.append('No')
										elif len(idiomas_i) == 1 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('1')
											des_idioma_extranjero.append('Ingles')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('2')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en ingles')
										elif len(idiomas_i) == 1 and 'INGLÉS ' not in idiomas_i and 'CASTELLANO ' not in idiomas_i:
											cod_idioma_extranjero.append('3')
											des_idioma_extranjero.append('Otro idioma extranjero')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' not in idiomas_i:
											cod_idioma_extranjero.append('4')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en otro idioma extranjero')
										else:
											cod_idioma_extranjero.append('None')
											des_idioma_extranjero.append('None')

										driver.back()
										driver.back()
										driver.back()
										break

									except:
										cod_idioma_extranjero.append('None')
										des_idioma_extranjero.append('None')
										print('  Except idiomas')
										driver.back()
										driver.back()
										driver.back()
										break


								else:
									print('	 No UPM', centro_uni[j].text, 'seguimos')
									#continue


							#En caso de que no haya 'Universidad Politécnica de Madrid  '
							if 'Universidad Politécnica de Madrid' not in centro_uni_i[-1]:
								print('   ', centro_uni_i)
								des_grado_presencialidad.append(' ')
								cod_idioma_extranjero.append('None')
								des_idioma_extranjero.append('None')
								print('	  No UPM final \n')

						except:
							print('FALLO UNIVERSIDADES')
							descripcion_click_i.pop(-1)
							driver.back()
							driver.back()
							pass


				if 'Universidades y centros' not in descripcion_click_i:
					print('No hay Universidadades y centros')
					des_grado_presencialidad.append(' ')
					cod_idioma_extranjero.append('None')
					des_idioma_extranjero.append('None')
					cod_rol_coordinacion.append(' ')


			if 'Calendario de implantación' in datos_i[-1]:
				datos[dat].click()

				try:
					anio = driver.find_elements_by_xpath('//*[@id="calendarioImplantacion_curso_Inicio"]')[0]
					anio_value = anio.get_attribute('value')
					print('  Try Año inicio', anio_value)
					if anio_value == '0':
						anio_inicio.append('8888')
						driver.back()
					
					else:
						anio_inicio.append(anio_value)
						driver.back()

					
				except:
					print('  Except Año inicio')
					anio_inicio.append('8888')
					driver.back()


		if 'Calendario de implantación' not in datos_i:
			print('      Not anio inicio fin')
			anio_inicio.append('8888')


		#Pagina principal 'Detalle'
		driver.back()


	#Cuando no hay link 'Ver en Detalle'!
	except IndexError as exception:
		print('No detalle')
		des_grado_presencialidad.append(' ')
		cod_idioma_extranjero.append('None')
		des_idioma_extranjero.append('None')
		anio_inicio.append('8888')
		cod_interuniversitario.append(' ')
		cod_rol_coordinacion.append(' ')


print('RESUMEN MASTER')
print('rama' ,len(rama_master))
print(rama_master)
print('num creditos necesarios', len(num_creditos_necesarios))
print('cod centro master', len(cod_centro_master))
print('nombre centro master', len(nombre_centro_master))
print('grado presencialidad', len(des_grado_presencialidad))
print('idioma extranjero', len(des_idioma_extranjero))
print('anio inicio', len(anio_inicio))
print(anio_inicio)
print(len(cod_interuniversitario))
print(len(cod_rol_coordinacion))


#PAGINA 7
pagina7 = driver.find_elements_by_xpath('//*[@id="ver"]/span[2]/a[9]')
pagina7[0].click()
masters = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr')
links = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a'))
print('Nº masters pagina 7: ', len(masters))

for master in masters:
	cod_master.append(master.find_elements_by_xpath('.//td[1]')[0].text)
	nombre_master.append(master.find_elements_by_xpath('.//td[2]')[0].text)
	estado_master.append(master.find_elements_by_xpath('.//td[5]')[0].text)
	cod_tipo_estudio.append('M')
	des_tipo_estudio.append('Master')

for link in range(0, links):
	#Un master no tiene rama
	try: 
		titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
		titulo[link].click()
		rama_click = driver.find_elements_by_xpath('//*[@id="ui-id-1"]/span')
		rama_click[0].click()
		rama = driver.find_elements_by_xpath('//*[@id="estudio_descripcionRama"]')[0].text
		rama_master.append(rama)

		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')
	
		driver.back()

	except:
		rama = 'None'
		rama_master.append(rama)
		
		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')

		driver.back()

	titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
	titulo[link].click()
	centros_click = driver.find_elements_by_xpath('//*[@id="tab3"]')
	centros_click[0].click()
	codigo = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[2]')[0].text
	cod_centro_master.append(codigo)
	centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]/a')[0].text
	nombre_centro_master.append(centro)
	driver.back()

links2 = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]'))
print('links2', links2)
for i in range(0, links2):
	try:
		detalle = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]/a')
		detalle[i].click()
		datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
		datos_i = list()
		print('len DATOS', len(datos))
		#Navegando menu 'Datos del titulo'
		for dat in range(0, len(datos)):
			datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
			datos_i.append(datos[dat].text)
			

			#DESCRIPCION DEL TITULO
			if 'Descripción del título' in datos[dat].text:
				datos[dat].click()
				descripcion_click = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/ul/li')
				descripcion_click_i = list()
				print('len DESCRIPCION', len(descripcion_click))

				#Navegando en 'Descripcion del titulo'
				for desc in range(0, len(descripcion_click)):

					#Click en 'Universidades y centros'
					if 'Universidades y centros' in descripcion_click[desc].text:
						
						try:
							descripcion_click_i.append(descripcion_click[desc].text)
							descripcion_click[desc].click()

							centro_uni = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]')
							centro_uni_i = list()
							centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[4]/a')
							participantes = driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[1]')
							participantes_i = list()
							for part in range(0, len(participantes)):
								#Si es = 4, es una universidad española
								participantes_i.append(len(participantes[part].text))
							
							cod_interuniversitario_i = list()
							#Es 'Interuniversitario', comprobar si hay universidades extranjeras
							if len(centro_uni) >= 2: #Centros
								for part in participantes_i:
									if part >= 5:
										cod_interuniversitario_i.append('2')
									if part < 5:
										cod_interuniversitario_i.append('1')

								if '2' in cod_interuniversitario_i:
									cod_interuniversitario.append('2')
								else:
									cod_interuniversitario.append('1')

							#A priori 'No interuniversitario'
							#Comprobacion interuniversitario, sino 'No interuniversitario'
							elif len(centro_uni) < 2:
								if len(participantes) >= 2:
									for part in participantes_i:
										if part >= 5:
											cod_interuniversitario_i.append('2')
										if part < 5:
											cod_interuniversitario_i.append('1')

									if '2' in cod_interuniversitario_i:
										cod_interuniversitario.append('2')
									else:
										cod_interuniversitario.append('1')


								if len(participantes) < 2:
									cod_interuniversitario.append('0')

							print('---------------')
							#Rol Coordinacion 
							print('cod_interuniversitario', cod_interuniversitario[-1])
							print(driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text)
							if cod_interuniversitario[-1] == '1' or cod_interuniversitario[-1] == '2':
								if 'Universidad Politécnica de Madrid' in driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text:
									cod_rol_coordinacion.append('1')
								else:
									cod_rol_coordinacion.append('0')	
							if cod_interuniversitario[-1] == '0':
								cod_rol_coordinacion.append('8')
							print('cod_rol_coordinacion', cod_rol_coordinacion)


							for j in range(0, len(centro_uni)):
								
								centro_uni_i.append(centro_uni[j].text)
								if 'Universidad Politécnica de Madrid' in centro_uni[j].text:

									print('  UPM', centro_uni[j].text)
									centro[j].click()
									try:
										presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_presencial"]')[0].get_attribute('checked')
										semi_presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_semipresencial"]')[0].get_attribute('checked')
										a_distancia = driver.find_elements_by_xpath('//*[@id="datosCentro_virtual"]')[0].get_attribute('checked')
										print('  Try presencialidad')

										#print(presencial, semi_presencial, a_distancia)

										des_grado_presencialidad_i = list()
										if presencial == 'true':
											des_grado_presencialidad_i.append('Estudio presencial')
										if semi_presencial == 'true':
											des_grado_presencialidad_i.append('Estudio semipresencial')
										if a_distancia == 'true':
											des_grado_presencialidad_i.append('Estudio no presencial')
										if len(des_grado_presencialidad_i) >= 2:
											des_grado_presencialidad_i = list()
											des_grado_presencialidad_i.append('Varias modalidades')
										if presencial != 'true' and semi_presencial != 'true' and a_distancia != 'true': #para DOCTORADOS
											des_grado_presencialidad_i.append(' ')

										des_grado_presencialidad.append(des_grado_presencialidad_i[0])

									except:
										des_grado_presencialidad.append(' ')
										print('  Except presencialidad')


									try:
										idiomas = driver.find_elements_by_xpath('//*[@id="lengua"]/tbody/tr/td')
										idiomas_i = list()
										print('  Try idiomas')
										for i in range(0, len(idiomas)):
											idiomas_i.append(idiomas[i].text)

										if len(idiomas_i) == 1 and 'CASTELLANO ' in idiomas_i:
											cod_idioma_extranjero.append('0')
											des_idioma_extranjero.append('No')
										elif len(idiomas_i) == 1 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('1')
											des_idioma_extranjero.append('Ingles')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('2')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en ingles')
										elif len(idiomas_i) == 1 and 'INGLÉS ' not in idiomas_i and 'CASTELLANO ' not in idiomas_i:
											cod_idioma_extranjero.append('3')
											des_idioma_extranjero.append('Otro idioma extranjero')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' not in idiomas_i:
											cod_idioma_extranjero.append('4')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en otro idioma extranjero')
										else:
											cod_idioma_extranjero.append('None')
											des_idioma_extranjero.append('None')

										driver.back()
										driver.back()
										driver.back()
										break

									except:
										cod_idioma_extranjero.append('None')
										des_idioma_extranjero.append('None')
										print('  Except idiomas')
										driver.back()
										driver.back()
										driver.back()
										break


								else:
									print('	 No UPM', centro_uni[j].text, 'seguimos')
									#continue


							#En caso de que no haya 'Universidad Politécnica de Madrid  '
							if 'Universidad Politécnica de Madrid' not in centro_uni_i[-1]:
								print('   ', centro_uni_i)
								des_grado_presencialidad.append(' ')
								cod_idioma_extranjero.append('None')
								des_idioma_extranjero.append('None')
								print('	  No UPM final \n')

						except:
							print('FALLO UNIVERSIDADES')
							descripcion_click_i.pop(-1)
							driver.back()
							driver.back()
							pass


				if 'Universidades y centros' not in descripcion_click_i:
					print('No hay Universidadades y centros')
					des_grado_presencialidad.append(' ')
					cod_idioma_extranjero.append('None')
					des_idioma_extranjero.append('None')
					cod_rol_coordinacion.append(' ')


			if 'Calendario de implantación' in datos_i[-1]:
				datos[dat].click()

				try:
					anio = driver.find_elements_by_xpath('//*[@id="calendarioImplantacion_curso_Inicio"]')[0]
					anio_value = anio.get_attribute('value')
					print('  Try Año inicio', anio_value)
					if anio_value == '0':
						anio_inicio.append('8888')
						driver.back()
					
					else:
						anio_inicio.append(anio_value)
						driver.back()

					
				except:
					print('  Except Año inicio')
					anio_inicio.append('8888')
					driver.back()


		if 'Calendario de implantación' not in datos_i:
			print('      Not anio inicio fin')
			anio_inicio.append('8888')


		#Pagina principal 'Detalle'
		driver.back()


	#Cuando no hay link 'Ver en Detalle'!
	except IndexError as exception:
		print('No detalle')
		des_grado_presencialidad.append(' ')
		cod_idioma_extranjero.append('None')
		des_idioma_extranjero.append('None')
		anio_inicio.append('8888')
		cod_interuniversitario.append(' ')
		cod_rol_coordinacion.append(' ')


print('RESUMEN MASTER')
print('rama' ,len(rama_master))
print(rama_master)
print('num creditos necesarios', len(num_creditos_necesarios))
print('cod centro master', len(cod_centro_master))
print('nombre centro master', len(nombre_centro_master))
print('grado presencialidad', len(des_grado_presencialidad))
print('idioma extranjero', len(des_idioma_extranjero))
print('anio inicio', len(anio_inicio))
print(anio_inicio)
print(len(cod_interuniversitario))
print(len(cod_rol_coordinacion))


'''
#----------------------------------------------------------------------------------
'''
#TITULACIONES - DOCTORADO
url = 'https://www.educacion.gob.es/ruct/consultaestudios?actual=estudios'
driver = webdriver.Chrome(driver_path, options=option)
driver.get(url)

uni = driver.find_elements_by_xpath('//*[@id="codigoUniversidad"]')
uni[0].click()
UPM = driver.find_elements_by_xpath('//*[@id="codigoUniversidad"]/option[79]')
UPM[0].click()

nivel_academico = driver.find_elements_by_xpath('//*[@id="codigoTipo"]')
nivel_academico[0].click()
doctorado = driver.find_elements_by_xpath('//*[@id="codigoTipo"]/option[3]')
doctorado[0].click()
buscar = driver.find_elements_by_xpath('//*[@id="consultaestudios_listaestudios"]')
buscar[0].click()

cod_doctorado = list()
nombre_doctorado = list()
estado_doctorado = list()
rama_doctorado = list()
cod_centro_doctorado = list()
nombre_centro_doctorado = list()

#PAGINA 1
doctorados = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr')
links = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a'))
print('len links', links)
print('Nº doctorados pagina 1: ', len(doctorados))

for doctorado in doctorados:
	cod_doctorado.append(doctorado.find_elements_by_xpath('.//td[1]')[0].text)
	nombre_doctorado.append(doctorado.find_elements_by_xpath('.//td[2]')[0].text)
	estado_doctorado.append(doctorado.find_elements_by_xpath('.//td[5]')[0].text)
	cod_tipo_estudio.append('M')
	des_tipo_estudio.append('Master')

for link in range(0, links):
	#Un master no tiene rama
	try: 
		titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
		titulo[link].click()
		rama_click = driver.find_elements_by_xpath('//*[@id="ui-id-1"]/span')
		rama_click[0].click()
		rama = driver.find_elements_by_xpath('//*[@id="estudio_descripcionRama"]')[0].text
		rama_doctorado.append(rama)

		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')
	
		driver.back()

	except:
		rama = 'None'
		rama_doctorado.append(rama)
		
		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')

		driver.back()

	titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
	titulo[link].click()

	centros_click = driver.find_elements_by_xpath('//*[@id="tab3"]')
	centros_click[0].click()
	codigo = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[2]')[0].text
	cod_centro_doctorado.append(codigo)
	centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]/a')[0].text
	nombre_centro_doctorado.append(centro)
	driver.back()

links2 = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]'))
print('links2', links2)
for i in range(0, links2):
	try:
		detalle = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]/a')
		detalle[i].click()
		datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
		datos_i = list()
		print('len DATOS', len(datos))
		#Navegando menu 'Datos del titulo'
		for dat in range(0, len(datos)):
			datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
			datos_i.append(datos[dat].text)
			

			#DESCRIPCION DEL TITULO
			if 'Descripción del título' in datos[dat].text:
				datos[dat].click()
				descripcion_click = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/ul/li')
				descripcion_click_i = list()
				print('len DESCRIPCION', len(descripcion_click))

				#Navegando en 'Descripcion del titulo'
				for desc in range(0, len(descripcion_click)):

					#Click en 'Universidades y centros'
					if 'Universidades y centros' in descripcion_click[desc].text:
						
						try:
							descripcion_click_i.append(descripcion_click[desc].text)
							descripcion_click[desc].click()

							centro_uni = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]')
							centro_uni_i = list()
							centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[4]/a')
							participantes = driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[1]')
							participantes_i = list()
							for part in range(0, len(participantes)):
								#Si es = 4, es una universidad española
								participantes_i.append(len(participantes[part].text))
							
							cod_interuniversitario_i = list()
							#Es 'Interuniversitario', comprobar si hay universidades extranjeras
							if len(centro_uni) >= 2: #Centros
								for part in participantes_i:
									if part >= 5:
										cod_interuniversitario_i.append('2')
									if part < 5:
										cod_interuniversitario_i.append('1')

								if '2' in cod_interuniversitario_i:
									cod_interuniversitario.append('2')
								else:
									cod_interuniversitario.append('1')

							#A priori 'No interuniversitario'
							#Comprobacion interuniversitario, sino 'No interuniversitario'
							elif len(centro_uni) < 2:
								if len(participantes) >= 2:
									for part in participantes_i:
										if part >= 5:
											cod_interuniversitario_i.append('2')
										if part < 5:
											cod_interuniversitario_i.append('1')

									if '2' in cod_interuniversitario_i:
										cod_interuniversitario.append('2')
									else:
										cod_interuniversitario.append('1')


								if len(participantes) < 2:
									cod_interuniversitario.append('0')

							print('---------------')
							#Rol Coordinacion 
							print('cod_interuniversitario', cod_interuniversitario[-1])
							print(driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text)
							if cod_interuniversitario[-1] == '1' or cod_interuniversitario[-1] == '2':
								if 'Universidad Politécnica de Madrid' in driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text:
									cod_rol_coordinacion.append('1')
								else:
									cod_rol_coordinacion.append('0')	
							if cod_interuniversitario[-1] == '0':
								cod_rol_coordinacion.append('8')
							print('cod_rol_coordinacion', cod_rol_coordinacion)


							for j in range(0, len(centro_uni)):
								
								centro_uni_i.append(centro_uni[j].text)
								if 'Universidad Politécnica de Madrid' in centro_uni[j].text:

									print('  UPM', centro_uni[j].text)
									centro[j].click()
									try:
										presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_presencial"]')[0].get_attribute('checked')
										semi_presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_semipresencial"]')[0].get_attribute('checked')
										a_distancia = driver.find_elements_by_xpath('//*[@id="datosCentro_virtual"]')[0].get_attribute('checked')
										print('  Try presencialidad')

										#print(presencial, semi_presencial, a_distancia)

										des_grado_presencialidad_i = list()
										if presencial == 'true':
											des_grado_presencialidad_i.append('Estudio presencial')
										if semi_presencial == 'true':
											des_grado_presencialidad_i.append('Estudio semipresencial')
										if a_distancia == 'true':
											des_grado_presencialidad_i.append('Estudio no presencial')
										if len(des_grado_presencialidad_i) >= 2:
											des_grado_presencialidad_i = list()
											des_grado_presencialidad_i.append('Varias modalidades')
										if presencial != 'true' and semi_presencial != 'true' and a_distancia != 'true': #para DOCTORADOS
											des_grado_presencialidad_i.append(' ')

										des_grado_presencialidad.append(des_grado_presencialidad_i[0])

									except:
										des_grado_presencialidad.append(' ')
										print('  Except presencialidad')


									try:
										idiomas = driver.find_elements_by_xpath('//*[@id="lengua"]/tbody/tr/td')
										idiomas_i = list()
										print('  Try idiomas')
										for i in range(0, len(idiomas)):
											idiomas_i.append(idiomas[i].text)

										if len(idiomas_i) == 1 and 'CASTELLANO ' in idiomas_i:
											cod_idioma_extranjero.append('0')
											des_idioma_extranjero.append('No')
										elif len(idiomas_i) == 1 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('1')
											des_idioma_extranjero.append('Ingles')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('2')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en ingles')
										elif len(idiomas_i) == 1 and 'INGLÉS ' not in idiomas_i and 'CASTELLANO ' not in idiomas_i:
											cod_idioma_extranjero.append('3')
											des_idioma_extranjero.append('Otro idioma extranjero')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' not in idiomas_i:
											cod_idioma_extranjero.append('4')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en otro idioma extranjero')
										else:
											cod_idioma_extranjero.append('None')
											des_idioma_extranjero.append('None')

										driver.back()
										driver.back()
										driver.back()
										break

									except:
										cod_idioma_extranjero.append('None')
										des_idioma_extranjero.append('None')
										print('  Except idiomas')
										driver.back()
										driver.back()
										driver.back()
										break


								else:
									print('	 No UPM', centro_uni[j].text, 'seguimos')
									#continue


							#En caso de que no haya 'Universidad Politécnica de Madrid  '
							if 'Universidad Politécnica de Madrid' not in centro_uni_i[-1]:
								print('   ', centro_uni_i)
								des_grado_presencialidad.append(' ')
								cod_idioma_extranjero.append('None')
								des_idioma_extranjero.append('None')
								print('	  No UPM final \n')

						except:
							print('FALLO UNIVERSIDADES')
							descripcion_click_i.pop(-1)
							driver.back()
							driver.back()
							pass


				if 'Universidades y centros' not in descripcion_click_i:
					print('No hay Universidadades y centros')
					des_grado_presencialidad.append(' ')
					cod_idioma_extranjero.append('None')
					des_idioma_extranjero.append('None')
					cod_rol_coordinacion.append(' ')


			if 'Calendario de implantación' in datos_i[-1]:
				datos[dat].click()

				try:
					anio = driver.find_elements_by_xpath('//*[@id="calendarioImplantacion_curso_Inicio"]')[0]
					anio_value = anio.get_attribute('value')
					print('  Try Año inicio', anio_value)
					if anio_value == '0':
						anio_inicio.append('8888')
						driver.back()
					
					else:
						anio_inicio.append(anio_value)
						driver.back()

					
				except:
					print('  Except Año inicio')
					anio_inicio.append('8888')
					driver.back()


		if 'Calendario de implantación' not in datos_i:
			print('      Not anio inicio fin')
			anio_inicio.append('8888')


		#Pagina principal 'Detalle'
		driver.back()


	#Cuando no hay link 'Ver en Detalle'!
	except IndexError as exception:
		print('No detalle')
		des_grado_presencialidad.append(' ')
		cod_idioma_extranjero.append('None')
		des_idioma_extranjero.append('None')
		anio_inicio.append('8888')
		cod_interuniversitario.append(' ')
		cod_rol_coordinacion.append(' ')
		

print('RESUMEN DOCTORADO')
print('rama' ,len(rama_doctorado))
print(rama_doctorado)
print('num creditos necesarios', len(num_creditos_necesarios))
print('cod centro doctorado', len(cod_centro_doctorado))
print('nombre centro doctorado', len(nombre_centro_doctorado))
print('grado presencialidad', len(des_grado_presencialidad))
print('idioma extranjero', len(des_idioma_extranjero))
print('anio inicio', len(anio_inicio))
print(anio_inicio)
print(len(cod_interuniversitario))
print(len(cod_rol_coordinacion))

#PAGINA 2
pagina2 = driver.find_elements_by_xpath('//*[@id="ver"]/span[2]/a[5]')
pagina2[0].click()
doctorados = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr')
links = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a'))
print('len links', links)
print('Nº doctorado pagina 2: ', len(doctorados))

for doctorado in doctorados:
	cod_doctorado.append(doctorado.find_elements_by_xpath('.//td[1]')[0].text)
	nombre_doctorado.append(doctorado.find_elements_by_xpath('.//td[2]')[0].text)
	estado_doctorado.append(doctorado.find_elements_by_xpath('.//td[5]')[0].text)
	cod_tipo_estudio.append('M')
	des_tipo_estudio.append('Master')

for link in range(0, links):
	#Un master no tiene rama
	try: 
		titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
		titulo[link].click()
		rama_click = driver.find_elements_by_xpath('//*[@id="ui-id-1"]/span')
		rama_click[0].click()
		rama = driver.find_elements_by_xpath('//*[@id="estudio_descripcionRama"]')[0].text
		rama_doctorado.append(rama)

		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')
	
		driver.back()

	except:
		rama = 'None'
		rama_doctorado.append(rama)
		
		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')

		driver.back()

	titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
	titulo[link].click()
	centros_click = driver.find_elements_by_xpath('//*[@id="tab3"]')
	centros_click[0].click()
	codigo = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[2]')[0].text
	cod_centro_doctorado.append(codigo)
	centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]/a')[0].text
	nombre_centro_doctorado.append(centro)
	driver.back()

links2 = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]'))
print('links2', links2)
for i in range(0, links2):
	try:
		detalle = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]/a')
		detalle[i].click()
		datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
		datos_i = list()
		print('len DATOS', len(datos))
		#Navegando menu 'Datos del titulo'
		for dat in range(0, len(datos)):
			datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
			datos_i.append(datos[dat].text)
			

			#DESCRIPCION DEL TITULO
			if 'Descripción del título' in datos[dat].text:
				datos[dat].click()
				descripcion_click = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/ul/li')
				descripcion_click_i = list()
				print('len DESCRIPCION', len(descripcion_click))

				#Navegando en 'Descripcion del titulo'
				for desc in range(0, len(descripcion_click)):

					#Click en 'Universidades y centros'
					if 'Universidades y centros' in descripcion_click[desc].text:
						
						try:
							descripcion_click_i.append(descripcion_click[desc].text)
							descripcion_click[desc].click()

							centro_uni = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]')
							centro_uni_i = list()
							centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[4]/a')
							participantes = driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[1]')
							participantes_i = list()
							for part in range(0, len(participantes)):
								#Si es = 4, es una universidad española
								participantes_i.append(len(participantes[part].text))
							
							cod_interuniversitario_i = list()
							#Es 'Interuniversitario', comprobar si hay universidades extranjeras
							if len(centro_uni) >= 2: #Centros
								for part in participantes_i:
									if part >= 5:
										cod_interuniversitario_i.append('2')
									if part < 5:
										cod_interuniversitario_i.append('1')

								if '2' in cod_interuniversitario_i:
									cod_interuniversitario.append('2')
								else:
									cod_interuniversitario.append('1')

							#A priori 'No interuniversitario'
							#Comprobacion interuniversitario, sino 'No interuniversitario'
							elif len(centro_uni) < 2:
								if len(participantes) >= 2:
									for part in participantes_i:
										if part >= 5:
											cod_interuniversitario_i.append('2')
										if part < 5:
											cod_interuniversitario_i.append('1')

									if '2' in cod_interuniversitario_i:
										cod_interuniversitario.append('2')
									else:
										cod_interuniversitario.append('1')


								if len(participantes) < 2:
									cod_interuniversitario.append('0')

							print('---------------')
							#Rol Coordinacion 
							print('cod_interuniversitario', cod_interuniversitario[-1])
							print(driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text)
							if cod_interuniversitario[-1] == '1' or cod_interuniversitario[-1] == '2':
								if 'Universidad Politécnica de Madrid' in driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text:
									cod_rol_coordinacion.append('1')
								else:
									cod_rol_coordinacion.append('0')	
							if cod_interuniversitario[-1] == '0':
								cod_rol_coordinacion.append('8')
							print('cod_rol_coordinacion', cod_rol_coordinacion)


							for j in range(0, len(centro_uni)):
								
								centro_uni_i.append(centro_uni[j].text)
								if 'Universidad Politécnica de Madrid' in centro_uni[j].text:

									print('  UPM', centro_uni[j].text)
									centro[j].click()
									try:
										presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_presencial"]')[0].get_attribute('checked')
										semi_presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_semipresencial"]')[0].get_attribute('checked')
										a_distancia = driver.find_elements_by_xpath('//*[@id="datosCentro_virtual"]')[0].get_attribute('checked')
										print('  Try presencialidad')

										#print(presencial, semi_presencial, a_distancia)

										des_grado_presencialidad_i = list()
										if presencial == 'true':
											des_grado_presencialidad_i.append('Estudio presencial')
										if semi_presencial == 'true':
											des_grado_presencialidad_i.append('Estudio semipresencial')
										if a_distancia == 'true':
											des_grado_presencialidad_i.append('Estudio no presencial')
										if len(des_grado_presencialidad_i) >= 2:
											des_grado_presencialidad_i = list()
											des_grado_presencialidad_i.append('Varias modalidades')
										if presencial != 'true' and semi_presencial != 'true' and a_distancia != 'true': #para DOCTORADOS
											des_grado_presencialidad_i.append(' ')

										des_grado_presencialidad.append(des_grado_presencialidad_i[0])

									except:
										des_grado_presencialidad.append(' ')
										print('  Except presencialidad')


									try:
										idiomas = driver.find_elements_by_xpath('//*[@id="lengua"]/tbody/tr/td')
										idiomas_i = list()
										print('  Try idiomas')
										for i in range(0, len(idiomas)):
											idiomas_i.append(idiomas[i].text)

										if len(idiomas_i) == 1 and 'CASTELLANO ' in idiomas_i:
											cod_idioma_extranjero.append('0')
											des_idioma_extranjero.append('No')
										elif len(idiomas_i) == 1 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('1')
											des_idioma_extranjero.append('Ingles')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('2')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en ingles')
										elif len(idiomas_i) == 1 and 'INGLÉS ' not in idiomas_i and 'CASTELLANO ' not in idiomas_i:
											cod_idioma_extranjero.append('3')
											des_idioma_extranjero.append('Otro idioma extranjero')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' not in idiomas_i:
											cod_idioma_extranjero.append('4')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en otro idioma extranjero')
										else:
											cod_idioma_extranjero.append('None')
											des_idioma_extranjero.append('None')

										driver.back()
										driver.back()
										driver.back()
										break

									except:
										cod_idioma_extranjero.append('None')
										des_idioma_extranjero.append('None')
										print('  Except idiomas')
										driver.back()
										driver.back()
										driver.back()
										break


								else:
									print('	 No UPM', centro_uni[j].text, 'seguimos')
									#continue


							#En caso de que no haya 'Universidad Politécnica de Madrid  '
							if 'Universidad Politécnica de Madrid' not in centro_uni_i[-1]:
								print('   ', centro_uni_i)
								des_grado_presencialidad.append(' ')
								cod_idioma_extranjero.append('None')
								des_idioma_extranjero.append('None')
								print('	  No UPM final \n')

						except:
							print('FALLO UNIVERSIDADES')
							descripcion_click_i.pop(-1)
							driver.back()
							driver.back()
							pass


				if 'Universidades y centros' not in descripcion_click_i:
					print('No hay Universidadades y centros')
					des_grado_presencialidad.append(' ')
					cod_idioma_extranjero.append('None')
					des_idioma_extranjero.append('None')
					cod_rol_coordinacion.append(' ')


			if 'Calendario de implantación' in datos_i[-1]:
				datos[dat].click()

				try:
					anio = driver.find_elements_by_xpath('//*[@id="calendarioImplantacion_curso_Inicio"]')[0]
					anio_value = anio.get_attribute('value')
					print('  Try Año inicio', anio_value)
					if anio_value == '0':
						anio_inicio.append('8888')
						driver.back()
					
					else:
						anio_inicio.append(anio_value)
						driver.back()

					
				except:
					print('  Except Año inicio')
					anio_inicio.append('8888')
					driver.back()


		if 'Calendario de implantación' not in datos_i:
			print('      Not anio inicio fin')
			anio_inicio.append('8888')


		#Pagina principal 'Detalle'
		driver.back()


	#Cuando no hay link 'Ver en Detalle'!
	except IndexError as exception:
		print('No detalle')
		des_grado_presencialidad.append(' ')
		cod_idioma_extranjero.append('None')
		des_idioma_extranjero.append('None')
		anio_inicio.append('8888')
		cod_interuniversitario.append(' ')
		cod_rol_coordinacion.append(' ')
		

print('RESUMEN DOCTORADO')
print('rama' ,len(rama_doctorado))
print(rama_doctorado)
print('num creditos necesarios', len(num_creditos_necesarios))
print('cod centro doctorado', len(cod_centro_doctorado))
print('nombre centro doctorado', len(nombre_centro_doctorado))
print('grado presencialidad', len(des_grado_presencialidad))
print('idioma extranjero', len(des_idioma_extranjero))
print('anio inicio', len(anio_inicio))
print(anio_inicio)
print(len(cod_interuniversitario))
print(len(cod_rol_coordinacion))



#PAGINA 3
pagina2 = driver.find_elements_by_xpath('//*[@id="ver"]/span[2]/a[7]')
pagina2[0].click()
doctorados = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr')
links = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a'))
print('len links', links)
print('Nº doctorado pagina 3: ', len(doctorados))

for doctorado in doctorados:
	cod_doctorado.append(doctorado.find_elements_by_xpath('.//td[1]')[0].text)
	nombre_doctorado.append(doctorado.find_elements_by_xpath('.//td[2]')[0].text)
	estado_doctorado.append(doctorado.find_elements_by_xpath('.//td[5]')[0].text)
	cod_tipo_estudio.append('M')
	des_tipo_estudio.append('Master')

for link in range(0, links):
	#Un master no tiene rama
	try: 
		titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
		titulo[link].click()
		rama_click = driver.find_elements_by_xpath('//*[@id="ui-id-1"]/span')
		rama_click[0].click()
		rama = driver.find_elements_by_xpath('//*[@id="estudio_descripcionRama"]')[0].text
		rama_doctorado.append(rama)

		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')
	
		driver.back()

	except:
		rama = 'None'
		rama_doctorado.append(rama)
		
		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')

		driver.back()

	titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
	titulo[link].click()
	centros_click = driver.find_elements_by_xpath('//*[@id="tab3"]')
	centros_click[0].click()
	codigo = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[2]')[0].text
	cod_centro_doctorado.append(codigo)
	centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]/a')[0].text
	nombre_centro_doctorado.append(centro)
	driver.back()

links2 = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]'))
print('links2', links2)
for i in range(0, links2):
	try:
		detalle = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]/a')
		detalle[i].click()
		datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
		datos_i = list()
		print('len DATOS', len(datos))
		#Navegando menu 'Datos del titulo'
		for dat in range(0, len(datos)):
			datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
			datos_i.append(datos[dat].text)
			

			#DESCRIPCION DEL TITULO
			if 'Descripción del título' in datos[dat].text:
				datos[dat].click()
				descripcion_click = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/ul/li')
				descripcion_click_i = list()
				print('len DESCRIPCION', len(descripcion_click))

				#Navegando en 'Descripcion del titulo'
				for desc in range(0, len(descripcion_click)):

					#Click en 'Universidades y centros'
					if 'Universidades y centros' in descripcion_click[desc].text:
						
						try:
							descripcion_click_i.append(descripcion_click[desc].text)
							descripcion_click[desc].click()

							centro_uni = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]')
							centro_uni_i = list()
							centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[4]/a')
							participantes = driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[1]')
							participantes_i = list()
							for part in range(0, len(participantes)):
								#Si es = 4, es una universidad española
								participantes_i.append(len(participantes[part].text))
							
							cod_interuniversitario_i = list()
							#Es 'Interuniversitario', comprobar si hay universidades extranjeras
							if len(centro_uni) >= 2: #Centros
								for part in participantes_i:
									if part >= 5:
										cod_interuniversitario_i.append('2')
									if part < 5:
										cod_interuniversitario_i.append('1')

								if '2' in cod_interuniversitario_i:
									cod_interuniversitario.append('2')
								else:
									cod_interuniversitario.append('1')

							#A priori 'No interuniversitario'
							#Comprobacion interuniversitario, sino 'No interuniversitario'
							elif len(centro_uni) < 2:
								if len(participantes) >= 2:
									for part in participantes_i:
										if part >= 5:
											cod_interuniversitario_i.append('2')
										if part < 5:
											cod_interuniversitario_i.append('1')

									if '2' in cod_interuniversitario_i:
										cod_interuniversitario.append('2')
									else:
										cod_interuniversitario.append('1')


								if len(participantes) < 2:
									cod_interuniversitario.append('0')

							print('---------------')
							#Rol Coordinacion 
							print('cod_interuniversitario', cod_interuniversitario[-1])
							print(driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text)
							if cod_interuniversitario[-1] == '1' or cod_interuniversitario[-1] == '2':
								if 'Universidad Politécnica de Madrid' in driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text:
									cod_rol_coordinacion.append('1')
								else:
									cod_rol_coordinacion.append('0')	
							if cod_interuniversitario[-1] == '0':
								cod_rol_coordinacion.append('8')
							print('cod_rol_coordinacion', cod_rol_coordinacion)


							for j in range(0, len(centro_uni)):
								
								centro_uni_i.append(centro_uni[j].text)
								if 'Universidad Politécnica de Madrid' in centro_uni[j].text:

									print('  UPM', centro_uni[j].text)
									centro[j].click()
									try:
										presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_presencial"]')[0].get_attribute('checked')
										semi_presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_semipresencial"]')[0].get_attribute('checked')
										a_distancia = driver.find_elements_by_xpath('//*[@id="datosCentro_virtual"]')[0].get_attribute('checked')
										print('  Try presencialidad')

										#print(presencial, semi_presencial, a_distancia)

										des_grado_presencialidad_i = list()
										if presencial == 'true':
											des_grado_presencialidad_i.append('Estudio presencial')
										if semi_presencial == 'true':
											des_grado_presencialidad_i.append('Estudio semipresencial')
										if a_distancia == 'true':
											des_grado_presencialidad_i.append('Estudio no presencial')
										if len(des_grado_presencialidad_i) >= 2:
											des_grado_presencialidad_i = list()
											des_grado_presencialidad_i.append('Varias modalidades')
										if presencial != 'true' and semi_presencial != 'true' and a_distancia != 'true': #para DOCTORADOS
											des_grado_presencialidad_i.append(' ')

										des_grado_presencialidad.append(des_grado_presencialidad_i[0])

									except:
										des_grado_presencialidad.append(' ')
										print('  Except presencialidad')


									try:
										idiomas = driver.find_elements_by_xpath('//*[@id="lengua"]/tbody/tr/td')
										idiomas_i = list()
										print('  Try idiomas')
										for i in range(0, len(idiomas)):
											idiomas_i.append(idiomas[i].text)

										if len(idiomas_i) == 1 and 'CASTELLANO ' in idiomas_i:
											cod_idioma_extranjero.append('0')
											des_idioma_extranjero.append('No')
										elif len(idiomas_i) == 1 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('1')
											des_idioma_extranjero.append('Ingles')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('2')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en ingles')
										elif len(idiomas_i) == 1 and 'INGLÉS ' not in idiomas_i and 'CASTELLANO ' not in idiomas_i:
											cod_idioma_extranjero.append('3')
											des_idioma_extranjero.append('Otro idioma extranjero')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' not in idiomas_i:
											cod_idioma_extranjero.append('4')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en otro idioma extranjero')
										else:
											cod_idioma_extranjero.append('None')
											des_idioma_extranjero.append('None')

										driver.back()
										driver.back()
										driver.back()
										break

									except:
										cod_idioma_extranjero.append('None')
										des_idioma_extranjero.append('None')
										print('  Except idiomas')
										driver.back()
										driver.back()
										driver.back()
										break


								else:
									print('	 No UPM', centro_uni[j].text, 'seguimos')
									#continue


							#En caso de que no haya 'Universidad Politécnica de Madrid  '
							if 'Universidad Politécnica de Madrid' not in centro_uni_i[-1]:
								print('   ', centro_uni_i)
								des_grado_presencialidad.append(' ')
								cod_idioma_extranjero.append('None')
								des_idioma_extranjero.append('None')
								print('	  No UPM final \n')

						except:
							print('FALLO UNIVERSIDADES')
							descripcion_click_i.pop(-1)
							driver.back()
							driver.back()
							pass


				if 'Universidades y centros' not in descripcion_click_i:
					print('No hay Universidadades y centros')
					des_grado_presencialidad.append(' ')
					cod_idioma_extranjero.append('None')
					des_idioma_extranjero.append('None')
					cod_rol_coordinacion.append(' ')


			if 'Calendario de implantación' in datos_i[-1]:
				datos[dat].click()

				try:
					anio = driver.find_elements_by_xpath('//*[@id="calendarioImplantacion_curso_Inicio"]')[0]
					anio_value = anio.get_attribute('value')
					print('  Try Año inicio', anio_value)
					if anio_value == '0':
						anio_inicio.append('8888')
						driver.back()
					
					else:
						anio_inicio.append(anio_value)
						driver.back()

					
				except:
					print('  Except Año inicio')
					anio_inicio.append('8888')
					driver.back()


		if 'Calendario de implantación' not in datos_i:
			print('      Not anio inicio fin')
			anio_inicio.append('8888')


		#Pagina principal 'Detalle'
		driver.back()


	#Cuando no hay link 'Ver en Detalle'!
	except IndexError as exception:
		print('No detalle')
		des_grado_presencialidad.append(' ')
		cod_idioma_extranjero.append('None')
		des_idioma_extranjero.append('None')
		anio_inicio.append('8888')
		cod_interuniversitario.append(' ')
		cod_rol_coordinacion.append(' ')
		

print('RESUMEN DOCTORADO')
print('rama' ,len(rama_doctorado))
print(rama_doctorado)
print('num creditos necesarios', len(num_creditos_necesarios))
print('cod centro doctorado', len(cod_centro_doctorado))
print('nombre centro doctorado', len(nombre_centro_doctorado))
print('grado presencialidad', len(des_grado_presencialidad))
print('idioma extranjero', len(des_idioma_extranjero))
print('anio inicio', len(anio_inicio))
print(anio_inicio)
print(len(cod_interuniversitario))
print(len(cod_rol_coordinacion))



#PAGINA 4
pagina2 = driver.find_elements_by_xpath('//*[@id="ver"]/span[2]/a[7]')
pagina2[0].click()
doctorados = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr')
links = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a'))
print('len links', links)
print('Nº doctorado pagina 4: ', len(doctorados))

for doctorado in doctorados:
	cod_doctorado.append(doctorado.find_elements_by_xpath('.//td[1]')[0].text)
	nombre_doctorado.append(doctorado.find_elements_by_xpath('.//td[2]')[0].text)
	estado_doctorado.append(doctorado.find_elements_by_xpath('.//td[5]')[0].text)
	cod_tipo_estudio.append('M')
	des_tipo_estudio.append('Master')

for link in range(0, links):
	#Un master no tiene rama
	try: 
		titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
		titulo[link].click()
		rama_click = driver.find_elements_by_xpath('//*[@id="ui-id-1"]/span')
		rama_click[0].click()
		rama = driver.find_elements_by_xpath('//*[@id="estudio_descripcionRama"]')[0].text
		rama_doctorado.append(rama)

		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')
	
		driver.back()

	except:
		rama = 'None'
		rama_doctorado.append(rama)
		
		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')

		driver.back()

	titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
	titulo[link].click()
	centros_click = driver.find_elements_by_xpath('//*[@id="tab3"]')
	centros_click[0].click()
	codigo = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[2]')[0].text
	cod_centro_doctorado.append(codigo)
	centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]/a')[0].text
	nombre_centro_doctorado.append(centro)
	driver.back()

links2 = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]'))
print('links2', links2)
for i in range(0, links2):
	try:
		detalle = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]/a')
		detalle[i].click()
		datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
		datos_i = list()
		print('len DATOS', len(datos))
		#Navegando menu 'Datos del titulo'
		for dat in range(0, len(datos)):
			datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
			datos_i.append(datos[dat].text)
			

			#DESCRIPCION DEL TITULO
			if 'Descripción del título' in datos[dat].text:
				datos[dat].click()
				descripcion_click = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/ul/li')
				descripcion_click_i = list()
				print('len DESCRIPCION', len(descripcion_click))

				#Navegando en 'Descripcion del titulo'
				for desc in range(0, len(descripcion_click)):

					#Click en 'Universidades y centros'
					if 'Universidades y centros' in descripcion_click[desc].text:
						
						try:
							descripcion_click_i.append(descripcion_click[desc].text)
							descripcion_click[desc].click()

							centro_uni = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]')
							centro_uni_i = list()
							centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[4]/a')
							participantes = driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[1]')
							participantes_i = list()
							for part in range(0, len(participantes)):
								#Si es = 4, es una universidad española
								participantes_i.append(len(participantes[part].text))
							
							cod_interuniversitario_i = list()
							#Es 'Interuniversitario', comprobar si hay universidades extranjeras
							if len(centro_uni) >= 2: #Centros
								for part in participantes_i:
									if part >= 5:
										cod_interuniversitario_i.append('2')
									if part < 5:
										cod_interuniversitario_i.append('1')

								if '2' in cod_interuniversitario_i:
									cod_interuniversitario.append('2')
								else:
									cod_interuniversitario.append('1')

							#A priori 'No interuniversitario'
							#Comprobacion interuniversitario, sino 'No interuniversitario'
							elif len(centro_uni) < 2:
								if len(participantes) >= 2:
									for part in participantes_i:
										if part >= 5:
											cod_interuniversitario_i.append('2')
										if part < 5:
											cod_interuniversitario_i.append('1')

									if '2' in cod_interuniversitario_i:
										cod_interuniversitario.append('2')
									else:
										cod_interuniversitario.append('1')


								if len(participantes) < 2:
									cod_interuniversitario.append('0')

							print('---------------')
							#Rol Coordinacion 
							print('cod_interuniversitario', cod_interuniversitario[-1])
							print(driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text)
							if cod_interuniversitario[-1] == '1' or cod_interuniversitario[-1] == '2':
								if 'Universidad Politécnica de Madrid' in driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text:
									cod_rol_coordinacion.append('1')
								else:
									cod_rol_coordinacion.append('0')	
							if cod_interuniversitario[-1] == '0':
								cod_rol_coordinacion.append('8')
							print('cod_rol_coordinacion', cod_rol_coordinacion)


							for j in range(0, len(centro_uni)):
								
								centro_uni_i.append(centro_uni[j].text)
								if 'Universidad Politécnica de Madrid' in centro_uni[j].text:

									print('  UPM', centro_uni[j].text)
									centro[j].click()
									try:
										presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_presencial"]')[0].get_attribute('checked')
										semi_presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_semipresencial"]')[0].get_attribute('checked')
										a_distancia = driver.find_elements_by_xpath('//*[@id="datosCentro_virtual"]')[0].get_attribute('checked')
										print('  Try presencialidad')

										#print(presencial, semi_presencial, a_distancia)

										des_grado_presencialidad_i = list()
										if presencial == 'true':
											des_grado_presencialidad_i.append('Estudio presencial')
										if semi_presencial == 'true':
											des_grado_presencialidad_i.append('Estudio semipresencial')
										if a_distancia == 'true':
											des_grado_presencialidad_i.append('Estudio no presencial')
										if len(des_grado_presencialidad_i) >= 2:
											des_grado_presencialidad_i = list()
											des_grado_presencialidad_i.append('Varias modalidades')
										if presencial != 'true' and semi_presencial != 'true' and a_distancia != 'true': #para DOCTORADOS
											des_grado_presencialidad_i.append(' ')

										des_grado_presencialidad.append(des_grado_presencialidad_i[0])

									except:
										des_grado_presencialidad.append(' ')
										print('  Except presencialidad')


									try:
										idiomas = driver.find_elements_by_xpath('//*[@id="lengua"]/tbody/tr/td')
										idiomas_i = list()
										print('  Try idiomas')
										for i in range(0, len(idiomas)):
											idiomas_i.append(idiomas[i].text)

										if len(idiomas_i) == 1 and 'CASTELLANO ' in idiomas_i:
											cod_idioma_extranjero.append('0')
											des_idioma_extranjero.append('No')
										elif len(idiomas_i) == 1 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('1')
											des_idioma_extranjero.append('Ingles')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('2')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en ingles')
										elif len(idiomas_i) == 1 and 'INGLÉS ' not in idiomas_i and 'CASTELLANO ' not in idiomas_i:
											cod_idioma_extranjero.append('3')
											des_idioma_extranjero.append('Otro idioma extranjero')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' not in idiomas_i:
											cod_idioma_extranjero.append('4')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en otro idioma extranjero')
										else:
											cod_idioma_extranjero.append('None')
											des_idioma_extranjero.append('None')

										driver.back()
										driver.back()
										driver.back()
										break

									except:
										cod_idioma_extranjero.append('None')
										des_idioma_extranjero.append('None')
										print('  Except idiomas')
										driver.back()
										driver.back()
										driver.back()
										break


								else:
									print('	 No UPM', centro_uni[j].text, 'seguimos')
									#continue


							#En caso de que no haya 'Universidad Politécnica de Madrid  '
							if 'Universidad Politécnica de Madrid' not in centro_uni_i[-1]:
								print('   ', centro_uni_i)
								des_grado_presencialidad.append(' ')
								cod_idioma_extranjero.append('None')
								des_idioma_extranjero.append('None')
								print('	  No UPM final \n')

						except:
							print('FALLO UNIVERSIDADES')
							descripcion_click_i.pop(-1)
							driver.back()
							driver.back()
							pass


				if 'Universidades y centros' not in descripcion_click_i:
					print('No hay Universidadades y centros')
					des_grado_presencialidad.append(' ')
					cod_idioma_extranjero.append('None')
					des_idioma_extranjero.append('None')
					cod_rol_coordinacion.append(' ')


			if 'Calendario de implantación' in datos_i[-1]:
				datos[dat].click()

				try:
					anio = driver.find_elements_by_xpath('//*[@id="calendarioImplantacion_curso_Inicio"]')[0]
					anio_value = anio.get_attribute('value')
					print('  Try Año inicio', anio_value)
					if anio_value == '0':
						anio_inicio.append('8888')
						driver.back()
					
					else:
						anio_inicio.append(anio_value)
						driver.back()

					
				except:
					print('  Except Año inicio')
					anio_inicio.append('8888')
					driver.back()


		if 'Calendario de implantación' not in datos_i:
			print('      Not anio inicio fin')
			anio_inicio.append('8888')


		#Pagina principal 'Detalle'
		driver.back()


	#Cuando no hay link 'Ver en Detalle'!
	except IndexError as exception:
		print('No detalle')
		des_grado_presencialidad.append(' ')
		cod_idioma_extranjero.append('None')
		des_idioma_extranjero.append('None')
		anio_inicio.append('8888')
		cod_interuniversitario.append(' ')
		cod_rol_coordinacion.append(' ')
		

print('RESUMEN DOCTORADO')
print('rama' ,len(rama_doctorado))
print(rama_doctorado)
print('num creditos necesarios', len(num_creditos_necesarios))
print('cod centro doctorado', len(cod_centro_doctorado))
print('nombre centro doctorado', len(nombre_centro_doctorado))
print('grado presencialidad', len(des_grado_presencialidad))
print('idioma extranjero', len(des_idioma_extranjero))
print('anio inicio', len(anio_inicio))
print(anio_inicio)
print(len(cod_interuniversitario))
print(len(cod_rol_coordinacion))



#PAGINA 5
pagina2 = driver.find_elements_by_xpath('//*[@id="ver"]/span[2]/a[7]')
pagina2[0].click()
doctorados = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr')
links = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a'))
print('len links', links)
print('Nº doctorado pagina 5: ', len(doctorados))

for doctorado in doctorados:
	cod_doctorado.append(doctorado.find_elements_by_xpath('.//td[1]')[0].text)
	nombre_doctorado.append(doctorado.find_elements_by_xpath('.//td[2]')[0].text)
	estado_doctorado.append(doctorado.find_elements_by_xpath('.//td[5]')[0].text)
	cod_tipo_estudio.append('M')
	des_tipo_estudio.append('Master')

for link in range(0, links):
	#Un master no tiene rama
	try: 
		titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
		titulo[link].click()
		rama_click = driver.find_elements_by_xpath('//*[@id="ui-id-1"]/span')
		rama_click[0].click()
		rama = driver.find_elements_by_xpath('//*[@id="estudio_descripcionRama"]')[0].text
		rama_doctorado.append(rama)

		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')
	
		driver.back()

	except:
		rama = 'None'
		rama_doctorado.append(rama)
		
		try:
			num_creditos_necesarios.append(driver.find_elements_by_xpath('//*[@id="estudio_creditos_ecs"]')[0].text)
		except:
			num_creditos_necesarios.append(' ')

		driver.back()

	titulo = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[2]/a')
	titulo[link].click()
	centros_click = driver.find_elements_by_xpath('//*[@id="tab3"]')
	centros_click[0].click()
	codigo = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[2]')[0].text
	cod_centro_doctorado.append(codigo)
	centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]/a')[0].text
	nombre_centro_doctorado.append(centro)
	driver.back()

links2 = len(driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]'))
print('links2', links2)
for i in range(0, links2):
	try:
		detalle = driver.find_elements_by_xpath('//*[@id="estudio"]/tbody/tr/td[6]/a')
		detalle[i].click()
		datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
		datos_i = list()
		print('len DATOS', len(datos))
		#Navegando menu 'Datos del titulo'
		for dat in range(0, len(datos)):
			datos = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/a')
			datos_i.append(datos[dat].text)
			

			#DESCRIPCION DEL TITULO
			if 'Descripción del título' in datos[dat].text:
				datos[dat].click()
				descripcion_click = driver.find_elements_by_xpath('//*[@id="menu-contenido"]/ul/li[3]/ul/li/ul/li/ul/li')
				descripcion_click_i = list()
				print('len DESCRIPCION', len(descripcion_click))

				#Navegando en 'Descripcion del titulo'
				for desc in range(0, len(descripcion_click)):

					#Click en 'Universidades y centros'
					if 'Universidades y centros' in descripcion_click[desc].text:
						
						try:
							descripcion_click_i.append(descripcion_click[desc].text)
							descripcion_click[desc].click()

							centro_uni = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[3]')
							centro_uni_i = list()
							centro = driver.find_elements_by_xpath('//*[@id="centro"]/tbody/tr/td[4]/a')
							participantes = driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[1]')
							participantes_i = list()
							for part in range(0, len(participantes)):
								#Si es = 4, es una universidad española
								participantes_i.append(len(participantes[part].text))
							
							cod_interuniversitario_i = list()
							#Es 'Interuniversitario', comprobar si hay universidades extranjeras
							if len(centro_uni) >= 2: #Centros
								for part in participantes_i:
									if part >= 5:
										cod_interuniversitario_i.append('2')
									if part < 5:
										cod_interuniversitario_i.append('1')

								if '2' in cod_interuniversitario_i:
									cod_interuniversitario.append('2')
								else:
									cod_interuniversitario.append('1')

							#A priori 'No interuniversitario'
							#Comprobacion interuniversitario, sino 'No interuniversitario'
							elif len(centro_uni) < 2:
								if len(participantes) >= 2:
									for part in participantes_i:
										if part >= 5:
											cod_interuniversitario_i.append('2')
										if part < 5:
											cod_interuniversitario_i.append('1')

									if '2' in cod_interuniversitario_i:
										cod_interuniversitario.append('2')
									else:
										cod_interuniversitario.append('1')


								if len(participantes) < 2:
									cod_interuniversitario.append('0')

							print('---------------')
							#Rol Coordinacion 
							print('cod_interuniversitario', cod_interuniversitario[-1])
							print(driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text)
							if cod_interuniversitario[-1] == '1' or cod_interuniversitario[-1] == '2':
								if 'Universidad Politécnica de Madrid' in driver.find_elements_by_xpath('//*[@id="universidad"]/tbody/tr/td[2]')[0].text:
									cod_rol_coordinacion.append('1')
								else:
									cod_rol_coordinacion.append('0')	
							if cod_interuniversitario[-1] == '0':
								cod_rol_coordinacion.append('8')
							print('cod_rol_coordinacion', cod_rol_coordinacion)


							for j in range(0, len(centro_uni)):
								
								centro_uni_i.append(centro_uni[j].text)
								if 'Universidad Politécnica de Madrid' in centro_uni[j].text:

									print('  UPM', centro_uni[j].text)
									centro[j].click()
									try:
										presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_presencial"]')[0].get_attribute('checked')
										semi_presencial = driver.find_elements_by_xpath('//*[@id="datosCentro_semipresencial"]')[0].get_attribute('checked')
										a_distancia = driver.find_elements_by_xpath('//*[@id="datosCentro_virtual"]')[0].get_attribute('checked')
										print('  Try presencialidad')

										#print(presencial, semi_presencial, a_distancia)

										des_grado_presencialidad_i = list()
										if presencial == 'true':
											des_grado_presencialidad_i.append('Estudio presencial')
										if semi_presencial == 'true':
											des_grado_presencialidad_i.append('Estudio semipresencial')
										if a_distancia == 'true':
											des_grado_presencialidad_i.append('Estudio no presencial')
										if len(des_grado_presencialidad_i) >= 2:
											des_grado_presencialidad_i = list()
											des_grado_presencialidad_i.append('Varias modalidades')
										if presencial != 'true' and semi_presencial != 'true' and a_distancia != 'true': #para DOCTORADOS
											des_grado_presencialidad_i.append(' ')

										des_grado_presencialidad.append(des_grado_presencialidad_i[0])

									except:
										des_grado_presencialidad.append(' ')
										print('  Except presencialidad')


									try:
										idiomas = driver.find_elements_by_xpath('//*[@id="lengua"]/tbody/tr/td')
										idiomas_i = list()
										print('  Try idiomas')
										for i in range(0, len(idiomas)):
											idiomas_i.append(idiomas[i].text)

										if len(idiomas_i) == 1 and 'CASTELLANO ' in idiomas_i:
											cod_idioma_extranjero.append('0')
											des_idioma_extranjero.append('No')
										elif len(idiomas_i) == 1 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('1')
											des_idioma_extranjero.append('Ingles')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' in idiomas_i:
											cod_idioma_extranjero.append('2')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en ingles')
										elif len(idiomas_i) == 1 and 'INGLÉS ' not in idiomas_i and 'CASTELLANO ' not in idiomas_i:
											cod_idioma_extranjero.append('3')
											des_idioma_extranjero.append('Otro idioma extranjero')
										elif len(idiomas_i) >= 2 and 'INGLÉS ' not in idiomas_i:
											cod_idioma_extranjero.append('4')
											des_idioma_extranjero.append('Existen planes separados, uno de ellos en otro idioma extranjero')
										else:
											cod_idioma_extranjero.append('None')
											des_idioma_extranjero.append('None')

										driver.back()
										driver.back()
										driver.back()
										break

									except:
										cod_idioma_extranjero.append('None')
										des_idioma_extranjero.append('None')
										print('  Except idiomas')
										driver.back()
										driver.back()
										driver.back()
										break


								else:
									print('	 No UPM', centro_uni[j].text, 'seguimos')
									#continue


							#En caso de que no haya 'Universidad Politécnica de Madrid  '
							if 'Universidad Politécnica de Madrid' not in centro_uni_i[-1]:
								print('   ', centro_uni_i)
								des_grado_presencialidad.append(' ')
								cod_idioma_extranjero.append('None')
								des_idioma_extranjero.append('None')
								print('	  No UPM final \n')

						except:
							print('FALLO UNIVERSIDADES')
							descripcion_click_i.pop(-1)
							driver.back()
							driver.back()
							pass


				if 'Universidades y centros' not in descripcion_click_i:
					print('No hay Universidadades y centros')
					des_grado_presencialidad.append(' ')
					cod_idioma_extranjero.append('None')
					des_idioma_extranjero.append('None')
					cod_rol_coordinacion.append(' ')


			if 'Calendario de implantación' in datos_i[-1]:
				datos[dat].click()

				try:
					anio = driver.find_elements_by_xpath('//*[@id="calendarioImplantacion_curso_Inicio"]')[0]
					anio_value = anio.get_attribute('value')
					print('  Try Año inicio', anio_value)
					if anio_value == '0':
						anio_inicio.append('8888')
						driver.back()
					
					else:
						anio_inicio.append(anio_value)
						driver.back()

					
				except:
					print('  Except Año inicio')
					anio_inicio.append('8888')
					driver.back()


		if 'Calendario de implantación' not in datos_i:
			print('      Not anio inicio fin')
			anio_inicio.append('8888')


		#Pagina principal 'Detalle'
		driver.back()


	#Cuando no hay link 'Ver en Detalle'!
	except IndexError as exception:
		print('No detalle')
		des_grado_presencialidad.append(' ')
		cod_idioma_extranjero.append('None')
		des_idioma_extranjero.append('None')
		anio_inicio.append('8888')
		cod_interuniversitario.append(' ')
		cod_rol_coordinacion.append(' ')
		

print('RESUMEN DOCTORADO')
print('rama' ,len(rama_doctorado))
print(rama_doctorado)
print('num creditos necesarios', len(num_creditos_necesarios))
print('cod centro doctorado', len(cod_centro_doctorado))
print('nombre centro doctorado', len(nombre_centro_doctorado))
print('grado presencialidad', len(des_grado_presencialidad))
print('idioma extranjero', len(des_idioma_extranjero))
print('anio inicio', len(anio_inicio))
print(anio_inicio)
print(len(cod_interuniversitario), cod_interuniversitario)
print(len(cod_rol_coordinacion), cod_rol_coordinacion)

#--------------------------
#AGRUPAR VARIABLES
#--------------------------
cod_titulacion = cod_grado + cod_master + cod_doctorado
des_titulacion = nombre_grado + nombre_master + nombre_doctorado
estado_titulacion = estado_grado + estado_master + estado_doctorado
des_rama = rama_grado + rama_master + rama_doctorado
des_unidad_responsable = nombre_centro_grado + nombre_centro_master + nombre_centro_doctorado
cod_unidad_responsable = cod_centro_grado + cod_centro_master + cod_centro_doctorado

cod_rama = list()
for i in range(0, len(des_rama)):
	if des_rama[i] == 'Artes y Humanidades':
		cod_rama.append('1')
	elif des_rama[i] == 'Ciencias':
		cod_rama.append('2')
	elif des_rama[i] == 'Ciencias Sociales y Jurídicas':
		cod_rama.append('3')
	elif des_rama[i] == 'Ingeniería y Arquitectura':
		cod_rama.append('4')
	elif des_rama[i] == 'Ciencias de la Salud':
		cod_rama.append('5')
	elif des_rama[i] == 'None':
		cod_rama.append('None')
	else:
		cod_rama.append('MAAAL')

print(len(cod_titulacion), len(des_titulacion), len(estado_titulacion), len(des_rama), 
	len(cod_rama), len(des_unidad_responsable), len(cod_unidad_responsable), len(des_grado_presencialidad),
	)

cod_grado_presencialidad = list()
for i in des_grado_presencialidad:
	if i == 'Estudio presencial':
		cod_grado_presencialidad.append('1')
	if i == 'Estudio semipresencial':
		cod_grado_presencialidad.append('2')
	if i == 'Estudio no presencial':
		cod_grado_presencialidad.append('3')
	if i == 'Varias modalidades':
		cod_grado_presencialidad.append('4')
	if i == ' ':
		cod_grado_presencialidad.append(' ')

cod_situacion_actual = list()
des_situacion_actual = list()
cod_impartido = list()
des_impartido = list()
for i in estado_titulacion:
	if 'A EXTINGUIR' in i:
		cod_situacion_actual.append('3')
		des_situacion_actual.append('En proceso de extincion')
		cod_impartido.append('1')
		des_impartido.append('Se imparte en el curso academico de referencia')
	elif 'TITULACIÓN EXcodTINGUIDA' in i:
		cod_situacion_actual.append('4')
		des_situacion_actual.append('Extinguido este curso')
		cod_impartido.append('0')
		des_impartido.append('No se imparte en el curso academico de referencia')
	else: #Publicado en BOE / Titulacion renovada
		cod_situacion_actual.append('1')
		des_situacion_actual.append('Activo')
		cod_impartido.append('1')
		des_impartido.append('Se imparte en el curso academico de referencia')


des_interuniversitario = list()
for i in cod_interuniversitario:
	if i == '0':
		des_interuniversitario.append('No es interuniversitario')
	if i == '1':
		des_interuniversitario.append('Si es interuniversitario, con alguna Universidad española')
	if i == '2':
		des_interuniversitario.append('Si es interuniversitario, con alguna Universidad extranjera')
	if i == ' ':
		des_interuniversitario.append(' ')


des_rol_coordinacion = list()
for i in cod_rol_coordinacion:
	if i == '0':
		des_rol_coordinacion.append('No es coordinadora')
	if i == '1':
		des_rol_coordinacion.append('Si es coordinadora')
	if i == '8':
		des_rol_coordinacion.append('No aplica coordinacion')
	if i == ' ':
		des_rol_coordinacion.append(' ')


print(len(cod_grado_presencialidad), len(estado_titulacion), len(cod_situacion_actual),
	len(des_situacion_actual), len(cod_interuniversitario),
	len(cod_impartido), len(des_impartido), len(des_interuniversitario),
	len(cod_rol_coordinacion), len(des_rol_coordinacion))
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------
#----------------------------------------------------------------------------------


#----------------------------------------------------------------------------------
#TITULACIONES DATASET

curso_academico = ['2020-21'] * len(cod_titulacion)
cod_universidad = ['025'] * len(cod_titulacion)
des_universidad = ['Universidad Politécnica de Madrid'] * len(cod_titulacion)
cod_tipo_estudio = cod_tipo_estudio
des_tipo_estudio =  des_tipo_estudio
cod_tipo_unidad_responsable = ['1'] * len(cod_titulacion) #¿Son todos Centro????
des_tipo_unidad_responsable = ['Centro'] * len(cod_titulacion)
cod_unidad_responsable = cod_unidad_responsable
des_unidad_responsable = des_unidad_responsable
cod_titulacion = cod_titulacion
des_titulacion = des_titulacion
cod_rama = cod_rama
des_rama = des_rama
cod_interuniversitario = cod_interuniversitario
des_interuniversitario = des_interuniversitario
cod_rol_coordinacion = cod_rol_coordinacion
des_rol_coordinacion = des_rol_coordinacion
cod_impartido = cod_impartido #IMPARTIDA: si tiene alumnos matriculados
des_impartido = des_impartido
anio_inicio = anio_inicio
cod_situacion_actual = cod_situacion_actual
des_situacion_actual = des_situacion_actual
cod_grado_presencialidad = cod_grado_presencialidad
des_grado_presencialidad = des_grado_presencialidad
cod_idioma_extranjero = cod_idioma_extranjero
des_idioma_extranjero = des_idioma_extranjero
precio_credito_1 = [' '] * len(cod_titulacion)
precio_credito_2 = [' '] * len(cod_titulacion)
precio_credito_3 = [' '] * len(cod_titulacion)
precio_credito_4 = [' '] * len(cod_titulacion)
precio_credito_5 = [' '] * len(cod_titulacion)
precio_tutela = [' '] * len(cod_titulacion)
num_creditos_necesarios = num_creditos_necesarios
num_creditos_ofertados = [' '] * len(cod_titulacion)

data = {'curso_academico':curso_academico,
		'codigo_universidad':cod_universidad,
		'nombre_universidad':des_universidad,
		'codigo_tipo_estudio':cod_tipo_estudio,
		'nombre_tipo_estudio':des_tipo_estudio, 
		'codigo_tipo_unidad_responsable':cod_tipo_unidad_responsable,
		'nombre_tipo_unidad_responsable':des_tipo_unidad_responsable,
		'codigo_unidad_responsable':cod_unidad_responsable,
		'nombre_unidad_responsable':des_unidad_responsable,
		'codigo_titulacion':cod_titulacion,
		'nombre_titulacion':des_titulacion,
		'codigo_rama':cod_rama,
		'descripcion_rama':des_rama,
		'codigo_interuniversitario':cod_interuniversitario,
		'descripcion_interuniversitario':des_interuniversitario,
		'codigo_rol_coordinacion':cod_rol_coordinacion,
		'descripcion_rol_coordinacion':des_rol_coordinacion,
		'codigo_impartido':cod_impartido,
		'descripcion_impartido':des_impartido,
		'anio_inicio':anio_inicio,
		'codigo_situacion_actual':cod_situacion_actual,
		'descripcion_situacion_actual':des_situacion_actual,
		'codigo_presencialidad':cod_grado_presencialidad,
		'descripcion_grado_presencialidad':des_grado_presencialidad,
		'codigo_idioma_extranjero':cod_idioma_extranjero,
		'descripcion_idioma_extranjero':des_idioma_extranjero,
		'precio_credito_1':precio_credito_1,
		'precio_credito_2':precio_credito_2,
		'precio_credito_3':precio_credito_3,
		'precio_credito_4':precio_credito_4,
		'precio_credito_5':precio_credito_5,
		'precio_tutela':precio_tutela,
		'num_creditos_necesarios':num_creditos_necesarios,
		'numero_creditos_ofertados':num_creditos_ofertados
}

titulaciones_df = DataFrame(data)
titulaciones_df.to_csv('UPM-titulaciones.csv')