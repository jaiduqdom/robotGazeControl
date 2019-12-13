#!/usr/bin/env python
import rospy
import numpy as np
from camara.msg import ArrayFloat

# Parametro de neuronas de la red
NEURONAS = 3

# Vector de estimulos de entrada
I = np.zeros(NEURONAS + 1)

def callback(data):
    global I
    I = data.data
    rospy.loginfo(rospy.get_caller_id() + "Estimulos de entrada =  %s", data.data)
    
def redcompetitiva():
    global I

    # Parametro de frecuencia (diferenciacion)
    FRECUENCIA = 10

    # Parametros utilizados en la red competitiva
    A = 0.6
    B = 1
    C = 1
    D = 20
    n = NEURONAS
    h = 1.0 / FRECUENCIA

    # Vectores de estado anterior de la red competitiva
    x = np.zeros(NEURONAS + 1)
    ft = np.zeros(NEURONAS + 1)
    ft_ant = np.zeros(NEURONAS + 1)
    x_ant = np.zeros(NEURONAS + 1)

    # Iniciar nodo
    rospy.init_node('redCompetitiva', anonymous=True)
    rospy.Subscriber("entradaRedCompetitiva", ArrayFloat, callback)
    pub = rospy.Publisher('salidaRedCompetitiva', ArrayFloat, queue_size=10)

    # Frecuencia de procesamiento
    rate = rospy.Rate(FRECUENCIA)

    salida = ArrayFloat()

    while not rospy.is_shutdown():
	# Algoritmo de red competitiva    
        ft_ant = ft
        x_ant = x    

        for k in range(1, n + 1):
	   suma = 0
	   for l in range(1, n + 1):
	      if k != l:
	         # mas rapida que lineal
	         suma = suma + D * x[l]**2
	         # lineal: suma = suma + x[l]
	
	   # mas rapida que lineal
	   ft[k] = -A*x[k] + C*(B-x[k])*(I[k])-x[k]*suma
	   # lineal: ft[k] = -A*x[k] + C*(B-x[k])*(I[k]+D * x[k]**2)-x[k]*suma
	
	   x[k] = x_ant[k] + (ft[k] + ft_ant[k]) * h / 2

	# Anadir time stamp
	salida.header.stamp = rospy.Time.now()
	# Datos de salida
	salida.data = x
	# Publicamos y escribimos la salida
        rospy.loginfo(salida)
        pub.publish(salida)
        rate.sleep()

if __name__ == '__main__':
    redcompetitiva()
