#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 09:32:37 2019

@author: Jaime Duque Domingo (UVA)

Esta clase permite enviar el movimiento a los servos

"""

import time
import math
import struct


"""
214
421


t_new=1.50098315672
p_new=2.44346095279



t = 1.50098315672
p = 2.44346095279
x = 432
y = 52

"""


class angulos:




  #######################################################################################################
  # Realiza el cálculo del nuevo ángulo del robot a partir de la posición de la cara y el ángulo anterior
  # del robot  
  # (x,y): Centro de la cara de la persona en la imagen.  
  # (t_new,p_new):(PAN,TILT): Ángulo nuevo donde está la cara
  #######################################################################################################
  def calcularAngulos(self, x, y):
    t = float(100)
    p = float(100)
    FOV_H = float(80)
    FOV_V = float(107)

    # Constantes utilizadas en función del FOV de la cámara
    t_new = (t - FOV_H / 2) + (x * FOV_H / float(640))
    p_new = (p - FOV_V / 2) + (y * FOV_V / float(480))

    t_new = t_new * math.pi / float(180)
    p_new = p_new * math.pi / float(180)

    print("t_new=" + str(t_new))
    print("p_new=" + str(p_new))


    return t_new, p_new
  #######################################################################################################

  #######################################################################################################
  # Realiza el cálculo inverso para obtener las coordenadas a partir del ángulo actual del robot y del 
  # nuevo ángulo a buscar (normalmente retornado por Kalman)
  # (x,y): Centro de la cara de la persona en la imagen.  
  # (t_new,p_new):(PAN,TILT): Ángulo nuevo donde está la cara
  #######################################################################################################

  def calcularCoordenadas(self, t_new, p_new):
    # (t,p):(PAN,TILT): Ángulo actual de la cabeza robótica
    # El ángulo del robot está centrado en la imagen. Llevamos sus valores al extremo superior izquierdo para 
    # calcular el ángulo real de la persona (utilizamos las variables globales de la posición del robot)    

    # Pasamos de radianes a grados. El filtro de Kalman lo guarda en radianes
    t_n = t_new * float(180) / math.pi
    p_n = p_new * float(180) / math.pi
 
    # El ángulo del robot está centrado en la imagen. Llevamos sus valores al extremo superior izquierdo para 
    # calcular el ángulo real de la persona (utilizamos las variables globales de la posición del robot)   
    t = float(100)
    p = float(100)

    FOV_H = float(80)
    FOV_V = float(107)

    # Constantes utilizadas del FOV de la cámara (campo de visión)
    x = int(float(640) * (t_n - (t - FOV_H / 2)) / FOV_H)
    y = int(float(480) * (p_n - (p - FOV_V / 2)) / FOV_V)

    #x = int(-1 * (640 / FOV_H) * (t_new - t + FOV_H / 2))
    #y = int(-1 * (480 / FOV_V) * (p_new - p + FOV_V / 2))
    return x, y
  #######################################################################################################



if __name__ == '__main__':
    # Creamos objeto movimientoMotor y lo movemos un poco
    a = angulos()
    t, p = a.calcularAngulos(214, 421)
    print( "t = " + str(t))
    print( "p = " + str(p))

    x, y = a.calcularCoordenadas(t, p)
    print( "x = " + str(x))
    print( "y = " + str(y))

