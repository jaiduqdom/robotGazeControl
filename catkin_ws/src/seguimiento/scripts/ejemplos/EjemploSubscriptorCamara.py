#!/usr/bin/env python
# -*- coding: utf-8 -*-
# license removed for brevity
import rospy
import sys
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class subscriptor_imagen:

  def __init__(self):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("imagen_topic",Image,self.callback)

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    cv2.imshow("Imagen recibida", cv_image)
    cv2.waitKey(3)

def main(args):
  ic = subscriptor_imagen()
  rospy.init_node('recibirFrames', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)

