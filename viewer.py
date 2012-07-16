#!/usr/local/bin/python
# Filename: viewer.py
# Project Github: http://github.com/super3/PyTrack
# Author: Shawn Wilkinson <me@super3.org>
# Author Website: http://super3.org/
# License: GPLv3 <http://gplv3.fsf.org/>

# Imports
from Classes.CompareFiles import *
from Classes.Helper import *
 
# Basic PyGame Variables
screen = pygame.display.set_mode((640, 480)) # Magic Window Size
clock = pygame.time.Clock()
running = True

# File Vars
currFile = 1
prossFile = 0

# Main Game Loop
while running: #1450
	# Fill Display
	screen.fill(BLACK)

	# If Current File is not the Processed File Then Update
	if currFile != prossFile:
		# Load Files
		compare = CompareFiles(genFile(currFile), genFile(currFile+1))
		# Compare with Thresholds
		tmpImage = compare.process( 0.3, (0.5, 0.5, 0.5), 300 )
		# Draw Annotations
		compare.drawCentroid(tmpImage)
		compare.drawBound(tmpImage)
		compare.drawTarget(tmpImage)
		# Print Info
		compare.printInfo()
		# Increment in the Correct Direction
		if currFile > prossFile:
			prossFile += 1
		else:
			prossFile -= 1

	# Draw Image
	screen.blit(tmpImage, dest=(0,0))

	# Look For Exit
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	# Get Keys
	key = pygame.key.get_pressed()
	# Change Current File
	if key[pygame.K_RIGHT] and currFile < 1450: # Magic
		currFile += 1
	elif key[pygame.K_LEFT] and currFile > 1:
		currFile -= 1
	
	# Refresh Display
	pygame.display.flip()
	# Limit Frames
	clock.tick(30)