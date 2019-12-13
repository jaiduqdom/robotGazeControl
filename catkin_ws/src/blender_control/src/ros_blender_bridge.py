#!/usr/bin/env python

'''
----------------------------------
Modulo ros_blender bridge

Descripcion:
  - Cliente conexion ROS - Blender

Realizado:   14 de enero 2017  
Modificado:  14 de junio 2017 
Revisado:    14 de junio 2017

Notas:

----------------------------------
'''

import rospy
import socket 
import time
import sys

# mensaje lista de unidades de accion
from avatar_msg.msg import AUlist

# posicion del rostro inicial
rostro = { 'AU0': 1, 'AU1': 1, 'AU2': 1, 'AU4': 1, 'AU5': 1, 'AU6': 1, 'AU7': 1, 'AU9': 1, 'AU10': 1, 'AU12': 1, 'AU15': 1, 'AU26': 1, 'AU45': 1, 'AU51': 1, 'AU52': 1, 'AU53': 1, 'AU54': 1, 'AU61': 1, 'AU62': 1, 'AU63': 1, 'AU64': 1}	

# conexion ROS-Blender
def conectarse_blender():

	ip = "127.0.0.1"
	port = 52248
	server_adress = ('localhost',52248)   
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	connected = 0

	while connected == 0: #esperamos a que se conecte el servidor
		try:
			sock.connect(server_adress)
			connected = 1	
			print "ROS conectado con exito"	
		except socket.error, msg:
			print("error code: " + str(msg[0]) + " Message " + msg[1])
	return sock

# separa unidades de accion
def split_aus(arr, size):

	arrs = []
	while len(arr) > size:
		pice = arr[:size]
		arrs.append(pice)
		arr = arr[size:]
	arrs.append(arr)
	return arrs

# construye el mensaje para blender y lo envia
def enviar_blender(msg):   
 
	global sock, rostro
        c = ""
        aus = split_aus(msg.au,2)
        print msg
        print "----------------------"
        for au in aus:
            # se transforma en un mensaje del tipo (au1, start1, end1, tiempo1),(au2, start2, end2, tiempo2)......
            # la intensidad maxima de 5 (e de acuerdo al FACS) se transforma en el fotograma 10
            c = c + str([int(au[0]), rostro['AU'+str(int(au[0]))], int(msg.it * au[1] * 10), msg.tt]) + ","
            rostro['AU'+str(int(au[0]))] = int(msg.it * au[1] * 10) #actualiza el valor en la matriz del rostro
        c = c[:-1] #quito la ultima coma
        c = "[" + c + "]"
        print c #imprime el mensaje enviado
        print "----------------------"        
	sock.send(c.encode())
        c = "" #reinicia el mensaje


if __name__ == '__main__':

	global sock
	rospy.init_node('blender', anonymous=True)
	print "Nodo creado"
	sock = conectarse_blender() # se conecta al servidor
	sub = rospy.Subscriber('topic_au', AUlist, enviar_blender, queue_size=1)
	rospy.spin()
