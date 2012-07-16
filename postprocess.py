#!/usr/local/bin/python
# Filename: postprocess.py
# Project Github: http://github.com/super3/PyTrack
# Author: Shawn Wilkinson <me@super3.org>
# Author Website: http://super3.org/
# License: GPLv3 <http://gplv3.fsf.org/>

# Imports
import datetime
from Classes.CompareFiles import *
from Classes.Helper import *

# Benchmark Class
class Benchmark:
	"""Allows for timing of load and process events."""
	def __init__(self, debug = False):
		"""
		Initializes a Benchmark Object.

		Data members:
		startTime -- Datetime object at start of benchmark.
		num -- Stores amount of objects loaded/processed so we can get a rate 
		debug -- Used to display or suppress the ouput
		"""
		self.debug = debug
		self.reset()
	def start(self, prefix, num):
		"""Starts the timer."""
		self.startTime = datetime.datetime.now()
		self.num = num
		if self.debug:
			print(prefix + " " + str(num) + " Images...")
	def end(self):
		"""Ends the timer."""
		# Returns Datetime Timedelta
		result =  datetime.datetime.now() - self.startTime
		rate = round(self.num / result.seconds, 3)
		if self.debug:
			print("Done in " + str(result.seconds) + " seconds. (" + str(rate) + " objects/sec)")
		self.reset()
	def reset(self):
		"""Resets the timer."""
		self.startTime = None
		self.num = 0

# PostProcess Class
class PostProcess:
	"""Used to process a batch of images."""
	def __init__(self, startFrame, endFrame):
		# Frame Vars
		self.startFrame = startFrame
		self.endFrame = endFrame
		self.totalFrames = abs(endFrame - startFrame)
		# Queue Vars
		self.queue = []
	def load(self):
		pass


# Main
if __name__ == "__main__":
	# Images to Process
	start = 1
	end = 500
	# Object Array
	queue = []
	# Benchmark Object
	timeIt = Benchmark(True)

	timeIt.start("Loading", abs(end-start))
	# Load Images into Memory 
	for i in range(start, end):
		queue.append( CompareFiles(genFile(i), genFile(i+1)) )
	timeIt.end()

	# Process Images in Queue
	timeIt.start("Processing", abs(end-start))
	for obj in queue:
		obj.process( 0.3, (0.5, 0.5, 0.5), 300 )
		queue.remove(obj)
	timeIt.end()