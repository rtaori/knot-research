import math
import numpy as np 
import transformations as tf 
import sched, time

class Knot:
	
	origin, xaxis, yaxis, zaxis = (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)
	p1 = 0.9808
	p2 = 0.8315
	p3 = 0.5556
	p4 = 0.1951

	#set properties
	tilt = 15.0
	bendRad = 2.0
	pipeRad = 0.8
	tilttan = math.tan(math.radians(tilt))

	b0 = [p1*pipeRad,p4*pipeRad,0]
	b1 = [p2*pipeRad,p3*pipeRad,0]
	b2 = [p3*pipeRad,p2*pipeRad,0]
	b3 = [p4*pipeRad,p1*pipeRad,0]

	b4 = [-p4*pipeRad,p1*pipeRad,0]
	b5 = [-p3*pipeRad,p2*pipeRad,0]
	b6 = [-p2*pipeRad,p3*pipeRad,0]
	b7 = [-p1*pipeRad,p4*pipeRad,0]
	b8 = [-p1*pipeRad,-p4*pipeRad,0]
	b9 = [-p2*pipeRad,-p3*pipeRad,0]
	b10 = [-p3*pipeRad,-p2*pipeRad,0]
	b11 = [-p4*pipeRad,-p1*pipeRad,0]

	b12 = [p4*pipeRad,-p1*pipeRad,0]
	b13 = [p3*pipeRad,-p2*pipeRad,0]
	b14 = [p2*pipeRad,-p3*pipeRad,0]
	b15 = [p1*pipeRad,-p4*pipeRad,0]

	m0 = [p1*pipeRad,p4*pipeRad,(bendRad-p1*pipeRad)*tilttan]
	m1 = [p2*pipeRad,p3*pipeRad,(bendRad-p2*pipeRad)*tilttan]
	m2 = [p3*pipeRad,p2*pipeRad,(bendRad-p3*pipeRad)*tilttan]
	m3 = [p4*pipeRad,p1*pipeRad,(bendRad-p4*pipeRad)*tilttan]

	m4 = [-p4*pipeRad,p1*pipeRad,(bendRad+p4*pipeRad)*tilttan]
	m5 = [-p3*pipeRad,p2*pipeRad,(bendRad+p3*pipeRad)*tilttan]
	m6 = [-p2*pipeRad,p3*pipeRad,(bendRad+p2*pipeRad)*tilttan]
	m7 = [-p1*pipeRad,p4*pipeRad,(bendRad+p1*pipeRad)*tilttan]

	m8 = [-p1*pipeRad,-p4*pipeRad,(bendRad+p1*pipeRad)*tilttan]
	m9 = [-p2*pipeRad,-p3*pipeRad,(bendRad+p2*pipeRad)*tilttan]
	m10 = [-p3*pipeRad,-p2*pipeRad,(bendRad+p3*pipeRad)*tilttan]
	m11 = [-p4*pipeRad,-p1*pipeRad,(bendRad+p4*pipeRad)*tilttan]

	m12 = [p4*pipeRad,-p1*pipeRad,(bendRad-p4*pipeRad)*tilttan]
	m13 = [p3*pipeRad,-p2*pipeRad,(bendRad-p3*pipeRad)*tilttan]
	m14 = [p2*pipeRad,-p3*pipeRad,(bendRad-p2*pipeRad)*tilttan]
	m15 = [p1*pipeRad,-p4*pipeRad,(bendRad-p1*pipeRad)*tilttan]
	blist = [b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15]
	mlist = [m0,m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15]

	# azims = [0,0,0,-45.0,0]
	utx = 55
	uty = 0
	utz = 0
	ux = 03
	uy = 0
	uz = 0
	azimStep = 0.001

	def __init__(self):
		self.modules = []
		self.azims = []
		self.end1a = []
		self.end1b = []
		self.end2a = []
		self.end2b = []
		self.optimizing = False
		self.sigma = 1
		self.currCost = 0
		self.s = None

 	'''Knot Building Section '''

	def buildKnot(self,azims):
		del self.modules[:]
		self.azims = azims
		for i in range(len(self.azims)):
			self.modules.append(self.module(i))
			self.modules.append(self.module(i,False))
		self.modules.append(self.buildBase())
		# print "dis",self.endDistance()
		# print "ang",self.endAngle()
		# print self.currCost

	def module(self,numRotations,upper=True):
		m = 2

		points = np.array(Knot.mlist+Knot.blist)
		pointFlipped = self.flipped(points)
		rotated = points
		rFlipped = pointFlipped
		if upper == False:
			azims = [-a for a in self.azims]
			m = -2
			# need extra rotation for lower half
			rotated = rotated - np.array([Knot.bendRad,0,0])
			rotated = np.dot(rotated,tf.rotation_matrix(m*math.radians(Knot.tilt),[0,1,0])[:3,:3].T)
			rotated = rotated + np.array([Knot.bendRad,0,0])

			rFlipped= rFlipped - np.array([Knot.bendRad,0,0])
			rFlipped = np.dot(rFlipped,tf.rotation_matrix(m*math.radians(Knot.tilt),[0,1,0])[:3,:3].T)
			rFlipped = rFlipped + np.array([Knot.bendRad,0,0])
		# print numRotations
		for i in range(numRotations):
			rotated = np.dot(rotated,tf.rotation_matrix(math.radians(self.azims[numRotations-i]),[0,0,1])[:3,:3].T)
			rotated = rotated - np.array([Knot.bendRad,0,0])
			rotated = np.dot(rotated,tf.rotation_matrix(m*math.radians(Knot.tilt),[0,1,0])[:3,:3].T)
			rotated = rotated + np.array([Knot.bendRad,0,0])

			rFlipped = np.dot(rFlipped,tf.rotation_matrix(math.radians(self.azims[numRotations-i]),[0,0,1])[:3,:3].T)
			rFlipped= rFlipped - np.array([Knot.bendRad,0,0])
			rFlipped = np.dot(rFlipped,tf.rotation_matrix(m*math.radians(Knot.tilt),[0,1,0])[:3,:3].T)
			rFlipped = rFlipped + np.array([Knot.bendRad,0,0])
		
		if upper == False:
			m = -1
		else: m = 1
		#half rotation for upper and lower so base module fits in between
		rotated = rotated - np.array([Knot.bendRad,0,0])
		rotated = np.dot(rotated,tf.rotation_matrix(m*math.radians(Knot.tilt),[0,1,0])[:3,:3].T)
		rotated = rotated + np.array([Knot.bendRad,0,0])

		rFlipped= rFlipped - np.array([Knot.bendRad,0,0])
		rFlipped = np.dot(rFlipped,tf.rotation_matrix(m*math.radians(Knot.tilt),[0,1,0])[:3,:3].T)
		rFlipped = rFlipped + np.array([Knot.bendRad,0,0])

		#if end module, compute center of blist and center of all points
		if numRotations == len(self.azims)-1:
			
			
			
			if upper:
				x_bar = sum([r[0] for r in rFlipped])/len(rFlipped)
				y_bar = sum([r[1] for r in rFlipped])/len(rFlipped)
				z_bar = sum([r[2] for r in rFlipped])/len(rFlipped)
				self.end1a = np.array([x_bar,y_bar,z_bar])
				b = rFlipped[rFlipped.shape[0]/2:]
				b_x_bar = sum([r[0] for r in b])/len(b)
				b_y_bar = sum([r[1] for r in b])/len(b)
				b_z_bar = sum([r[2] for r in b])/len(b)
				self.end1b = np.array([b_x_bar,b_y_bar,b_z_bar])
			else:
				x_bar = sum([r[0] for r in rotated])/len(rotated)
				y_bar = sum([r[1] for r in rotated])/len(rotated)
				z_bar = sum([r[2] for r in rotated])/len(rotated)
				self.end2a = np.array([x_bar,y_bar,z_bar])
				b = rotated[rotated.shape[0]/2:]
				b_x_bar = sum([r[0] for r in b])/len(b)
				b_y_bar = sum([r[1] for r in b])/len(b)
				b_z_bar = sum([r[2] for r in b])/len(b)
				self.end2b = np.array([b_x_bar,b_y_bar,b_z_bar])

		return rotated, rFlipped

	def buildBase(self):
		points = np.array(Knot.mlist+Knot.blist)
		pointFlipped = self.flipped(points)
		rotated = points
		rFlipped = pointFlipped
		rotated = rotated - np.array([Knot.bendRad,0,0])
		rotated = np.dot(rotated,tf.rotation_matrix(-1*math.radians(Knot.tilt),[0,1,0])[:3,:3].T)
		rotated = rotated + np.array([Knot.bendRad,0,0])

		rFlipped= rFlipped - np.array([Knot.bendRad,0,0])
		rFlipped = np.dot(rFlipped,tf.rotation_matrix(-1*math.radians(Knot.tilt),[0,1,0])[:3,:3].T)
		rFlipped = rFlipped + np.array([Knot.bendRad,0,0])
		return rotated,rFlipped

	'''Optimization Section'''
	def startOptimizing(self):
		print "starting optimization"
		if not self.optimizing:
			self.optimizing = True
			self.s = sched.scheduler(time.time,time.sleep)
			self.s.enter(0.001,1,self.optimize,())
			self.s.run()

	def stopOptimizing(self):
		print "stopping optimization"
		if self.optimizing:
			self.optimizing = False
			self.s = None

	def setSigma(self,num):
		self.sigma = num
		print "set sigma to ",self.sigma

	def cost(self):
		return self.endDistance() + self.endAngle()

	def optimize(self):
		# if self.optimizing:
		a0Increment = self.takeAzimuthStep(0)
		a1Increment = self.takeAzimuthStep(1)
		a2Increment = self.takeAzimuthStep(2)
		a3Increment = self.takeAzimuthStep(3)
		a4Increment = self.takeAzimuthStep(4)

		biggest = float(max([abs(x) for x in [a0Increment,a1Increment,a2Increment,a3Increment,a4Increment]]))
		a0Increment = a0Increment/biggest * Knot.azimStep
		a1Increment = a1Increment/biggest * Knot.azimStep
		a2Increment = a2Increment/biggest * Knot.azimStep
		a3Increment = a3Increment/biggest * Knot.azimStep
		a4Increment = a4Increment/biggest * Knot.azimStep

		self.azims[0]+= a0Increment*self.sigma
		self.azims[1]+= a1Increment*self.sigma
		self.azims[2]+= a2Increment*self.sigma
		self.azims[3]+= a3Increment*self.sigma
		self.azims[4]+= a4Increment*self.sigma
		print self.azims
		self.buildKnot(self.azims)
		self.currCost = self.cost()
		print "cost",self.currCost
		print "angle",self.endAngle()
		print "distance",self.endDistance()
			# self.s.enter(0.1,1,self.optimize,())

	'''Helpers'''

	def endDistance(self):
		return math.sqrt((self.end1b[0]-self.end2b[0])**2 + (self.end1b[1]-self.end2b[1])**2 + (self.end1b[2]-self.end2b[2])**2)

	def endAngle(self):
		v1 = self.end1b - self.end1a
		v2 = self.end2b - self.end2a
		return 180-math.degrees(tf.angle_between_vectors(v1,v2))

	def takeAzimuthStep(self,i):
		azim = self.azims[i]
		astep = azim+Knot.azimStep
		temp = self.azims
		temp[i] = astep
		self.buildKnot(temp)
		print "the cost with a 0.001 change in the",i," is ", str(self.cost())
		print "the improvement is " +str(self.currCost-self.cost())
		print ""
		improvementRatio = (self.currCost-self.cost()) / self.currCost
		print "improvement ratio: ",improvementRatio
		aIncrement = improvementRatio
		print "a",i," incremenet: ",aIncrement
		print ""
		return aIncrement

	def flipped(self,points):
		#rotate 180
		rotated = np.dot(points,tf.rotation_matrix(math.pi,[1,0,0])[:3,:3].T)
		#translate out bend rad
		rotated = rotated - np.array([Knot.bendRad,0,0])
		# rotated = np.dot(rotated,  tf.translation_matrix([bendRad,0,0])[:3,:3])
		#tilt
		rotated = np.dot(rotated,tf.rotation_matrix(2*math.radians(Knot.tilt),[0,1,0])[:3,:3].T)
		#translate back
		rotated = rotated + np.array([Knot.bendRad,0,0])
		return rotated