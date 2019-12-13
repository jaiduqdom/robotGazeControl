#!/usr/bin/env python
# -*- coding: utf-8 -*-
# license removed for brevity
"""
Created on Tue Jul  23 10:28:23 2019

@author: Jaime Duque Domingo UVA

Investigación sobre la orientación de cabeza robótica
Obtención de puntos de la cara utilizando librería DLIB

Este nodo se suscribe al topic imagen_topic de obtención de una imagen, lo procesa y
crea el topic puntosCara con los puntos extraídos mediante la librería DLIB

Más información en:
http://wiki.ros.org/cv_bridge/Tutorials/ConvertingBetweenROSImagesAndOpenCVImagesPython
http://dlib.net/face_landmark_detection.py.html

"""
import rospy
import sys
import cv2
import numpy as np
import dlib
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from camara.msg import puntosCaras

class publicadorSubscriptorPuntosCara:

  def __init__(self):
    # Creamos un objeto de tipo bridge para transferir imágenes OpenCV por ROS
    self.bridge = CvBridge()

    # Creamos el subscriptor al topic de imágenes OpenCV
    self.image_sub = rospy.Subscriber("imagen_topic",Image,self.callback)

    # Creamos el publicador del topic puntosCara
    self.image_pub = rospy.Publisher("puntosCara",puntosCaras)

    # Definimos el fichero de detección de caras entrenado de DLIB
    self.predictor_path = "/home/disa/catkin_ws/src/camara/scripts/shape_predictor_68_face_landmarks.dat"

    # Definimos las utilidades de detección de caras y puntos de DLIB
    self.detector = dlib.get_frontal_face_detector()
    self.predictor = dlib.shape_predictor(self.predictor_path)

    # Constante de número de puntos devueltos por DLIB
    self.PUNTOS_DLIB = 68

  def callback(self,data):

    # Primero leemos la imagen del topic imagen_topic
    try:
	cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
	print(e)

    cv2.imshow("Imagen OpenCV recibida", cv_image)

    # Reducimos la imagen a 500 píxeles de ancho
    ancho = 500
    alto_origen = cv_image.shape[0]
    ancho_origen = cv_image.shape[1]
    alto = ancho * alto_origen / ancho_origen

    # Dimensiones
    dim = (ancho, alto)
 
    # Reducir
    imagen_reducida = cv2.resize(cv_image, dim, interpolation = cv2.INTER_AREA)

    # Transformamos a escala de grises
    gris_imagen = cv2.cvtColor(imagen_reducida, cv2.COLOR_BGR2GRAY)

    # Imagen reducida en gris
    cv2.imshow("Imagen reducida en gris", gris_imagen) 

    # Definimos objeto a publicar con los datos de las caras
    caras = puntosCaras()
    caras.header.stamp = rospy.Time.now()

    # Como imagen le pasamos la imagen procesada
    try:
    	caras.imagen = self.bridge.cv2_to_imgmsg(gris_imagen, "mono8")
    except CvBridgeError as e:
	print(e)

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
    # (puntoX,puntoY) representan los puntos característicos de la imagen para
    # cada cara y número de punto (68 devuelve DLIB)
    # los puntos se llevan a un array de una dimensión donde cada 68 puntos
    # consecutivos corresponden a caras diferentes
    caras.puntoX = np.arange(numeroCaras * self.PUNTOS_DLIB)
    caras.puntoY = np.arange(numeroCaras * self.PUNTOS_DLIB)

    for k, d in enumerate(dets):
    	rospy.loginfo("Caras detectada %d = (%d,%d)-(%d,%d)", 
                      k, d.left(), d.top(), d.right(), d.bottom())

        # Coordenadas de la cara
        caras.x1[k] = d.left()
        caras.y1[k] = d.top()
        caras.x2[k] = d.right()
        caras.y2[k] = d.bottom()

        # Get the landmarks/parts for the face in box d.
        shape = self.predictor(gris_imagen, d)

        # Recorremos los valores (x,y) de los landmarks de la cara y los devolvemos
        # for i in range(0, shape.num_parts):
	for i in range(0, self.PUNTOS_DLIB):
            caras.puntoX[self.PUNTOS_DLIB * k + i] = shape.part(i).x
            caras.puntoY[self.PUNTOS_DLIB * k + i] = shape.part(i).y

    # Publicar el resultado como topic puntosCara
    self.image_pub.publish(caras)

    cv2.waitKey(3)

def main(args):
  ic = publicadorSubscriptorPuntosCara()
  rospy.init_node('publicadorSubscriptorPuntosCara', anonymous=True)
  try:
	rospy.spin()
  except KeyboardInterrupt:
	print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)

