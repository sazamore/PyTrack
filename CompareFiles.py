#!/usr/local/bin/python
# Filename: CompareFiles.py
# Project Github: http://github.com/super3/PyTrack
# Author: Shawn Wilkinson <me@super3.org>
# Author Website: http://super3.org/
# License: GPLv3 <http://gplv3.fsf.org/>

# Imports
from ImageFile import *
from Helper import *

# Clarifications:
# Ta

class CompareFiles:
	"""For Comparing Two ImageFiles."""
	def __init__(self, pathLeft, pathRight):
		"""
		Load in two images to compare. 

		Data members:
		imgLeft, imgRight -- The two images to be compared (ImageFile Class)
		minX, maxX, minY, maxY -- Bounds for a bounding box. These are all initialized
								  to unreasonable values that will be adjusted after
								  the two images are compared
		totalConflicts -- Percentage of change between images
		thirdConflicts -- Percentage of change in the top 1/3 of the bounding box (target)
		boundHeight -- Stores the height of the bounding box

		"""
		# Images
		# We are assuming these loaded correctly, and are the same size.
		self.imgLeft  = ImageFile(pathLeft) # TODO: Error Check
		self.imgRight = ImageFile(pathRight) # TODO: Error Check

		# Bounds
		self.minX = 1000
		self.maxX = -1000
		self.minY = 1000
		self.maxY = -1000

		# Info
		self.totalConflicts = 0
		self.targetConflicts = 0
		self.targetCentroid = (0,0)
		self.targetComponents = 0
		self.boundHeight = 0

	def findBounds(self, x, y):
		"""Based on passed values, this narrows the bounds."""
		if x < self.minX:
			self.minX = x
		if x > self.maxX:
			self.maxX = x	
		if y < self.minY:
			self.minY = y
		if y > self.maxY:
			self.maxY = y

	def printInfo(self):
		"""Print basic information about the image comparison."""
		info = "[Bounds] "
		info += "Min X: " + str(self.minX) + ", "
		info += "Max X: " + str(self.maxX) + ", "
		info += "Min Y: " + str(self.minY) + ", "
		info += "Max Y: " + str(self.maxY)
		info += "\n[Conflicts] "
		info += "Total: " + str(self.totalConflicts) + "%, "
		info += "Target: " + str(self.targetConflicts) + "%"
		info += "\n[Target Centroid] "
		info += str(self.targetCentroid)
		info += "\n[Target Components] "
		info += str(self.targetComponents)
		print(info)

	def process(self, compareDistance, compareWeights, componentSize):
		"""
		Compare the two images, and return annotated surface.

		Keyword arguments:
		compareDistance -- Used as threshold for the color detection
						   Range: 0.0 to 1.0
		compareWeights -- Calculate the distance between the colors
						  Example: (0.299, 0.587, 0.114)
		componentSize -- Minimum number of pixels for it to be detected as an object

		See Also:
		http://www.pygame.org/docs/ref/pixelarray.html#PixelArray.compare
		http://www.pygame.org/docs/ref/mask.html#Mask.connected_components

		"""
		print("Comparing '" +  self.imgLeft.getFilePath() + "' to '" +  self.imgRight.getFilePath() + "'") # Debug

		# Grab Pixel Array's of Both Images
		left = self.imgLeft.getPixelArr()
		right = self.imgRight.getPixelArr()

		# Compare Pixel Arrays (with params) and Get Surface
		surfDiff = left.compare( right, compareDistance, compareWeights ).surface
		# Set Alpha to Black
		surfDiff.set_colorkey(BLACK)

		# Create a Mask from the Difference Surface
		mask = pygame.mask.from_surface(surfDiff)

		# Get Total Conflicts as Percent
		self.totalConflicts = round((mask.count() / self.imgLeft.getArea()) * 100, 5)

		# Get Bounding Rects
		rects = mask.get_bounding_rects()
		# Find Bounding Box through the Limits of the Bounding Rects
		for aRect in rects:
			# ----------------------------------------------
			# Track all object on the screen
			# pygame.draw.rect(tmpSurface, (255,0,0), aRect) 
			# ----------------------------------------------
			self.findBounds(aRect.left, aRect.top)
			self.findBounds(aRect.right, aRect.bottom)

		# Get Bounding Box Height
		self.boundHeight = abs(self.minY - self.maxY)

		# Get Top 1/3 Portion of the Bounding Box as our Target Area
		targetWidth = abs(self.minX - self.maxX)
		targetHeight = self.boundHeight*0.3
		targetRect = pygame.Rect(self.minX, self.minY, targetWidth, targetHeight)
		targetSurf = surfDiff.subsurface(targetRect)

		# Create a Mask from the Target Surface
		targetMask = pygame.mask.from_surface(targetSurf)

		# Get Target Conflicts as Percent
		self.targetConflicts = round((targetMask.count()/(targetWidth*targetHeight)) * 100, 5)

		# Get Target Centroid
		self.targetCentroid = targetMask.centroid()

		# Get Connected Components within componentSize Tolerance 
		self.targetComponents = len(targetMask.connected_components(componentSize))

		# Return Diff Image
		return targetSurf

	def drawCentroid(self, surface):
		"""Draw the centroid on a surface."""
		pygame.draw.circle(surface, GREEN, self.targetCentroid, 5)

	def drawRect(self, mode, surface):
		"""
		Draws bounding box(s) based on max and min points on a surface.

		Keyword arguments:
		mode -- how to draw the bounding boxes
				0 - no bounding boxes
				1 - full bounding box
				2 - full boundomg box + target area

		"""
		# Note: Rect Colors and Border Sizes are Magic
		if mode >= 1:
			tmpRect = pygame.Rect(self.minX, self.minY, abs(self.minX - self.maxX), abs(self.minY - self.maxY))
			pygame.draw.rect(surface, BLUE, tmpRect, 3)
		if mode == 2:
			tmpRect = pygame.Rect(self.minX, self.minY, abs(self.minX - self.maxX), abs(self.inY - self.maxY)*0.3)
			pygame.draw.rect(surface, RED, tmpRect, 3)
		
# Main
if __name__ == "__main__":
	# Load Sample Images
	compare = CompareFiles('SampleData/moth0001.jpg', 'SampleData/moth0002.jpg')
	# Compare Images
	compare.process( 0.3, (0.5, 0.5, 0.5), 300)
	# Display comparison Info
	compare.printInfo()