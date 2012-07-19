#!/usr/bin/env python
# Filename: realtime.py
# Project Github: http://github.com/super3/PyTrack
# Author: Shawn Wilkinson <me@super3.org>
# Author Website: http://super3.org/
# License: GPLv3 <http://gplv3.fsf.org/>

# PyTrack Imports
from Classes.Images import ImageBuffer
from Classes.CompareImages import *
from Classes.CompareFiles import *

# Ros Imports
import roslib; roslib.load_manifest('moth_3d')
import rospy
from sensor_msgs.msg import Image

# Loop Vars
file1 = None
file2 = None
start = True

# Functions
def callback(data):
	#rospy.loginfo(rospy.get_name() + "I heard %s", data.data)
	
	# Get Vars
	global file1
	global file2
	global start

	# Fill Both ImageFile Objects Just After Start
	if start:
		file1 = ImageBuffer(data.data, (data.width, data.height), 'RGB')
		file2 = ImageBuffer(data.data, (data.width, data.height), 'RGB')
		start = False
	else:
		# Switch Objects and Load in New One
		file1 = file2
		file2 = ImageBuffer(data.data, (data.width, data.height), 'RGB')
		# Compare and Print Info
		compare = CompareFiles(file1, file2)
		compare.process(0.2, (0.5, 0.5, 0.5), 300)
		compare.printInfo()
def listener():
	rospy.init_node('pytrack', anonymous=True)
	rospy.Subscriber("image_raw", Image, callback)
	rospy.spin()

# Main
if __name__ == '__main__':
	listener()
