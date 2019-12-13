#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 09:32:37 2019

@author: Jaime Duque Domingo (UVA)

Esta clase permite hacer un test del comportamiento del avatar

"""

import rospy
import sys
from comportamiento import comportamiento
from time import time
import threading

class testComportamiento:

  def __init__(self):
    ########################################################################################
    # Inicialización de las expresiones del avatar
    ########################################################################################
    self.avatar = comportamiento()
    rospy.sleep(1.0)
    rospy.set_param("AVATAR_ACTIVO", False)

  def worker(self):
    tiempo = time()
    # Expresiones de prueba
    # self.avatar.mostrarAlegre()
    # self.avatar.mostrarTriste()
    self.avatar.mirarDerecha()
    # self.avatar.mirarIzquierdaAlegre()
    # self.avatar.realizarParpadeo()
    print("Tiempo en caras = " + str(time() - tiempo))

  def procesar(self):
    t = threading.Thread(target=self.worker, args=())
    t.start()

def main(args):
  rospy.init_node('testComportamiento', anonymous=True)

  ic = testComportamiento()

  # Ratio de proceso de 20 imágenes por segundo
  rate = rospy.Rate(20) # 20hz

  tiempo = time()

  while not rospy.is_shutdown():

	if time() - tiempo > 10:
		# cada 10 segundos
		ic.procesar()
		tiempo = time()

        rate.sleep()

if __name__ == '__main__':
    main(sys.argv)


