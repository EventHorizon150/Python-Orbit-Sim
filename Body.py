# Nathaniel Morin
# 8/22/2021

import pygame
import sys
import math
import itertools

pygame.init()

# Body class
class Body:
	max_speed = 32 # max initial speed

	color = (220, 220, 220)
	vecColor = (255, 0, 0)
	gravColor = (0, 255, 0)
	aggGravColor = (100, 100, 255) # the aggregate/net force of gravity
	fixedColor = (255, 150, 150)
	trailColor = (168, 50, 121)
	centerOfMassColor = (158, 181, 255)

	# What portion of the *radius* of the smaller body (between its and the other body's center) needs to be non-overlapping for it to not collide.
	# 1 means that it just needs to be tangential for a collision to be detected, since it means that the whole radius needs to be outside the other body for it not to collide
	# 0 means that it needs to be submerged up to its center before it collides
	collisionDistanceFactor = 0.6
	# How many times longer the displayed vector is than the distance they will travel in the next frame
	vectorDisplayFactor = 3
	# What portion of the real magnitude of the gravity vectors are displayed
	gravDisplayFactor = 0.001

	density = 1000 # kg/m^3
	# the real gravitational constant, 6.67408 * 10^-11, is not used.
	G = 6.67408 * 10**-4 # gravitational constant * 10^7

	# self, position of the center (x, y), vector, mass, surface
	# released stores whether the body has been launched
	# fixed stores whether the body is fixed at a certain point (cannot move)
	def __init__(self, pos, vec, mass, srf, released = False, fixed = False):
		self.initPos = pos # initial position
		self.initVec = vec # initial vector
		self.initMass = mass # initial mass (kg)
		self.pos = pos # position [x, y]
		self.vec = vec # vector components [dx, dy]
		self.setMass(mass) # radius and mass
		self.trailList = [] # a list of points marking the trail of the body
		self.gravVecList = [] # a list of gravity vectors acting on the ball
		self.srf = srf # surface (the screen)
		self.released = released # whether the body has been launched
		self.fixed = fixed

	# Finds the volume of the body (sphere)
	def findVolume(self):
		return (4*math.pi*self.rad**3)/3

	# sets a body's radius
	def setRadius(self, newRad):
		self.rad = newRad
		self.mass = self.findVolume()*Body.density
		return self

	# sets an body's mass
	def setMass(self, newMass):
		self.mass = newMass
		newVolume = self.mass/Body.density
		self.rad = (3*newVolume/(4*math.pi))**(1/3)
		return self

	# Returns the body's magnitude
	def findMagnitude(self):
		return math.sqrt(self.vec[0]**2 + self.vec[1]**2)

	def findVelocity(self):
		return self.findMagnitude()/self.mass	

	# Updates the position of the body, applying intertia
	def update(self):
		self.trailList.append(self.pos)
		# adjusting the position
		if not self.fixed:
			self.pos = [self.pos[0] + self.vec[0]/self.mass, self.pos[1] + self.vec[1]/self.mass]
		else:
			self.vec = [0, 0]	
		return self

	# Resets a body
	def reset(self):
		self.vec = self.initVec
		self.pos = self.initPos
		self.setMass(self.initMass)
		self.trailList.clear()
		return self

	# Distance formula
	@staticmethod
	def findDistance(pos1, pos2):
		return math.sqrt((pos2[0] - pos1[0])**2 + (pos2[1] - pos1[1])**2)

	# Determines whether the two given bodies are colliding
	@staticmethod
	def bodiesAreColliding(body1, body2):
		distanceBetweenCenters = Body.findDistance(body1.pos, body2.pos)
		# returns true if the distance between their center is less than or equal two the sum of their radii
		return distanceBetweenCenters <= body2.mass + body2.mass

	# Gets the angle (in radians) from the center of a circle (given in center_coords) to the point given in coords
	@staticmethod
	def findRadianAngleFromCoords(center_coords, coords):
		return math.atan2(coords[1] - center_coords[1], coords[0] - center_coords[0])

	# Returns a list {dx, dy} for a Body vector based on the magnitude (speed) of the body and the angle that it is going at
	@staticmethod
	def findVectorFromMagnitudeAndAngle(magnitude, angle):
		# defining dx and dy with this new vector angle
		dx, dy = magnitude * math.cos(angle), magnitude * math.sin(angle)
		return [dx, dy]

	# Finds the force (magnitude) of gravitational attraction between two bodies (yes I know gravity isn't a force)
	@staticmethod
	def findGravitationalAttraction(body1, body2):
		return (Body.G * body1.mass * body2.mass)/(Body.findDistance(body1.pos, body2.pos)**2)

	# Adds two vectors
	@staticmethod
	def addVectors(vec1, vec2):
		return [vec1[0]+vec2[0], vec1[1]+vec2[1]]

	# A function that iterates over a list of bodies and handles collisions between them
	# returns the new list of bodies (post-collisions)
	@staticmethod
	def checkForBodyCollision(lst):
		# Iterates over all possible body combinations
		pairs = list(itertools.combinations(lst, 2))
		for pair in pairs:
			body1, body2 = pair[0], pair[1]
			if body1.released and body2.released:
				dist = Body.findDistance(body1.pos, body2.pos)
				# true if body1 is bigger and they are colliding
				absorb = dist <= body1.rad + body2.rad*Body.collisionDistanceFactor and body1.mass >= body2.mass
				# if body2 is bigger and they are colliding
				if dist <= body2.rad + body1.rad*0.5 and body2.mass >= body1.mass:
					absorb = True
					# swapping them so that body1 refers to the larger
					temp = body2
					body2 = body1
					body1 = temp
				if absorb:
					body1.vec = Body.addVectors(body1.vec, body2.vec)
					body1.setMass(body1.mass + body2.mass)
					if body2 in lst:
						lst.remove(body2)

	# function that iterates over a list of bodies and handles shifts to their vectors due to gravitational interactions
	@staticmethod
	def applyGravity(lst):
		for body in lst:
			body.gravVecList.clear()
		pairs = list(itertools.combinations(lst, 2))
		for pair in pairs:
			body1, body2 = pair[0], pair[1]
			if body1.released and body2.released:
				attr = Body.findGravitationalAttraction(body1, body2)
				b1ToB2Angle = Body.findRadianAngleFromCoords(body1.pos, body2.pos)
				gVec1 = Body.findVectorFromMagnitudeAndAngle(attr, b1ToB2Angle)
				gVec2 = Body.findVectorFromMagnitudeAndAngle(attr, b1ToB2Angle+math.pi)
				body1.vec = Body.addVectors(body1.vec, gVec1)
				body2.vec = Body.addVectors(body2.vec, gVec2)

				body1.gravVecList.append(gVec1)
				body2.gravVecList.append(gVec2)

	@staticmethod
	def findCenterOfMass(lst):
		totalMass = 0
		averagePos = [0, 0]
		for b in lst:
			totalMass += b.mass
			averagePos[0] += b.pos[0]*b.mass
			averagePos[1] += b.pos[1]*b.mass
		return (averagePos[0]/totalMass, averagePos[1]/totalMass), totalMass

	@staticmethod
	def drawCenterOfMass(lst, screen):
		centerOfMassPos, totalMass = Body.findCenterOfMass(lst)
		centerOfMassRad = (3*(totalMass/Body.density)/(4*math.pi))**(1/3)
		pygame.draw.circle(screen, Body.centerOfMassColor, centerOfMassPos, centerOfMassRad)

	# Draws the body	
	def draw(self, drawVec = False, drawGrav = False, drawAgg = False, drawTrail = False):
		# drawing the body
		clr = Body.color if not self.fixed else Body.fixedColor
		pygame.draw.circle(self.srf, clr, self.pos, self.rad)
		# drawing the vector of the ball
		if drawVec:
			pygame.draw.line(self.srf, Body.vecColor, self.pos, \
				(self.pos[0]+self.vec[0]/self.mass*Body.vectorDisplayFactor, self.pos[1]+self.vec[1]/self.mass*Body.vectorDisplayFactor))
		# drawing the vectors displaying all gravity effects
		if drawGrav:
			for gVec in self.gravVecList:
				pygame.draw.line(self.srf, Body.gravColor, self.pos, (self.pos[0]+gVec[0]*Body.gravDisplayFactor, self.pos[1]+gVec[1]*Body.gravDisplayFactor))
		# drawing aggregate gravitational effect vector
		if drawAgg and len(self.gravVecList) > 0:
			sumVec = self.gravVecList[0]
			if len(self.gravVecList) > 1:
				for gVec in self.gravVecList[1:]:
					sumVec = Body.addVectors(sumVec, gVec)
			pygame.draw.line(self.srf, Body.aggGravColor, self.pos, (self.pos[0]+sumVec[0]*Body.gravDisplayFactor, self.pos[1]+sumVec[1]*Body.gravDisplayFactor))
		# drawing the trail
		if drawTrail:
			if len(self.trailList) > 0:
				pygame.draw.lines(self.srf, Body.trailColor, False, self.trailList+[self.pos])
		else:
			self.trailList.clear() # saving space