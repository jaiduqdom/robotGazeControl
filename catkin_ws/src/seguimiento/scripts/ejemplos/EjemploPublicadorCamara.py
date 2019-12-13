#!/usr/bin/env python
# -*- coding: utf-8 -*-
# license removed for brevity
import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def publicarFrames():

    # Iniciar nodo
    rospy.init_node('publicarFrames', anonymous=True)
    
    # Crear publicador
    pub = rospy.Publisher("imagen_topic",Image)

    # Definir ratio
    rate = rospy.Rate(20) # 20hz

    # Captura con OpenCV
    cap = cv2.VideoCapture(0)

    # Creamos el bridge ROS<->CV2
    bridge = CvBridge()

    while not rospy.is_shutdown():

        # Lectura de frame
        ret, frame = cap.read()

	# Publicación de frame
	try:
		# Convertir imagen OpenCV en mensaje ROS y publicar
	      	pub.publish(bridge.cv2_to_imgmsg(frame, "bgr8"))
	except CvBridgeError as e:
	      	print(e)

	# Espera
	cv2.waitKey(3)

        # rate.sleep()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        publicarFrames()
    except rospy.ROSInterruptException:
        pass

