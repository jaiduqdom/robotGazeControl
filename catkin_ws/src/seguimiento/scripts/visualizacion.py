#!/usr/bin/env python
# -*- coding: utf-8 -*-
# license removed for brevity
"""
Created on Tue Jul  23 10:28:23 2019

@author: Jaime Duque Domingo UVA

Investigación sobre la orientación de cabeza robótica
Orientación de la cabeza robótica

Nodo de visualización de la cámara con las caras y resultados

Se suscribe a los topic:
        imagenComprimida, con la imagen JPEG
	puntosCara, para tratar los puntos extraídos con DLIB
	ganador, para obtener el ganador según la red competitiva

"""
import rospy
import sys
import cv2
import numpy as np
import math
from time import time
#from sensor_msgs.msg import Image
#from cv_bridge import CvBridge, CvBridgeError
from seguimiento.msg import puntosCaras
from seguimiento.msg import ganador
from sensor_msgs.msg import CompressedImage
from calculoAngulos import calculoAngulos

class visualizacion:

  # Inicialización de objeto definiendo las variables globales de la instancia del objeto
  def __init__(self):
    #####################################################################################
    # Objetos recibidos mediante funciones de callback
    # PuntosCaras
    self.pCaras = puntosCaras()
    # ImagenComprimida
    self.iComp = CompressedImage()
    # Ganador
    self.seleccionado = ganador()
    self.seleccionado.ganador = -1
    # Tiempo en el que mantenemos a un ganador
    self.tiempo_inicio = 0

    # Semáforo de indicación de si los objetos han sido tratados
    self.tratado_pCaras = True
    self.tratado_iComp = True
    #####################################################################################

    # Creamos un objeto de tipo bridge para transferir imágenes OpenCV por ROS
    # self.bridge = CvBridge()

    # Creamos el subscriptor al topic de puntos de la cara
    self.pCaras_sub = rospy.Subscriber("puntosCaras",puntosCaras,self.callbackCaras)

    # Creamos el subscriptor al topic de imágenes comprimidas
    self.iComp_sub = rospy.Subscriber("imagenTratada",CompressedImage,self.callbackImagen, queue_size = 1, buff_size = 2**24)

    # Creamos el subscriptor al topic de ganador
    self.ganador_sub = rospy.Subscriber("ganador",ganador,self.callbackGanador)

    # Constante de número de puntos devueltos por DLIB
    self.PUNTOS_DLIB = 68

    # Máximo de caras del histórico
    self.MAXIMO_CARAS = rospy.get_param("MAXIMO_PERSONAS", 10)

    # Objeto de cálculo de ángulos
    # Nos permite calcular el ángulo de una cara a partir del ángulo actual del robot y de las
    # coordenadas de la cara
    self.cA = calculoAngulos()

  #########################################################################################
  # Función de procesamiento de los estímulos a partir de los mensajes de entrada
  #########################################################################################
  def visualizacion(self, caras, iComp, seleccionado):

    # Primero leemos la imagen del topic imagen_topic
    np_arr = np.fromstring(iComp.data, np.uint8)
    dlib_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    #try:
    #	dlib_image = self.bridge.imgmsg_to_cv2(caras.imagen, "mono8")
    #except CvBridgeError as e:
    #	print(e)

    # Transformamos a color para añadir caras y puntos
    # color_imagen = cv2.cvtColor(dlib_image, cv2.COLOR_GRAY2BGR)
    color_imagen = dlib_image

    # Matriz bidimensional para los landmarks de la cara
    lX = np.zeros((caras.numeroCaras, self.PUNTOS_DLIB)).astype(int)
    lY = np.zeros((caras.numeroCaras, self.PUNTOS_DLIB)).astype(int)

    # Para cada cara añadimos el recuadro en verde y puntos en rojo
    for i in range(0, caras.numeroCaras):
	# Añadir recuadro verde
	cv2.rectangle(color_imagen, (caras.x1[i], caras.y1[i]), 
		(caras.x2[i], caras.y2[i]), (0, 255, 0), 2)
	# Añadir puntos en rojo
	for j in range(0, self.PUNTOS_DLIB):
		# Primero pasamos array a matriz bidimensional
		lX[i][j] = caras.puntoX[i * self.PUNTOS_DLIB + j]
		lY[i][j] = caras.puntoY[i * self.PUNTOS_DLIB + j]
		# Ahora pintamos los puntos
		cv2.circle(color_imagen, (lX[i][j], lY[i][j]), 1, (0, 0, 255), -1)

	# Obtenemos el índice de la cara para visualizarlo
	indiceCara = caras.indiceCara[i]
	cv2.putText(color_imagen, "Person {}".format(indiceCara), (caras.x1[i], caras.y2[i] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2) 

    # Si existe un ganador, lo escribimos y lo mostramos resaltado (si se puede)
    # El filtro de Kalman está devolviendo la posición del medio de la cara, por lo que miraremos
    # si se encuentra entre el vértice superior izquierdo y el inferior derecho de alguna cara
    # Indicamos la persona ganadora en la imagen
    if self.seleccionado.ganador != -1:
            # Calculamos la posición (x,y) del ángulo ganador a partir de los ángulos de la cabeza robótica y de los ángulos del ganador
            x, y = self.cA.calcularCoordenadas(seleccionado.pan, seleccionado.tilt)

            # Mostramos círculo en torno al resultado de Kalman
	    cv2.putText(color_imagen, "Winner {}".format(seleccionado.ganador), (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2) 
            # Mostramos círculo en torno al resultado de Kalman
	    cv2.circle(color_imagen, (x, y), 10, (255, 0, 0), thickness=4, lineType=8, shift=0)
	    # Mostramos cuadrado en color rojo
	    for i in range(0, caras.numeroCaras):
		if caras.x1[i] <= x and caras.y1[i] <= y and caras.x2[i] >= x and caras.y2[i] >= y:
			cv2.rectangle(color_imagen, (caras.x1[i], caras.y1[i]), (caras.x2[i], caras.y2[i]), (0, 0, 255), 2)

    # Mostramos la imagen en pantalla
    cv2.namedWindow("Resultado")
    #cv2.moveWindow("Resultado", 1800,300)
    cv2.imshow("Resultado", color_imagen) 
    cv2.waitKey(3)

  def callbackCaras(self, caras):
    if self.tratado_pCaras == True:
	self.pCaras = caras
	self.tratado_pCaras = False
    self.procesoGeneral()

  def callbackImagen(self, iComp):
    if self.tratado_iComp == True:
	self.iComp = iComp
	self.tratado_iComp = False

  def callbackGanador(self, eGanador):
    self.seleccionado = eGanador

  def procesoGeneral(self):
    if self.tratado_pCaras == False and self.tratado_iComp == False:
       	self.visualizacion(self.pCaras, self.iComp, self.seleccionado)
	self.tratado_pCaras = True
	self.tratado_iComp = True
	# Refrescamos el ganador cada 2 segundos a no ser que cambie
	if self.tiempo_inicio == 0:
		self.tiempo_inicio = time()
	if time() - self.tiempo_inicio > 10:
		self.tiempo_inicio = time()
		self.seleccionado.ganador = -1

  # wait_for_message(topic, topic_type, timeout=None)

def main(args):
  ic = visualizacion()
  rospy.init_node('visualizacion', anonymous=True)
  try:
	rospy.spin()
  except KeyboardInterrupt:
	print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)

