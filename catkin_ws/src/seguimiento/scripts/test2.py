#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 09:32:37 2019

@author: Jaime Duque Domingo (UVA)

Esta clase permite hacer un test del comportamiento del avatar

"""
import rospy
import sys
import cv2
import time
import numpy as np


def main(args):
  rospy.init_node('test2', anonymous=True)
  for i in range(1, 9):
	img = cv2.imread("/home/disa/Imagen" + str(i).strip() + ".png") 
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	borrosidad = float(cv2.Laplacian(gray, cv2.CV_64F).var())
	
	rospy.loginfo("Borrosidad cara %d = %f", i, borrosidad)

  cap = cv2.VideoCapture(0)

  cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1024) 

  rospy.loginfo("CAP_PROP_FRAME_WIDTH : %d", cap.get(cv2.CAP_PROP_FRAME_WIDTH))
  rospy.loginfo("CAP_PROP_FRAME_HEIGHT : %d", cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
  rospy.loginfo("CAP_PROP_FPS : %d", cap.get(cv2.CAP_PROP_FPS))
  rospy.loginfo("CAP_PROP_AUTO_EXPOSURE : %d", cap.get(cv2.CAP_PROP_AUTO_EXPOSURE))

  image = cv2.imread('/home/disa/Imagen2.png')
  sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
  sharpen = cv2.filter2D(image, -1, sharpen_kernel)

  cv2.imshow('sharpen', sharpen)
  cv2.waitKey()


  time.sleep(2)

  cap.set(cv2.CAP_PROP_EXPOSURE, 40) 

  rospy.loginfo("CAP_PROP_EXPOSURE : %f", cap.get(15))

if __name__ == '__main__':
    main(sys.argv)









