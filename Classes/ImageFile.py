#!/usr/local/bin/python
# Filename: imagefile.py
# Project Github: http://github.com/super3/PyTrack
# Author: Shawn Wilkinson <me@super3.org>
# Author Website: http://super3.org/
# License: GPLv3 <http://gplv3.fsf.org/>
	
# Imports
import sys
import pygame
from Classes.Helper import *

class ImageFile:
	"""An Image File Class."""
	def __init__(self, filePath):
		# Grab File Path
		self.filePath = filePath

		# Read In The File and Print
		self.imgFile = pygame.image.load(filePath) # TODO: Error Check
		#print("Loaded '" + filePath + "'...") # Debug

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
	def getPixelArr(self):
		"""Returns a pixel array."""
		return pygame.PixelArray(self.imgFile)

	# Info
	def printInfo(self):
		"""Prints basic information for the image."""
		print("Image Width: " + str(self.width) + "px")
		print("Image Height: " + str(self.height) + "px")
		print("Image Area: " + str(self.getArea()) + "px")