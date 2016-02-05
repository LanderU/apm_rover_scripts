#
#message -> mavros/OverrideRCIn
#topic -> mavros/rc/override
#

#!/usr/bin/env python3

import os
import sys
#import math
#import socket
import rospy
import time
from mavros_msgs.msg import OverrideRCIn
from mavros_msgs.srv import SetMode

throttle_channel=2
steer_channel=0
exec_time=1 #exc time in secs

def talker():
	pub = rospy.Publisher('mavros/rc/override', OverrideRCIn, queue_size=10)
    	rospy.init_node('custom_talker', anonymous=True)
	r = rospy.Rate(10) #10hz
	msg = OverrideRCIn()
	start = time.time()
        flag=True #time flag
	#for i in range (0,8):
        #        msg.channels[i]=2000
	#speed='SLOW'
	speed='FAST'
	if speed =='SLOW':
		msg.channels[throttle_channel]=1560
		msg.channels[steer_channel]=1370
	elif speed =='NORMAL':
		msg.channels[throttle_channel]=1565
                msg.channels[steer_channel]=1370
	elif speed == 'FAST':	
		msg.channels[throttle_channel]=1570
                msg.channels[steer_channel]=1370
	while not rospy.is_shutdown() and flag:
		sample_time=time.time()
		if ((sample_time - start) > exec_time):
			flag=False
        	rospy.loginfo(msg)
        	pub.publish(msg)
        	r.sleep()

if __name__ == '__main__':

	rospy.wait_for_service('/mavros/set_mode')
	change_mode = rospy.ServiceProxy('/mavros/set_mode', SetMode)
	resp1 = change_mode(custom_mode="manual")
	print (resp1)
        
	if "True" in str(resp1):
    		try:
	        	talker()
	
		except rospy.ROSInterruptException: pass

