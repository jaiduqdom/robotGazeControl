#!/usr/bin/env python
# -*- coding: utf-8 -*-
# license removed for brevity
"""
Created on Tue Jul  25 10:28:23 2019

@author: Jaime Duque Domingo UVA

Investigación sobre la orientación de cabeza robótica
Esta función devuelve el valor rms medio de amplitud de sonido durante un intervalo de tiempo
Publicación de nivel de audio detectado en mensaje /nivelAudio:

Header header
float32 rms

"""
import rospy
import sys
import numpy as np
import audioop
import pyaudio
from camara.msg import nivelAudio

class deteccionAudio:

  def __init__(self):
    self.pub = rospy.Publisher("nivelAudio", nivelAudio)

    # Dispositivo audio
    self.audio = pyaudio.PyAudio()

    # Indicamos frames de audio
    self.chunk = 1024

    # Abrimos un stream de audio
    self.stream = self.audio.open(format=pyaudio.paInt16,
       	            channels=1,
       	            rate=44100,
       	            input=True,
       	            frames_per_buffer=self.chunk)

  def procesar(self):

    # Creamos un mensaje con el header y el rms obtenido
    nAudio = nivelAudio()
    nAudio.header.stamp = rospy.Time.now()
   
    # Leemos stream de audio
    data = self.stream.read(self.chunk)
    
    # Calculamos la media de amplitud de sonido
    #   width=2 for format=paInt16
    rms = audioop.rms(data, 2)
    
    # Publicamos mensaje
    rospy.loginfo("Nivel de audio detectado. RMS = %f. ", rms)
    nAudio.rms = rms

    # Publicar el resultado como topic puntosCara
    self.pub.publish(nAudio)

  def parar(self):
    # Cerramos audio
    self.audio.close

def main(args):

    # Iniciamos el nodo
    rospy.init_node('deteccionAudio', anonymous=True)

    # Ratio de proceso de 20 detecciones por segundo
    rate = rospy.Rate(20) # 20hz

    # Objeto de detección de audio
    dAudio = deteccionAudio()

    while not rospy.is_shutdown():

	# Proceso de detección de audio
	dAudio.procesar()

	# Espera
        rate.sleep()

    # Cerramos audio
    dAudio.parar()

if __name__ == '__main__':
    main(sys.argv)

