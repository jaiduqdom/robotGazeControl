#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 09:32:37 2019

@author: Jaime Duque Domingo (UVA)

Esta clase permite enviar el movimiento a los servos

"""

import serial, time
import rospy
#import numpy as np
#import math
#from time import time
import struct

class movimientoMotor:

  def __init__(self):
    # Conexión con la placa arduino
    self.arduino = serial.Serial("/dev/ttyUSB0", 115200)
    time.sleep(2)
    self.velocidad = 30
    # Ángulos centrales del robot
    self.P_CENTRAL = 100
    self.T_CENTRAL = 100

  # Inicializa la posición de los sensores
  def inicializar(self):
    self.mover(self.P_CENTRAL, self.T_CENTRAL)


  def recibirArduino(self):
    # Devolvemos la salida como un string según se va produciendo
    salida = ""

    while self.arduino.inWaiting() > 0:
	x = self.arduino.read(1)
	salida = salida + x
	time.sleep(0.001)

    return salida


  def mover(self, p, t):
    # Mueve la cabeza a la posición t, p (en grados)
    self.arduino.flush()
    setTemp1 = str(p)
    setTemp2 = str(t)
    setTemp3 = str(self.velocidad)
    sendMsg = setTemp1 + " " + setTemp2 + " " + setTemp3
    print("Mensaje enviado: " + sendMsg)

    self.arduino.write(sendMsg)

    # Leemos la posición hasta llegar a la indicada. En dicho momento termina el movimiento.
    terminar = False
    tiempo = float(0)

    # Si el tiempo es superior a 4 segundos paramos igualmente
    while terminar == False:
	time.sleep(0.001) # sleep during 1ms
        #print(str(self.arduino.inWaiting()))
        if self.arduino.inWaiting() > 0:
		recMsg = self.recibirArduino()
		print("Mensaje recibido: " + recMsg)
		rM = recMsg.split()
		if len(rM) == 2:
			# Paramos si llegamos al ángulo final
			if int(rM[0]) == p and int(rM[1]) == t:
				terminar = True
	tiempo = tiempo + 0.001
	if tiempo >= 4:
		terminar = True

    #time.sleep(4)
    # recMsg = self.arduino.read(self.arduino.inWaiting())
    # print("Mensaje recibido: " + recMsg)

  def __del__(self):
    # Destrucción del objeto
    self.arduino.close()

if __name__ == '__main__':
    # Creamos objeto movimientoMotor y lo movemos un poco
    mM = movimientoMotor()
    #mM.inicializar()
    # 80 grados en horizontal
    #mM.mover(97, 100)
    #time.sleep(3)

    mM.mover(100, 100)
    time.sleep(3)

    mM.mover(100, 120)
    time.sleep(3)


    """mM.mover(50, 100)
    time.sleep(3)
    mM.mover(150, 100)
    time.sleep(3)
    mM.mover(105, 130)
    time.sleep(3)
    mM.mover(105, 70)
    time.sleep(3)
    mM.mover(105, 100)
    time.sleep(3)"""
    #time.sleep(4)
    #mM.mover(100, 50)
    #time.sleep(4)
    #mM.mover(164, 100)
    #time.sleep(4)
    #time.sleep(4)
    #mM.mover(84, 100)
    del mM

