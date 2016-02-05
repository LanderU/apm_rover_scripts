#!/usr/bin/env python3

import os
import sys
import math
import socket
import rospy
from mavros_msgs.srv import SetMode

def talker():
	
	rospy.init_node('rover_mode')
	rospy.wait_for_service('/mavros/set_mode')
	try:
		change_mode = rospy.ServiceProxy('/mavros/set_mode', SetMode)
		resp1 = change_mode(custom_mode="guided")
		return resp1.success
    	except rospy.ServiceException, e:
		print ("Service call failed: %s" %e)
    
print (talker())
