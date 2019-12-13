# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 15:15:55 2019

@author: Jaime Duque Domingo (UVA)

Implementación del filtro de Kalman

"""
import numpy as np
import matplotlib.pyplot as plt
from random import randint, uniform,random

#**************************************************
# Función de proceso de movimiento de una cara
# estado Xk=[x,y]
# T periodo de muestreo
#**************************************************
def proceso(Xk_ant):
    Xk = np.zeros(2)
    Xk[0] = Xk_ant[0]
    Xk[1] = Xk_ant[1]
    return Xk

#**************************************************
# Función de propagación
#**************************************************
def propaga(Xk, Pk, T):
    A=[[1,0],[0,1]]
    Pk = A*Pk*np.traspose(A)
    return np.traspose(Xk), Pk
 
#**************************************************
# Función de actualización
#**************************************************
def actualiza(Xk,Pk,Hk,Zk,Zek,R,V):
    I=[[1, 0],[0, 1]]
    K=Pk*np.traspose(Hk)*np.linalg.inv(Hk*Pk*np.traspose(Hk)+V*R*np.traspose(V))
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
    Xk=np.traspose([x y])
    Xkreal=Xk

    Pk=[[1, 0], [0, 1]]
    Q=[[0.01, 0],[0, 0.01]]

    Hk=[[1, 0],[0, 1]]
    V=[[1, 0],[0, 1]]
    R=[[desv_xy**2, 0],[0, desv_xy**2]]

    # Salvar valores
    XF=np.zeros((Npasos, 2))
    ZF=np.zeros((Npasos, 2))
    XFreal=np.zeros((Npasos, 2))
    nmedidas=0

    # Trayectoria estimada por filtro despues propagación y actualización si existe
    XF[1]=np.traspose(Xk)
    # Trayectoria Real
    XFreal[1]=np.traspose(Xkreal)

    for k in range(1, Npasos):
	Xkreal=np.traspose(proceso(Xkreal,T));
        Xk_ant,Pk_ant=propaga(Xk,Pk,T);
   
	if k % Nciclos == 0:
		# Llega medida
   		# Zk=observa(Xkreal);
   		Zk = Xkreal + np.array([random() * 10, random() * 10])
		# Observaciones estimadas
      		Zek=Xk_ant   
      		Xk,Pk = actualiza(Xk_ant,Pk_ant,Hk,Zk,Zek,R,V);
      		ZF[k] = np.traspose(Zk)
		nmedidas=nmedidas+1;
	else:
		Xk=Xk_ant 
		Pk=Pk_ant
	
	# Guarda resultados
        # Trayectoria estimada por filtro despues propagación y actualización si existe
	XF[k] = np.traspose(Xk)
	# Trayectoria real
	XFreal[k] = np.traspose(Xkreal)

    #**************************************************
    # Representación gráfica
    #**************************************************
    plt.ion()

    # Creamos una figura con 3 gráficos: Valor de entrada, red habituación y red competitiva
    fig, ax = plt.subplots(nrows=1, ncols=1)

    figure(1);
    plt.plot(XF[:,1:1],XF[:,2:2],'r--',ZF[:,1:1],ZF[:,2:2],'r+',XFreal[:,1:1],XFreal[:,2:2],'g--')
    plt.title('Posicion x-y')
    plt.legend('Estimación','Medida','Real')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

if __name__== "__main__":
  filtroKalman()


