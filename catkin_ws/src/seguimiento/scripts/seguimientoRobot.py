#!/usr/bin/env python
# -*- coding: utf-8 -*-
# license removed for brevity
"""
Created on Tue Jul  23 10:28:23 2019

@author: Jaime Duque Domingo UVA

Investigación sobre la orientación de cabeza robótica
Orientación de la cabeza robótica

Este nodo le permite al robot decidir hacia donde orientarse a partir de los datos recibidos de la red competitiva
y el filtro de Kalman

Se suscribe a los topic:
	salidaRedCompetitiva, con los resultados de la red competitiva
	salidaKalman, con las coordenadas de cada cara

Publica los topic:
	ganador, con el indicador de ganador así como sus coordenadas a partir de Kalman

"""
import rospy
import sys
import numpy as np
import math
from time import sleep
from time import time
from seguimiento.msg import direccionAudio
from seguimiento.msg import salidaKalman
from seguimiento.msg import salidaRedCompetitiva
from seguimiento.msg import ganador
from movimientoMotor import movimientoMotor
from comportamiento  import comportamiento
from calculoAngulos import calculoAngulos
from calculoDireccionAudio import calculoDireccionAudio

class seguimiento:

  # Inicialización de objeto definiendo las variables globales de la instancia del objeto
  def __init__(self):
    ########################################################################################
    # Inicialización de las expresiones del avatar
    ########################################################################################
    self.avatar = comportamiento()
    rospy.sleep(1.0)
    rospy.set_param("AVATAR_ACTIVO", False)

    #####################################################################################
    # Objetos recibidos mediante funciones de callback
    # Salida de Kalman
    self.sKalman = salidaKalman()
    # Salida de Red Competitiva
    self.sRCompetitiva = salidaRedCompetitiva()
    # Detección de audio
    self.dAudio = direccionAudio()
    #####################################################################################

    # Clase para calcular la dirección del audio
    self.dA = calculoDireccionAudio()

    # Creamos el publicador del topic ganador
    self.ganador_pub = rospy.Publisher("ganador", ganador, queue_size=1)

    # Número de movimientos de la cabeza robótica cada vez que cambia de ángulo (100 pequeños movimientos por defecto)
    self.INCREMENTOS = 100

    # Máximo de caras del histórico
    self.MAXIMO_PERSONAS = rospy.get_param("MAXIMO_PERSONAS", 10)

    ########################################################################################
    # Inicialización del control del movimiento de la cabeza robótica
    ########################################################################################
    # Ángulos de movimiento del robot ( en radianes )
    self.PAN_CENTRAL = rospy.get_param("ANGULO_PAN_CENTRAL", 100) * math.pi / 180
    self.TILT_CENTRAL = rospy.get_param("ANGULO_TILT_CENTRAL", 100) * math.pi / 180
    self.MAXIMO_PAN = rospy.get_param("ANGULO_MAXIMO_PAN", 160) * math.pi / 180
    self.MAXIMO_TILT = rospy.get_param("ANGULO_MAXIMO_TILT", 160) * math.pi / 180

    # Primero marcamos que el motor está en movimiento para no permitir más movimientos
    rospy.set_param("EN_MOVIMIENTO", True)
    # Al crear un objeto de tipo movimiento se mueve la cabeza al punto central
    self.mM = movimientoMotor()
    # Ahora indicamos que hemos terminado el movimiento
    rospy.set_param("EN_MOVIMIENTO", False)

    # Variable utilizada para el movimiento exploratorio
    self.exploracion = 0
    # Hacemos exploración cada 2 segundos
    self.tiempo_inicio = 0

    # Los subscriptores van al final para evitar variables no declaradas

    # Creamos el subscriptor al topic de salida de Kalman
    self.sKalman_sub = rospy.Subscriber("salidaKalman",salidaKalman,self.callbackKalman)

    # Creamos el subscriptor al topic de salida de la red competitiva
    self.sRCompetitiva_sub = rospy.Subscriber("salidaRedCompetitiva",salidaRedCompetitiva,self.callbackRecCompetitiva)

    # Creamos el subscriptor al topic de audio
    # Este topic se utiliza si no hay ningún ganador en la red competitiva. En dicho caso se detecta si hay
    # audio para iniciar un proceso de exploración
    self.dAudio_sub = rospy.Subscriber("direccionAudio",direccionAudio,self.callbackAudio)

    # Movimiento previo
    # Si el movimiento anterior es igual al nuevo, no lo ejecutamos.
    self.pan_previo = 0
    self.tilt_previo = 0

    # Tiempo para parpadeo de ojos
    self.tiempo_parpadeo = 0

    # Objeto de cálculo de ángulos
    # Nos permite calcular el ángulo de una cara a partir del ángulo actual del robot y de las
    # coordenadas de la cara
    self.cA = calculoAngulos()
    # Ancho de la imagen
    self.width = float(rospy.get_param("ANCHO_IMAGEN", 640))

  #########################################################################################
  # Función de seguimiento
  #########################################################################################
  def seguimiento(self, sKalman, sRedCompetitiva):

    # Cada 10 segundos hacemos un parpadeo de ojos si es posible
    # Esto transmite naturalidad
    if self.tiempo_parpadeo == 0:
	self.tiempo_parpadeo = time()
    if time() - self.tiempo_parpadeo > 10:
	self.tiempo_parpadeo = time()
	self.avatar.realizarParpadeo()

    # Buscar ganador según la red competitiva mirando si tiene un filtro de Kalman asociado
    # Hay dos personas que son ficticias y nos sirven para cuando alguien nuevo aparece en la escena.
    maximo = -1
    mGanador = -1
    for i in range(0, self.MAXIMO_PERSONAS + 2):
	if sKalman.identificador:
		if sRedCompetitiva.data[i] > maximo and sKalman.identificador[i] != -2:
			maximo = sRedCompetitiva.data[i]
        	        mGanador = i

    # Si el valor de salida de la red competitiva es muy pequeño (próximo a 0) 
    # es que no hay nadie enfrente del robot
    # En dicho caso el robot debe hacer un movimiento exploratorio
    if maximo < 0.02:
	mGanador = -1
	maximo = -1

    # Como no hay un ganador, debemos hacer un movimiento exploratorio si se detecta audio
    if self.tiempo_inicio == 0:
	self.tiempo_inicio = time()
    # Dejamos esta línea comentada. 
    if mGanador == -1 and self.dAudio.vad == True and time() - self.tiempo_inicio > 10:
        self.tiempo_inicio = time()
	# Calculamos los distintos ángulos exploratorios donde nos vamos a mover
	center_PAN = self.PAN_CENTRAL
	center_TILT = self.TILT_CENTRAL
	right_PAN = (self.PAN_CENTRAL + self.MAXIMO_PAN / 3)
	left_PAN = (self.PAN_CENTRAL - self.MAXIMO_PAN / 3)
	up_TILT = (self.TILT_CENTRAL + self.MAXIMO_TILT / 4)
	down_TILT = (self.TILT_CENTRAL - self.MAXIMO_TILT / 4)

	# Añadimos un movimiento exploratorio hasta la mitad
	right_mPAN = (self.PAN_CENTRAL + self.MAXIMO_PAN / 6)
	left_mPAN = (self.PAN_CENTRAL - self.MAXIMO_PAN / 6)
	up_mTILT = (self.TILT_CENTRAL + self.MAXIMO_TILT / 8)
	down_mTILT = (self.TILT_CENTRAL - self.MAXIMO_TILT / 8)

	# Ver si la cabeza está orientada a derecha o izquierda
	if rospy.get_param("PAN_ROBOT", 0) > rospy.get_param("ANGULO_PAN_CENTRAL", 100):
		orientacion = 1
	else:
		if rospy.get_param("PAN_ROBOT", 0) == rospy.get_param("ANGULO_PAN_CENTRAL", 100):
			orientacion = 0
		else:
			orientacion = -1

        # Cálculo de la dirección del audio para ver si la exploración va a derecha o izquierda
	# Devuelve -1 si el audio le viene de la izquierda, 0 si viene del centro o +1 si viene de la derecha
	indicador = self.dA.indicadorDireccion(self.dAudio)
	if indicador == -1:
		if orientacion == -1:
			self.exploracion = 6
		if orientacion == 0:
			self.exploracion = 6
		if orientacion == 1:
			self.exploracion = 5
	if indicador == 0:
		self.exploracion = 0
	if indicador == 1:
		if orientacion == -1:
			self.exploracion = 0
		if orientacion == 0:
			self.exploracion = 1
		if orientacion == 1:
			self.exploracion = 1

	# Como no tiene a nadie delante le mostramos triste
	self.avatar.mostrarTriste()

        if self.exploracion == 0:
		# Primero vamos al centro
		self.movimientoRobot(center_PAN, center_TILT)
		self.exploracion = 1
	else:
		if self.exploracion == 1:
			# Después vamos a la derecha arriba (la mitad de este movimiento)
			self.movimientoRobot(right_mPAN, up_mTILT)
			self.exploracion = 2
		else:
			if self.exploracion == 2:
				# Después vamos a la derecha arriba
				self.movimientoRobot(right_PAN, up_TILT)
				self.exploracion = 3
			else:
				if self.exploracion == 3:
					# Después vamos a la derecha abajo
					self.movimientoRobot(right_PAN, down_TILT)				
					self.exploracion = 4
				else:
					if self.exploracion == 4:
						# Después vamos a la derecha abajo (la mitad de este movimiento)
						self.movimientoRobot(right_mPAN, down_mTILT)
						self.exploracion = 5
					else:
						if self.exploracion == 5:
							# Después vamos al centro
							self.movimientoRobot(center_PAN, center_TILT)
							self.exploracion = 6
						else:
							if self.exploracion == 6:
								# Después vamos a la izquierda arriba (la mitad de este movimiento)
								self.movimientoRobot(left_mPAN, up_mTILT)
								self.exploracion = 7
							else:
								if self.exploracion == 7:
									# Después vamos a la izquierda arriba
									self.movimientoRobot(left_PAN, up_TILT)
									self.exploracion = 8
								else:
									if self.exploracion == 8:
										# Después vamos a la izquierda abajo
										self.movimientoRobot(left_PAN, down_TILT)
										self.exploracion = 9
									else:
										if self.exploracion == 9:
											# Después vamos a la izquierda abajo (la mitad de este movimiento)
											self.movimientoRobot(left_mPAN, down_mTILT)
											# Finalmente vamos al centro
											self.exploracion = 0

    # Buscar coordenadas de Kalman verificando que el identificador no es -2 (existe el filtro asociado)
    if mGanador != -1:
	if sKalman.identificador:
	    	if sKalman.identificador[mGanador] != -2:
			g = ganador()
	    		g.header.stamp = rospy.Time.now()
			g.ganador = mGanador
                        # Kalman publica los ángulos ganadores. Es donde se tiene que orientar la
                        # cabeza robótica.
			g.pan = sKalman.pan[mGanador]
			g.tilt = sKalman.tilt[mGanador]
			self.ganador_pub.publish(g)
		        rospy.loginfo("Ganador: %s, Angulo:(%f, %f)", str(g.ganador), g.pan, g.tilt)

                        # Cuando el ángulo que vamos a mover es menor que una cierta cantidad,
                        # movemos los ojos en vez de los motores
			angulo_pan_robot = float(rospy.get_param("PAN_ROBOT", 0)) * math.pi / float(180)
			valor_movimiento = abs(angulo_pan_robot - g.pan)
			# Consideramos un movimiento inferior a 10 grados
			if valor_movimiento < float(10) * math.pi / float(180):
				# Calculamos las coordenadas de la persona en pantalla. Damos un margen de 5 píxeles
				x, y = self.cA.calcularCoordenadas(g.pan, g.tilt)
				dist = abs(x - self.width / 2)
				if dist > 5:
					if x > self.width / 2:
						self.avatar.mirarDerecha()
					else:
						self.avatar.mirarIzquierda()

				"""# Damos un pequeño margen para no estar continuamente moviendo ojos
				if valor_movimiento > float(4) * math.pi / float(180):
					# Si la persona está a la derecha miramos hacia la derecha
					if g.pan > angulo_pan_robot:
						#self.avatar.mirarDerecha()
						self.avatar.mirarIzquierda()
					else:
						#self.avatar.mirarIzquierda()
						self.avatar.mirarDerecha()"""
			else:
				# Si el robot no está en movimiento, mostramos alegre al avatar
				# De esta forma evitamos sobrecargar la cola de mensajes
				if rospy.get_param("EN_MOVIMIENTO") == False:
					# Movemos la cabeza robótica a la nueva posición haciendo una animación en función de la dirección.
					if g.pan > angulo_pan_robot:
						self.avatar.mirarIzquierdaAlegre()
					else:
						self.avatar.mirarDerechaAlegre()
					self.movimientoRobot(g.pan, g.tilt)

  #########################################################################################
  # Función de movimiento
  # Se encarga de mover la cabeza robótica desdel ángulo actual del robot hasta el nuevo
  # ángulo indicado
  #########################################################################################
  def movimientoRobot(self, t_new, p_new):
    # Parámetro para bloqueo de movimiento
    if rospy.get_param("BLOQUEO_MOVIMIENTO", False) == True:
	return

    # Cuando se encuentra en movimiento, no procesamos otro movimiento
    if rospy.get_param("EN_MOVIMIENTO") == True:
	return

    # Pasamos el ángulo de entrada de radianes a grados ya que el motor trabaja con grados
    PAN_new = int(t_new * 180 / math.pi)
    TILT_new = int(p_new * 180 / math.pi)

    # Si el movimiento es menor a un grado para PAN/TILT respecto al último ejecutado, lo descartamos
    # De esta forma evitamos mucho movimiento
    if abs(self.pan_previo - PAN_new) <= 1 and abs(self.tilt_previo - TILT_new) <= 1:
	rospy.set_param("EN_MOVIMIENTO", False)
	return

    # Actualizamos los ángulos con los nuevos enviados
    self.pan_previo = PAN_new
    self.tilt_previo = TILT_new

    # Bloqueamos el movimiento
    rospy.set_param("EN_MOVIMIENTO", True)

    # Mover cabeza robótica
    self.mM.mover(PAN_new, TILT_new)

    # Desbloqueamos movimiento y actualizamos la posición de la cabeza robótica
    #rospy.set_param("PAN_ROBOT", PAN_new)
    #rospy.set_param("TILT_ROBOT", TILT_new)

    # Esperamos un tiempo a que el robot se estabilice. He detectado que cuando el robot está en movimiento 
    # la cámara devuelve imágenes borrosas. Cuando el movimiento termina, la cabeza tiende a moverse un poco
    # debido a la amortiguación del movimiento. Como el reconocimiento facial solo está activo cuando no hay
    # ningún tipo de movimiento, tenemos que esperar un poco antes de reactivar el movimiento.
    rospy.sleep(1)

    rospy.set_param("EN_MOVIMIENTO", False)

    # Aviso de terminación de movimiento
    rospy.loginfo("Se encuentra en movimiento: %s. ", rospy.get_param("EN_MOVIMIENTO"))

  def callbackKalman(self, srKalman):
    self.sKalman = srKalman

    # Cada vez que llega un resultado de Kalman actualizamos los ángulos globales de la
    # cabeza robótica (REVISAR)
    # valores = self.mM.leer()
    # rospy.loginfo("Valores motores " + valores)

  def callbackRecCompetitiva(self, srRedCompetitiva):
    self.sRedCompetitiva = srRedCompetitiva
    self.seguimiento(self.sKalman, self.sRedCompetitiva)

  # wait_for_message(topic, topic_type, timeout=None)

  def callbackAudio(self, audio):
    self.dAudio = audio

def main(args):
  ic = seguimiento()
  rospy.init_node('seguimientoRobot', anonymous=True)
  try:
	rospy.spin()
  except KeyboardInterrupt:
	print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)

