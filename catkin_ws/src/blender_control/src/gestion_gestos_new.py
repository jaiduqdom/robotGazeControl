#!/usr/bin/env python

'''
----------------------------------
Modulo gestion de gestos

Descripcion:
  - Recibe expresiones y envia unidades de accion

Realizado:   14 de enero 2017  
Modificado:  14 de junio 2017 
Revisado:    14 de junio 2017

Notas:

----------------------------------
'''

import rospy
import curses
import socket 
import time
import sys
import yaml

from avatar_msg.msg import AUlist
from avatar_msg.msg import expresion

stream = open(str(rospy.get_param("GESTOS_AVATAR", "../cfg/gestos4_12.yaml")).strip())
data = yaml.load(stream)
stream.close()

# publica la it, tt, y unidades de accion
def handle_exp(req):
        # se llama el diccionario de gestos del archivo yaml
        global pub

        # publica la expresion deseada
        # options = [data]
        expr = data[req.exp]
        action_units = list(expr['aus']) + list(req.au_ext) # se suma las unidades de accion a las de la expresion base
        print action_units
        pub.publish(req.it, req.tt, action_units)

# creacion del nodo
def gestion_gestos():
        global pub
        rospy.init_node('gestion_gestos', anonymous=True)
        print "Nodo gestion gestos creado"
        pub = rospy.Publisher('topic_au', AUlist, queue_size=1)
        sub = rospy.Subscriber("topic_expresion",expresion,handle_exp,queue_size=1)
        rospy.spin()        

if __name__ == '__main__':
	try:
		gestion_gestos()
	except rospy.ROSInterruptException:
		pass
