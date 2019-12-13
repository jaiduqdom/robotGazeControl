#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 09:32:37 2019

@author: Jaime Duque Domingo (UVA)

Esta clase permite corregir la distorsión de la lente del robot
Si se cambia de cámara habrá que recalibrar los valores según el algoritmo mostrado en:
https://medium.com/@kennethjiang/calibrate-fisheye-lens-using-opencv-333b05afa0b0

El código de calibración está en catkin_ws/src/calibracionOjoPez

"""

import rospy
import cv2
assert cv2.__version__[0] == '3', 'The fisheye module requires opencv version >= 3.0.0'

import numpy as np
import os
import glob
import sys

class correctorDistorsionOjoPez:

  def __init__(self):
    # You should replace these 3 lines with the output in calibration step
    self.DIM=(640, 480)
    self.K=np.array([[381.509884911731, 0.0, 342.01179674191275], [0.0, 378.9520933716717, 228.85867749447283], [0.0, 0.0, 1.0]])
    self.D=np.array([[-0.09312454499934952], [-0.03429930494615691], [0.05725257344822597], [-0.0319059798908104]])

  ###############################################################################################
  # Corrección de la distorsión de la cámara del robot
  ###############################################################################################
  def undistort(self, imagen):
    #img = cv2.imread(img_path)
    h,w = imagen.shape[:2]    

    map1, map2 = cv2.fisheye.initUndistortRectifyMap(self.K, self.D, np.eye(3), self.K, self.DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(imagen, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)    
    #cv2.imshow("undistorted", undistorted_img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return undistorted_img

