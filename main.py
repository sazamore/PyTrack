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

# Open the Files
# file1 = open("absdiff.txt", mode="w", encoding="utf-8")
# file2 = open("absy.txt", mode="w", encoding="utf-8")

# Basic PyGame Variables
screen = pygame.display.set_mode((640, 480)) # Magic Window Size
clock = pygame.time.Clock()
running = True

# File Var
currFile = 1
prossFile = 0
# File Function
def genFile(i):
	return 'SampleData/moth' + str(i).zfill(4) + '.jpg'

# Main Game Loop
while running: #1450
	# Fill Display
	screen.fill(BLACK)

	# Load Compare
	if currFile != prossFile:
		compare = CompareFiles(genFile(currFile), genFile(currFile+1))
		tmpImage = compare.process( 0.3, (0.5, 0.5, 0.5), 300 )
		compare.drawCentroid(tmpImage)
		compare.drawBound(tmpImage)
		compare.drawTarget(tmpImage)
		compare.printInfo()
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
	if key[pygame.K_RIGHT]:
		currFile += 1
	elif key[pygame.K_LEFT] and currFile > 1:
		currFile -= 1
	
	# Refresh Display
	pygame.display.flip()
	# Limit Frames
	clock.tick(30)
	
# Close the Files
# file1.close()
# file2.close()