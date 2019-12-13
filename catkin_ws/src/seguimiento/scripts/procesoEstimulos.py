#!/usr/bin/env python
# -*- coding: utf-8 -*-
# license removed for brevity
"""
Created on Tue Jul  23 10:28:23 2019

@author: Jaime Duque Domingo UVA

Investigación sobre la orientación de cabeza robótica
Orientación de la cabeza robótica

Este nodo realiza un procesamiento de las caras detectadas y el sonido obtenido para generar los
estímulos de la red competitiva y llevar el control mediante el filtro de Kalmanm

Se suscribe a los topic:
	puntosCara para tratar los puntos extraídos con DLIB
	direccionAudio para detectar VAD (Voice Activity Detection) y DOA (Direction of Arrival)

Publica los topic:
	entradaRedCompetitiva con las personas del histórico
	entradaKalman con las coordenadas de cada cara

"""
import rospy
import sys
import numpy as np
import math
import cv2
from seguimiento.msg import puntosCaras
from seguimiento.msg import direccionAudio
from seguimiento.msg import entradaKalman
from seguimiento.msg import salidaKalman
from seguimiento.msg import entradaRedCompetitiva
from pose_estimator import PoseEstimator
from stabilizer import Stabilizer
from sensor_msgs.msg import CompressedImage
from calculoAngulos import calculoAngulos
from calculoDireccionAudio import calculoDireccionAudio

class procesoEstimulos:

  # Inicialización de objeto definiendo las variables globales de la instancia del objeto
  def __init__(self):
    #####################################################################################
    # Objetos recibidos mediante funciones de callback
    # Detección de audio
    self.dAudio = direccionAudio()
    # PuntosCaras
    self.pCaras = puntosCaras()

    # Salida de Kalman. La necesitamos para calcular determinados estímulos que tienen en cuenta
    # la existencia y posición de personas previamente detectadas.
    self.sKalman = salidaKalman()

    # Semáforo de indicación de si los objetos han sido tratados
    # self.tratado_dAudio = True
    # self.tratado_pCaras = True
    #####################################################################################

    # Clase para calcular la dirección del audio
    self.dA = calculoDireccionAudio()

    # Pesos de los estímulos
    self.P1 = float(rospy.get_param("PESO_ESTIMULO_PERSONA_DETECTADA_VISUALMENTE", 1))
    self.P2 = float(rospy.get_param("PESO_ESTIMULO_PERSONA_HABLA_VISUAL_CON_AUDIO", 1))
    self.P3 = float(rospy.get_param("PESO_ESTIMULO_PERSONA_MIRANDO_ROBOT", 1))
    self.P4 = float(rospy.get_param("PESO_ESTIMULO_PERSONA_SE_MUEVE_MUCHO", 1))
    self.P5 = float(rospy.get_param("PESO_ESTIMULO_PERSONAS_EN_FOCO_ATENCION", 1))
    self.P6 = float(rospy.get_param("PESO_ESTIMULO_PERSONAS_NO_DETECTADAS_CON_AUDIO", 1))
    self.P7 = float(rospy.get_param("PESO_ESTIMULO_PERSONA_PROXIMA", 1))

    # Creamos el subscriptor al topic de puntos de la cara
    self.pCaras_sub = rospy.Subscriber("puntosCaras",puntosCaras,self.callbackCaras)

    # Creamos el subscriptor al topic de audio
    self.dAudio_sub = rospy.Subscriber("direccionAudio",direccionAudio,self.callbackAudio)

    # Creamos el subscriptor al topic de imágenes comprimidas para poder visualizar la pose
    self.iComp_sub = rospy.Subscriber("imagenTratada",CompressedImage,self.callbackImagen, queue_size = 1, buff_size = 2**24)

    # Creamos el subscriptor al topic de salida de Kalman
    self.sKalman_sub = rospy.Subscriber("salidaKalman",salidaKalman,self.callbackKalman)

    # Objeto de cálculo de ángulos
    # Nos permite calcular el ángulo de una cara a partir del ángulo actual del robot y de las
    # coordenadas de la cara
    self.cA = calculoAngulos()

    # Creamos el publicador del topic entradaKalman
    self.kalman_pub = rospy.Publisher("entradaKalman", entradaKalman, queue_size=1)

    # Creamos el publicador del topic entradaRedCompetitiva
    self.redCompetitiva_pub = rospy.Publisher("entradaRedCompetitiva",entradaRedCompetitiva, queue_size=1)

    # Constante de número de puntos devueltos por DLIB
    self.PUNTOS_DLIB = 68

    # Máximo de caras del histórico
    self.MAXIMO_PERSONAS = rospy.get_param("MAXIMO_PERSONAS", 10)

    # Número de frames considerados para la detección del habla
    self.FRAMES = rospy.get_param("FRAMES_CONSIDERADOS", 5)

    # Usamos los últimos frames para ver si hay diferencia significativa en los labios
    self.variacion_labios = np.zeros((self.MAXIMO_PERSONAS, self.FRAMES))
    # Además, almacenamos la distancia de labios del último frame
    self.distancia_anterior = np.zeros(self.MAXIMO_PERSONAS)
    # Umbral de detección de una persona hablando
    self.THRESHOLD_MOVIMIENTO_LABIOS = 0.30

    # Umbral de detección de una persona moviéndose mucho
    self.THRESHOLD_MOVIMIENTO_PERSONA = 0.30

    # Umbral de detección de proximidad. Si el cálculo de la distancia de la cara es mayor que este
    # valor, se considera que la persona está próxima al robot.
    self.THRESHOLD_DETECCION_PROXIMIDAD = 30

    # Usamos los últimos frames para ver si la persona se mueve mucho
    self.posicion_anterior_pan = np.zeros((self.MAXIMO_PERSONAS, 5 * self.FRAMES))
    self.posicion_anterior_tilt = np.zeros((self.MAXIMO_PERSONAS, 5 * self.FRAMES))

    # Audio detectado en los últimos frames
    # self.aDetectado = np.zeros(self.FRAMES)

    #####################################################################################
    # Pose estimator and stabilizer
    # Utilizamos estos estimadores para ver dónde está mirando una persona
    self.pose_estimator = None
    self.pose_stabilizers = None
    self.width = rospy.get_param("ANCHO_IMAGEN", 640)
    # Por defecto imágenes de 640 x 480 para aplicar regla del 3
    # self.height = int(480 * self.width / 640)
    self.height = rospy.get_param("ALTO_IMAGEN", 480)
    #self.THRESHOLD_MIRADA = self.width / 2
    self.THRESHOLD_MIRADA = 5

    # Cargamos la imagen publicada de manera temporal para poder mostrar las poses generadas
    self.iComp = None
    self.imagenGris = None
    self.imagenRecibida = False
    #####################################################################################

  #########################################################################################
  # Función de procesamiento de los estímulos a partir de los mensajes de entrada
  #########################################################################################
  def procesoEstimulos(self, caras, audio):

    # De manera temporal, utilizamos la imagen publicada para poder mostrar la pose de las personas
    # Primero leemos la imagen del topic imagen_topic
    if self.iComp != None:
    	np_arr = np.fromstring(self.iComp.data, np.uint8)
	self.imagenGris = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
	self.imagenRecibida = True
	# Imagen color a partir de gris: gris_imagen = cv2.merge((gris_imagen,gris_imagen,gris_imagen))

    # Array para controlar qué persona está hablando para enviarlo a la red competitiva
    persona_hablando = np.zeros(self.MAXIMO_PERSONAS)
    persona_proxima = np.zeros(self.MAXIMO_PERSONAS)
    persona_mirando = np.zeros(self.MAXIMO_PERSONAS)
    angulo_mirada = np.zeros(self.MAXIMO_PERSONAS)
    persona_detectada = np.zeros(self.MAXIMO_PERSONAS)
    persona_se_mueve = np.zeros(self.MAXIMO_PERSONAS)

    # Cuando se mueve la cabeza hay que inicializar variables que utilizamos para detección de estímulos ya
    # que acumulan valores de frames anteriores. Al mover la cabeza dichos valores se desplazan y afectan
    # a los cálculos
    if rospy.get_param("EN_MOVIMIENTO") == True:
	# Inicializamos el histórico de persona en movimiento ya que al moverse la cabeza hace que 
	# el estímulo de una persona que se ve se dispare al mantener valores de posición antiguos
	self.posicion_anterior_pan = np.zeros((self.MAXIMO_PERSONAS, 5 * self.FRAMES))
	self.posicion_anterior_tilt = np.zeros((self.MAXIMO_PERSONAS, 5 * self.FRAMES))
	# Lo mismo ocurre con el movimiento de los labios. Al mover el robot se pierden las
	# posibles referencias
	self.variacion_labios = np.zeros((self.MAXIMO_PERSONAS, self.FRAMES))
	self.distancia_anterior = np.zeros(self.MAXIMO_PERSONAS)

    # Matriz bidimensional para los landmarks de la cara
    lX = np.zeros((caras.numeroCaras, self.PUNTOS_DLIB)).astype(int)
    lY = np.zeros((caras.numeroCaras, self.PUNTOS_DLIB)).astype(int)

    # Mensaje de Kalman
    # Publicamos un mensaje con las caras detectadas para el filtro de Kalman
    eKalman = entradaKalman()
    eKalman.header.stamp = rospy.Time.now()
    eKalman.identificador = np.zeros(self.MAXIMO_PERSONAS + 2)
    eKalman.pan = np.zeros(self.MAXIMO_PERSONAS + 2) 
    eKalman.tilt = np.zeros(self.MAXIMO_PERSONAS + 2) 
    for i in range(0, self.MAXIMO_PERSONAS + 2):
	eKalman.identificador[i] = -1

    for i in range(0, caras.numeroCaras):
	for j in range(0, self.PUNTOS_DLIB):
		# Pasamos array a matriz bidimensional
		lX[i][j] = caras.puntoX[i * self.PUNTOS_DLIB + j]
		lY[i][j] = caras.puntoY[i * self.PUNTOS_DLIB + j]

        #####################################################################################
        # Calculamos los ratios de la cara actual y la buscamos en el histórico
    	x_DLIB = lX[i]
	y_DLIB = lY[i]

        # El índice de la cara viene del publicador de caras
        indice_cara = caras.indiceCara[i]
	es_cara_nueva = caras.caraNueva[i]

	# Punto medio de la cara
        x_medio = (caras.x1[i] + caras.x2[i]) / 2
        y_medio = (caras.y1[i] + caras.y2[i]) / 2
        # Calculamos los ángulos de la cara actual
	# Llamamos a la función con las variables de memoria que guardan los ángulos actuales del robot
        PAN_new, TILT_new = self.cA.calcularAngulos(x_medio, y_medio)

	rospy.loginfo("Angulos PAN,TILT: (%f, %f)", PAN_new, TILT_new)

	# Añadimos cara al filtro de Kalman
    	eKalman.identificador[indice_cara] = indice_cara
    	eKalman.pan[indice_cara] = PAN_new
    	eKalman.tilt[indice_cara] = TILT_new

	# Activamos el flag de persona detectada visualmente
	persona_detectada[indice_cara] = 1

        # Activamos el flag si la persona está hablando visualmente
	# Si el robot está en movimiento no lo activamos ya que interfiere con el control visual
	# Al moverse el robot los puntos DLIB se descentran mucho
	persona_hablando[indice_cara] = 0
        if self.deteccionVisualHabla(x_DLIB, y_DLIB, indice_cara) == True: # and rospy.get_param("EN_MOVIMIENTO") == False:
		persona_hablando[indice_cara] = 1

        # Activamos el flag si la persona está a una cierta proximidad
        if self.deteccionDistanciaPersona(x_DLIB, y_DLIB, indice_cara) == True:
		persona_proxima[indice_cara] = 1
        
	# rospy.loginfo("Persona %i hablando visualmente: %f.", indice_cara, persona_hablando[indice_cara])

	# Activamos el flag si la persona tiene una pose en la que está mirando al robot
	mirandoRotot, anguloMirada = self.deteccionMiradaHaciaRobot(x_DLIB, y_DLIB, indice_cara, es_cara_nueva)
	angulo_mirada[indice_cara] = anguloMirada
        if mirandoRotot == True:
		persona_mirando[indice_cara] = 1
        
	rospy.loginfo("Persona %i mirando al robot: %f.", indice_cara, persona_mirando[indice_cara])

        # Activamos el flag si la persona se está moviendo mucho
	if self.deteccionMovimientoPersona(eKalman, indice_cara) == True:
		persona_se_mueve[indice_cara] = 1

	rospy.loginfo("Persona %i se mueve mucho: %f.", indice_cara, persona_se_mueve[indice_cara])

    # Activamos el boolean de detección de audio si se ha detectado audio
    # audio_detectado = self.deteccionAudio(audio)
    # rospy.loginfo("Detección de audio: %f.", audio_detectado)
    rospy.loginfo("Dirección del audio: %s.", str(audio.doa))

    # Si algún valor de Kalman es nulo, no indicamos identificador
    for r in range(0, self.MAXIMO_PERSONAS):
	if eKalman.pan[r] == 0 or eKalman.tilt[r] == 0:
		eKalman.identificador[r] = -1

    # Publicamos un mensaje con las caras detectadas para el filtro de Kalman solo si no estamos en movimiento
    rospy.loginfo("En movimiento: %s.", rospy.get_param("EN_MOVIMIENTO"))
    if rospy.get_param("EN_MOVIMIENTO") == False:
	# Añadimos una posición para una persona ficticia de Kalman
	eKalman.pan[self.MAXIMO_PERSONAS] = float(150) * math.pi / 180
	eKalman.tilt[self.MAXIMO_PERSONAS] = rospy.get_param("ANGULO_TILT_CENTRAL", 100) * math.pi / 180
	eKalman.identificador[self.MAXIMO_PERSONAS] = self.MAXIMO_PERSONAS
	eKalman.pan[self.MAXIMO_PERSONAS + 1] = float(50) * math.pi / 180
	eKalman.tilt[self.MAXIMO_PERSONAS + 1] = rospy.get_param("ANGULO_TILT_CENTRAL", 100) * math.pi / 180
	eKalman.identificador[self.MAXIMO_PERSONAS + 1] = self.MAXIMO_PERSONAS + 1
	self.kalman_pub.publish(eKalman)

    # Publicamos los estímulos calculados
    eRC = entradaRedCompetitiva()
    eRC.header.stamp = rospy.Time.now()
    eRC.data = self.obtencionEstimulos(persona_hablando, audio, persona_detectada, persona_se_mueve, persona_mirando, persona_proxima, angulo_mirada, eKalman, self.sKalman)
    self.redCompetitiva_pub.publish(eRC)

    # Visualización de las poses de las personas
    if self.imagenRecibida == True:
	cv2.namedWindow("Poses de las personas")
	#cv2.moveWindow("Poses de las personas", 2500,300)
    	cv2.imshow("Poses de las personas", self.imagenGris)
	cv2.waitKey(3)

  """#########################################################################################
  # Función para determinar si ha habido audio
  # Para mejorar el rendimiento verificamos si en los últimos frames se ha hablado.
  # Si se ha hablado en alguno de ellos, consideramos que se ha detectado audio
  #########################################################################################
  def deteccionAudio(self, audio):
    # Desplazamos resultados de audio a modo de pila FIFO
    for k in range(1, self.FRAMES):
        self.aDetectado[k-1] = self.aDetectado[k]
    # Registramos el nuevo audio
    self.aDetectado[self.FRAMES - 1] = 0
    if audio.audioDetectado == True:
        self.aDetectado[self.FRAMES - 1] = 1
    # Si en algún frame se ha detectado audio, retornamos 1. De lo contrario 0
    resultado = 0
    for k in range(0, self.FRAMES):
        if self.aDetectado[k] == 1:
        	resultado = 1
		break
    return resultado"""

  #########################################################################################
  # Función para calcular la distancia de la persona al robot en función de tamaño cara
  #########################################################################################
  def deteccionDistanciaPersona(self, x_DLIB, y_DLIB, indice_cara):
    # Calculamos la distancia entre el punto medio de los ojos y la barbilla

    x_ojos = (x_DLIB[36] + x_DLIB[45]) / 2
    y_ojos = (y_DLIB[36] + y_DLIB[45]) / 2
    distancia_barbilla = math.sqrt((x_ojos-x_DLIB[8])**2 + (y_ojos-y_DLIB[8])**2)

    resultado = False        
    if distancia_barbilla > self.THRESHOLD_DETECCION_PROXIMIDAD:
	resultado = True

    #rospy.loginfo("Distancia cara total = %f.", distancia_barbilla)

    return resultado

  #########################################################################################
  # Función para determinar si una persona está hablando basándose en los puntos de la boca
  #########################################################################################
  def deteccionVisualHabla(self, x_DLIB, y_DLIB, indice_cara):
    # Calculamos las diferencias entre las coordenadas de los puntos 61-67, 62-66, 63-65 y 
    # calculamos la suma de distancias cuadrática. Si entre dos frames hay una diferencia
    # superior a un determinado umbral, concluimos que la persona está hablando

    distancia_abertura_boca = (math.sqrt((x_DLIB[61]-x_DLIB[67])**2 + (y_DLIB[61]-y_DLIB[67])**2) 
            + math.sqrt((x_DLIB[62]-x_DLIB[66])**2 + (y_DLIB[62]-y_DLIB[66])**2) 
            + math.sqrt((x_DLIB[63]-x_DLIB[65])**2 + (y_DLIB[63]-y_DLIB[65])**2)
            + math.sqrt((x_DLIB[48]-x_DLIB[54])**2 + (y_DLIB[48]-y_DLIB[54])**2)
            + math.sqrt((x_DLIB[50]-x_DLIB[58])**2 + (y_DLIB[50]-y_DLIB[58])**2)
            + math.sqrt((x_DLIB[51]-x_DLIB[57])**2 + (y_DLIB[51]-y_DLIB[57])**2)
            + math.sqrt((x_DLIB[52]-x_DLIB[56])**2 + (y_DLIB[52]-y_DLIB[56])**2))        
        
    distancia_ojos = math.sqrt((x_DLIB[36]-x_DLIB[45])**2 + (y_DLIB[36]-y_DLIB[45])**2)
        
    # Normalizamos la distancia entre los labios dividiendo con la distancia extremo a extremo de 
    # los ojos para normalizar
    if distancia_ojos != 0:
       distancia_abertura_boca_normalizada = distancia_abertura_boca / distancia_ojos
    else:
       distancia_abertura_boca_normalizada = 0
            
    # desplazamos distancias en el array a modo de pila FIFO
    for k in range(1, self.FRAMES):
        self.variacion_labios[indice_cara][k-1] = self.variacion_labios[indice_cara][k]
            
    # Grabamos nueva variación en la última posición
    if self.distancia_anterior[indice_cara] != 0:
       self.variacion_labios[indice_cara][self.FRAMES-1] = distancia_abertura_boca_normalizada - self.distancia_anterior[indice_cara]
                
    self.distancia_anterior[indice_cara] = distancia_abertura_boca_normalizada
      
    # Sumamos euclídeamente todas las variaciones a ver si se sobrepasa un umbral
    variacion_total = float(0.0)
    for k in range(0, self.FRAMES):
        variacion_total = variacion_total + self.variacion_labios[indice_cara][k] ** 2
    variacion_total = math.sqrt(variacion_total)

    resultado = False        

    rospy.loginfo("Variación de movimiento de labios de la persona %d es : %f.", indice_cara, variacion_total)
    self.THRESHOLD_MOVIMIENTO_LABIOS = 0.50

    if variacion_total > self.THRESHOLD_MOVIMIENTO_LABIOS:
       resultado = True

    return resultado

  #########################################################################################
  # Función para determinar si una persona se mueve mucho entre distintos frames
  # Esto muestra inquietud y el robot le dona estímulo. Lo calculamos a partir de los 
  # valores de entrada de Kalman
  #########################################################################################
  def deteccionMovimientoPersona(self, eKalman, indice_cara):
    if eKalman.identificador[indice_cara] != indice_cara:
	return False

    # desplazamos valores anteriores de Kalman en el array a modo de pila FIFO
    for k in range(1, 5 * self.FRAMES):
        self.posicion_anterior_pan[indice_cara][k-1] = self.posicion_anterior_pan[indice_cara][k]
        self.posicion_anterior_tilt[indice_cara][k-1] = self.posicion_anterior_tilt[indice_cara][k]
    # grabamos la nueva posición en el último elemento
    self.posicion_anterior_pan[indice_cara][5*self.FRAMES-1] = eKalman.pan[indice_cara]
    self.posicion_anterior_tilt[indice_cara][5*self.FRAMES-1] = eKalman.tilt[indice_cara]
      
    # sumamos euclídeamente todas las variaciones a ver si se sobrepasa un umbral
    variacion_total = float(0.0)
    for k in range(0, 5 * self.FRAMES - 1):
	if (self.posicion_anterior_pan[indice_cara][k] != 0 and self.posicion_anterior_pan[indice_cara][k+1] != 0 and
	   self.posicion_anterior_tilt[indice_cara][k] != 0 and self.posicion_anterior_tilt[indice_cara][k+1] != 0):
		variacion_total = variacion_total + math.sqrt((self.posicion_anterior_pan[indice_cara][k] - self.posicion_anterior_pan[indice_cara][k+1]) ** 2 +
	                                    (self.posicion_anterior_tilt[indice_cara][k] - self.posicion_anterior_tilt[indice_cara][k+1]) ** 2)

    rospy.loginfo("Variación total = %f.", variacion_total)

    # Si sobrepasamos umbral, entonces consideramos que se mueve mucho
    resultado = False
    if variacion_total > self.THRESHOLD_MOVIMIENTO_PERSONA:
       resultado = True

    return resultado

  #########################################################################################
  # Función para determinar si una persona tiene una pose en la que está mirando al robot
  # Usamos Pnp para obtener el modelo tridimensional e inferir hacia dónde está mirando la persona
  # Pnp es un algoritmo que permite asociar un modelo tridimensional (ej, una cara) con 
  #  un conjunto de puntos obtenido en 2D (68 puntos DLIB)
  # Mirar solvePnp: https://docs.opencv.org/2.4/modules/calib3d/doc/camera_calibration_and_3d_reconstruction.html
  #########################################################################################
  def iniciarPoses(self):
    self.pose_estimator = []
    self.pose_stabilizers = []
    for k in range(0, self.MAXIMO_PERSONAS):
	self.pose_estimator.append(PoseEstimator(img_size=(self.height, self.width)))
	self.pose_stabilizers.append([Stabilizer(
			state_num=2,
			measure_num=1,
			cov_process=0.1,
			cov_measure=0.1) for _ in range(6)])

  def deteccionMiradaHaciaRobot(self, x_DLIB, y_DLIB, indice_cara, es_cara_nueva):

    if es_cara_nueva == True or self.pose_estimator == None:
	# Iniciar array de estimadores de pose
	if self.pose_estimator == None:
		self.iniciarPoses()
	# Creamos un nuevo estimador.
	# Introduce pose estimator to solve pose. Get one frame to setup the estimator according to the image size.
	self.pose_estimator[indice_cara] = PoseEstimator(img_size=(self.height, self.width))

	# Introduce scalar stabilizers for pose.
	self.pose_stabilizers[indice_cara] = [Stabilizer(
			state_num=2,
			measure_num=1,
			cov_process=0.1,
			cov_measure=0.1) for _ in range(6)]

    # Recorremos los valores (x,y) de los landmarks de la cara y los devolvemos
    ptos = np.zeros((self.PUNTOS_DLIB, 2))
    for i in range(0, self.PUNTOS_DLIB):
	ptos[i][0] = x_DLIB[i]
	ptos[i][1] = y_DLIB[i]

    # Lanzamos el estimador de pose a partir de los 68 puntos DLIB
    pose = self.pose_estimator[indice_cara].solve_pose_by_68_points(ptos)

    # Estabilizar la pose
    steady_pose = []
    pose_np = np.array(pose).flatten()
    for value, ps_stb in zip(pose_np, self.pose_stabilizers[indice_cara]):
	ps_stb.update([value])
	steady_pose.append(ps_stb.state[0])
    steady_pose = np.reshape(steady_pose, (-1, 3))

    # Mostramos la pose en una ventana creada a tal efecto
    pto_Origen = []
    # Angulo de mirada
    angulo_mirada = 0
    if self.imagenRecibida == True:
	# Dibujar rectángulos de orientación
	self.pose_estimator[indice_cara].draw_annotation_box(self.imagenGris, steady_pose[0], steady_pose[1], color=(128, 255, 128))
    	
    	# Obtener punto de la imagen de orientación de cada persona
	pto_Origen, pto_Infinito = self.pose_estimator[indice_cara].dibuja_linea_infinito(self.imagenGris, steady_pose[0], steady_pose[1], color=(255, 0, 0))

        # Pruebas
        # self.pose_estimator[indice_cara].calcula_direccion(self.imagenGris, steady_pose[0], steady_pose[1], color=(255, 0, 0))

	# Calcular el ángulo de mirada
	angulo_mirada = self.pose_estimator[indice_cara].calcular_angulo_mirada(pto_Origen, pto_Infinito)

    # Verificar si la distancia euclídea al punto central de la pantalla es menor que un determinado umbral
    persona_mirando = False
    #distancia_centro_imagen = math.sqrt((self.width / 2 - pto_Infinito[0])**2 + (self.height / 2 - pto_Infinito[1])**2) 
    #if distancia_centro_imagen < self.THRESHOLD_MIRADA:
    #	persona_mirando = True

    if len(pto_Origen) > 0:
	# Calcular el módulo del vector 2D
	modulo = math.sqrt((pto_Origen[0] - pto_Infinito[0])**2 + (pto_Origen[1] - pto_Infinito[1])**2)
	# Dividimos el módulo entre el tamaño de la cara para hacerlo insensible a la distancia
	distancia_ojos = math.sqrt((x_DLIB[36]-x_DLIB[45])**2 + (y_DLIB[36]-y_DLIB[45])**2)
	indicador = modulo / distancia_ojos
    else:
        # Si no se ha dado de alta la pose, forzamos para que el indicador sea mayor que el umbral
	indicador = self.THRESHOLD_MIRADA

    # Si el indicador es menor que un determinado umbral, la persona está mirando
    # print("Indicador")
    # print(indicador)
    if indicador < self.THRESHOLD_MIRADA:
    	persona_mirando = True

    # Uncomment following line to draw head axes on frame.
    # self.pose_estimator.draw_axes(imagen_reducida, stabile_pose[0], stabile_pose[1])

    # Mostrar modelo 3D
    #self.pose_estimator[indice_cara].show_3d_model()
    
    return persona_mirando, angulo_mirada

  # Obtención de Estímulos de las capas a partir de valores recogidos de los sensores de imagen/sonido
  # Como entrada:
  #       persona_hablando[x] (x=1 a MAXIMO_PERSONAS): Vale 1 si la persona x habla visualmente
  #       audio: Devuelve los indicadores VAD (Voice Activity Detection) y DOA (Direction of Arrival)
  #       persona_detectada[x] (x=1 a MAXIMO_PERSONAS): Vale 1 si la persona x se detecta visualmente o 0 en caso contrario
  #       persona_se_mueve[x] (x=1 a MAXIMO_PERSONAS): Vale 1 si la persona x se mueve mucho. Incompatible con hablar visualmente
  #       persona_mirando[x] (x=1 a MAXIMO_PERSONAS): Vale 1 si la persona x mira al robot
  #       persona_proxima[x] (x=1 a MAXIMO_PERSONAS): Vale 1 si la persona x está próxima al robot
  #       angulo_mirada[x] (x=1 a MAXIMO_PERSONAS): Indica el valor del ángulo del vector de mirada hacia el robot
  #       eKalman[x] (x=1 a MAXIMO_PERSONAS): Posiciones de las personas en el filtro de Kalman. Sirven para ver si una persona se
  #                                           encuentra a la izquierda/derecha del robot
  #       sKalman[x] (x=1 a MAXIMO_PERSONAS): Posiciones de las personas en salida del filtro de Kalman. Necesitamos la posición
  #                                           de personas previamente encontradas por Kalman para calcular ciertos estímulos como 
  #                                           el del foco de atención. El vector de salida de Kalman incluye todas las personas
  #                                           previamente localizadas.

  # Como salida: vector de estímulos para la capa STM
  # Importante: Los índices de persona empiezan en 0: persona_hablando[0] es la primera persona
  #             De la misma manera, la salida devuelve el índice de la persona ganadora comenzando en 0.
  def obtencionEstimulos(self, persona_hablando, audio, persona_detectada, persona_se_mueve, persona_mirando, persona_proxima, angulo_mirada, eKalman, sKalman):
    # Cálculo de las actividades neuronales: Cada estímulo incrementa el valor de la neurona de entrada:
    #   1. Si se detecta la persona, se multiplica 1 por el peso P1
    #   2. Si visualmente la persona habla y hay audio, se multiplica 1 por el peso P2
    #   3. Si visualmente la persona mira al robot, se multiplica 1 por el peso P3
    #   4. Si la persona se mueve, se multiplica 1 por el peso P4
    #   5. Si ninguna de las personas visualmente están hablando, se multiplica 1 por el peso P5
    #      para aquellas personas que se encuentran en la dirección del audio y no son detectadas
    #   6. Cuando las personas detectadas visualmente no están mirando el robot y están mirando hacia otro lado (con un ángulo parecido),
    #      entonces se incrementará el estímulo para aquellas personas situadas en la dirección de la mirada (si hay), multiplicando 1 por el peso P6
    #   7. Si la persona está próxima, se multiplica 1 por el peso P7
    #
    # Dividimos el resultado entre la suma total de los pesos para devolver una salida normalizada de 0 a 1

    # Cálculo de la dirección del audio.
    indicador = self.dA.indicadorDireccion(audio)
    audio_izquierda = False
    audio_central = False
    audio_derecha = False
    if indicador == -1:
       audio_izquierda = True
    if indicador == 0:
       audio_central = True
    if indicador == 1:
       audio_derecha = True

    n = self.MAXIMO_PERSONAS
    # Vector de inputs
    I = np.zeros(n + 2)
    
    # Los estímulos se ven fuertemente afectados por el movimiento de la cabeza. Por ejemplo, el movimiento de una persona se disparará si
    # la cabeza se mueve, o el movimiento de los labios confundirá y se detectará habla.
    # Solo consideramos detección de persona / distancia a persona
    if rospy.get_param("EN_MOVIMIENTO") == True:
	for k in range(0, n):
		if persona_detectada[k] == 1:
			I[k] = I[k] + self.P1 * 1
			# Normalizamos los estímulos para que su valor se encuentre entre 0 y 1. Como son 6 estímulos, dividimos entre los 6 pesos
			I[k] = I[k] / (self.P1 + self.P2 + self.P3 + self.P4 + self.P5 + self.P6 + self.P7)
	return I

    # SOLO CONTINUAMOS SI NO HAY MOVIMIENTO PARA EVITAR CALCULAR ESTÍMULOS INCORRECTAMENTE

    # Ángulo en el que se encuentra la cabeza robótica
    # Nos sirve para ver si una persona está a la izquierda o derecha de la cabeza en su posición actual
    angulo_pan_robot = float(rospy.get_param("PAN_ROBOT", 0)) * math.pi / float(180)
    hablando_frente_robot = False

    for k in range(0, n):
	# Persona detectada
	if persona_detectada[k] == 1:
		I[k] = I[k] + self.P1 * 1
	# Persona próxima
	if persona_proxima[k] == 1:
		I[k] = I[k] + self.P7 * 1

	# Detectar si alguien habla frente al robot
	habla = 0
	if persona_hablando[k] == 1:
		if audio_central == True:
			hablando_frente_robot = True
			habla = 1
			I[k] = I[k] + self.P2 * 1
		else:
			# También consideramos si el audio se detecta en izquierda/derecha, pero la persona está levemente
			# a la izquierda/ derecha del robot
			if len(sKalman.identificador) > 0:
				if sKalman.identificador[k] != -2:
					if sKalman.pan[k] > angulo_pan_robot and audio_derecha == True:
						hablando_frente_robot = True
						habla = 1
						I[k] = I[k] + self.P2 * 1
					else:
						if sKalman.pan[k] < angulo_pan_robot and audio_izquierda == True:
							hablando_frente_robot = True
							habla = 1
							I[k] = I[k] + self.P2 * 1	

	#rospy.loginfo("Persona %i hablando: %i.", k, habla)

	if persona_mirando[k] == 1:
		I[k] = I[k] + self.P3 * 1
	if persona_se_mueve[k] == 1:
		I[k] = I[k] + self.P4 * 1

    ########################################################################################################################
    # Estímulo de personas no detectadas visualmente cuando hay audio. Si ninguna de las personas visualmente están hablando,
    # tendremos que añadir estímulo a las personas que no se encuentran frente al robot en la dirección del audio
    ########################################################################################################################
    if hablando_frente_robot == False:
	detectada_derecha = False
	detectada_izquierda = False

	for k in range(0, n):
		# Indicamos que solo añadimos estímulo a personas previamente detectadas (existen en la salida de Kalman)
		if len(sKalman.identificador) > 0:
		        if persona_detectada[k] != 1 and sKalman.identificador[k] != -2:
				#rospy.loginfo("PERSONA NO DETECTADA!")
				#rospy.loginfo("sKalman.pan = %f", sKalman.pan[k])
				#rospy.loginfo("pan_robot = %f", angulo_pan_robot)
				#if audio_derecha == True:
				#	rospy.loginfo("Audio derecha")
				#if audio_izquierda == True:
				#	rospy.loginfo("Audio izquierda")

				# Se añade si la persona está situada en la misma dirección del audio
				if sKalman.pan[k] > angulo_pan_robot and audio_derecha == True:
					I[k] = I[k] + self.P6 * 1
					detectada_derecha = True
				else:
					if sKalman.pan[k] < angulo_pan_robot and audio_izquierda == True:
						I[k] = I[k] + self.P6 * 1
						detectada_izquierda = True
	# Se añade persona ficticia si la persona está situada en la misma dirección del audio
	# Esto nos sirve para cuando aparece alguien nuevo en la escena
	# A las personas ficticias les damos el estímulo 6 reducido a la mitad ya que de lo contrario
	# puede que ganen la competición si no se detecta muy bien el habla de las personas que están en la escena.
	if audio_derecha == True and detectada_derecha == False:
		I[self.MAXIMO_PERSONAS] = I[self.MAXIMO_PERSONAS] + self.P6 * 0.5
	if audio_izquierda == True and detectada_izquierda == False:
		I[self.MAXIMO_PERSONAS + 1] = I[self.MAXIMO_PERSONAS + 1] + self.P6 * 0.5

    ########################################################################################################################
    # Estímulo del foco de atención
    ########################################################################################################################
    # Ver si todas las personas detectadas visualmente no están mirando el robot y están mirando hacia la misma dirección.
    # Lo entendemos como que están mirando a una persona situada en la dirección de otra persona. 
    angulo_anterior = 99999

    # dirección de mirada: 1 derecha / -1 izquierda
    direccion_mirada = 0
    # test para indicar si todos miran en la misma dirección
    test_misma_direccion = True

    for k in range(0, n):
        if persona_detectada[k] == 1 and persona_mirando[k] == 0:
		# Si los ángulos de todas ellas se diferencian menos de pi/6 (30º) consideramos que miran a una misma dirección
		# correspondiente a las personas situadas a la derecha/izquierda del robot
		if angulo_anterior == 99999:
			angulo_anterior = angulo_mirada[k]

		# ver si ambos miran en la misma dirección. atan2 devuelve valores entre -pi/2 y pi/2 que corresponden a mirar a la derecha
		i1 = 0
		i2 = 0
		if angulo_mirada[k] >= -(math.pi / 2) and angulo_mirada[k] <= (math.pi / 2):
			i1 = 1
		else:
			i1 = -1
		if angulo_anterior >= -(math.pi / 2) and angulo_anterior <= (math.pi / 2):
			i2 = 1
		else:
			i2 = -1
		# Continuamos solo si ambos miran en la misma dirección (derecha o izquierda)
		if i1 == i2:
			# Calculamos si la diferencia entre ambos ángulos es menor de pi/6 (30º)
			diferencia = abs(angulo_mirada[k] - angulo_anterior)
			if diferencia < (math.pi/6):
				direccion_mirada = i1
			else:
				test_misma_direccion = False
				break
		else:
			test_misma_direccion = False
			break
		# Refrescamos el ángulo anterior para el próximo test
		angulo_anterior = angulo_mirada[k]

    # Si el test ha ido bien y tenemos una dirección de mirada, entonces buscamos personas situadas en dicha dirección para 
    # incrementar sus estímulos de entrada de la red competitiva
    pan_robot = float(rospy.get_param("PAN_ROBOT")) * math.pi / float(180)

    if test_misma_direccion == True and direccion_mirada != 0 and sKalman:
	for k in range(0, n):
		# Comprobamos que la persona no ha sido detectada y está situada a derecha o izquierda del robot
		# Lo aplicamos solo si la persona ha sido previamente registrada en Kalman. Para ello utilizamos
		# la salida del filtro de Kalman
        	if persona_detectada[k] == 0 and sKalman.identificador:
			if direccion_mirada == 1 and sKalman.identificador[k] != -2 and sKalman.pan[k] > pan_robot:
				I[k] = I[k] + self.P5 * 1
			if direccion_mirada == -1 and sKalman.identificador[k] != -2 and sKalman.pan[k] < pan_robot:
				I[k] = I[k] + self.P5 * 1

    # Normalizamos los estímulos para que su valor se encuentre entre 0 y 1. Como son 7 estímulos, dividimos entre los 7 pesos
    for k in range(0, n + 2):
        I[k] = I[k] / (self.P1 + self.P2 + self.P3 + self.P4 + self.P5 + self.P6 + self.P7)

    return I

  def callbackCaras(self, caras):
    self.pCaras = caras
    self.procesoEstimulos(self.pCaras, self.dAudio)
    # Reiniciamos la detección de audio hasta el próximo frame
    # self.dAudio.audioDetectado = False

  def callbackAudio(self, audio):
    self.dAudio = audio

  # Este callback lo introducimos de manera temporal para poder leer la imagen publicada por
  # el publicador de puntos y mostrar las poses de las personas
  def callbackImagen(self, iComp):
    self.iComp = iComp

  def callbackKalman(self, srKalman):
    self.sKalman = srKalman

  # wait_for_message(topic, topic_type, timeout=None)

def main(args):
  ic = procesoEstimulos()
  rospy.init_node('procesoEstimulos', anonymous=True)
  try:
	rospy.spin()
  except KeyboardInterrupt:
	print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)

