#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 09:32:37 2019

@author: Jaime Duque Domingo (UVA)

Esta clase permite publicar expresiones en el avatar

"""

import rospy
import numpy as np
import math
import yaml
import optparse
import threading
from optparse import OptionParser
from avatar_msg.msg import expresion
from time import time

class comportamiento:

  def __init__(self):
    # Constantes de expresiones
    self.NEUTRAL = "neutra"
    self.ALEGRIA = "alegria"
    self.TRISTEZA = "tristeza"
    self.SORPRESA = "sorpresa"
    self.DISGUSTO = "disgusto"
    self.IZQUIERDA = "mirar_izquierda"
    self.DERECHA = "mirar_derecha"
    self.PARPADEO = "parpadeo"
    self.ALEGRIA_DERECHA = "alegria_derecha"
    self.ALEGRIA_IZQUIERDA = "alegria_izquierda"

    # Semáforo que indica si estamos mostrando una expresión. Si estamos mostrando una
    # expresión, no podemos mostrar otra.
    # self.activo = False

    # Cargamos la relación de expresiones en memoria a partir del fichero yaml
    archivo_expresiones = str(rospy.get_param("EXPRESIONES_AVATAR")).strip()
    assert archivo_expresiones != None, "Fichero de expresiones no encontrado."
    # Utilizamos el fichero yaml
    stream = open(archivo_expresiones)
    self.expresiones = yaml.load(stream)
    assert len(self.expresiones) > 0, "No se han encontrado expresiones válidas."
    stream.close()

    # Creamos el publicador de expresiones vacío. Se rellena desde la clase padre
    self.pubExpresion = rospy.Publisher("topic_expresion", expresion, queue_size=1)

  def worker(self, ep, au_ext, it, tt, te, ep_n, au_ext_n, it_n, tt_n, te_n):
    # Publicamos dos mensajes separados por un tiempo de espera especificado en segundos
    # De esta manera damos tiempo para terminar la animación
    # El primer mensaje indica la expresión a mostrar. El segundo mensaje indica la
    # expresión neutra para devolver al avatar a su situación de reposo

    self.pubExpresion.publish(ep, au_ext, it, tt) 
    # rospy.sleep(0.01)
    rospy.sleep(te)
    self.pubExpresion.publish(ep_n, au_ext_n, it_n, tt_n) 
    rospy.sleep(te_n)
    #rospy.sleep(4)

    # Esperamos 10 segundos para permitir otro movimiento ya que de lo contrario queda
    # muy repetitivo
    # rospy.sleep(10)
    # Reactivamos las animaciones al terminar el worker
    # Esperamos también el tiempo de la animación. Utilizamos aproximadamente 4 segundos para todas las animaciones.
    rospy.sleep(4)
    rospy.set_param("AVATAR_ACTIVO", False)
    # self.activo = False

  def workerCompuesto(self, ep1, au_ext1, it1, tt1, te1, ep2, au_ext2, it2, tt2, te2, ep_n, au_ext_n, it_n, tt_n, te_n):
    # Publicamos dos mensajes separados por un tiempo de espera especificado en segundos
    # De esta manera damos tiempo para terminar la animación
    # El primer mensaje indica la expresión a mostrar. El segundo mensaje indica la
    # expresión neutra para devolver al avatar a su situación de reposo

    self.pubExpresion.publish(ep2, au_ext2, it2, tt2) 
    rospy.sleep(0.2)
    self.pubExpresion.publish(ep1, au_ext1, it1, tt1) 
    rospy.sleep(te1)
    self.pubExpresion.publish(ep_n, au_ext_n, it_n, tt_n) 
    rospy.sleep(te_n)

    # Reactivamos las animaciones al terminar el worker
    # Esperamos también el tiempo de la animación. Utilizamos aproximadamente 4 segundos para todas las animaciones.
    rospy.sleep(4)
    rospy.set_param("AVATAR_ACTIVO", False)


  def buscarExpresion(self, expresion):
    # Devuelve los valores de una expresión
    for i in range(len(self.expresiones)):
	a = self.expresiones['esp_'+str(i)]
	ep = a['expresion']
	if ep.strip() == expresion.strip():
		au_ext = a['ua_extras']
		it = a['intensidad_total']
		tt = a['tiempo_total']
		te = a['tiempo_espera']
		return ep, au_ext, it, tt, te
    return None

  def publicarExpresion(self, expresion):
    # rospy.loginfo(self.activo)
    # if self.activo == False:
    # Comprobamos semáforo
    if rospy.get_param("AVATAR_ACTIVO") == False:
	# rospy.loginfo("ENTRAMOS")
	# Bloqueamos las animaciones
	# self.activo = True
        rospy.set_param("AVATAR_ACTIVO", True)
	# Busca la expresión que le indicamos
	ep, au_ext, it, tt, te = self.buscarExpresion(expresion)
	# Busca la expresión neutra. La llamamos después de cada expresión.
	ep_n, au_ext_n, it_n, tt_n, te_n = self.buscarExpresion(self.NEUTRAL)
	# Creamos un hilo de ejecución donde se mostrará la expresión
	# De esta manera no bloqueamos el proceso normal de ejecución

	if expresion == self.PARPADEO:
		tt_n = 7

	if expresion == self.IZQUIERDA or expresion == self.DERECHA:
		te_n = 7

	t = threading.Thread(target=self.worker, args=(ep, au_ext, it, tt, te, ep_n, au_ext_n, it_n, tt_n, te_n))
	t.start()
	# rospy.loginfo("SALIMOS")

  def publicarExpresionCompuesta(self, expresion):
    # Comprobamos semáforo
    if rospy.get_param("AVATAR_ACTIVO") == False:
	# Bloqueamos las animaciones
        rospy.set_param("AVATAR_ACTIVO", True)
	# Busca la expresión que le indicamos
	if expresion == self.ALEGRIA_DERECHA:
		ep1, au_ext1, it1, tt1, te1 = self.buscarExpresion(self.ALEGRIA)
		ep2, au_ext2, it2, tt2, te2 = self.buscarExpresion(self.DERECHA)
	if expresion == self.ALEGRIA_IZQUIERDA:
		ep1, au_ext1, it1, tt1, te1 = self.buscarExpresion(self.ALEGRIA)
		ep2, au_ext2, it2, tt2, te2 = self.buscarExpresion(self.IZQUIERDA)

	# Busca la expresión neutra. La llamamos después de cada expresión.
	ep_n, au_ext_n, it_n, tt_n, te_n = self.buscarExpresion(self.NEUTRAL)

	if expresion == self.ALEGRIA_IZQUIERDA or expresion == self.ALEGRIA_DERECHA:
		te_n = 7

	# Creamos un hilo de ejecución donde se mostrará la expresión
	# De esta manera no bloqueamos el proceso normal de ejecución
	t = threading.Thread(target=self.workerCompuesto, args=(ep1, au_ext1, it1, tt1, te1, ep2, au_ext2, it2, tt2, te2, ep_n, au_ext_n, it_n, tt_n, te_n))
	t.start()

  def mostrarAlegre(self):
    # Muestra alegría en el avatar
    self.publicarExpresion(self.ALEGRIA)

  def mirarDerechaAlegre(self):
    # Muestra alegría en el avatar y mira a la derecha
    self.publicarExpresionCompuesta(self.ALEGRIA_DERECHA)

  def mirarIzquierdaAlegre(self):
    # Muestra alegría en el avatar y mira a la izquierda
    self.publicarExpresionCompuesta(self.ALEGRIA_IZQUIERDA)

  def mostrarTriste(self):
    # Muestra tristeza en el avatar
    self.publicarExpresion(self.TRISTEZA)

  def mostrarNeutral(self):
    # Muestra expresión neutra
    self.publicarExpresion(self.NEUTRAL)

  def mirarDerecha(self):
    # Mueve los ojos a la derecha
    self.publicarExpresion(self.DERECHA)

  def mirarIzquierda(self):
    # Mueve los ojos a la izquierda
    self.publicarExpresion(self.IZQUIERDA)

  def realizarParpadeo(self):
    # Realizar un parpadeo
    self.publicarExpresion(self.PARPADEO)

