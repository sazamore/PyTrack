#!/usr/local/bin/python
# Filename: imagefile.py
# Project Github: http://github.com/super3/PyTrack
# Author: Shawn Wilkinson <me@super3.org>
# Author Website: http://super3.org/
# License: GPLv3 <http://gplv3.fsf.org/>
	
# Imports
import sys
import pygame
import numpy

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED   = (255,0,0)
GREEN = (0,255,0)
BLUE  = (0,0,255)

class ImageFile:
	"""An Image File Class."""
	def __init__(self, filePath):
		# Grab File Path
		self.filePath = filePath

		# Read In The File and Print
		self.imgFile = pygame.image.load(filePath)
		print("Loaded '" + filePath + "'...") # Debug

		# Get Image Size
		self.width = self.imgFile.get_width()
		self.height = self.imgFile.get_height()
		
		# Create Surface Array(self.pixels) and 
		# Pixel Area(self.pixarr) from Image Surface
		self.pixels = pygame.surfarray.array2d(self.imgFile)
		self.pixarr = pygame.PixelArray(self.imgFile)
			
	def getArea(self):
		"""Returns the pixel area of the image."""
		return self.width * self.height

	def printInfo(self):
		"""Prints basic information for the image."""
		print("Image Width: " + str(self.width) + "px")
		print("Image Height: " + str(self.height) + "px")
		print("Image Area: " + str(self.getArea()) + "px")

	def drawRect(self, mode, minX, maxX, minY, maxY, screen):
		"""
		Draws bounding box(s) based on max and min points.

		Keyword arguments:
		mode -- how to draw the bounding boxes
				0 - no bounding boxes
				1 - full bounding box
				2 - full boundomg box + target area
		minX, maxX, minY, maxY -- points used to draw bounding boxes
		screen -- surface to draw on

		"""
		# Note: Rect Colors and Border Sizes are Magic
		if mode >= 1:
			tmpRect = pygame.Rect(minX, minY, abs(minX - maxX), abs(minY - maxY))
			pygame.draw.rect(screen, BLUE, tmpRect, 3)
		if mode == 2:
			tmpRect = pygame.Rect(minX, minY, abs(minX - maxX), abs(minY - maxY)*0.3)
			pygame.draw.rect(screen, RED, tmpRect, 3)
		
	def display(self, mode = 0, minX = 0, maxX = 0, minY = 0, maxY = 0):
		"""
		Draw image to a PyGame window.

		Keyword arguments:
		See drawRect's DocString
		"""
		# Basic PyGame Variables
		screen = pygame.display.set_mode((self.width, self.height))
		clock = pygame.time.Clock()
		running = True
		
		# Main Game Loop
		while running:
			# Display Image
			screen.fill(WHITE)
			#screen.blit(self.imgFile, dest=(0,0))
			pygame.surfarray.blit_array(screen, self.pixels)

			# Draw Rect
			if mode != 0:
				self.drawRect(mode, minX, maxX, minY, maxY, screen)
	
			# Look For Exit
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False

			# Key Press
			key = pygame.key.get_pressed()
			# Move View Window
			if key[pygame.K_RIGHT]:
				running = False
			
			# Refresh Display
			pygame.display.flip()
			# Limit Frames
			clock.tick(30)
		
# Main
if __name__ == "__main__":
	# Load Sample JPG
	img = ImageFile('JPGs/moth0001.jpg')
	# Display Image Info
	img.printInfo()
	# Display Image
	img.display()