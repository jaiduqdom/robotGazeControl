#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 09:32:37 2019

@author: Jaime Duque Domingo (UVA)

Esta clase permite enviar el movimiento a los servos

"""

import serial, time
import rospy
import struct

class movimientoMotor:

  def __init__(self):
    # Conexión con la placa arduino
    self.arduino = serial.Serial("/dev/ttyUSB0", 115200)
    time.sleep(2)
    self.velocidad = rospy.get_param("VELOCIDAD_CABEZA", 25)
    # Ángulos centrales del robot
    self.P_CENTRAL = rospy.get_param("ANGULO_PAN_CENTRAL", 100)
    self.T_CENTRAL = rospy.get_param("ANGULO_TILT_CENTRAL", 100)
    # Ángulos máximos
    self.P_MAX = rospy.get_param("ANGULO_MAXIMO_PAN", 160)
    self.T_MAX = rospy.get_param("ANGULO_MAXIMO_TILT", 160)

    # Inicializa la posición de los sensores
    self.mover(self.P_CENTRAL, self.T_CENTRAL)

    # Actualizamos la variable de la posición del motor al lugar central
    rospy.set_param("PAN_ROBOT", rospy.get_param("ANGULO_PAN_CENTRAL"))
    rospy.set_param("TILT_ROBOT", rospy.get_param("ANGULO_TILT_CENTRAL"))    

    # self.mover(100, self.T_CENTRAL)

  def recibirArduino(self):
    # Devolvemos la salida como un string según se va produciendo
    # En el puerto serie se recibe de byte en byte por lo que tenemos
    # que agrupar la salida leyendo poco a poco
    salida = ""

    while self.arduino.inWaiting() > 0:
	x = self.arduino.read(1)
	salida = salida + x
	time.sleep(0.001)

    return salida

  def mover(self, p, t):
    rospy.loginfo("Moviendo: " + str(p) + ", " + str(t))
    # El ángulo p está invertido
    #if p > self.P_CENTRAL:
    #	p = self.P_CENTRAL - (p - self.P_CENTRAL)
    #else:
    #	if p < self.P_CENTRAL:
    #		p = self.P_CENTRAL + (self.P_CENTRAL - p)

    # Control de valores máximos y mínimos
    if p > (self.P_CENTRAL + self.P_MAX / 2):
	p = (self.P_CENTRAL + self.P_MAX / 2)
    if p < (self.P_CENTRAL - self.P_MAX / 2):
	p = (self.P_CENTRAL - self.P_MAX / 2)

    if t > (self.T_CENTRAL + self.T_MAX / 2):
	t = (self.T_CENTRAL + self.T_MAX / 2)
    if t < (self.T_CENTRAL - self.T_MAX / 2):
	t = (self.T_CENTRAL - self.T_MAX / 2)

    #test
    #p=150
    #t=100

    rospy.loginfo("Moviendo: " + str(p) + ", " + str(t))

    # Mueve la cabeza a la posición t, p (en grados)
    # self.arduino.flush()
    setTemp1 = str(p)
    setTemp2 = str(t)
    setTemp3 = str(self.velocidad)
    sendMsg = setTemp1 + " " + setTemp2 + " " + setTemp3
    rospy.loginfo("Mensaje enviado: " + sendMsg)

    self.arduino.flush()
    self.arduino.write(sendMsg)
    self.arduino.flush()

    # Leemos la posición hasta llegar a la indicada. En dicho momento termina el movimiento.
    terminar = False
    tiempo = float(0)

    # Si el tiempo es superior a 4 segundos paramos igualmente
    while terminar == False:
	time.sleep(0.001) # sleep during 1ms
	# Cuando se recibe algo en el serie lo leemos completamente
        if self.arduino.inWaiting() > 0:
		recMsg = self.recibirArduino()
		rospy.loginfo("Mensaje recibido: " + recMsg)
		rM = recMsg.split()
		if len(rM) == 2:
			# Actualizamos las variables de los ángulos del robot
			rospy.set_param("PAN_ROBOT", int(rM[0]))
			rospy.set_param("TILT_ROBOT", int(rM[1]))
			# Paramos si llegamos al ángulo final
                        time.sleep(0.002) # sleep during 2ms
			if self.arduino.inWaiting() == 0 and int(rM[0]) == p and int(rM[1]) == t:
				terminar = True
	tiempo = tiempo + 0.001
	# Ponemos un límite de tiempo al movimiento para no poderse bloquear en ninguna situación
	# , como por ejemplo un problema de lectura del puerto serie
	if tiempo >= 4:
		terminar = True

    self.arduino.flush()
    time.sleep(0.002) # sleep during 2ms

    # Esperamos 4 segundos
    # time.sleep(4)
    # recMsg = self.arduino.read(self.arduino.inWaiting())

  #def leer(self):
  #  return self.arduino.read(self.arduino.inWaiting())

  def __del__(self):
    # Destrucción del objeto
    self.arduino.close()

