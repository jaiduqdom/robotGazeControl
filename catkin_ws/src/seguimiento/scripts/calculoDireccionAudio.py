#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 09:32:37 2019

@author: Jaime Duque Domingo (UVA)

Esta clase permite decidir la dirección del audio en función del ángulo
devuelto por el sensor ReSpeaker y la posición de la cabeza robótica

"""

import rospy

class calculoDireccionAudio:

  def __init__(self):
    self.angulo_central_Respeaker = int(rospy.get_param("ANGULO_RESPEAKER_CENTRAL", 0))

  #######################################################################################################
  # Le pasamos el mensaje de audio devuelto por deteccionAudio donde se incluyen los valores:
  #    audio.vad: Voice Activity Detection
  #    audio.doa: Direction of Arrival
  # La salida devuelve:
  #    -1: Sonido procedente de la izquierda
  #     0: Sonido procedente del centro
  #     1: Sonido procedente de la derecha
  #  9999: No hay audio
  #######################################################################################################
  def indicadorDireccion(self, audio):

    indicador = 9999
    # Realizamos el cálculo únicamente si hay detección de audio
    if audio.vad == True:
	# Alineamos con la posición 0. El ángulo devuelto considera que el 0 es justo delante del robot fijo.
	# Para ello utilizamos el ángulo base del Respeaker
	angulo_doa = audio.doa - self.angulo_central_Respeaker
	if angulo_doa >= 360:
		angulo_doa = angulo_doa - 360
	if angulo_doa < 0:
		angulo_doa = angulo_doa + 360

	# Vemos cuánto se ha desplazado el ángulo PAN de la cabeza respecto al centro
	# Si es positivo se habrá desplazado a la derecha. En caso contrario a la izquierda
	movimiento_pan = int(rospy.get_param("PAN_ROBOT", 0) - rospy.get_param("ANGULO_PAN_CENTRAL", 97))
	# El ángulo central a considerar en el micrófono debe estar alineado con el de la cabeza robótica
	# Para ello sumamos el DOA al desplazamiento del ángulo PAN para alinearlo con el 0
	angulo_doa = angulo_doa + movimiento_pan
	#if angulo_doa < 180:
	#	angulo_doa = angulo_doa + movimiento_pan
	#else:
	#	angulo_doa = angulo_doa + movimiento_pan
	if angulo_doa >= 360:
		angulo_doa = angulo_doa - 360
	if angulo_doa < 0:
		angulo_doa = angulo_doa + 360

	# Cálculo de la dirección del audio. Tenemos que alinear el ángulo de la cabeza robótica con el ángulo del sensor
	# Ángulo central del Respeaker. Nos vale para saber si el sonido viene de la derecha o izquierda de la cabeza robótica
	# Distinguiremos 3 zonas:
	#     - Audio izquierda: < 320 y > 180 grados
	#     - Audio central: 320 a 40 grados
	#     - Audio derecha: > 40 grados y < 180 grados
	lim1 = 320
	lim2 = 180
	lim3 = 40

	#rospy.loginfo("CALCULO DIRECCION AUDIO")
	#rospy.loginfo("PAN_ROBOT : %s", str(rospy.get_param("PAN_ROBOT", 0)))
	#rospy.loginfo("PAN_CENTRAL : %s", str(rospy.get_param("ANGULO_PAN_CENTRAL", 0)))
	#rospy.loginfo("RESPEAKER_CENTRAL : %s", str(rospy.get_param("ANGULO_RESPEAKER_CENTRAL", 0)))
	#rospy.loginfo("DOA : %s", str(audio.doa))
	#rospy.loginfo("Ángulo DOA calculado : %s", str(angulo_doa))

	if angulo_doa < lim1 and angulo_doa > lim2:
		rospy.loginfo("Audio viene de la: Derecha.")
		indicador = 1
	else:
		if angulo_doa > lim3 and angulo_doa < lim2:
			rospy.loginfo("Audio viene de la: Izquierda.")
			indicador = -1
		else:
			rospy.loginfo("Audio viene del: Centro.")
			indicador = 0
    return indicador

