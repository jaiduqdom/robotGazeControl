#!/usr/bin/env python
# -*- coding: utf-8 -*-
# license removed for brevity
import rospy
import numpy as np
import sys
import math
from seguimiento.msg import entradaRedCompetitiva
from seguimiento.msg import salidaRedCompetitiva

class redCompetitiva:

  #***************************************************************************************
  # Inicialización de objeto definiendo las variables globales de la instancia del objeto
  #***************************************************************************************
  def __init__(self):

    # Parametro de neuronas de la red
    self.NEURONAS = rospy.get_param("MAXIMO_PERSONAS")

    # Vector de estimulos de entrada
    self.I = np.zeros(self.NEURONAS)

    # Parametro de frecuencia (diferenciacion)
    self.FRECUENCIA = 10

    # Vectores de estado de la capa de habituación
    self.ti = np.zeros(self.NEURONAS)
    self.I_old = np.zeros(self.NEURONAS)
    # self.y = np.zeros(self.NEURONAS)
    # self.gt = np.zeros(self.NEURONAS)
    # self.gt_ant = np.zeros(self.NEURONAS)
    # self.y_ant = np.zeros(self.NEURONAS)

    # Vectores de estado de la capa STM
    self.z = np.zeros(self.NEURONAS)
    self.zt = np.zeros(self.NEURONAS)
    self.zt_ant = np.zeros(self.NEURONAS)
    self.z_ant = np.zeros(self.NEURONAS)

    # El nodo se subscribe a la entrada de la red competitiva
    rospy.Subscriber("entradaRedCompetitiva", entradaRedCompetitiva, self.callback)

  def callback(self, data):
    self.I = data.data
    rospy.loginfo(rospy.get_caller_id() + "Estimulos de entrada =  %s", data.data)


  # La red competitiva recibe los estímulos a partir de la función de callback
  # Se procesa a mayores la capa de habituación/STM
  def redCompetitiva(self):

    # Parametros utilizados en la red competitiva
    A = rospy.get_param("RED_COMPETITIVA_A")
    B = rospy.get_param("RED_COMPETITIVA_B")
    C = rospy.get_param("RED_COMPETITIVA_C")
    D = rospy.get_param("RED_COMPETITIVA_D")
    n = self.NEURONAS
    h = 1.0 / self.FRECUENCIA

    # Vectores de estado anterior de la red competitiva
    x = np.zeros(self.NEURONAS)
    ft = np.zeros(self.NEURONAS)
    ft_ant = np.zeros(self.NEURONAS)
    x_ant = np.zeros(self.NEURONAS)

    # Definimos los publicadores
    pub_Competitiva = rospy.Publisher('salidaRedCompetitiva', salidaRedCompetitiva, queue_size=10)
    pub_STM = rospy.Publisher('salidaCapaSTM', salidaRedCompetitiva, queue_size=10)
    pub_Habituacion = rospy.Publisher('salidaCapaHabituacion', salidaRedCompetitiva, queue_size=10)

    # Frecuencia de procesamiento
    rate = rospy.Rate(self.FRECUENCIA)

    salida = salidaRedCompetitiva()
    # Creamos dos mensajes de salida con las capas STM y de habituación para poder visualizar
    # con ROS los resultados de las entradas y pasos intermedios
    stm = salidaRedCompetitiva()
    habituacion = salidaRedCompetitiva() 

    while not rospy.is_shutdown():

    	# Procesamos capa STM
	self.I = self.capaSTM(self.I)
	# Publicamos su resultado
	stm.header.stamp = rospy.Time.now()
	stm.data = self.I
	pub_STM.publish(stm)

    	# Procesamos capa Habituación
	self.I = self.capaHabituacion(self.I)
	# Publicamos su resultado
	habituacion.header.stamp = rospy.Time.now()
	habituacion.data = self.I
	pub_Habituacion.publish(habituacion)

	# Algoritmo de red competitiva    
	ft_ant = ft
	x_ant = x    

	for k in range(0, n):
	   suma = 0
	   for l in range(0, n):
	      if k != l:
		 # mas rapida que lineal
		 suma = suma + D * x[l]**2
		 # lineal: suma = suma + x[l]
	
	   # mas rapida que lineal
	   ft[k] = -A*x[k] + C*(B-x[k])*(self.I[k])-x[k]*suma
	   # lineal: ft[k] = -A*x[k] + C*(B-x[k])*(I[k]+D * x[k]**2)-x[k]*suma
	
	   x[k] = x_ant[k] + (ft[k] + ft_ant[k]) * h / 2

	# Anadir time stamp
	salida.header.stamp = rospy.Time.now()
	# Datos de salida
	salida.data = x
	# Publicamos y escribimos la salida
	rospy.loginfo(rospy.get_caller_id() + "Estimulos de salida =  %s", salida.data)
	pub_Competitiva.publish(salida)
	rate.sleep()

  # Implementación de la capa de habituación
  # Como entrada:
  #   La entrada de la capa de habituación es el conjunto de outputs producidos en la capa STM junto
  #   con un instante de tiempo utilizado para llevar un contador temporal.
  # Como salida se obtiene el conjunto de estímulos tratados válidos para la red competitiva

  # Importante: Los índices de persona empiezan en 0: persona_hablando[0] es la primera persona
  #             De la misma manera, la salida devuelve el índice de la persona ganadora comenzando en 0.
  def capaHabituacion(self,I):
    
    # Parámetros utilizados en la red habituación
    M = rospy.get_param("CAPA_HABITUACION_M")
    L = rospy.get_param("CAPA_HABITUACION_L")
    
    # número de neuronas
    n = self.NEURONAS
    h = 1.0 / self.FRECUENCIA
    Out = np.zeros(n)    

    # Algoritmo de red de habituación    
    for k in range(0, n):
        self.ti[k] = self.ti[k] + h
        angulo = (1/2) * math.pi + self.ti[k] * math.pi / L
        if angulo > ((3/2) * math.pi):
            valor = -1  # valor mínimo gráficamente
        else:
            valor = math.sin(angulo)
        if I[k] == self.I_old[k]:
            valor_estimulo_maximo = I[k]
            valor_estimulo_minimo = M * I[k]
            # en la función seno los valores van de -1 a 1 (2)
            Out[k] =  valor_estimulo_minimo + (valor + 1) * (valor_estimulo_maximo - valor_estimulo_minimo) / 2
        else:
            self.ti[k] = 0
            Out[k] = I[k]
        self.I_old[k] = I[k]           
    return Out

  # Implementación de la capa de STM
  # Como entrada:
  #   La entrada de la capa de STM es el conjunto de inputs de entrada junto
  #   con un instante de tiempo utilizado para llevar un contador temporal.
  # Como salida se obtiene el conjunto de estímulos tratados válidos para la capa de habituación

  # Importante: Los índices de persona empiezan en 0: persona_hablando[0] es la primera persona
  #             De la misma manera, la salida devuelve el índice de la persona ganadora comenzando en 0.
  def capaSTM(self,I):
   
    # Parámetros utilizados en la capa STM
    # El factor de decaimiento es muy bajo para permitir prolongar la duración de un estímulo
    A = rospy.get_param("CAPA_STM_A")
    B = rospy.get_param("CAPA_STM_B")
    C = rospy.get_param("CAPA_STM_C")

    # número de neuronas    
    n = self.NEURONAS
    h = 1.0 / self.FRECUENCIA

    # Creamos la fila de valores para la matriz de visualización que se usa con el dataframe
    Out = np.zeros(n)
    
    # Algoritmo de red competitiva    
    self.zt_ant = self.zt
    self.z_ant = self.z    

    for k in range(0, n):
        # más rápida que lineal
        self.zt[k] = -A*self.z[k] + C*(B-self.z[k])*(I[k])
        # lineal: ft[k] = -A*x[k] + C*(B-x[k])*(I[k]+D * x[k]**2)
        
        self.z[k] = self.z_ant[k] + (self.zt[k] + self.zt_ant[k]) * h / 2
        
        Out[k] = self.z[k]

    return Out

def main(args):
  # Iniciar nodo
  rospy.init_node('redCompetitiva', anonymous=True)
  ic = redCompetitiva()
  ic.redCompetitiva()

if __name__ == '__main__':
    main(sys.argv)

