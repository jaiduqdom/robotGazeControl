#!/usr/bin/env python
# -*- coding: utf-8 -*-
# license removed for brevity
import rospy
import numpy as np
import sys
from seguimiento.msg import entradaRedCompetitiva
from seguimiento.msg import salidaRedCompetitiva

class redCompetitiva:

  #***************************************************************************************
  # Inicialización de objeto definiendo las variables globales de la instancia del objeto
  #***************************************************************************************
  def __init__(self):

    # Parametro de neuronas de la red
    # Contamos con dos personas ficticias por si aparece alguien en un lateral 
    self.NEURONAS = rospy.get_param("MAXIMO_PERSONAS", 10) + 2

    # Vector de estimulos de entrada
    self.I = np.zeros(self.NEURONAS)

    # Parametro de frecuencia (diferenciacion)
    self.FRECUENCIA = 10

    # Vectores de estado de la capa de habituación
    self.y = np.zeros(self.NEURONAS)
    self.gt = np.zeros(self.NEURONAS)
    self.gt_ant = np.zeros(self.NEURONAS)
    self.y_ant = np.zeros(self.NEURONAS)

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
    A = rospy.get_param("RED_COMPETITIVA_A", 0.6)
    B = rospy.get_param("RED_COMPETITIVA_B", 1)
    C = rospy.get_param("RED_COMPETITIVA_C", 1)
    D = rospy.get_param("RED_COMPETITIVA_D", 15)
    n = self.NEURONAS
    h = 1.0 / self.FRECUENCIA

    # Vectores de estado anterior de la red competitiva
    x = np.zeros(self.NEURONAS)
    ft = np.zeros(self.NEURONAS)
    ft_ant = np.zeros(self.NEURONAS)
    x_ant = np.zeros(self.NEURONAS)

    # Definimos los publicadores
    pub_Competitiva = rospy.Publisher('salidaRedCompetitiva', salidaRedCompetitiva, queue_size=1)
    pub_STM = rospy.Publisher('salidaCapaSTM', salidaRedCompetitiva, queue_size=1)
    pub_Habituacion = rospy.Publisher('salidaCapaHabituacion', salidaRedCompetitiva, queue_size=1)

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

        rospy.loginfo(rospy.get_caller_id() + "Estimulos de STM =  %s", stm.data)

    	# Procesamos capa Habituación
	self.I = self.capaHabituacion(self.I)
	# Publicamos su resultado
	habituacion.header.stamp = rospy.Time.now()
	habituacion.data = self.I
	pub_Habituacion.publish(habituacion)

        rospy.loginfo(rospy.get_caller_id() + "Estimulos de habituación =  %s", habituacion.data)

	# Algoritmo de red competitiva    
	ft_ant = ft
	x_ant = x    

	"""print ("I : ", self.I)
	print ("ft : ", ft)
	print ("x : ", x)"""

	for k in range(0, n):
	   suma = 0
	   for l in range(0, n):
	      if k != l:
		 # mas rapida que lineal
		 suma = suma + D * x_ant[l]**2
		 # lineal: suma = suma + x[l]

	   #print ("suma : ", suma)
	
	   # más rápida que lineal
	   ft[k] = -A*x[k] + C*(B-x[k])*(self.I[k]) - x[k]*suma
	   # lineal: ft[k] = -A*x[k] + C*(B-x[k])*(I[k]+D * x[k]**2)-x[k]*suma
	
	   x[k] = x_ant[k] + (ft[k] + ft_ant[k]) * h / 2

	   # Ponemos unos límites al algoritmo para evitar que se pueda producir un desbordamiento
	   if x[k] > 100 or ft[k] > 100 or x[k] < -100 or ft[k] < -100:
	   	x[k] = 0
		ft[k] = 0

	"""print ("Nuevo ft : ", ft)
	print ("Nuevo  : ", x)
	print ("A : ", A)
	print ("B  : ", B)
	print ("C  : ", C)"""

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
    E = rospy.get_param("CAPA_HABITUACION_E", 0.5)
    F = rospy.get_param("CAPA_HABITUACION_F", 0.05)
    #E = 0.8
    #F = 0.8
    # número de neuronas
    n = self.NEURONAS
    h = 1.0 / self.FRECUENCIA

    Out = np.zeros(n)    
    
    # Algoritmo de red de habituación    
    self.gt_ant = self.gt
    self.y_ant = self.y

    T = np.zeros(n)
    for k in range(0, n):
        self.gt[k] = E * (1-self.y[k])-F*I[k]*self.y[k]
        self.y[k] = self.y_ant[k] + (self.gt[k]+self.gt_ant[k])*h/2
        T[k] = self.y[k] * I[k]
        Out[k] = T[k]

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
    A = rospy.get_param("CAPA_STM_A", 0.6)
    B = rospy.get_param("CAPA_STM_B", 5)
    C = rospy.get_param("CAPA_STM_C", 1)

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

