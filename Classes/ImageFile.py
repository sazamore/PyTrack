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
from Classes.Helper import *

class ImageFile:
	"""An Image File Class."""
	def __init__(self, filePath):
		# Grab File Path
		self.filePath = filePath

		# Read In The File and Print
		self.imgFile = pygame.image.load(filePath) # TODO: Error Check
		print("Loaded '" + filePath + "'...") # Debug

		# Get Image Size
		self.width = self.imgFile.get_width()
		self.height = self.imgFile.get_height()

	# Accessors
	def getFilePath(self):
		"""Returns the filepath."""
		return self.filePath
	def getArea(self):
		"""Returns the pixel area of the image."""
		return self.width * self.height
	def getSurfArr(self):
		"""Returns a 2D array of pixels."""
		return pygame.surfarray.array2d(self.imgFile)
	def getPixelArr(self):
		"""Returns a pixel array."""
		return pygame.PixelArray(self.imgFile)

	# Info
	def printInfo(self):
		"""Prints basic information for the image."""
		print("Image Width: " + str(self.width) + "px")
		print("Image Height: " + str(self.height) + "px")
		print("Image Area: " + str(self.getArea()) + "px")
		
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
			pygame.surfarray.blit_array(screen, self.getSurfArr())

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
	# Load Sample Image
	img = ImageFile('SampleData/moth0001.jpg')
	# Display Image Info
	img.printInfo()
	# Display Image
	img.display()