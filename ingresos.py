import pandas as pd
from pandas import DataFrame
import re 
from unicodedata import normalize

cod_universidad = list()
des_universidad = list()
anio = list()
cod_capitulo = list()
des_capitulo = list()
cod_articulo = list()
des_articulo = list()
cod_concepto = list()
des_concepto = list()
cod_subconcepto = list()
des_subconcepto = list()
cod_partida = list() #No esta
des_partida = list() #No esta
#Clasificacion organica
cod_seccion = list()
des_seccion = list()
cod_servicio = list()
des_servicio = list()
cod_unidad_de_coste = list() #No esta
des_unidad_de_coste = list() #No esta
cod_organica_libre_1 = list() #No esta
des_organica_libre_1 = list() #No esta
cod_organica_libre_2 = list() #No esta
des_organica_libre_2 = list() #No esta
fecha_referencia = list()
credito_inicial = list()
modificaciones = list()
credito_total = list()
derechos_reconocidos_netos = list()
recaudacion_neta = list()


ingresos_organico = pd.read_csv('Presupuestos/UPM-ingresos-1-2021.csv', sep=';', header = 1, dtype = 'str')
ingresos_subconcepto = pd.read_csv('Presupuestos/UPM-ingresos-2-2021.csv', sep=';', header = 2, dtype = 'str')


afectado = list()
subconcepto = list()
importe = list()
total_importe = list()

ingresos_organico['IMPORTE'] = ingresos_organico['IMPORTE'].fillna('0')
for i in range(0,len(ingresos_organico)-3): #eliminamos las ultimas 3 columnas que son de totales
	if len(ingresos_organico.loc[i,'CÓDIGO']) <= 2:
		seccion = ingresos_organico.loc[i,'CÓDIGO']
		cod_seccion.append(ingresos_organico.loc[i,'CÓDIGO'])
		des_seccion.append(ingresos_organico.loc[i,'CENTRO'])
		cod_servicio.append('None')
		des_servicio.append('None')
	if len(ingresos_organico.loc[i,'CÓDIGO']) >= 3:
		if '.' in ingresos_organico.loc[i,'CÓDIGO']:
			cod_seccion.append(ingresos_organico.loc[i,'CÓDIGO'].split('.')[0])
			des_seccion.append(ingresos_organico.loc[ingresos_organico['CÓDIGO'] == cod_seccion[1], 'CENTRO'][0])
			cod_servicio.append(ingresos_organico.loc[i,'CÓDIGO'])
			des_servicio.append(ingresos_organico.loc[i,'CENTRO'])
		if '.' not in ingresos_organico.loc[i,'CÓDIGO']:
			cod_seccion.append(ingresos_organico.loc[i,'CÓDIGO'][:2])
			des_seccion.append(ingresos_organico.loc[ingresos_organico['CÓDIGO'] == cod_seccion[1], 'CENTRO'][0])
			cod_servicio.append(ingresos_organico.loc[i,'CÓDIGO'])
			des_servicio.append(ingresos_organico.loc[i,'CENTRO'])
	afectado.append(ingresos_organico.loc[i,'Afectado/No Afectado'])
	subconcepto.append(ingresos_organico.loc[i,'CONCEPTO / SUBCONC.'])
	importe.append(ingresos_organico.loc[i,'IMPORTE'])
	total_importe.append(ingresos_organico.loc[i,'TOTAL ORGÁNICA'])	

print(len(cod_seccion), len(des_seccion), len(cod_servicio), len(des_servicio), len(afectado), len(subconcepto), len(importe), len(total_importe))
print
print(des_seccion[11], '\n', des_servicio[11])

'''
Unnamed: 0
Unnamed: 1
Unnamed: 2
Unnamed: 3
Unnamed: 4
Unnamed: 5
'''

concepto_row = list()
for i in subconcepto:
	try:
		#Solo concepto
		if '.' not in i:
			#print(i)
			des_subconcepto.append('None')
			cod_subconcepto.append('None')

			concepto = str(ingresos_subconcepto.loc[ingresos_subconcepto['Unnamed: 0'] == i, 'Unnamed: 1'])
			des_concepto.append(re.search(r'(\d*)(\s*)(.*)', concepto)[3])
			cod_concepto.append(i)

			articulo = str(ingresos_subconcepto.loc[ingresos_subconcepto['Unnamed: 0'] == i[:-1], 'Unnamed: 1'])
			des_articulo.append(re.search(r'(\d*)(\s*)(.*)', articulo)[3])
			cod_articulo.append(i[:-1])

			capitulo = f'Capítulo {i[:-2]}'
			for j in range(0, len(ingresos_subconcepto)):
				cap = str(ingresos_subconcepto.loc[j, 'Unnamed: 0'])
				if capitulo in cap:
					des_capitulo.append(cap)
					cod_capitulo.append(i[:-2])

			credito_inicial.append(re.search(r'(\d*)(\s*)(.*)', str(ingresos_subconcepto.loc[ingresos_subconcepto['Unnamed: 0'] == i, 'Unnamed: 3']))[3])

		if '.' in i:
			concepto = str(ingresos_subconcepto.loc[ingresos_subconcepto['Unnamed: 0'] == i[:3], 'Unnamed: 1'])
			des_concepto.append(re.search(r'(\d*)(\s*)(.*)', concepto)[3])
			cod_concepto.append(i[:3])

			articulo = str(ingresos_subconcepto.loc[ingresos_subconcepto['Unnamed: 0'] == i[:2], 'Unnamed: 1'])
			des_articulo.append(re.search(r'(\d*)(\s*)(.*)', articulo)[3])
			cod_articulo.append(i[:2])

			capitulo = f'Capítulo {i[:1]}'
			for j in range(0, len(ingresos_subconcepto)):
				cap = str(ingresos_subconcepto.loc[j, 'Unnamed: 0'])
				if capitulo in cap:
					des_capitulo.append(cap)
					cod_capitulo.append(i[:1])

			#Row number
			row_concepto = str(ingresos_subconcepto.loc[ingresos_subconcepto['Unnamed: 0'] == i[:3], 'Unnamed: 0'].index[0])
			#print('		-----',row_concepto, i[:3])
			#SUBCONCEPTO
			for r in range(int(row_concepto)+1, int(row_concepto)+20):
				try:
					row_subconcepto = str(ingresos_subconcepto.loc[r, 'Unnamed: 0']) #valor fila de la 1º columna
					if row_subconcepto[0] != '.':
						if row_subconcepto == 'nan':
							des_subconcepto.append('None')
							cod_subconcepto.append('None')
							credito_inicial.append('None')
						print(i, row_subconcepto, r, ingresos_subconcepto.loc[r, 'Unnamed: 1'], row_concepto)
						break
					if row_subconcepto[0] == '.':
						if str(i[3:]) == row_subconcepto:
							des_subconcepto.append(str(ingresos_subconcepto.loc[r, 'Unnamed: 1']))
							cod_subconcepto.append(i)
							credito_inicial.append(str(ingresos_subconcepto.loc[r, 'Unnamed: 2']))
							break
						
				except: 
					print('Fallo 1')
					pass
					
	except TypeError:
		print('Fallo', i)
		pass




print(len(cod_capitulo), len(des_capitulo), len(cod_concepto), len(des_concepto), len(cod_subconcepto), len(des_subconcepto), len(credito_inicial),
	len(cod_articulo), len(des_articulo))



#Arreglos de Formato
for sec in range(len(cod_seccion)):
	if cod_seccion[sec] == 'None':
		pass
	else:
		cod_seccion[sec] = 'UPM-' + cod_seccion[sec]

for serv in range(len(cod_servicio)):
	if cod_servicio[serv] == 'None':
		pass
	else:
		cod_servicio[serv] = 'UPM-' + cod_servicio[serv]

for cap in range(len(cod_capitulo)):
	if cod_capitulo[cap] == 'None':
		pass
	else:
		cod_capitulo[cap] = 'UPM-' + cod_capitulo[cap]

for art in range(len(cod_articulo)):
	if cod_articulo[art] == 'None':
		pass
	else:
		cod_articulo[art] = 'UPM-' + cod_articulo[art]

for conc in range(len(cod_concepto)):
	if cod_concepto[conc] == 'None':
		pass
	else:
		cod_concepto[conc] = 'UPM-' + cod_concepto[conc]

for subconc in range(len(cod_subconcepto)):
	if cod_subconcepto[subconc] == 'None':
		pass
	else:
		cod_subconcepto[subconc] = 'UPM-' + cod_subconcepto[subconc]


for ini in range(len(credito_inicial)):
	credito_inicial[ini] = credito_inicial[ini].replace('.', '')
	if credito_inicial[ini] == 'nan' or credito_inicial[ini] == 'NaN':
		credito_inicial[ini] = '0'





#INGRESOS DATASET
cod_universidad = ['UPM'] * len(cod_capitulo)
des_universidad = ['Universidad Politecnica de Madrid'] * len(cod_capitulo)
anio = ['2021'] * len(cod_capitulo)
cod_capitulo = cod_capitulo
des_capitulo = des_capitulo
cod_articulo = cod_articulo
des_articulo = des_articulo
cod_concepto = cod_concepto
des_concepto = des_concepto
cod_subconcepto = cod_subconcepto
des_subconcepto = des_subconcepto
cod_partida = ['None']  * len(cod_capitulo)
des_partida = ['None']  * len(cod_capitulo)
cod_seccion = cod_seccion
des_seccion = des_seccion
cod_servicio = cod_servicio
des_servicio = des_servicio
cod_unidad_de_coste = ['None']  * len(cod_capitulo)
des_unidad_de_coste = ['None']  * len(cod_capitulo)
cod_organica_libre_1 = ['None']  * len(cod_capitulo)
des_organica_libre_1 = ['None']  * len(cod_capitulo)
cod_organica_libre_2 = ['None']  * len(cod_capitulo)
des_organica_libre_2 = ['None']  * len(cod_capitulo)
fecha_referencia = ['20210620'] * len(cod_capitulo)
credito_inicial = importe
modificaciones = ['None'] * len(cod_capitulo)
credito_total = ['None'] * len(cod_capitulo)
derechos_reconocidos_netos = ['None'] * len(cod_capitulo)
recaudacion_neta = ['None'] * len(cod_capitulo)

#print(len(cod_universidad), len(anio), len(cod_articulo), len(cod_subconcepto), len(cod_concepto), len(cod_partida), len(cod_unidad_de_coste), len(credito_inicial))

data = {'codigo_universidad':cod_universidad,
		'nombre_universidad':des_universidad,
		'anio':anio,
		'cod_capitulo':cod_capitulo,
		'des_capitulo':des_capitulo,
		'cod_articulo':cod_articulo,
		'des_articulo':des_articulo,
		'cod_concepto':cod_concepto,
		'des_concepto':des_concepto,
		'cod_subconcepto':cod_subconcepto,
		'des_subconcepto':des_subconcepto,
		'cod_partida':cod_partida,
		'des_partida':des_partida,
		'cod_seccion':cod_seccion,
		'des_seccion':des_seccion,
		'cod_servicio':cod_servicio,
		'des_servicio':des_servicio,
		'cod_unidad_de_coste':cod_unidad_de_coste,
		'des_unidad_de_coste':des_unidad_de_coste,
		'cod_organica_libre_1':cod_organica_libre_1,
		'des_organica_libre_1':des_organica_libre_1,
		'cod_organica_libre_2':cod_organica_libre_2,
		'des_organica_libre_2':des_organica_libre_2,
		'fecha_referencia':fecha_referencia,
		'credito_inicial':credito_inicial,
		'modificaciones':modificaciones,
		'credito_total':credito_total,
		'derechos_reconocidos_netos':derechos_reconocidos_netos,
		'recaudacion_neta':recaudacion_neta	
}

ingresos_df = DataFrame(data)
ingresos_df.to_csv('UPM-ingresos.csv')
