#
#message -> mavros/OverrideRCIn
#topic -> mavros/rc/override
#

#!/usr/bin/env python3

import os
import sys
import rospy
import time
from mavros_msgs.msg import OverrideRCIn
from mavros_msgs.srv import SetMode

throttle_channel=2
steer_channel=0
exec_time=1 #exc time in secs

'''
PWM values are hardcoded right now.
Best practices could be to read the max and min
of steer and throttle in order to calculate:
- Right PWM
- Center PWM
- Left PWM
- Full gas PWM
- Normal speed PWM
- Slow PWM
'''

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

	direction='LEFT'
	if direction =='CENTER':
		msg.channels[steer_channel]=1385
	elif direction =='RIGHT':
		msg.channels[steer_channel]=1450
	elif direction == 'LEFT':	
		msg.channels[steer_channel]=1300

	msg.channels[throttle_channel]=1558
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

