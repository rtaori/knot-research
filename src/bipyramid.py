from math import sqrt
import numpy as np 
import transformations as tf 

class Geometry:

	origin, xaxis, yaxis, zaxis = (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)


	# CHANGEABLE PARAMETERS
	scale = 1.5
	top_height = 1.75 * scale
	square_tip_out = 1.25 * scale
	square_tip_up = 1 * scale
	line_out = 1.5 * scale


	plist = []

	# top half top point
	plist.append([0, 0, top_height])

	# calculations for top and bottom halves
	x_dist = sqrt(3) * square_tip_out / 2.0
	y_dist = square_tip_out / 2.0

	# top half corner top points
	plist.append([0, square_tip_out, square_tip_up])
	plist.append([-x_dist, -y_dist, square_tip_up])
	plist.append([x_dist, -y_dist, square_tip_up])

	# bottom half bottom point
	plist.append([0, 0, -top_height])

	# bottom half corner bottom points
	plist.append([0, square_tip_out, -square_tip_up])
	plist.append([-x_dist, -y_dist, -square_tip_up])
	plist.append([x_dist, -y_dist, -square_tip_up])

	# calculations for connector line points
	x_offset = scale / 4.0
	y_offset = scale * sqrt(3) / 4.0
	x_coord = line_out * sqrt(3) / 2.0
	y_coord = line_out / 2.0

	# bottom bar connector line points
	plist.append([scale/2.0, -line_out, 0])
	plist.append([-scale/2.0, -line_out, 0])

	# wing connector line points
	plist.append([x_coord + x_offset, y_coord - y_offset, 0])
	plist.append([x_coord - x_offset, y_coord + y_offset, 0])
	plist.append([-x_coord - x_offset, y_coord - y_offset, 0])
	plist.append([-x_coord + x_offset, y_coord + y_offset, 0])


	def __init__(self):
		self.cubes = []
		self.extraTranslation = 0

	'''Building Section'''

	def buildGeometry(self):
		del self.cubes[:]
		# make a few translated cubes
		for i in range(1):
			print('building cube', i)
			self.cubes.append(self.buildCube(i*3))

	def buildCube(self,translation):
		points = np.array(Geometry.plist)
		# add the x translation to the points
		p = points+ np.array([translation+self.extraTranslation,0,0])
		return p



