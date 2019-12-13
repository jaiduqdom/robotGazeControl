#!/usr/bin/env python
# -*- coding: utf-8 -*-
# license removed for brevity
"""
Created on Tue Jul  23 10:28:23 2019

@author: Jaime Duque Domingo UVA

Investigación sobre la orientación de cabeza robótica
Obtención de puntos de la cara utilizando librería DLIB

Este nodo obtiene la imagen con OpenCV, la transforma en grises y la reduce, a continuación
la procesa con DLIB para obtener los puntos característicos de la cara. Finalmente publica el 
resultado en el topic puntosCara, un mensaje de tipo Caras:

Header header
sensor_msgs/Image imagen
int32 numeroCaras
int32[] x1
int32[] y1
int32[] x2
int32[] y2
int32[] puntoX
int32[] puntoY
int32[] indiceCara

donde (x1[c],y1[c])-(x2[c],y2[c]) definen el rectángulo de la cara para cada cara "c" devuelta
y (puntoX[68*c + i], puntoY[68*c + i]) definen el punto característico "i" DLIB para cada 
cara "c"

Más información en:
http://wiki.ros.org/cv_bridge/Tutorials/ConvertingBetweenROSImagesAndOpenCVImagesPython
http://dlib.net/face_landmark_detection.py.html

"""
import rospy
import sys
import cv2
import numpy as np
import dlib
import math

from sensor_msgs.msg import Image
# from cv_bridge import CvBridge, CvBridgeError
from seguimiento.msg import puntosCaras
from sensor_msgs.msg import CompressedImage
from reconocimientoFacial import reconocimientoFacial
import dlib
import dlib.cuda as cuda

class publicadorPuntosCaras:

  def __init__(self):
    # Creamos el subscriptor al topic de imágenes comprimidas para poder obtener la imagen
    self.iComp_sub = rospy.Subscriber("imagenEntrada",CompressedImage,self.callbackImagen)

    # Creamos el publicador del topic imagenTratada, con la imagen realmente procesada
    # Hacemos esto para que el resultado al visualizar sea el correcto
    self.iComp_pub = rospy.Publisher("imagenTratada", CompressedImage, queue_size=1)

    # Creamos el publicador del topic puntosCara
    self.caras_pub = rospy.Publisher("puntosCaras", puntosCaras, queue_size=1)

    # Definimos el fichero de detección de caras entrenado de DLIB
    self.predictor_path = "/home/disa/catkin_ws/src/camara/scripts/shape_predictor_68_face_landmarks.dat"

    # Definimos las utilidades de detección de caras y puntos de DLIB
    cuda.set_device(0)

    self.detector = dlib.get_frontal_face_detector()
    self.predictor = dlib.shape_predictor(self.predictor_path)

    rospy.loginfo("Utilizando CUDA = %s", dlib.DLIB_USE_CUDA)

    # Constante de número de puntos devueltos por DLIB
    self.PUNTOS_DLIB = 68

    # Objeto de reconocimiento facial
    self.rF = reconocimientoFacial()

    # Herramienta de visualización DLIB
    # self.win = dlib.image_window()

    # Máximo de caras del histórico
    self.MAXIMO_PERSONAS = rospy.get_param("MAXIMO_PERSONAS")

    # Trackers
    self.trackers = []
    for i in range(0, self.MAXIMO_PERSONAS):
	self.trackers.append(dlib.correlation_tracker())
    self.tracker_iniciado = np.zeros(self.MAXIMO_PERSONAS)
    # Si el tracking detecta a la persona no volvemos a reconocer facialmente. Esto aumenta la velocidad
    # Calculamos puntos medios del tracker
    self.x_medio = np.zeros(self.MAXIMO_PERSONAS)
    self.y_medio = np.zeros(self.MAXIMO_PERSONAS)

  def procesar(self, imagen_flip):

    # Convertir cara de BGR (OpenCV) a RGB (DLIB)
    imagen_dlib = imagen_flip[:, :, ::-1]

    # Transformamos a escala de grises
    gris_imagen = cv2.cvtColor(imagen_flip, cv2.COLOR_BGR2GRAY)

    # Definimos objeto a publicar con los datos de las caras
    caras = puntosCaras()
    caras.header.stamp = rospy.Time.now()

    # Identificar los límites de cada cara. El 1 del segundo argumento indica que
    # se puede ampliar la imagen 1 vez para detectar más caras
    dets = self.detector(gris_imagen, 1)
    numeroCaras = len(dets)
    rospy.loginfo("Caras detectadas = %d", numeroCaras)
    caras.numeroCaras = numeroCaras

    # Ajustamos los tamaños de los vectores publicados
    # (x1,y1)-(x2,y2) son los extremos de cada cara en la imagen
    caras.x1 = np.arange(numeroCaras)
    caras.y1 = np.arange(numeroCaras)
    caras.x2 = np.arange(numeroCaras)
    caras.y2 = np.arange(numeroCaras)
    caras.indiceCara = np.arange(numeroCaras)
    caras.caraNueva = np.arange(numeroCaras)
    # (puntoX,puntoY) representan los puntos característicos de la imagen para
    # cada cara y número de punto (68 devuelve DLIB)
    # los puntos se llevan a un array de una dimensión donde cada 68 puntos
    # consecutivos corresponden a caras diferentes
    caras.puntoX = np.arange(numeroCaras * self.PUNTOS_DLIB)
    caras.puntoY = np.arange(numeroCaras * self.PUNTOS_DLIB)

    # Avanzamos tiempo de todas las caras detectadas en el histórico
    self.rF.avanzar_Tiempo_Inactiva()

    # Hacemos un tracking de todos los objetos de la pantalla. Si estamos siguiendo una cara no realizaremos
    # reconocimiento facial nuevamente al ser una de las caras anteriores.
    for i in range(0, self.MAXIMO_PERSONAS):
	if self.tracker_iniciado[i] == 1:
        	self.trackers[i].update(imagen_dlib)
		pos = self.trackers[i].get_position()
		# unpack the position object
		startX = int(pos.left())
		startY = int(pos.top())
		endX = int(pos.right())
		endY = int(pos.bottom())
                self.x_medio[i] = (startX + endX) / 2
                self.y_medio[i] = (startY + endY) / 2

    for k, d in enumerate(dets):
    	rospy.loginfo("Caras detectada %d = (%d,%d)-(%d,%d)", 
                      k, d.left(), d.top(), d.right(), d.bottom())

        # Coordenadas de la cara
        caras.x1[k] = d.left()
        caras.y1[k] = d.top()
        caras.x2[k] = d.right()
        caras.y2[k] = d.bottom()

        # Ver si la cara detectada es una del tracking
	indice_cara = -1
	es_cara_nueva = False
	for i in range(0, self.MAXIMO_PERSONAS):
		if self.tracker_iniciado[i] == 1:
			# Miramos si el punto medio del tracking está dentro de la cara detectada
			if (self.x_medio[i] > caras.x1[k] and self.x_medio[i] < caras.x2[k] and 
			    self.y_medio[i] > caras.y1[k] and self.y_medio[i] < caras.y2[k]):
				indice_cara = i
				es_cara_nueva = False
				break
	# Get the landmarks/parts for the face in box d.
	shape = self.predictor(imagen_flip, d)

	# Si la cara no se ha detectado en el tracking, volvemos a reconocerla facialmente
	if indice_cara == -1:
		# Buscar el índice de la cara y verificar si es una cara nueva
		# Caso 1: indice_cara, es_cara_nueva = self.rF.buscar_indice_cara(shape)
		indice_cara, es_cara_nueva = self.rF.buscar_indice_cara_ENC(imagen_flip, shape, caras.x1[k],caras.y1[k],caras.x2[k],caras.y2[k])
		# Caso 5: indice_cara, es_cara_nueva = self.rF.buscar_indice_cara_IMG(imagen_flip,caras.x1[k],caras.y1[k],caras.x2[k],caras.y2[k])

	        # Arrancamos un nuevo tracking
		self.trackers[indice_cara].start_track(imagen_dlib, dlib.rectangle(caras.x1[k] , caras.y1[k] , caras.x2[k] , caras.y2[k] ))
		#self.tracker[indice_cara].update(imagen_dlib)
		self.tracker_iniciado[indice_cara] = 1

        # Actualizar mensaje
	caras.indiceCara[k] = indice_cara
        caras.caraNueva[k] = es_cara_nueva

        # Recorremos los valores (x,y) de los landmarks de la cara y los devolvemos
        # for i in range(0, shape.num_parts):
	for i in range(0, self.PUNTOS_DLIB):
            caras.puntoX[self.PUNTOS_DLIB * k + i] = shape.part(i).x
            caras.puntoY[self.PUNTOS_DLIB * k + i] = shape.part(i).y

    # Publicar los puntos de la cara en topic puntosCaras
    self.caras_pub.publish(caras)
    # Publicar la imagen tratada como comprimida
    img_msg = CompressedImage()
    img_msg.header.stamp = rospy.Time.now()
    img_msg.format = "jpeg"
    img_msg.data = np.array(cv2.imencode('.jpg', gris_imagen)[1]).tostring()
    self.iComp_pub.publish(img_msg)

    # Como imagen le pasamos la imagen procesada
    #try:
    #	caras.imagen = self.bridge.cv2_to_imgmsg(gris_imagen, "mono8")
    #except CvBridgeError as e:
    #	print(e)
    # cv2.waitKey(3)

  # Este callback lo introducimos para poder leer la imagen publicada en imagenComprimida y procesarla
  def callbackImagen(self, iComp):
    # Recuperamos imagen como OpenCV
    np_arr = np.fromstring(iComp.data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    self.procesar(img)

def main(args):
  ic = publicadorPuntosCaras()
  rospy.init_node('publicadorPuntosCara', anonymous=True)
  try:
	rospy.spin()
  except KeyboardInterrupt:
	print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)
