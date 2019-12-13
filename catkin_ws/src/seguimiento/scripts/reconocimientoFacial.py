#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 09:32:37 2019

@author: Jaime Duque Domingo (UVA)

Distintas posibilidades utilizadas para el reconocimiento facial

Clase de reconocimiento facial con distintos experimentos:
	1. Utilizando los 8 ratios de la cara para cada una de las 10 caras. 
        2. Utilizando la librería face_recognition. Es muy efectivo pero lento con CPU (0,42 segundos en obtener descriptor
           de 128 para una cara). Se necesitaría GPU
	3. Utilizando la librería openface. Al igual que el anterior, genera un descriptor de 128 valores. Al procesarse
           como una red profunda sobre la propia imagen, es lento. 0,22 segundos en CPU. Requeriría GPU
	4. Pruebas con SIFT. Obteniendo los puntos característicos con SIFT. Es rápido pero parece que no ofrece buenos resultados
        5. Comparación de imágenes píxel a píxel. Para ello se alinea la imagen de la cara para tener los ojos en una posición
           concreta y se procede a la comparación.
"""

import rospy
import numpy as np
import math
import cv2
import openface
from PIL import Image as image2
import face_recognition
from time import time
import dlib
import dlib.cuda as cuda

try:
    import face_recognition_models
except Exception:
    print("Please install `face_recognition_models` with this command before using `face_recognition`:\n")
    print("pip install git+https://github.com/ageitgey/face_recognition_models")
    quit()
from copy import deepcopy

class reconocimientoFacial:

  def __init__(self):

    self.contador = 1

    # Umbrar de distancia para ver si una cara corresponde a una persona
    self.UMBRAL_DISTANCIA = 0.20

    # Constante de número de puntos devueltos por DLIB
    self.PUNTOS_DLIB = 68

    # Definimos el fichero de detección de caras entrenado de DLIB
    self.predictor_path = "/home/disa/catkin_ws/src/seguimiento/scripts/shape_predictor_68_face_landmarks.dat"

    self.openface_path = "/home/disa/catkin_ws/src/seguimiento/scripts/nn4.small2.v1.t7"

    self.align = openface.AlignDlib(self.predictor_path)
    self.net = openface.TorchNeuralNet(self.openface_path, 96)

    # Definimos las utilidades de detección de caras y puntos de DLIB
    # cuda.set_device(0)

    self.detector = dlib.get_frontal_face_detector()
    self.predictor = dlib.shape_predictor(self.predictor_path)

    # Face encoder para la librería de face_recognition
    self.face_encoder = dlib.face_recognition_model_v1("/home/disa/catkin_ws/src/seguimiento/scripts/dlib_face_recognition_resnet_model_v1.dat")

    # Indicamos por pantalla si utilizamos la GPU mediante CUDA
    rospy.loginfo("Utilizando GPU (CUDA) = %s", dlib.DLIB_USE_CUDA)

    #####################################################################################
    # HISTORICO DE CONTROL DE LAS CARAS A LO LARGO DEL TIEMPO.
    # Máximo de caras del histórico
    self.MAXIMO_PERSONAS = rospy.get_param("MAXIMO_PERSONAS", 10)
    # Frames en los que una cara no ha sido detectada
    self.Tiempo_Inactiva = np.zeros(self.MAXIMO_PERSONAS)
    # Caso 1: Ratios de las caras, 8 por cara
    self.Ratios_Caras = np.zeros((self.MAXIMO_PERSONAS, 8))
    # Caso 2-5: Histórico de descriptores face_recognition, openface, SIFT, etc
    self.HISTORICO = []
    #####################################################################################

  def avanzar_Tiempo_Inactiva(self):
    for i in range(0, self.MAXIMO_PERSONAS):
	self.Tiempo_Inactiva[i] = self.Tiempo_Inactiva[i] + 1

  #######################################################################################################
  # Extrae el cuadrado de la imagen en una nueva imagen
  #######################################################################################################
  def extraer_cara(self, imagen, x1, y1, x2, y2):
    d1 = abs(x2 - x1)
    d2 = abs(y2 - y1)
    xb1 = int(x1 - d1/2)
    xb2 = int(x2 + d1/2)
    yb1 = int(y1 - d2)
    yb2 = int(y2 + d2)
    if xb1 < 0:
	xb1 = 0
    if xb2 < 0:
	xb2 = 0
    if yb1 < 0:
	yb1 = 0
    if yb2 < 0:
	yb2 = 0
    alto = imagen.shape[0]
    ancho = imagen.shape[1]
    if xb1 >= ancho:
	xb1 = ancho - 1
    if xb2 >= ancho:
	xb2 = ancho - 1
    if yb1 >= alto:
	yb1 = alto - 1
    if yb2 >= alto:
	yb2 = alto - 1
    imagenCara = imagen[yb1:yb2, xb1:xb2]
    return imagenCara, xb1, yb1, xb2, yb2

  # Alinea y reduce la imagen
  def alinear_cara(self, imagen, x1, y1, x2, y2):
    imagen_cara, xb1, yb1, xb2, yb2 = self.extraer_cara(imagen, x1, y1, x2, y2)

    if imagen_cara is None:
	return None

    rgbImg = cv2.cvtColor(imagen_cara, cv2.COLOR_BGR2RGB)

    bb = self.align.getLargestFaceBoundingBox(rgbImg)

    if bb is None:
	return None

    alignedFace = self.align.align(96, rgbImg, bb,
                              landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)

    if alignedFace is None:
	return None
    return alignedFace


  ##############################################################################################################################
  # CASO 1: Esta función calcula los 8 ratios de la cara y los devuelve como un array (de 0 a 7). Como entrada se pasa 
  # el array de puntos generado por la librería DLIB para la coordenada X e Y. Va de 0 a 67
  # Los ratios son normalizados dividiendo por 2 veces la distancia de los ojos
  ##############################################################################################################################
  def obtener_ratios_cara(self, face_landmarks):
    # Obtenemos los puntos de la cara
    x_DLIB = np.zeros(self.PUNTOS_DLIB).astype(int)
    y_DLIB = np.zeros(self.PUNTOS_DLIB).astype(int)

    for i in range(0, self.PUNTOS_DLIB):
	x_DLIB[i] = face_landmarks.part(i).x
	y_DLIB[i] = face_landmarks.part(i).y
    
    R = np.zeros(8)
    
    # R0 - distance between middles of the eyes
    # R1 - distance between middle of the left eyes and middle point of mouth 
    # R2 - distance between middle of the right eyes and middle point of mouth
    # R3 - distance between middle of the left eyes and middle point of nose
    # R4 - distance between middle of the rigth eyes and middle point of nose
    # R5 - distance between middle point of mouth and middle point of nose
    # R6 - distance of middle point of R1 and middle of nose
    # R7 - width of nose
    
    # Centro ojo izquierdo:
    OI_x = (x_DLIB[37] + x_DLIB[38] + x_DLIB[41] + x_DLIB[40]) / 4
    OI_y = (y_DLIB[37] + y_DLIB[38] + y_DLIB[41] + y_DLIB[40]) / 4

    # Centro ojo derecho:
    OD_x = (x_DLIB[43] + x_DLIB[44] + x_DLIB[47] + x_DLIB[46]) / 4
    OD_y = (y_DLIB[43] + y_DLIB[44] + y_DLIB[47] + y_DLIB[46]) / 4

    # Punto medio de los ojos
    ME_x = (OI_x + OD_x) / 2
    ME_y = (OI_y + OD_y) / 2    
    
    # Centro boca:
    BO_x = (x_DLIB[61] + x_DLIB[63] + x_DLIB[67] + x_DLIB[65]) / 4
    BO_y = (y_DLIB[61] + y_DLIB[63] + y_DLIB[67] + y_DLIB[65]) / 4
    
    # R0
    R[0] = math.sqrt((OI_x - OD_x)**2 + (OI_y - OD_y)**2)
    # R1
    R[1] = math.sqrt((OI_x - BO_x)**2 + (OI_y - BO_y)**2) 
    # R2
    R[2] = math.sqrt((OD_x - BO_x)**2 + (OD_y - BO_y)**2)   
    # R3
    R[3] = math.sqrt((OI_x - x_DLIB[30])**2 + (OI_y - y_DLIB[30])**2)  
    # R4
    R[4] = math.sqrt((OD_x - x_DLIB[30])**2 + (OD_y - y_DLIB[30])**2)  
    # R5
    R[5] = math.sqrt((BO_x - x_DLIB[30])**2 + (BO_y - y_DLIB[30])**2)  
    # R6
    R[6] = math.sqrt((ME_x - x_DLIB[30])**2 + (ME_y - y_DLIB[30])**2)  
    # R7
    R[7] = math.sqrt((x_DLIB[31] - x_DLIB[35])**2 + (y_DLIB[31] - y_DLIB[35])**2)  
    
    # Normalizamos los ratios dividiendo por 2 veces la distancia de los ojos. Esta técnica hace los ratios
    # invariables a distancia
    for i in range(0, 8):
        R[i] = R[i] / (2 * R[0])

    return R

  # Esta función calcula la distancia entre 2 caras a partir de sus conjuntos de ratios R1 y R2.
  # Tanto R1 como R2 tienen 8 ratios de la cara numerados de 0 a 7
  def distancia_ratios_cara(self, R1, R2):
    
    resultado = 0
    for i in range(0, 8):
        resultado = resultado + (R1[i] - R2[i])**2
    resultado = math.sqrt(resultado)
    return resultado

  # Devuelve el indicador de la cara encontrada más próxima según el histórico de caras.
  # Si ninguna cara sobrepasa un umbral de detección, entonces se devuelve -1
  # La cara de entrada R es un array con los ratios de la cara a buscar
  # CH es una matriz de la forma CH[número de cara][número de ratio]
  def buscar_cara(self, R, CH):
    numero_caras = CH.shape[0]
    distancia_minima = 999999999
    indice_cara_minima = -1
    
    for i in range(0, numero_caras):
        distancia = self.distancia_ratios_cara(R, CH[i])
    	rospy.loginfo("Distancia cara a %d = %f", i, distancia)

        if distancia < distancia_minima:
            distancia_minima = distancia
            indice_cara_minima = i
    
    # Verificamos que la cara más similar se encuentre a una distancia inferior a un umbral establecido
    resultado = indice_cara_minima
    if distancia_minima >= self.UMBRAL_DISTANCIA:
        resultado = -1
    
    return resultado

  # Buscar hueco en el histórico de caras para poder introducir nueva cara. Para ello:
  # 1. Si hay huecos, se registra en los huecos. Un hueco corresponde a una cara con todos los ratios a 0
  # 2. Si no hay huecos, se busca la cara que lleve desaparecida más tiempo utilizando el tiempo de inactividad
  #    medido en número de frames inactivos
  # Se devuelve el índice para la nueva cara
  def buscar_hueco(self, CH, Tiempo_Inactiva):
    numero_caras = CH.shape[0]
    
    # Buscamos hueco, considerando un hueco donde todos los ratios son 0
    hueco = -1
    for i in range(0, numero_caras):
        libre = True
        for j in range(0, 8):
            if CH[i][j] != 0:
            	libre = False
            	break
        if libre == True:
            hueco = i
            break
    
    # Si no hay hueco, buscamos la cara que lleva más tiempo inactiva
    if hueco == -1:
        tiempo_maximo = -1
        for i in range(0, numero_caras):
            if Tiempo_Inactiva[i] > tiempo_maximo:
            	tiempo_maximo = Tiempo_Inactiva[i]
            	hueco = i
    return hueco

  # Función general para detectar el índice de la cara y ver si es una cara nueva en el sistema
  def buscar_indice_cara(self, face_landmarks):
    start_time = time()
    R = self.obtener_ratios_cara(face_landmarks)

    rospy.loginfo("Ratios R = [%f,%f,%f,%f,%f,%f,%f,%f]", R[0], R[1], R[2], R[3], R[4], R[5], R[6], R[7])

    indice_cara = self.buscar_cara(R, self.Ratios_Caras)

    # Si no encontramos la cara, buscamos hueco en el histórico
    es_cara_nueva = False
    if indice_cara == -1:
       indice_cara = self.buscar_hueco(self.Ratios_Caras, self.Tiempo_Inactiva)
       es_cara_nueva = True
                
    # Actualizamos los ratios y marcamos la cara como activa
    self.Ratios_Caras[indice_cara] = R
    self.Tiempo_Inactiva[indice_cara] = 0

    # Calcular tiempo transcurrido
    elapsed_time = time() - start_time
    print("Tiempo encoding cara con ratios: %0.10f seconds." % elapsed_time)

    return indice_cara, es_cara_nueva
  ##############################################################################################################################

  ##############################################################################################################################
  # CASO 2: Codifica la cara utilizando la librería Face Recognition
  # La cara de entrada ha sido leída con OpenCV
  # Utilizando librería de Face Recognition
  # https://pypi.org/project/face_recognition/
  # https://medium.com/@ageitgey/machine-learning-is-fun-part-4-modern-face-recognition-with-deep-learning-c3cffc121d78
  # Revisar: install cuda library ubuntu 16.04
  # Utilizando la librería face_recognition. Es muy efectivo pero lento con CPU (0,42 segundos en obtener descriptor
  # de 128 para una cara). Se necesitaría GPU
  ##############################################################################################################################
  def obtener_encoding_cara(self, imagen, face_landmarks, x1, y1, x2, y2):
    imagen_cara, xb1, yb1, xb2, yb2 = self.extraer_cara(imagen,x1, y1, x2, y2)

    #cv2.imshow("imagen_cara", imagen_cara)
    #cv2.waitKey(3)

    #cv2.imwrite("/home/disa/Imagen" + str(self.contador).strip() + ".png", imagen_cara)
    #self.contador = self.contador + 1

    # Convertir cara de BGR (OpenCV) a RGB (DLIB)
    imagen_dlib = imagen_cara[:, :, ::-1]

    #https://www.pyimagesearch.com/2015/09/07/blur-detection-with-opencv/

    """print("IMAGEN_DLIB")
    print(len(imagen_dlib))"""
    encoding = face_recognition.face_encodings(imagen_dlib)
    """ print("ENCODING")
    print(encoding)

    if len(encoding) == 0:
	win = dlib.image_window()
	win.set_image(imagen_dlib)
	dlib.hit_enter_to_continue()"""

    if encoding is None:
	return None

    if len(encoding) > 0:
    	return encoding[0]
    else:
	return None
 
  def obtener_encoding_cara_old(self, imagen, face_landmarks, x1, y1, x2, y2):
    start_time = time()

    # Obtener array de imagen
    #im_pil = image2.fromarray(imagen)
    #im_np = np.asarray(im_pil)

    im_np = np.array(imagen)

    # Obtener los raw_landmarks
    raw_landmarks = []
    raw_landmarks.append(face_landmarks)

    # Obtener encoding
    # En vez de utilizar la función de face encoding, partimos con los puntos DLIB ya calculados
    # Obtener el encoding (128 ratios por cara). Consideramos que solo hay una cara
    encodings = [np.array(self.face_encoder.compute_face_descriptor(im_np, raw_landmark_set)) for raw_landmark_set in raw_landmarks]

    """# Let's generate the aligned image using get_face_chip
    face_chip = dlib.get_face_chip(imagen, face_landmarks)        

    # Now we simply pass this chip (aligned image) to the api
    face_descriptor_from_prealigned_image = self.face_encoder.compute_face_descriptor(face_chip)"""     

    print(encodings[0])       

    # Calcular tiempo transcurrido
    elapsed_time = time() - start_time
    print("Tiempo encoding cara con Face_Recognition: %0.10f seconds." % elapsed_time)

    return encodings[0]
    #return face_descriptor_from_prealigned_image

  # Devuelve el indicador de la cara encontrada más próxima según un conjunto de caras codificadas
  # Si ninguna cara coincide, entonces se devuelve -1
  # ENCL es una lista de encodings de caras
  # ENC es el encoding de la cara a buscar
  def buscar_cara_ENC(self, ENC, ENCL):
    numero_caras = len(ENCL)

    if ENC is None:
	return -1

    if len(ENC) == 0:
	return -1

    # Si se encuentra la cara, interrumpimos el bucle y devolvemos el índice
    # If you are getting multiple matches for the same person, it might be that the people in your photos
    # look very similar and a lower tolerance valueis needed to make face comparisons more strict. 
    # You can do that with the--tolerance parameter. The default tolerancevalue is 0.6 and lower numbers 
    # make face comparisons more strict:

    if numero_caras > 0 and ENC != None:
	# resultado = face_recognition.compare_faces(ENCL, ENC, tolerance=0.7)
	resultado = face_recognition.compare_faces(ENCL, ENC, tolerance=0.6)
	#resultado = face_recognition.compare_faces(ENCL, ENC)
        # print("Cara individual")
        # print(ENC)
	for i in range(0, numero_caras):
		if resultado[i] == True:
	    		return i

    # Si no se encuentra devolvemos -1
    return -1

  # Buscar hueco en el histórico de caras para poder introducir nueva cara. Para ello:
  # 1. Si hay huecos, se registra en los huecos. Un hueco corresponde a una cara con todos los ratios a 0
  # 2. Si no hay huecos, se busca la cara que lleve desaparecida más tiempo utilizando el tiempo de inactividad
  #    medido en número de frames inactivos
  # Se devuelve el índice para la nueva cara
  def buscar_hueco_ENC(self, R, CH, Tiempo_Inactiva):
    numero_caras = len(CH)

    if numero_caras < self.MAXIMO_PERSONAS:
	CH.append(R)
	return len(CH) - 1

    tiempo_maximo = -1
    for i in range(0, numero_caras):
	if Tiempo_Inactiva[i] > tiempo_maximo:
            	tiempo_maximo = Tiempo_Inactiva[i]
            	hueco = i
    CH[hueco] = R
    return hueco

  # Función general para detectar el índice de la cara con SIFT
  def buscar_indice_cara_ENC(self, imagen, face_landmarks, x1, y1, x2, y2):
    start_time = time()

    # Obtenemos el encoding de la cara (vector con 128 características)
    encoding = self.obtener_encoding_cara(imagen, face_landmarks, x1, y1, x2, y2)

    if encoding is None:
	return -1, False

    # Buscamos la cara en la lista de las últimas personas conocidas
    indice_cara = self.buscar_cara_ENC(encoding, self.HISTORICO)

    # Si el encoding de la cara es nulo (imagen de persona borrosa), no procesamos su cara
    # Devolvemos un -1 y un es_cara_nueva = False
    # Lo interceptamos fuera de este método

    if indice_cara == -1 and encoding is None:
	return -1, False

    if indice_cara == -1 and len(encoding) == 0:
	return -1, False

    es_cara_nueva = False
    if indice_cara == -1:
	indice_cara = self.buscar_hueco_ENC(encoding, self.HISTORICO, self.Tiempo_Inactiva)
	es_cara_nueva = True

    # Actualizamos el histórico y marcamos la cara como activa
    self.HISTORICO[indice_cara] = encoding
    self.Tiempo_Inactiva[indice_cara] = 0

    # Calcular tiempo transcurrido
    elapsed_time = time() - start_time
    print("Tiempo búsqueda cara con FACE_RECOGNITION: %0.10f seconds." % elapsed_time)

    return indice_cara, es_cara_nueva


  ##############################################################################################################################

  ##############################################################################################################################
  # CASO 3: Utilizando la librería openface. Al igual que el anterior, genera un descriptor de 128 valores. Al procesarse
  #         como una red profunda sobre la propia imagen, es lento. 0,22 segundos en CPU. Requeriría GPU
  ##############################################################################################################################
  def obtener_encoding_cara_open_face(self, imagen, face_landmarks, x1, y1, x2, y2):
    start_time = time()

    alignedFace = self.alinear_cara(imagen, x1, y1, x2, y2)

    cv2.imshow("alignedFace", alignedFace)
    cv2.waitKey(3)

    if alignedFace == None:
	return None
    rep = self.net.forward(alignedFace)

    # Calculate the elapsed time.
    elapsed_time = time() - start_time
    print("Tiempo encoding cara con Open_Face: %0.10f seconds." % elapsed_time)

    return rep
  ##############################################################################################################################

  ##############################################################################################################################
  # CASO 4. Pruebas con SIFT. Obteniendo los puntos característicos con SIFT. Es rápido pero parece que no
  #         ofrece buenos resultados
  ##############################################################################################################################
  def obtener_encoding_SIFT(self, imagen, x1, y1, x2, y2):
    start_time = time()

    imagen_cara, xb1, yb1, xb2, yb2 = self.extraer_cara(imagen, x1, y1, x2, y2)

    if imagen_cara is None:
	return None

    gray = cv2.cvtColor(imagen_cara,cv2.COLOR_BGR2GRAY)

    sift = cv2.xfeatures2d.SIFT_create()

    #n_kp = 50
    #sift = cv2.xfeatures2d.SIFT_create(n_kp)

    kp, des = sift.detectAndCompute(gray,None)

    img = cv2.drawKeypoints(gray,kp, outImage=np.array([]), color=(0, 0, 255))

    elapsed_time = time() - start_time
    print("(SIFT) Elapsed time: %0.10f seconds." % elapsed_time)


    cv2.imshow("keyPoints", img)
    cv2.waitKey(3)

    return des

  # Esta función calcula la distancia entre 2 caras a partir de sus conjuntos de keys SIFT
  def distancia_caras_SIFT(self, sift1, sift2):
    
    resultado = 0

    # BFMatcher with default params
    bf = cv2.BFMatcher()

    if sift1 != None and sift2 != None:
	# BFMatcher with default params
	bf = cv2.BFMatcher()
	matches = bf.knnMatch(sift1,sift1, k=2)

	# Apply ratio test
	good = []
	for m,n in matches:
	    if m.distance < 0.75*n.distance:
		good.append([m])

	resultado = len(good)

    # matches = sorted(matches, key=lambda val: val.distance)
    #img3 = drawMatches(img1,kp1,img2,kp2,matches[:25])
    
    return resultado

  # Devuelve el indicador de la cara encontrada más próxima según el histórico de caras.
  # Si ninguna cara sobrepasa un umbral de detección, entonces se devuelve -1
  def buscar_cara_SIFT(self, R, CH):
    if CH:
    	numero_caras = len(CH)
    else:
	numero_caras = 0

    rospy.loginfo("NUM CARAS %d", numero_caras)
    distancia_maxima = -99999
    indice_cara_maxima = -1
    
    for i in range(0, numero_caras):
        distancia = self.distancia_caras_SIFT(R, CH[i])
        print(distancia)
    	rospy.loginfo("Distancia cara a %d = %f", i, distancia)

        if distancia > distancia_maxima:
            distancia_maxima = distancia
            indice_cara_maxima = i
    
    # Verificamos que la cara más similar se encuentre a una distancia inferior a un umbral establecido
    resultado = indice_cara_maxima
    # 5 emparejamientos de cara se considera ser la misma persona
    UMBRAL_DISTANCIA = 50
    if distancia_maxima < UMBRAL_DISTANCIA:
        resultado = -1
    
    return resultado

  # Buscar hueco en el histórico de caras para poder introducir nueva cara. Para ello:
  # 1. Si hay huecos, se registra en los huecos. Un hueco corresponde a una cara con todos los ratios a 0
  # 2. Si no hay huecos, se busca la cara que lleve desaparecida más tiempo utilizando el tiempo de inactividad
  #    medido en número de frames inactivos
  # Se devuelve el índice para la nueva cara
  def buscar_hueco_SIFT(self, R, CH, Tiempo_Inactiva):
    numero_caras = len(CH)

    if numero_caras < self.MAXIMO_PERSONAS:
	CH.append(R)
	return len(CH) - 1

    tiempo_maximo = -1
    for i in range(0, numero_caras):
	if Tiempo_Inactiva[i] > tiempo_maximo:
            	tiempo_maximo = Tiempo_Inactiva[i]
            	hueco = i
    CH[hueco] = R
    return hueco

  # Función general para detectar el índice de la cara con SIFT
  def buscar_indice_cara_SIFT(self, imagen, x1, y1, x2, y2):
    start_time = time()

    siftFace = self.obtener_encoding_SIFT(imagen, x1, y1, x2, y2)
    indice_cara = self.buscar_cara_SIFT(siftFace, self.HISTORICO)

    es_cara_nueva = False
    if indice_cara == -1:
	indice_cara = self.buscar_hueco_SIFT(siftFace, self.HISTORICO, self.Tiempo_Inactiva)
	es_cara_nueva = True

    # Actualizamos el histórico y marcamos la cara como activa
    self.HISTORICO[indice_cara] = siftFace
    self.Tiempo_Inactiva[indice_cara] = 0

    # Calcular tiempo transcurrido
    elapsed_time = time() - start_time
    print("Tiempo búsqueda cara con SIFT: %0.10f seconds." % elapsed_time)

    return indice_cara, es_cara_nueva

  ##############################################################################################################################
  # CASO 5: Comparación de imágenes píxel a píxel. Para ello se alinea la imagen de la cara para tener los ojos en una posición
  #         concreta y se procede a la comparación.
  ##############################################################################################################################
  def obtener_diferencia_imagenes(self, imagen1, imagen2):
    alto = imagen1.shape[0]
    ancho = imagen1.shape[1]

    diferencia = 0.0
    for i in range(0, alto):
    	for j in range(0, ancho):
		diferencia = diferencia + (imagen1[i][j] - imagen2[i][j]) / 255
    return diferencia

  # Devuelve el indicador de la cara encontrada más próxima según el histórico de caras.
  # Si ninguna cara sobrepasa un umbral de detección, entonces se devuelve -1
  def buscar_cara_IMG(self, R, CH):
    if CH:
    	numero_caras = len(CH)
    else:
	numero_caras = 0

    distancia_minima = 9999999999
    indice_cara_minima = -1
    
    for i in range(0, numero_caras):
        distancia = self.obtener_diferencia_imagenes(R, CH[i])
    	rospy.loginfo("Distancia cara a %d = %f", i, distancia)

        if distancia < distancia_minima:
            distancia_minima = distancia
            indice_cara_minima = i

    UMBRAL = 50*96*96/255
    
    if distancia_minima > UMBRAL:
    	indice_cara_minima = -1 
    
    return indice_cara_minima

  # Buscar hueco en el histórico de caras para poder introducir nueva cara. Para ello:
  # 1. Si hay huecos, se registra en los huecos. Un hueco corresponde a una cara con todos los ratios a 0
  # 2. Si no hay huecos, se busca la cara que lleve desaparecida más tiempo utilizando el tiempo de inactividad
  #    medido en número de frames inactivos
  # Se devuelve el índice para la nueva cara
  def buscar_hueco_IMG(self, R, CH, Tiempo_Inactiva):
    numero_caras = len(CH)

    if numero_caras < self.MAXIMO_PERSONAS:
	CH.append(R)
	return len(CH) - 1

    tiempo_maximo = -1
    for i in range(0, numero_caras):
	if Tiempo_Inactiva[i] > tiempo_maximo:
            	tiempo_maximo = Tiempo_Inactiva[i]
            	hueco = i
    CH[hueco] = R
    return hueco

  # Función general para detectar el índice de la cara y ver si es una cara nueva en el sistema
  def buscar_indice_cara_IMG(self, imagen, x1, y1, x2, y2):
    start_time = time()

    imagen_alineada = self.alinear_cara(imagen, x1, y1, x2, y2)
    gray = cv2.cvtColor(imagen_alineada,cv2.COLOR_BGR2GRAY)

    indice_cara = self.buscar_cara_IMG(gray, self.HISTORICO)

    # Si no encontramos la cara, buscamos hueco en el histórico
    es_cara_nueva = False
    if indice_cara == -1:
       indice_cara = self.buscar_hueco_IMG(gray, self.HISTORICO, self.Tiempo_Inactiva)
       es_cara_nueva = True
                
    # Actualizamos los ratios y marcamos la cara como activa
    self.HISTORICO[indice_cara] = gray
    self.Tiempo_Inactiva[indice_cara] = 0

    # Calcular tiempo transcurrido
    elapsed_time = time() - start_time
    print("Tiempo con comparación de imágenes: %0.10f seconds." % elapsed_time)

    return indice_cara, es_cara_nueva
  ##############################################################################################################################






