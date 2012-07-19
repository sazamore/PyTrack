#!/usr/bin/env python
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
	def __init__(self):
		"""
		Initializes a Benchmark Object.
		Note: It will break if it grabs a time less than a second. 

		Data members:
		startTime -- Datetime object at start of benchmark.
		num -- Stores amount of objects loaded/processed so we can get a rate 
		"""
		self.reset()
	def start(self, prefix, num):
		"""Starts the timer."""
		self.startTime = datetime.datetime.now()
		self.num = num
		print(prefix + " " + str(num) + " Images...")
	def end(self):
		"""Ends the timer. Returns seconds took."""
		# Returns Datetime Timedelta
		result =  datetime.datetime.now() - self.startTime
		rate = round(self.num / result.seconds, 3)
		print("Done in " + str(result.seconds) + " seconds. (" + str(rate) + " objects/sec)")
		self.reset()
		return result.seconds
	def reset(self):
		"""Resets the timer."""
		self.startTime = None
		self.num = 0

# PostProcess Class
# This would work really nice with threading.
class PostProcess:
	"""Used to process a batch of images."""
	def __init__(self, startFrame, endFrame, benchmark = False):
		"""
		Initializes a PostProcess Object.

		Data members:
		startFrame -- Start frame of post process
		endFrame -- End frame of post process
		totalFrames -- Total frames to post process
		queue -- A list of CompareFiles objects to process
		benchmark -- To enable/disable benchmarking
		"""
		# Frame Vars
		self.startFrame = startFrame
		self.endFrame = endFrame
		self.totalFrames = abs(endFrame - startFrame)
		# Queue Var
		self.queue = []
		# Benchmark Object
		self.benchmark = benchmark
		if self.benchmark:
			self.bench = Benchmark()
	def load(self):
		"""Load frames from disk to memory, and add them to queue."""
		if self.benchmark:
			self.bench.start("Loading", self.totalFrames)
		for i in range(self.startFrame, self.endFrame):
			img1 = ImageFile(genFile(i))
			img2 = ImageFile(genFile(i+1))
			self.queue.append( CompareFiles(img1,img2) )
		if self.benchmark:
			self.bench.end()
	def process(self):
		"""Process frames in queue."""
		if self.benchmark:
			self.bench.start("Processing", self.totalFrames)
		for obj in self.queue:
			obj.process( 0.3, (0.5, 0.5, 0.5), 300 )
			# Grab Obj's Internal Data Here
			self.queue.remove(obj)
		if self.benchmark:
			self.bench.end()
	def run(self):
		"""Load and process selected frames."""
		self.load()
		self.process()

# Main
if __name__ == "__main__":
	# Vars
	start = 1
	end = 1450
	limit = 500
	inter = abs(end-start)
	# Intended to split a process job into managemable chunks
	# The range function is a little wonky, and there is probably a better way
	# See: http://stackoverflow.com/q/312443
	for i in range(1, inter, limit):
		# To prevent going over with silly range
		if i+limit-1 > end:
			process = PostProcess(i, end, True)
		else:
			process = PostProcess(i, i+limit-1, True)
		process.run()