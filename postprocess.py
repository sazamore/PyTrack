#!/usr/local/bin/python
# Filename: postprocess.py
# Project Github: http://github.com/super3/PyTrack
# Author: Shawn Wilkinson <me@super3.org>
# Author Website: http://super3.org/
# License: GPLv3 <http://gplv3.fsf.org/>

# Imports
from Classes.ImageFile import *
from Classes.CompareFiles import *
from Classes.Helper import *

# Benchmark 
import datetime

# Images to Process
start = 1
end = 500

# Object Array
queue = []

startTime = datetime.datetime.now() # Benchmark
# Load Images into Memory 
print("Loading " + str(abs(end-start)) + " Images into Memory...") # Debug
for i in range(start, end):
	queue.append( CompareFiles(genFile(i), genFile(i+1)) )
print("Loaded Images into Memory...")   #Debug
endTime = datetime.datetime.now() - startTime # Benchmark
print("Loaded in " + str(endTime.seconds) + " seconds.") # Benchmark
print("Rate is " + str(abs(end-start)/endTime.seconds) + " objects/second.\n") # Benchmark

# Process Images in Queue
startTime = datetime.datetime.now() # Benchmark
print("Processing...")
for obj in queue:
	obj.process( 0.3, (0.5, 0.5, 0.5), 300 )
	queue.remove(obj)
print("Processing Done!")
endTime = datetime.datetime.now() - startTime # Benchmark
print("Loaded in " + str(endTime.seconds) + " seconds.") # Benchmark
print("Rate is " + str(abs(end-start)/endTime.seconds) + " objects/second.") # Benchmark