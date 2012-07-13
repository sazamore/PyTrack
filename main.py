#!/usr/local/bin/python
# Filename: main.py
# Project Github: http://github.com/super3/PyTrack
# Author: Shawn Wilkinson <me@super3.org>
# Author Website: http://super3.org/
# License: GPLv3 <http://gplv3.fsf.org/>

# Imports
from ImageFile import *
from CompareFiles import *
from Helper import *

# Start the Class
runIt = Main()

# Open the Files
file1 = open("absdiff.txt", mode="w", encoding="utf-8")
file2 = open("absy.txt", mode="w", encoding="utf-8")

# Loop
for i in range(1, 1450): # Max 1450
	# Read In Files
	jpg1 = 'SampleData/moth' + str(i).zfill(4) + '.jpg'
	jpg2 = 'SampleData/moth' + str(i+1).zfill(4) + '.jpg'
	# Print Files
	img1 = ImageFile(jpg1)
	img2 = ImageFile(jpg2)
	print("Comparing '" + jpg1 + "' to '" + jpg2 + "'")
	runIt.compareFile(img1, img2, 0.5)
	# file1.write(str(runIt.conflicts) + "\n")
	# file2.write(str(runIt.absy) + "\n")
	
# Close the Files
file1.close()
file2.close()