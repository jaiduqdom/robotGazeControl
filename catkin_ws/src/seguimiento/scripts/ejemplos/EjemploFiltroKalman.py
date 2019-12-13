#!/usr/bin/env python
# -*- coding: utf-8 -*-
# license removed for brevity
import rospy
import numpy as np
import matplotlib.pyplot as plt
import sys
from random import random

#**************************************************
# Función de proceso de movimiento de una cara
# estado Xk=[x,y]
# T periodo de muestreo
#**************************************************
def proceso(Xk_ant):
    return Xk_ant

#**************************************************
# Función de propagación
#**************************************************
def propaga(Xk, Pk, T):
    A=np.matrix([[1,0],[0,1]])
    Pk = A*Pk*np.transpose(A)
    return np.transpose(Xk), Pk
 
#**************************************************
# Función de actualización
#**************************************************
def actualiza(Xk,Pk,Hk,Zk,Zek,R,V):
    I=np.matrix([[1, 0],[0, 1]])
    K=Pk*np.transpose(Hk)*np.linalg.inv(Hk*Pk*np.transpose(Hk)+V*R*np.transpose(V))
    Xk=Xk+K*(Zk-Zek);
    Pk=(I-K*Hk)*Pk;
    return Xk, Pk

#**************************************************
# Función de observación
#**************************************************
def observa(Xk):
    Zk=Xk
    return Zk

#**************************************************
# Implementamos el filtro de Kalman
#**************************************************
def filtroKalman():
    # Proceso del sistema
    Npasos=1200

    # Paso de tiempo
    T=0.1

    # Cada cuántos ciclos se recibe una medidad
    Nciclos=50

    # Condiciones iniciales
    x=0
    y=0

    # Desviación error
    desv_xy=0.01

    # Estado
    Xk = np.transpose(np.matrix([x, y]))
    Xkreal = Xk

    Pk = np.matrix([[1, 0], [0, 1]])
    Hk = np.matrix([[1, 0], [0, 1]])
    V = np.matrix([[1, 0], [0, 1]])
    R = np.matrix([[desv_xy**2, 0],[0, desv_xy**2]])

    # Salvar valores
    XF = np.zeros((Npasos, 2))
    ZF = np.zeros((Npasos, 2))
    XFreal = np.zeros((Npasos, 2))
    nmedidas=0

    # Trayectoria estimada por filtro despues propagación y actualización si existe
    XF[1,:] = np.transpose(Xk).ravel()
    
    # Trayectoria Real
    XFreal[1,:]=np.transpose(Xkreal).ravel()

    for k in range(1, Npasos):

        Xkreal = np.transpose(proceso(Xkreal))
        
        Xk_ant,Pk_ant = propaga(Xk,Pk,T)
   
        if (k % Nciclos == 0):
            # Llega medida
            # Observaciones reales van a Xkreal y Zk
            Zk = Xkreal + np.array([[random() * 10], [random() * 10]])

            # Observaciones estimadas
            Zek=Xk_ant   
            Xk,Pk = actualiza(Xk_ant,Pk_ant,Hk,Zk,Zek,R,V)
            ZF[k,:] = np.transpose(Zk).ravel()
            nmedidas=nmedidas+1
        else:
            Xk=Xk_ant 
            Pk=Pk_ant
        
        # Guarda resultados
        # Trayectoria estimada por filtro despues propagación y actualización si existe
        XF[k,:] =  np.transpose(Xk).ravel()
        XFreal[k,:] = np.transpose(Xkreal).ravel()

    #**************************************************
    # Representación gráfica
    #**************************************************
    plt.ion()

    # Creamos una figura con 3 gráficos: Valor de entrada, red habituación y red competitiva
    fig, ax = plt.subplots(nrows=1, ncols=1)
    plt.plot(XF[:,0],XF[:,1],'r--', label = 'Estimacion')
    plt.plot(ZF[:,0],ZF[:,1],'r+', label = 'Medida')
    plt.plot(XFreal[:,0],XFreal[:,1],'g--', label = 'Real')   
    plt.legend()
    plt.title('Posicion x-y')
    #plt.legend('Estimación','Medida','Real')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()
    plt.pause(0.02)

    salir = False
    while salir == False:
	tecla = sys.stdin.read(1)
	if tecla == 'q':
		salir = True

if __name__== "__main__":
  filtroKalman()

