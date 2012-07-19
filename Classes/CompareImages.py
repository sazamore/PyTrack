#!/usr/bin/env python
# Filename: CompareFiles.py
# Project Github: http://github.com/super3/PyTrack
# Author: Shawn Wilkinson <me@super3.org>
# Author Website: http://super3.org/
# License: GPLv3 <http://gplv3.fsf.org/>

# Imports
from Classes.ImageFile import *
from Classes.Helper import *

class CompareFiles:
	"""For Comparing Two ImageFiles."""
	def __init__(self, imgLeft, imgRight):
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
		self.imgLeft  = imgLeft # TODO: Error Check
		self.imgRight = imgRight # TODO: Error Check

		# Bounds
		self.minX = 1000
		self.maxX = -1000
		self.minY = 1000
		self.maxY = -1000

		# Info
		self.boundCenter = (0,0)
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
		info += "Max Y: " + str(self.maxY) + ", "
		info += "\n[Bound Center] " + str(self.boundCenter)
		info += "\n[Conflicts] "
		info += "Total: " + str(self.totalConflicts) + "%, "
		info += "Target: " + str(self.targetConflicts) + "%"
		info += "\n[Target Centroid] "
		info += str(self.targetCentroid)
		info += "\n[Target Components] "
		info += str(self.targetComponents)
		info += "\n"
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
		#print("Comparing '" +  self.imgLeft.getFilePath() + "' to '" +  self.imgRight.getFilePath() + "'") # Debug

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

		# Process Bound amd Target
		self.processBound(mask)
		self.processTarget(surfDiff, componentSize)

		# Return Diff Image
		return surfDiff

	def processBound(self, mask):
		"""Find the Bounding Box."""
		# Get Bounding Rects
		rects = mask.get_bounding_rects()
		# Find Bounding Box through the Limits of the Bounding Rects
		for aRect in rects:
			# ----------------------------------------------
			# Track all object on the screen
			# pygame.draw.rect(surfDiff, (255,0,0), aRect) 
			# ----------------------------------------------
			self.findBounds(aRect.left, aRect.top)
			self.findBounds(aRect.right, aRect.bottom)

		# Get Bounding Box Height
		self.boundHeight = abs(self.minY - self.maxY)

		# Get Centroid 
		tmpRect = pygame.Rect(self.minX, self.minY, abs(self.minX - self.maxX), abs(self.minY - self.maxY))
		self.boundCenter = tmpRect.center

	def processTarget(self, surfDiff, componentSize):
		"""Find the Target."""
		# Get Top 1/3 Portion of the Bounding Box as our Target Area
		targetWidth = abs(self.minX - self.maxX)
		targetHeight = abs(self.minY - self.maxY)*0.3
		targetRect = pygame.Rect(self.minX, self.minY, targetWidth, targetHeight)
		targetSurf = surfDiff.subsurface(targetRect)

		# Create a Mask from the Target Surface
		targetMask = pygame.mask.from_surface(targetSurf)

		# Get Target Conflicts as Percent
		self.targetConflicts = round((targetMask.count()/(targetWidth*targetHeight)) * 100, 5)

		# Get Target Centroid and Offset Correctly
		self.targetCentroid = targetMask.centroid()
		self.targetCentroid = (self.targetCentroid[0] + self.minX, self.targetCentroid[1] + self.minY)

		# Get Connected Components within componentSize Tolerance 
		self.targetComponents = len(targetMask.connected_components(componentSize))

	def drawTargetCentroid(self, surface):
		"""Draw the target centroid on a surface."""
		center = self.targetCentroid
		pygame.draw.circle(surface, GREEN, (center[0], center[1]), 5)

	def drawBoundCenter(self, surface):
		"""Draw the bound centroid on a surface."""
		center = self.boundCenter
		pygame.draw.circle(surface, GREEN, (center[0], center[1]), 5)

	def drawBound(self, surface):
		"""Draw the bounding box on a surface."""
		tmpRect = pygame.Rect(self.minX, self.minY, abs(self.minX - self.maxX), abs(self.minY - self.maxY))
		pygame.draw.rect(surface, BLUE, tmpRect, 3)

	def drawTarget(self, surface):
		"""Draws the target box on a surface."""
		tmpRect = pygame.Rect(self.minX, self.minY, abs(self.minX - self.maxX), abs(self.minY - self.maxY)*0.3)
		pygame.draw.rect(surface, RED, tmpRect, 3)