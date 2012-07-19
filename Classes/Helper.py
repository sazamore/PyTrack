#!/usr/bin/env python
# Filename: Helper.py
# Project Github: http://github.com/super3/PyTrack
# Author: Shawn Wilkinson <me@super3.org>
# Author Website: http://super3.org/
# License: GPLv3 <http://gplv3.fsf.org/>

# Imports
import os

# Constant Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED   = (255,0,0)
GREEN = (0,255,0)
BLUE  = (0,0,255)

# Helpful Functions
def genFile(i):
	"""Return a usable image path."""
	return 'SampleData/moth' + str(i).zfill(4) + '.jpg'

def fileExists(path):
	"""Simply checks if a file exists. Prints an error if not."""
	if not os.path.exists( path ):
		print(path + " Load Failed!")
		print("Could not find file: " + str(path))
		return False
	return True