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

Basado en librería auditok:

Uso de auditok
https://github.com/amsehili/auditok

Instalación:
	git clone https://github.com/amsehili/auditok.git
	cd auditok
	python setup.py install

"""
import rospy
from auditok import ADSFactory, AudioEnergyValidator, StreamTokenizer, player_for
import pyaudio
import numpy as np
import sys
from seguimiento.msg import audioDetectado

# Iniciamos el nodo
rospy.init_node('deteccionAudio', anonymous=True)
pub = rospy.Publisher("audioDetectado", audioDetectado, queue_size=10)

try:

   energy_threshold = 45
   duration = 10000000 # seconds

   while not rospy.is_shutdown():

	   # record = True so that we'll be able to rewind the source.
	   # max_time = 10: read 10 seconds from the microphone
	   asource = ADSFactory.ads(record=True, max_time = duration)

	   validator = AudioEnergyValidator(sample_width=asource.get_sample_width(), energy_threshold = energy_threshold)
	   #tokenizer = StreamTokenizer(validator=validator, min_length=20, max_length=250, max_continuous_silence=30)

	   tokenizer = StreamTokenizer(validator=validator, min_length=20, max_length=20, max_continuous_silence=10)

	   player = player_for(asource)

	   def echo(data, start, end):
		# Creamos un mensaje con el header y el rms obtenido
		dAudio = audioDetectado()
		dAudio.header.stamp = rospy.Time.now()
		dAudio.audioDetectado = True
		dAudio.inicio = start
		dAudio.final = end

		# Publicar el resultado como topic puntosCara
		pub.publish(dAudio)

	      	rospy.loginfo("Acoustic activity at: {0}--{1}".format(start, end))
	      	player.play(b''.join(data))

	   asource.open()

	   rospy.loginfo("Iniciando escucha de audio (Duración:{}, Energía:{})...".format(duration, energy_threshold))

	   tokenizer.tokenize(asource, callback=echo)

	   asource.close()
	   player.stop()

except KeyboardInterrupt:

   player.stop()
   asource.close()
   sys.exit(0)

except Exception as e:
   
   sys.stderr.write(str(e) + "\n")
   sys.exit(1)
