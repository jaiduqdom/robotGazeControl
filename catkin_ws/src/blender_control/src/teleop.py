#!/usr/bin/env python

'''
----------------------------------
Modulo joystick

Descripcion:
  - Recibe datos de joy y los pasa al avatar

Realizado:   14 de enero 2017  
Modificado:  14 de junio 2017 
Revisado:    14 de junio 2017

Notas:

------------------------------------
'''

import rospy
import time

from sensor_msgs.msg import Joy
from avatar_msg.msg import AUlist
from avatar_msg.msg import expresion

def nodo_joy(joy):
    global aus
 
    # nodo de unidades de accion
    # botones
    if joy.buttons[0]:
      aus += [1, 5]
    if joy.buttons[1]:
      aus += [1, 5]
    if joy.buttons[2]:
      aus += [2, 5]
    if joy.buttons[3]:
      aus += [45, 5]
    if joy.buttons[4]:
      aus += [61, 5]
    if joy.buttons[5]:
      aus += [62, 5]
    if joy.buttons[6]:
      aus += [51, 5]
    if joy.buttons[7]:
      aus += [52,5]


    if len(aus) == 0:
        pub.publish(1, 0,[0, 1])
    else:	
        pub.publish(1, 0, aus)	
        aus = []

if __name__ == '__main__':
  global aus
  aus = []
  rospy.init_node('teleop')

  # el nodo de teleoperacion se conecta con el gestor de expresiones y el modulo de unidades de accion
  sub = rospy.Subscriber("joy", Joy, nodo_joy)
  pub = rospy.Publisher("topic_au", AUlist, queue_size=1)
  pub_2 = rospy.Publisher("topic_expresion", expresion, queue_size=1)
  rospy.spin()
