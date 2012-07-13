#!/usr/local/bin/python
# Filename: main.py
# Project Github: http://github.com/super3/PyTrack
# Author: Shawn Wilkinson <me@super3.org>
# Author Website: http://super3.org/
# License: GPLv3 <http://gplv3.fsf.org/>

# Imports
from ImageFile import *
from CompareFiles import *

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED   = (255,0,0)
GREEN = (0,255,0)
BLUE  = (0,0,255)

class Main:
	def __init__(self):
		# Bounds of Pixel Cloud
		self.minX = 1000
		self.maxX = -1000
		self.minY = 1000
		self.maxY = -1000

		# Total Conflicts %
		self.conflicts = 0
		# Conflicts in Top 3rd %
		self.conflicts3 = 0
		# Height of Bounding Box
		self.absy = 0
			
	def findBounds(self, x, y):
		if x < self.minX:
			self.minX = x
		if x > self.maxX:
			self.maxX = x	
		if y < self.minY:
			self.minY = y
		if y > self.maxY:
			self.maxY = y
	
	def printBounds(self):
		print("Min X: " + str(self.minX))
		print("Max X: " + str(self.maxX))
		print("Min Y: " + str(self.minY))
		print("Max Y: " + str(self.maxY))

	def resetBounds(self):
		self.minX = 1000
		self.maxX = -1000
		self.minY = 1000
		self.maxY = -1000
	
	# Compare Files Function
	# Assumes That They Are the Same Size
	def compareFile(self, jpgLeft, jpgRight, thres):
		# Class Template
		result = jpgLeft

		# Compare and Get Surface
		result.pixarr = jpgLeft.pixarr.compare( jpgRight.pixarr, 0.3, (thres, thres, thres) )
		tmpSurface = result.pixarr.surface
		tmpSurface.set_colorkey(BLACK)

		# Create Mask
		resultMask = pygame.mask.from_surface(tmpSurface)

		# Total Conflicts %
		pixConflict = resultMask.count()
		totalpix = result.getArea()
		self.conflicts = (pixConflict/totalpix) *100
		print("Conflicts %: " + str(self.conflicts))

		# Get Bounding Rects
		rects = resultMask.get_bounding_rects()
		self.resetBounds()
		for aRect in rects:
			#pygame.draw.rect(tmpSurface, (255,0,0), aRect) # Important! Could use as tracking!
			self.findBounds(aRect.left, aRect.top)
			self.findBounds(aRect.right, aRect.bottom)
		# Print Bounds
		self.printBounds()

		# 1/3 Bound Box Subsurface
		tmpRect = pygame.Rect(self.minX, self.minY, abs(self.minX - self.maxX), abs(self.minY - self.maxY)*0.3)
		target = tmpSurface.subsurface(tmpRect)

		# Mask from Target Subsurface
		targetMask = pygame.mask.from_surface(target)

		# Get Connected Components from Target Mask
		connect = len(targetMask.connected_components(300))
		print("Components: " + str(connect))

		# Get Centroid
		centroid = targetMask.centroid()
		print("Centroid: " + str(centroid))
		pygame.draw.circle(target, (255,0,0), centroid, 5)

		# Display Annotated Result (Optional and will Pause Program)
		result.pixels = pygame.surfarray.array2d(tmpSurface)
		result.display(2, self.minX, self.maxX, self.minY, self.maxY)

# Main
if __name__ == "__main__":
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