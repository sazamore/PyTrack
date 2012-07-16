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
# This would work really nice with threading.
class PostProcess:
	"""Used to process a batch of images."""
	def __init__(self, startFrame, endFrame):
		# Frame Vars
		self.startFrame = startFrame
		self.endFrame = endFrame
		self.totalFrames = abs(endFrame - startFrame)
		# Queue Var
		self.queue = []
		# Benchmark Object
		self.bench = Benchmark(True)
	def load(self, start, end):
		self.bench.start("Loading", self.totalFrames)
		for i in range(start, end):
			self.queue.append( CompareFiles(genFile(i), genFile(i+1)) )
		self.bench.end()
	def process(self):
		self.bench.start("Processing", self.totalFrames)
		for obj in self.queue:
			obj.process( 0.3, (0.5, 0.5, 0.5), 300 )
			# Grab Obj's Internal Data Here
			self.queue.remove(obj)
		self.bench.end()
	def run(self):
		self.load(self.startFrame, self.endFrame)
		self.process()



# Main
if __name__ == "__main__":
	process = PostProcess(1, 500)
	process.run() 