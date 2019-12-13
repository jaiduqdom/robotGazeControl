#!/usr/bin/env python
# -*- coding: utf-8 -*-
# license removed for brevity
"""
Created on Tue Jul  23 10:28:23 2019

@author: Jaime Duque Domingo UVA

Investigación sobre la orientación de cabeza robótica
Orientación de la cabeza robótica

Test de dirección de audio dentro de ROS

"""
import rospy
import sys
import numpy as np
from seguimiento.msg import direccionAudio
from calculoDireccionAudio import calculoDireccionAudio

class testAudio:

  # Inicialización de objeto definiendo las variables globales de la instancia del objeto
  def __init__(self):
    #####################################################################################
    # Objetos recibidos mediante funciones de callback
    # Detección de audio
    self.dAudio = direccionAudio()

    # Creamos el subscriptor al topic de audio
    self.dAudio_sub = rospy.Subscriber("direccionAudio",direccionAudio,self.callbackAudio, buff_size = 2**24)

    rospy.set_param("PAN_ROBOT", rospy.get_param("ANGULO_PAN_CENTRAL", 97)) 

    # Clase para calcular la dirección del audio
    self.dA = calculoDireccionAudio()

  def testAudio(self, audio):
    # Cálculo de la dirección del audio.
    indicador = self.dA.indicadorDireccion(audio)
    audio_izquierda = False
    audio_central = False
    audio_derecha = False
    if indicador == -1:
       audio_izquierda = True
    if indicador == 0:
       audio_central = True
    if indicador == 1:
       audio_derecha = True

    if audio_izquierda == True:
	rospy.loginfo("Audio procede de: Izquierda.")

    if audio_central == True:
	rospy.loginfo("Audio procede de: Centro.")

    if audio_derecha == True:
	rospy.loginfo("Audio procede de: Derecha.")

  def callbackAudio(self, audio):
    self.dAudio = audio
    self.testAudio(self.dAudio)

def main(args):
  ic = testAudio()
  rospy.init_node('testAudio', anonymous=True)
  try:
	rospy.spin()
  except KeyboardInterrupt:
	print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)

