#!/usr/bin/env python
# -*- coding: utf-8 -*-
# license removed for brevity
"""
Created on Tue Jul  23 10:28:23 2019

@author: Jaime Duque Domingo UVA

Reproducción de un badge para visualizar las gráficas

"""
import rospy
import sys
import numpy as np
import math
from time import sleep
from time import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from time import time
from seguimiento.msg import salidaRedCompetitiva

# Salida de Red Competitiva
sRedCompetitiva = salidaRedCompetitiva()
 
params = {'legend.fontsize': '30',
       	'figure.figsize': (15, 5),
        'axes.labelsize': '35',
       	'axes.titlesize':'35',
       	'xtick.labelsize':'25',
        'ytick.labelsize':'25'}

pylab.rcParams.update(params)

columnas = [["Tiempo", "Person 1", "Person 2", "Person 3"]]
vector = np.array(columnas)    
valores_neuronas = np.zeros(3 + 1)
    
plt.ion()
# Creamos ventana
fig, ax = plt.subplots(figsize=(15, 10))
ax.legend(prop=dict(size=30))
    
plt.xlabel('Time (s)')
plt.ylabel('Stimulus')

# Dibujamos el dataframe actual
plt.show()
start_time = time()

semaforo = False

tiempo_inicio = -1

inicio = time()

def callbackRecCompetitiva(srRedCompetitiva):
    global semaforo
    global sRedCompetitiva
    sRedCompetitiva = srRedCompetitiva
    semaforo = True

# Máximo de caras del histórico
MAXIMO_PERSONAS = rospy.get_param("MAXIMO_PERSONAS", 10)

# Creamos el subscriptor al topic de salida de la red competitiva
#sRCompetitiva_sub = rospy.Subscriber("salidaRedCompetitiva",salidaRedCompetitiva,callbackRecCompetitiva)
sRCompetitiva_sub = rospy.Subscriber("entradaRedCompetitiva",salidaRedCompetitiva,callbackRecCompetitiva)

t = 0
p = 1

rospy.init_node('reproductorBadge', anonymous=True)
try:
	while not rospy.core.is_shutdown():
		rospy.rostime.wallsleep(0.1)

		#if t > 64 or time() - inicio > 20:
		if time() - inicio > 20:
			# Fin del proceso
			# Creamos dataframe y limpiamos ejes del anterior
			dframe = pd.DataFrame(data=vector[1:,1:], index=vector[1:,0], columns=vector[0,1:])
			dframe=dframe.astype(float)                
			plt.cla()
			plt.xlabel('Time (s)')
			plt.ylabel('Stimulus')    
			# Dibujamos el dataframe actual
			#ax.get_legend().set_bbox_to_anchor((.8532,.3))
			dframe.plot(ax=ax, linewidth=4)
			#plt.legend(loc='upper right', bbox_to_anchor=(1.0, 0.5))
			fig.savefig('test.png', dpi=300)
			plt.pause(20)
			rospy.signal_shutdown("Fin")

                if semaforo == True:
			inicio = time()
			if tiempo_inicio == -1:
				tiempo_inicio = sRedCompetitiva.header.stamp.to_sec()
			t = sRedCompetitiva.header.stamp.to_sec() - tiempo_inicio
			vector = np.r_[vector,[[int(t), sRedCompetitiva.data[0], sRedCompetitiva.data[1], sRedCompetitiva.data[2]]]]

			p = p + 1
			if p > 100:
				p = 1
				dframe = pd.DataFrame(data=vector[1:,1:], index=vector[1:,0], columns=vector[0,1:])
				dframe=dframe.astype(float)                
				plt.cla()
				# Dibujamos el dataframe actual
				dframe.plot(ax=ax, linewidth=4)
				plt.xlabel('Time (s)')
				plt.ylabel('Stimulus')
				plt.pause(0.02)
			semaforo = False

except KeyboardInterrupt:
	print("Shutting down")


