#!/usr/bin/env python
# -*- coding: utf-8 -*-
# license removed for brevity
"""
Created on Tue Jul  23 10:28:23 2019

@author: Jaime Duque Domingo UVA

Investigación sobre la orientación de cabeza robótica
Orientación de la cabeza robótica

Este nodo realiza una implementación del filtro de Kalman para devolver una posición de la persona
a partir de los datos obtenidos anteriormente y considerando un cierto ruido

Se suscribe al topic:
	entradaKalman, donde hay varios identificadores, uno por filtro y persona asociado

Publica los topic:
	salidaKalman

"""
import rospy
import numpy as np
import sys
#from random import random
from time import time
from seguimiento.msg import entradaKalman
from seguimiento.msg import salidaKalman

class filtroKalman:

  #***************************************************************************************
  # Inicialización de objeto definiendo las variables globales de la instancia del objeto
  #***************************************************************************************
  def __init__(self):

    # Creamos el subscriptor al topic entradaKalman
    self.sub = rospy.Subscriber("entradaKalman",entradaKalman,self.callback)

    # Creamos el publicador al topic salidaKalman
    self.pub = rospy.Publisher("salidaKalman", salidaKalman, queue_size=1)

    # Identificadores de los distintos filtros (por defecto igual al número máximo de personas)
    # Añadimos dos personas ficticias para los laterales del robot
    self.MAXIMO_FILTROS = rospy.get_param("MAXIMO_PERSONAS", 10) + 2
    self.identificador = np.zeros(self.MAXIMO_FILTROS)
    # Iniciamos a -2 la tabla de identificadores ya que -1 es utilizado en procesoEstimulos y
    # 0 corresponde a una persona identificada por 0
    for f in range(0, self.MAXIMO_FILTROS):
	self.identificador[f] = -2

    # Tiempo de vida de un filtro si no ha estado activo (30 segundos)
    self.MAXIMO_TIEMPO_VIDA = 30
    self.tiempo_vida = []
    for i in range(0, self.MAXIMO_FILTROS):
	self.tiempo_vida.append(time())

    # Paso de tiempo
    self.T = 0.1

    # Desviación error
    self.desv_xy = rospy.get_param("KALMAN_DESV_XY", 0.5)

    # Almacenamos los distintos filtros de Kalman
    # self.Xk = np.arange(self.MAXIMO_FILTROS)
    # self.Xkreal = np.arange(self.MAXIMO_FILTROS)
    # self.Pk = np.arange(self.MAXIMO_FILTROS)

    # Iniciamos los arrays con una matriz aleatoria para que los considere matrices
    self.Xk = []
    self.Xkreal = []
    self.Pk = []

    for i in range(0, self.MAXIMO_FILTROS):
    	self.Xk.append(np.matrix([[0, 0], [0, 0]]))
    	self.Xkreal.append(np.matrix([[0, 0], [0, 0]]))
    	self.Pk.append(np.matrix([[0, 0], [0, 0]]))

  #**************************************************
  # Función de proceso de movimiento de una cara
  # estado Xk=[x,y]
  # T periodo de muestreo
  #**************************************************
  def proceso(self, Xk_ant):
    return Xk_ant

  #**************************************************
  # Función de propagación
  #**************************************************
  def propaga(self, Xk, Pk, T):
    A=np.matrix([[1,0],[0,1]])
    Pk = A*Pk*np.transpose(A)
    # Este problema lo he detectado en la versión de matlab
    #return np.transpose(Xk), Pk
    return Xk, Pk
 
  #**************************************************
  # Función de actualización
  #**************************************************
  def actualiza(self, Xk,Pk,Hk,Zk,Zek,R,V):
    I=np.matrix([[1, 0],[0, 1]])
    K=Pk*np.transpose(Hk)*np.linalg.inv(Hk*Pk*np.transpose(Hk)+V*R*np.transpose(V))
    Xk=Xk+K*(Zk-Zek)
    Pk=(I-K*Hk)*Pk
    return Xk, Pk

  #**************************************************
  # Implementamos el filtro de Kalman
  #**************************************************
  def inicioFiltroKalman(self, identificador, x, y):

    # Creamos un filtro nuevo con un estado inicial
    self.Xk[identificador] = np.transpose(np.matrix([x, y]))
    self.Xkreal[identificador] = self.Xk[identificador]
    self.Pk[identificador] = np.matrix([[1, 0], [0, 1]])
    # Iniciamos su tiempo de vida
    self.tiempo_vida[identificador] = time()

  def procesoFiltroKalman(self, identificador, x, y, nuevaMedida):

    # Procesamos nuevos valores recibidos
    Hk = np.matrix([[0.1, 0], [0, 0.1]])
    V = np.matrix([[1, 0], [0, 1]])
    R = np.matrix([[self.desv_xy**2, 0],[0, self.desv_xy**2]])
 
    self.Xkreal[identificador] = np.transpose(self.proceso(self.Xkreal[identificador]))
        
    Xk_ant,Pk_ant = self.propaga(self.Xk[identificador],self.Pk[identificador],self.T)

    if (nuevaMedida == True):
        # Llega medida
        # Observaciones reales van a Xkreal y Zk
        self.Xkreal[identificador] = np.transpose(np.matrix([x, y]))

        # Zk = Xkreal + np.array([[random() * 10], [random() * 10]])
        Zk = self.Xkreal[identificador]

        # Observaciones estimadas
        Zek=Xk_ant   

        self.Xk[identificador],self.Pk[identificador] = self.actualiza(Xk_ant,Pk_ant,Hk,Zk,Zek,R,V)
    else:
        self.Xk[identificador]=Xk_ant 
        self.Pk[identificador]=Pk_ant

  #*************************************************************************
  # Implementamos función de callback ante llegada mensaje entradaKalman
  #*************************************************************************
  def callback(self, entradaKalman):

    # Procesamos cada filtro creado
    for f in range(0, self.MAXIMO_FILTROS):
	# Iniciamos filtros con un tiempo de vida superior al máximo
	# Esto nos vale para evitar que el filtro se tienda a saturar en torno a un punto 
	# y para eliminar filtros de personas que no se han detectado por más de dicho tiempo máximo
	if time() - self.tiempo_vida[f] > self.MAXIMO_TIEMPO_VIDA:
		self.identificador[f] = -2
		self.tiempo_vida[f] = time()

	# Miramos si está en la entrada
	recibidaMedida = False
    	for e in range(0, len(entradaKalman.identificador)):
		#if entradaKalman.identificador[e] == self.identificador[f]:
		if entradaKalman.identificador[e] == f:
			recibidaMedida = True
			indice = e
			break
        # Por evitar complicar el algoritmo, consideramos que el número de identificador
        # que se envía coincide con el identificador de filtro. Hay tantos filtros como
        # personas se están siguiendo
	if recibidaMedida == True:
		# Si existe filtro y no ha estado inutilizado en más de 100 iteraciones,
                # inyectamos nueva medida
		if self.identificador[f] != -2:
			self.procesoFiltroKalman(f, entradaKalman.pan[indice], entradaKalman.tilt[indice], True)
		# Si no existe filtro, creamos uno nuevo en la misma posición
		else:
			self.identificador[f] = entradaKalman.identificador[indice]
			self.inicioFiltroKalman(f, entradaKalman.pan[indice], entradaKalman.tilt[indice])
	else:
		# Si existe filtro, procesamos filtro sin nueva medida
		if self.identificador[f] != -2:
			self.procesoFiltroKalman(f, 0, 0, False)
			"""# Cuando llega a su tiempo de vida máximo sin ser utilizado, se destruye
			if time() - self.tiempo_vida[f] > self.MAXIMO_TIEMPO_VIDA:
				self.identificador[f] = -2
				self.tiempo_vida[f] = time()"""

    # Publicamos la salida del filtro
    sKalman = salidaKalman()
    sKalman.header.stamp = rospy.Time.now()
    sKalman.identificador = np.zeros(self.MAXIMO_FILTROS)
    sKalman.pan = np.zeros(self.MAXIMO_FILTROS)
    sKalman.tilt = np.zeros(self.MAXIMO_FILTROS)
    for f in range(0, self.MAXIMO_FILTROS):
	sKalman.identificador[f] = self.identificador[f]
	if self.identificador[f] != -2:
		# rospy.loginfo(self.Xk[f])
		sKalman.pan[f] = self.Xk[f][0].item()
		sKalman.tilt[f] = self.Xk[f][1].item()
	else:
		sKalman.pan[f] = 0
		sKalman.tilt[f] = 0

    rospy.loginfo("Entrada Filtro Kalman (PAN) Personas 0, 1 y 2: %f %f %f", entradaKalman.pan[0], entradaKalman.pan[1], entradaKalman.pan[2])
    rospy.loginfo("Entrada Filtro Kalman (TIL) Personas 0, 1 y 2: %f %f %f", entradaKalman.tilt[0], entradaKalman.tilt[1], entradaKalman.tilt[2])

    """rospy.loginfo("Entrada Filtro Kalman:")
    rospy.loginfo(entradaKalman.pan)
    rospy.loginfo(entradaKalman.tilt)

    rospy.loginfo("Salida Filtro Kalman:")
    rospy.loginfo(sKalman.pan)
    rospy.loginfo(sKalman.tilt)"""
    self.pub.publish(sKalman)

def main(args):
  ic = filtroKalman()
  rospy.init_node('filtroKalman', anonymous=True)
  try:
	rospy.spin()
  except KeyboardInterrupt:
	print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)
