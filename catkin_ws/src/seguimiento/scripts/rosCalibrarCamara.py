#!/usr/bin/env python
# -*- coding: utf-8 -*-
# license removed for brevity
"""
Created on Tue Jul  23 10:28:23 2019

@author: Jaime Duque Domingo UVA

Investigación sobre la orientación de cabeza robótica
Calibración para calcular los ángulos de la cabeza robótica

"""
import serial, time
import rospy
import sys
import cv2
import numpy as np
import math

from sensor_msgs.msg import Image
from correctorDistorsionOjoPez import correctorDistorsionOjoPez

class rosCalibrarCamara:

  def __init__(self):
    # Conexión con la placa arduino
    self.arduino = serial.Serial("/dev/ttyUSB0", 115200)
    time.sleep(2)
    self.velocidad = 30
    # Ángulos centrales del robot
    self.T_CENTRAL = 100
    self.P_CENTRAL = 100

    # Corrección de la imagen de tipo ojo de pez (cámara del robot)
    self.cO = correctorDistorsionOjoPez()

  def procesar(self, cv_image):
    # Corrección de la distorsión provocada por la imagen de tipo ojo pez 
    # (cámara del robot con gran angular)
    # Convertimos previamente a 640*480, ya que la calibración inicial de la cámara se realizó utilizando dichas dimensiones.
    dim = (640, 480)
    imagen_640480 = cv2.resize(cv_image, dim, interpolation = cv2.INTER_AREA)
    cv_image_corregida = self.cO.undistort(imagen_640480)

    # Flip imagen
    imagen_flip = cv2.flip(cv_image_corregida, 2)

    # Mostramos la imagen en pantalla
    cv2.imshow("Imagen", imagen_flip) 
    cv2.waitKey(3)

  # Inicializa la posición de los sensores
  def inicializar(self):
    self.mover(self.T_CENTRAL, self.P_CENTRAL)

  def mover(self, t, p):
    # Mueve la cabeza a la posición t, p (en grados)
    self.arduino.flush()
    setTemp1 = str(t)
    setTemp2 = str(p)
    setTemp3 = str(self.velocidad)
    sendMsg = setTemp1 + " " + setTemp2 + " " + setTemp3
    print("Mensaje enviado: " + sendMsg)

    self.arduino.write(sendMsg)
    time.sleep(4)
    recMsg = self.arduino.read(self.arduino.inWaiting())
    print("Mensaje recibido: " + recMsg)

  def __del__(self):
    # Destrucción del objeto
    self.arduino.close()


def main(args):
  ic = rosCalibrarCamara()
  rospy.init_node('rosCalibrarCamara', anonymous=True)

  # Captura con OpenCV
  cap = cv2.VideoCapture(0)

  # Ratio de proceso de 20 imágenes por segundo
  rate = rospy.Rate(20) # 20hz

  # Creamos el objeto de publicación de imágenes
  pC = rosCalibrarCamara()

  pC.inicializar()
  # 80 grados en horizontal y 107 en vertical
  pC.mover(60, 100)
  time.sleep(4)

  ret = True
  while ret == True and not rospy.is_shutdown():

	# Lectura de frame
        ret, frame = cap.read()
	# Proceso de frame y publicación
	if ret == True:
		pC.procesar(frame)
    	rate.sleep()

  cap.release()
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
