#!/usr/bin/env python
# -*- coding: utf-8 -*-
# license removed for brevity
"""
Created on Tue Jul  23 10:28:23 2019

@author: Jaime Duque Domingo UVA

Investigación sobre la orientación de cabeza robótica
Publicación de imagen OpenCV

Este nodo obtiene la imagen con OpenCV, la reduce, hace un flip y a continuación
la publica en topic imagenComprimida

"""
import rospy
import sys
import cv2
import numpy as np
import math

from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage

class publicadorImagenes:

  def __init__(self):
    # Creamos un objeto de tipo bridge para transferir imágenes OpenCV por ROS
    # self.bridge = CvBridge()

    # Creamos el publicador de imágenes
    self.image_pub = rospy.Publisher("imagenEntrada", CompressedImage, queue_size=1)

  def procesar(self, cv_image):

    # cv2.imshow("Imagen OpenCV obtenida", cv_image)

    # Reducimos la imagen al tamaño indicado en parámetros
    ancho = rospy.get_param("ANCHO_IMAGEN")
    alto_origen = cv_image.shape[0]
    ancho_origen = cv_image.shape[1]
    alto = int(ancho * alto_origen / ancho_origen)

    # Si el alto es diferente a los parámetros lo actualizamos ya que el alto se utiliza en otros
    # procedimientos (proceso estímulos, cálculo ángulos, etc)
    alto_param = rospy.get_param("ALTO_IMAGEN")
    if alto != alto_param:
       rospy.set_param("ALTO_IMAGEN",alto)

    # Dimensiones
    dim = (ancho, alto)
 
    # Reducir
    imagen_reducida = cv2.resize(cv_image, dim, interpolation = cv2.INTER_AREA)

    # Flip imagen
    imagen_flip = cv2.flip(imagen_reducida, 2)

    # Publicar la imagen comprimida en topic imagenComprimida
    img_msg = CompressedImage()
    img_msg.header.stamp = rospy.Time.now()
    img_msg.format = "jpeg"
    img_msg.data = np.array(cv2.imencode('.jpg', imagen_flip)[1]).tostring()
    self.image_pub.publish(img_msg)

def main(args):

    # Iniciamos el nodo
    rospy.init_node('publicadorImagenes', anonymous=True)

    # Captura con OpenCV
    cap = cv2.VideoCapture(0)
    #cap = cv2.VideoCapture('/home/disa/head_pose/Seq37-2P-S0M0/Video/Seq37-2P-S0M0_CAM1.mp4')

    # Ratio de proceso de 20 imágenes por segundo
    rate = rospy.Rate(20) # 20hz

    # Creamos el objeto de publicación de imágenes
    pImg = publicadorImagenes()

    ret = True
    while ret == True and not rospy.is_shutdown():

        # Lectura de frame
        ret, frame = cap.read()

	# Proceso de frame y publicación
	if ret == True:
		pImg.procesar(frame)

        rate.sleep()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)

