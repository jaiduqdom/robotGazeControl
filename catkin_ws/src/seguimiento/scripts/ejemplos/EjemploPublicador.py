#!/usr/bin/env python
# license removed for brevity
import rospy
import numpy as np
from camara.msg import ArrayFloat

def talker():
    pub = rospy.Publisher('chatter', ArrayFloat, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    #vector.data = np.zeros(10)
    vector = ArrayFloat()

    vector.data = np.zeros(10)

    while not rospy.is_shutdown():

	vector.header.stamp = rospy.Time.now()


    	vector.data[0] += 1
    	vector.data[1] += 2


	
        #hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(vector)
        pub.publish(vector)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass

