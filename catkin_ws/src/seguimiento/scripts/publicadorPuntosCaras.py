#!/usr/bin/env python
# -*- coding: utf-8 -*-
# license removed for brevity
"""
Created on Tue Jul  23 10:28:23 2019

@author: Jaime Duque Domingo UVA

Investigación sobre la orientación de cabeza robótica
Obtención de puntos de la cara utilizando librería DLIB

Este nodo obtiene la imagen con OpenCV, la transforma en grises y la reduce, a continuación
la procesa con DLIB para obtener los puntos característicos de la cara. Finalmente publica el 
resultado en el topic puntosCara, un mensaje de tipo Caras:

Header header
sensor_msgs/Image imagen
int32 numeroCaras
int32[] x1
int32[] y1
int32[] x2
int32[] y2
int32[] puntoX
int32[] puntoY
int32[] indiceCara

donde (x1[c],y1[c])-(x2[c],y2[c]) definen el rectángulo de la cara para cada cara "c" devuelta
y (puntoX[68*c + i], puntoY[68*c + i]) definen el punto característico "i" DLIB para cada 
cara "c"

Más información en:
http://wiki.ros.org/cv_bridge/Tutorials/ConvertingBetweenROSImagesAndOpenCVImagesPython
http://dlib.net/face_landmark_detection.py.html

"""
import rospy
import sys
import cv2
import numpy as np
import dlib
import math

from sensor_msgs.msg import Image
# from cv_bridge import CvBridge, CvBridgeError
from seguimiento.msg import puntosCaras
from sensor_msgs.msg import CompressedImage
from reconocimientoFacial import reconocimientoFacial
from correctorDistorsionOjoPez import correctorDistorsionOjoPez
from seguimiento.msg import salidaKalman
from calculoAngulos import calculoAngulos
import dlib
import dlib.cuda as cuda

class publicadorPuntosCaras:

  def __init__(self):
    # Creamos el subscriptor al topic de salida de Kalman
    self.sKalman_sub = rospy.Subscriber("salidaKalman",salidaKalman,self.callbackKalman)

    # Creamos el publicador del topic imagenTratada, con la imagen realmente procesada
    # Hacemos esto para que el resultado al visualizar sea el correcto
    self.iComp_pub = rospy.Publisher("imagenTratada", CompressedImage, queue_size=1)

    # Creamos el publicador del topic puntosCara
    self.caras_pub = rospy.Publisher("puntosCaras", puntosCaras, queue_size=1)

    # Definimos el fichero de detección de caras entrenado de DLIB
    self.predictor_path = "/home/disa/catkin_ws/src/seguimiento/scripts/shape_predictor_68_face_landmarks.dat"

    # Definimos las utilidades de detección de caras y puntos de DLIB
    cuda.set_device(0)

    self.detector = dlib.get_frontal_face_detector()
    self.predictor = dlib.shape_predictor(self.predictor_path)

    rospy.loginfo("Utilizando CUDA = %s", dlib.DLIB_USE_CUDA)

    # Constante de número de puntos devueltos por DLIB
    self.PUNTOS_DLIB = 68

    # Objeto de reconocimiento facial
    self.rF = reconocimientoFacial()

    # Corrección de la imagen de tipo ojo de pez (cámara del robot)
    self.cO = correctorDistorsionOjoPez()

    # Herramienta de visualización DLIB
    # self.win = dlib.image_window()

    # Máximo de caras del histórico
    self.MAXIMO_PERSONAS = rospy.get_param("MAXIMO_PERSONAS", 10)

    # Threshold de Borrosidad
    self.THRESHOLD_BORROSIDAD = float(rospy.get_param("THRESHOLD_BORROSIDAD", 800))

    # Trackers
    self.trackers = []
    for i in range(0, self.MAXIMO_PERSONAS):
	self.trackers.append(dlib.correlation_tracker())
    self.tracker_iniciado = np.zeros(self.MAXIMO_PERSONAS)
    # Si el tracking detecta a la persona no volvemos a reconocer facialmente. Esto aumenta la velocidad
    # Calculamos puntos medios del tracker
    self.x_medio = np.zeros(self.MAXIMO_PERSONAS)
    self.y_medio = np.zeros(self.MAXIMO_PERSONAS)

    # Salida de Kalman. La necesitamos para identificar si la persona de una posición había previamente sido identificada
    self.sKalman = salidaKalman()
    # Objeto de cálculo de ángulos
    # Nos permite calcular el ángulo de una cara a partir del ángulo actual del robot y de las coordenadas de la cara
    self.cA = calculoAngulos()

  def procesar(self, cv_image):
    # Corrección de la distorsión provocada por la imagen de tipo ojo pez 
    # (cámara del robot con gran angular)
    # Convertimos previamente a 640*480, ya que la calibración inicial de la cámara se realizó utilizando dichas dimensiones.
    dim = (640, 480)
    imagen_640480 = cv2.resize(cv_image, dim, interpolation = cv2.INTER_AREA)
    cv_image_corregida = self.cO.undistort(imagen_640480)

    # Reducimos la imagen al tamaño indicado en parámetros
    ancho = rospy.get_param("ANCHO_IMAGEN", 640)
    alto_origen = cv_image_corregida.shape[0]
    ancho_origen = cv_image_corregida.shape[1]
    alto = int(ancho * alto_origen / ancho_origen)

    # Si el alto es diferente a los parámetros lo actualizamos ya que el alto se utiliza en otros
    # procedimientos (proceso estímulos, cálculo ángulos, etc)
    alto_param = rospy.get_param("ALTO_IMAGEN", 480)
    if alto != alto_param:
       rospy.set_param("ALTO_IMAGEN",alto)

    # Dimensiones
    dim = (ancho, alto)

    # Reducir
    imagen_reducida = cv2.resize(cv_image_corregida, dim, interpolation = cv2.INTER_AREA)

    # Flip imagen
    imagen_flip = cv2.flip(imagen_reducida, 2)

    # Convertir cara de BGR (OpenCV) a RGB (DLIB)
    imagen_dlib = imagen_flip[:, :, ::-1]

    # Transformamos a escala de grises
    gris_imagen = cv2.cvtColor(imagen_flip, cv2.COLOR_BGR2GRAY)

    # Definimos objeto a publicar con los datos de las caras
    caras = puntosCaras()
    caras.header.stamp = rospy.Time.now()

    # Identificar los límites de cada cara. El 1 del segundo argumento indica que
    # se puede ampliar la imagen 1 vez para detectar más caras
    dets = self.detector(gris_imagen, 1)
    numeroCaras = len(dets)
    rospy.loginfo("Caras detectadas = %d", numeroCaras)
    caras.numeroCaras = numeroCaras

    # Ajustamos los tamaños de los vectores publicados
    # (x1,y1)-(x2,y2) son los extremos de cada cara en la imagen
    caras.x1 = np.arange(numeroCaras)
    caras.y1 = np.arange(numeroCaras)
    caras.x2 = np.arange(numeroCaras)
    caras.y2 = np.arange(numeroCaras)
    caras.indiceCara = np.arange(numeroCaras)
    caras.caraNueva = np.arange(numeroCaras)
    # (puntoX,puntoY) representan los puntos característicos de la imagen para
    # cada cara y número de punto (68 devuelve DLIB)
    # los puntos se llevan a un array de una dimensión donde cada 68 puntos
    # consecutivos corresponden a caras diferentes
    caras.puntoX = np.arange(numeroCaras * self.PUNTOS_DLIB)
    caras.puntoY = np.arange(numeroCaras * self.PUNTOS_DLIB)

    # Avanzamos tiempo de todas las caras detectadas en el histórico
    self.rF.avanzar_Tiempo_Inactiva()

    # Si la cabeza se mueve reiniciamos los trackers ya que he visto que dan problemas con el movimiento
    if rospy.get_param("EN_MOVIMIENTO") == True:
	for i in range(0, self.MAXIMO_PERSONAS):
		self.tracker_iniciado[i] = 0

    # Hacemos un tracking de todos los objetos de la pantalla. Si estamos siguiendo una cara no realizaremos
    # reconocimiento facial nuevamente al ser una de las caras anteriores.
    for i in range(0, self.MAXIMO_PERSONAS):
	if self.tracker_iniciado[i] == 1:
        	self.trackers[i].update(imagen_dlib)
		pos = self.trackers[i].get_position()
		# unpack the position object
		startX = int(pos.left())
		startY = int(pos.top())
		endX = int(pos.right())
		endY = int(pos.bottom())
                self.x_medio[i] = (startX + endX) / 2
                self.y_medio[i] = (startY + endY) / 2
    
    # Reiniciamos las caras
    for i in range(0, caras.numeroCaras):
	caras.indiceCara[i] = -1

    for k, d in enumerate(dets):
    	rospy.loginfo("Caras detectada %d = (%d,%d)-(%d,%d)", 
                      k, d.left(), d.top(), d.right(), d.bottom())

        # Coordenadas de la cara
        caras.x1[k] = d.left()
        caras.y1[k] = d.top()
        caras.x2[k] = d.right()
        caras.y2[k] = d.bottom()

        # Ver si la cara detectada es una del tracking
	indice_cara = -1
	es_cara_nueva = False
	for i in range(0, self.MAXIMO_PERSONAS):
		if self.tracker_iniciado[i] == 1:
			# Miramos si el punto medio del tracking está dentro de la cara detectada
			if (self.x_medio[i] > caras.x1[k] and self.x_medio[i] < caras.x2[k] and 
			    self.y_medio[i] > caras.y1[k] and self.y_medio[i] < caras.y2[k]):
				indice_cara = i
				es_cara_nueva = False
				break

	rospy.loginfo("ASIGNACION PERSONA %d POR TRACKING: %d.", k, indice_cara)

	# Get the landmarks/parts for the face in box d.
	shape = self.predictor(imagen_flip, d)

	# Las caras muy borrosas son excluidas del tratamiento ya que no podemos detectar cuestiones como el habla visual
	# Analizamos la borrosidad de la imagen de la cara con una laplaciana.
	# Si está muy borrosa la descartamos ya que dará problemas en todo el proceso
	imagen_cara, xb1, yb1, xb2, yb2 = self.rF.extraer_cara(imagen_flip, caras.x1[k],caras.y1[k],caras.x2[k],caras.y2[k])
	gray = cv2.cvtColor(imagen_cara, cv2.COLOR_BGR2GRAY)
	borrosidad = float(cv2.Laplacian(gray, cv2.CV_64F).var())
	
	rospy.loginfo("Borrosidad cara = %f", borrosidad)
        if borrosidad < self.THRESHOLD_BORROSIDAD:
		indice_cara = -1
		caras.indiceCara[k] = -1
	else:
		# Si la cara no se ha detectado en el tracking, la buscamos a través de Kalman o reconocimiento facial si la cabeza no está en movimiento:
		#       1. La buscamos en las salidas del filtro de Kalman
		#	2. Si no la encontramos, la volvemos a reconocerla facialmente
		if indice_cara == -1 and rospy.get_param("EN_MOVIMIENTO") == False:
			#################################################################################################################################################
			# Buscamos la cara en el filtro de Kalman
			# Para ello calculamos primero el ángulo actual de la cara para ver si se distancia menos de 5 grados respecto al almacenado. Usamos solo el PAN.
			diferencia_maxima = math.pi * float(10) / float(180)
			# Punto medio de la cara
		        x_medio = (caras.x1[k] + caras.x2[k]) / 2
	        	y_medio = (caras.y1[k] + caras.y2[k]) / 2
		        # Calculamos los ángulos de la cara actual
			# Llamamos a la función con las variables de memoria que guardan los ángulos actuales del robot
		        PAN_new, TILT_new = self.cA.calcularAngulos(x_medio, y_medio)

			#rospy.loginfo("x_medio = %f, PAN_new = %f, PAN_ROBOT = %f", x_medio, PAN_new, rospy.get_param("PAN_ROBOT",0))

			if self.sKalman.identificador:
			# Recorremos los filtros de Kalman para localizar la cara más cercana
				cara_encontrada = -1
				distancia_cara_encontrada = float(9999999)
				for j in range(0, self.MAXIMO_PERSONAS):
					if self.sKalman.identificador[j] != -2:
						d = abs(self.sKalman.pan[j] - PAN_new)
						if d < distancia_cara_encontrada:
							distancia_cara_encontrada = d
							cara_encontrada = j
				# Si la distancia es inferior a 10 grados, la consideramos la cara 
				# El indicador de cara nueva es necesario para que en el nodo de proceso de estímulos se cree una nueva pose. De lo contrario
				# intentará utilizar la pose anterior y no la encontrará
				if distancia_cara_encontrada < diferencia_maxima:
					indice_cara = cara_encontrada
					es_cara_nueva = True
				dcerad = float(180) * distancia_cara_encontrada / math.pi
				rospy.loginfo("ASIGNACION PERSONA %d POR KALMAN: %d. Distancia = %f a elemento %d", k, indice_cara, dcerad, cara_encontrada)
			#################################################################################################################################################
			# Si no hemos encontrado la cara, seguimos con la prueba de reconocimiento facial
			if indice_cara == -1:
				# Buscar el índice de la cara y verificar si es una cara nueva
				# Caso 1: indice_cara, es_cara_nueva = self.rF.buscar_indice_cara(shape)

				indice_cara, es_cara_nueva = self.rF.buscar_indice_cara_ENC(imagen_flip, shape, caras.x1[k],caras.y1[k],caras.x2[k],caras.y2[k])
				# Caso 5: indice_cara, es_cara_nueva = self.rF.buscar_indice_cara_IMG(imagen_flip,caras.x1[k],caras.y1[k],caras.x2[k],caras.y2[k])

			rospy.loginfo("ASIGNACION PERSONA %d POR RECONOCIMIENTO FACIAL: %d.", k, indice_cara)

	                # Solo si obtenemos un índice correcto de imagen arrancamos el tracking
        	        # Cuando las imágenes son borrosas, no se obtiene un encoding claro y el índice permanece a -1
        	        if indice_cara != -1:
		        	# Arrancamos un nuevo tracking
				self.trackers[indice_cara].start_track(imagen_dlib, dlib.rectangle(caras.x1[k] , caras.y1[k] , caras.x2[k] , caras.y2[k] ))
				#self.tracker[indice_cara].update(imagen_dlib)
				self.tracker_iniciado[indice_cara] = 1

        # Actualizar mensaje
	caras.indiceCara[k] = indice_cara
        caras.caraNueva[k] = es_cara_nueva

        # Recorremos los valores (x,y) de los landmarks de la cara y los devolvemos
        # for i in range(0, shape.num_parts):
	for i in range(0, self.PUNTOS_DLIB):
            caras.puntoX[self.PUNTOS_DLIB * k + i] = shape.part(i).x
            caras.puntoY[self.PUNTOS_DLIB * k + i] = shape.part(i).y

	# Si el robot está en movimiento tampoco procesamos los estímulos o la entrada de Kalman
	#if rospy.get_param("EN_MOVIMIENTO") == True:
	#	caras.indiceCara[k] = -1

    ##########################################################################################
    # Filtro de control que evita 2 personas asignadas a mismo identificador
    ##########################################################################################
    for i in range(0, caras.numeroCaras):
	for j in range(0, i):
		if caras.indiceCara[i] == caras.indiceCara[j]:
			caras.indiceCara[i] = -1

    ##########################################################################################
    # Reconstruimos el mensaje de las caras publicadas sin caras borrosas o caras donde no
    # se ha obtenido un reconocimiento facial correcto (con índice a -1)
    ##########################################################################################
    numeroCarasFiltradas = 0
    for i in range(0, caras.numeroCaras):
	if caras.indiceCara[i] != -1:
		numeroCarasFiltradas = numeroCarasFiltradas + 1

    #rospy.loginfo("Caras filtradas = %d", numeroCarasFiltradas)

    # Definimos objeto a publicar con los datos de las caras
    carasF = puntosCaras()
    carasF.header.stamp = rospy.Time.now()
    carasF.numeroCaras = numeroCarasFiltradas

    # Ajustamos los tamaños de los vectores publicados
    # (x1,y1)-(x2,y2) son los extremos de cada cara en la imagen
    carasF.x1 = np.arange(numeroCarasFiltradas)
    carasF.y1 = np.arange(numeroCarasFiltradas)
    carasF.x2 = np.arange(numeroCarasFiltradas)
    carasF.y2 = np.arange(numeroCarasFiltradas)
    carasF.indiceCara = np.arange(numeroCarasFiltradas)
    carasF.caraNueva = np.arange(numeroCarasFiltradas)
    # (puntoX,puntoY) representan los puntos característicos de la imagen para
    # cada cara y número de punto (68 devuelve DLIB)
    # los puntos se llevan a un array de una dimensión donde cada 68 puntos
    # consecutivos corresponden a caras diferentes
    carasF.puntoX = np.arange(numeroCarasFiltradas * self.PUNTOS_DLIB)
    carasF.puntoY = np.arange(numeroCarasFiltradas * self.PUNTOS_DLIB)

    # Rellenamos mensaje
    j = 0
    for i in range(0, caras.numeroCaras):
	if caras.indiceCara[i] != -1:
		#rospy.loginfo("Caras publicada %d = (%d,%d)-(%d,%d)",  caras.indiceCara[i], caras.x1[i], caras.y1[i], caras.x2[i], caras.y2[i])
		carasF.x1[j] = caras.x1[i]
		carasF.y1[j] = caras.y1[i]
		carasF.x2[j] = caras.x2[i]
		carasF.y2[j] = caras.y2[i]
		carasF.indiceCara[j] = caras.indiceCara[i]
		carasF.caraNueva[j] = caras.caraNueva[i]
		# Recorremos los valores (x,y) de los landmarks de la cara y los devolvemos
		for p in range(0, self.PUNTOS_DLIB):
			carasF.puntoX[self.PUNTOS_DLIB * j + p] = caras.puntoX[self.PUNTOS_DLIB * i + p] 
			carasF.puntoY[self.PUNTOS_DLIB * j + p] = caras.puntoY[self.PUNTOS_DLIB * i + p] 
		j = j + 1

    # Publicar los puntos de la cara en topic puntosCaras
    self.caras_pub.publish(carasF)
    # Publicar la imagen tratada como comprimida
    img_msg = CompressedImage()
    img_msg.header.stamp = rospy.Time.now()
    img_msg.format = "jpeg"
    img_msg.data = np.array(cv2.imencode('.jpg', gris_imagen)[1]).tostring()
    self.iComp_pub.publish(img_msg)

  def callbackKalman(self, srKalman):
    self.sKalman = srKalman

def main(args):
  ic = publicadorPuntosCaras()
  rospy.init_node('publicadorPuntosCara', anonymous=True)

  # Captura con OpenCV
  cap = cv2.VideoCapture(0)
  #cap = cv2.VideoCapture('/home/disa/head_pose/Seq37-2P-S0M0/Video/Seq37-2P-S0M0_CAM1.mp4')

  # Ratio de proceso de 20 imágenes por segundo
  rate = rospy.Rate(20) # 20hz

  # Creamos el objeto de publicación de imágenes
  pC = publicadorPuntosCaras()

  ret = True
  while ret == True and not rospy.is_shutdown():

	# Lectura de frame
        ret, frame = cap.read()

	# Proceso de frame y publicación
	if ret == True:
		pC.procesar(frame)

        rate.sleep()

  cap.release()
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
