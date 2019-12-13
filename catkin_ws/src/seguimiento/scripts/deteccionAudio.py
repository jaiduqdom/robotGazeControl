#!/usr/bin/env python
# -*- coding: utf-8 -*-
# license removed for brevity
"""
Created on Tue Jul  25 10:28:23 2019

@author: Jaime Duque Domingo UVA

Investigación sobre la orientación de cabeza robótica
Esta función detecta si hay audio y, en dicho caso, devuelve la dirección del sonido. Utiliza ReSpeaker 2.0
La dirección se devuelve en grados (Direction of Arrival)

Header header
int doa

"""
import rospy
import sys
sys.path.append('/home/disa/catkin_ws/src/seguimiento/scripts/usb_4_mic_array')

from tuning import Tuning
import usb.core
import usb.util
import time
from seguimiento.msg import direccionAudio

def main(args):
  # Iniciamos el nodo
  rospy.init_node('deteccionAudio', anonymous=True)
  pub = rospy.Publisher("direccionAudio", direccionAudio, queue_size=1)

  # Ratio: 5 detecciones por segundo
  rate = rospy.Rate(3) # 5 hz

  # Buscamos el micrófono ReSpeaker 2.0
  dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)

  # Si existe lo iniciamos y comenzamos bucle de lectura
  if dev:
	Mic_tuning = Tuning(dev)
	Mic_tuning.write("ECHOONOFF", 1)
	Mic_tuning.write("AGCONOFF", 1)
	#Mic_tuning.write("GAMMAVAD_SR", 15)
	# Este parámetro es el umbral de detección de VAD. Inicialmente estaba a 15 pero funcionaba muy mal
	Mic_tuning.write("GAMMAVAD_SR", 2)

	while not rospy.is_shutdown():
		try:
			# Voice activity detection y Direction of arrival
			vad = Mic_tuning.is_voice()
			doa = Mic_tuning.direction

			rospy.loginfo("Detección de audio: %s", str(vad))
			# rospy.loginfo("Dirección de audio: %s", str(doa))

			#rospy.loginfo("STATNOISEONOFF_SR: %s", str(Mic_tuning.read("STATNOISEONOFF_SR")))
			#rospy.loginfo("NONSTATNOISEONOFF_SR: %s", str(Mic_tuning.read("NONSTATNOISEONOFF_SR")))
			#rospy.loginfo("STATNOISEONOFF: %s", str(Mic_tuning.read("STATNOISEONOFF")))
			#rospy.loginfo("NONSTATNOISEONOFF: %s", str(Mic_tuning.read("NONSTATNOISEONOFF")))
			#rospy.loginfo("FREEZEONOFF: %s", str(Mic_tuning.read("FREEZEONOFF")))
			#rospy.loginfo("AECFREEZEONOFF: %s", str(Mic_tuning.read("AECFREEZEONOFF")))
			#rospy.loginfo("GAMMAVAD_SR: %s", str(Mic_tuning.read("GAMMAVAD_SR")))
		
			# Creamos el mensaje de audio
			dAudio = direccionAudio()
			dAudio.header.stamp = rospy.Time.now()
			dAudio.vad = False
			dAudio.doa = 0

			# Si hay actividad, enviamos la dirección del sonido (DOA)
			# Cuando estamos en movimiento no analizamos el sonido por el ruido de los motores
			if vad != 0 and rospy.get_param("EN_MOVIMIENTO", False) == False:
				# Indicamos que se ha detectado audio
				dAudio.vad = True

				rospy.loginfo("Dirección de audio: %s", str(doa))

				#rospy.loginfo("ECHOONOFF: %s", str(Mic_tuning.read("ECHOONOFF")))
				#rospy.loginfo("AGCONOFF: %s", str(Mic_tuning.read("AGCONOFF")))

				# Publicamos mensaje con la dirección del audio
				dAudio.doa = doa

			# Publicamos el mensaje
			pub.publish(dAudio)

			rate.sleep()
		except KeyboardInterrupt:
			sys.exit(0)
			break

if __name__ == '__main__':
    main(sys.argv)

