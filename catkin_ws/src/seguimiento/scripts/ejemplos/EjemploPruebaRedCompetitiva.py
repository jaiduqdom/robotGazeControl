#!/usr/bin/env python
# license removed for brevity
import rospy
import numpy as np
from camara.msg import ArrayFloat
from time import time

def talker():
    pub = rospy.Publisher('entrada', ArrayFloat, queue_size=10)
    rospy.init_node('pubRedCompetitiva', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    tiempo_anterior = time()

    contador = 1

    #vector.data = np.zeros(10)
    vector = ArrayFloat()

    while not rospy.is_shutdown():

	if time() > tiempo_anterior + 5:
		contador = contador + 1
		tiempo_anterior = time()
    	vector.data = np.zeros(4)
	if contador > 3:
		contador = 1
	vector.data[contador] = 1

	vector.header.stamp = rospy.Time.now()


        #hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(vector)
        pub.publish(vector)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

