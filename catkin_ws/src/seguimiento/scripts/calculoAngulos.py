#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 09:32:37 2019

@author: Jaime Duque Domingo (UVA)

Esta clase permite obtener el cálculo de los ángulos de la cabeza robótica

"""

import rospy
import numpy as np
import math
from time import time

class calculoAngulos:

  def __init__(self):
    # FOV de la cámara (calculado manualmente)
    self.FOV_H = float(rospy.get_param("FOV_HORIZONTAL", 80))
    self.FOV_V = float(rospy.get_param("FOV_VERTICAL", 100))

    # Ancho de la imagen
    self.width = float(rospy.get_param("ANCHO_IMAGEN", 640))

    # Alto de la imagen
    self.height = float(rospy.get_param("ALTO_IMAGEN", 480))

    # Buscamos el ángulo del robot. Si no existe lo iniciamos al central
    """t = rospy.get_param("PAN_ROBOT", 99999)
    if t == 99999:
	rospy.set_param("PAN_ROBOT", rospy.get_param("ANGULO_PAN_CENTRAL"))
    p = rospy.get_param("TILT_ROBOT", 99999)
    if p == 99999:
	rospy.set_param("TILT_ROBOT", rospy.get_param("ANGULO_TILT_CENTRAL"))"""

  #######################################################################################################
  # Realiza el cálculo del nuevo ángulo del robot a partir de la posición de la cara y el ángulo anterior
  # del robot  
  # (x,y): Centro de la cara de la persona en la imagen.  
  # (t_new,p_new):(PAN,TILT): Ángulo nuevo donde está la cara
  #######################################################################################################
  def calcularAngulos(self, x, y):
    # (t,p):(PAN,TILT): Ángulo actual de la cabeza robótica
    # El ángulo del robot está centrado en la imagen. Llevamos sus valores al extremo superior izquierdo para 
    # calcular el ángulo real de la persona (utilizamos las variables globales de la posición del robot)    
    t = float(rospy.get_param("PAN_ROBOT", rospy.get_param("ANGULO_PAN_CENTRAL")))
    p = float(rospy.get_param("TILT_ROBOT", rospy.get_param("ANGULO_TILT_CENTRAL")))

    # rospy.loginfo("Ángulos robot: (%f, %f)", t, p)
    # rospy.loginfo("Valores (x, y): (%f, %f)", x, y)

    # Constantes utilizadas en función del FOV de la cámara
    t_new = (t - float(self.FOV_H) / 2) + ((float(self.width) - float(x)) * float(self.FOV_H) / float(self.width))
    p_new = (p - float(self.FOV_V) / 2) + (float(y) * float(self.FOV_V) / float(self.height))

    # Pasamos los ángulos a radianes
    t_new = float(t_new) * math.pi / float(180)
    p_new = float(p_new) * math.pi / float(180)

    return t_new, p_new
  #######################################################################################################

  #######################################################################################################
  # Realiza el cálculo inverso para obtener las coordenadas a partir del ángulo actual del robot y del 
  # nuevo ángulo a buscar (normalmente retornado por Kalman)
  # (x,y): Centro de la cara de la persona en la imagen.  
  # (t_new,p_new):(PAN,TILT): Ángulo nuevo donde está la cara
  #######################################################################################################
  def calcularCoordenadas(self, t_new, p_new):
    # Pasamos de radianes a grados. El filtro de Kalman lo guarda en radianes
    t_n = t_new * float(180) / math.pi
    p_n = p_new * float(180) / math.pi

    # (t,p):(PAN,TILT): Ángulo actual de la cabeza robótica 
    # El ángulo del robot está centrado en la imagen. Llevamos sus valores al extremo superior izquierdo para 
    # calcular el ángulo real de la persona (utilizamos las variables globales de la posición del robot)   
    t = float(rospy.get_param("PAN_ROBOT", rospy.get_param("ANGULO_PAN_CENTRAL")))
    p = float(rospy.get_param("TILT_ROBOT", rospy.get_param("ANGULO_TILT_CENTRAL")))

    # Constantes utilizadas del FOV de la cámara (campo de visión)
    x = int(self.width - (float(self.width) * (t_n - (t - float(self.FOV_H) / 2)) / float(self.FOV_H)))
    y = int(float(self.height) * (p_n - (p - float(self.FOV_V) / 2)) / float(self.FOV_V))
    return x, y
  #######################################################################################################

