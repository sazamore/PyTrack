#!/usr/bin/env python
# Filename: viewer.py
# Project Github: http://github.com/super3/PyTrack
# Author: Shawn Wilkinson <me@super3.org>
# Author Website: http://super3.org/
# License: GPLv3 <http://gplv3.fsf.org/>

# Imports
from Classes.CompareImages import *
from Classes.Helper import *
from Classes.Behavior import AbTrack
from Classes.Behavior import CentroidTrack
 
# Basic PyGame Variables
screen = pygame.display.set_mode((640, 480)) # Magic Window Size
clock = pygame.time.Clock()
running = True

# File Vars
currFile = 1
prossFile = 0

# Trackers
track = AbTrack(15)
track2 = CentroidTrack(40)

# Main Game Loop
while running: #1450
	# Fill Display
	screen.fill(BLACK)

	# If Current File is not the Processed File Then Update
	if currFile != prossFile:
		# Load Files
		img1 = ImageFile(genFile(currFile))
		img2 = ImageFile(genFile(currFile+1))
		compare = CompareFiles(img1,img2)
		# Compare with Thresholds
		tmpImage = compare.process( 0.3, (0.5, 0.5, 0.5), 300 )
		# ! Get Internal Data !
		track.compare( compare.boundCenter, compare.targetCentroid )
		track2.add( compare.targetCentroid )
		# Draw Annotations
		compare.drawTargetCentroid(tmpImage)
		compare.drawBoundCenter(tmpImage)
		compare.drawBound(tmpImage)
		compare.drawTarget(tmpImage)
		# Print Info
		print("----------------------------------------------------------------")
		compare.printInfo()
		print("[Abdomen Direction] "  + track.getDir())
		track2.printInfo()
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