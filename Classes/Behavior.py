#!/usr/bin/env python
# Filename: Behavior.py
# Project Github: http://github.com/super3/PyTrack
# Author: Shawn Wilkinson <me@super3.org>
# Author Website: http://super3.org/
# License: GPLv3 <http://gplv3.fsf.org/>

# Imports
import math

class AbTrack:
	"""Tracks the abdomen's movement."""
	def __init__(self, thres):
		self.body = (0,0)
		self.tail = (0,0)
		self.thres = thres
		self.dir = "Unknown"
	def compare(self, boundCenter, targetCentroid):
		self.body = boundCenter
		self.tail = targetCentroid
		if abs(self.body[0] - self.tail[0]) <= self.thres:
			self.dir = "Center"
		elif (self.body[0] - self.tail[0]) > 0:
			self.dir = "Left"
		else:
			self.dir = "Right"
	def getDir(self):
		return self.dir

class CentroidTrack:
	"""Tracks centroid accuracy."""
	def __init__(self, thres):
		self.count = 0
		self.decount = 0
		self.thres = thres
		self.previousCentroid = (0,0)
	def add(self, centroid):
		x1 = self.previousCentroid[0]
		x2 = centroid[0]
		y1 = self.previousCentroid[1]
		y2 = centroid[1]
		dist = math.hypot(x1-x2, y1-y2)
		if dist <= self.thres:
			self.count += 1
			self.decount = 0
		else:
			self.decount += 1
			self.count = 0
		self.previousCentroid = centroid
	def printInfo(self):
		info = "[Abdomen Track] "
		if self.count < 3:
			info += "Poor"
		elif self.count >= 3 and self.count <= 7:
			info += "Fair"
		else:
			info += "Good" 
		info += str(self.count)
		info += "\n[Legs Deployed] "
		if self.decount <= 3:
			info += "No"
		else:
			info += "Yes!"
		info += str(self.decount)
		print(info)
