from math import sqrt
import numpy as np 
import transformations as tf 
from math import sqrt, pi, acos, degrees

class Geometry:

	origin, xaxis, yaxis, zaxis = (0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)


	def __init__(self):
		self.solid = []
		self.extraTranslation = 0
		self.plist = []

		self.scale = 2
		# CHANGEABLE PARAMETERS
		self.top_height = 1.75 * self.scale
		self.square_tip_out = 1.25 * self.scale
		self.square_tip_up = 1 * self.scale
		self.line_out = 1.5 * self.scale


	def scale_all(self, value):
		self.scale += value
		self.top_height = 1.75 * self.scale
		self.square_tip_out = 1.25 * self.scale
		self.square_tip_up = 1 * self.scale
		self.line_out = 1.5 * self.scale


	'''Building Section'''

	def redraw(self):
		del self.plist[:]

		# top half top point
		self.plist.append([0, 0, self.top_height])

		# calculations for top and bottom halves
		x_dist = sqrt(3) * self.square_tip_out / 2.0
		y_dist = self.square_tip_out / 2.0

		# top half corner top points
		self.plist.append([0, self.square_tip_out, self.square_tip_up])
		self.plist.append([-x_dist, -y_dist, self.square_tip_up])
		self.plist.append([x_dist, -y_dist, self.square_tip_up])

		# bottom half bottom point
		self.plist.append([0, 0, -self.top_height])

		# bottom half corner bottom points
		self.plist.append([0, self.square_tip_out, -self.square_tip_up])
		self.plist.append([-x_dist, -y_dist, -self.square_tip_up])
		self.plist.append([x_dist, -y_dist, -self.square_tip_up])

		# calculations for connector line points
		x_offset = self.scale / 4.0
		y_offset = self.scale * sqrt(3) / 4.0
		x_coord = self.line_out * sqrt(3) / 2.0
		y_coord = self.line_out / 2.0

		# bottom bar connector line points
		self.plist.append([self.scale/2.0, -self.line_out, 0])
		self.plist.append([-self.scale/2.0, -self.line_out, 0])

		# wing connector line points
		self.plist.append([x_coord + x_offset, y_coord - y_offset, 0])
		self.plist.append([x_coord - x_offset, y_coord + y_offset, 0])
		self.plist.append([-x_coord - x_offset, y_coord - y_offset, 0])
		self.plist.append([-x_coord + x_offset, y_coord + y_offset, 0])


	def buildGeometry(self):
		self.redraw()
		self.solid = np.array(self.plist)

	def length_cost(self, weight):

		def distance(point1, point2):
			diff = 0
			for i in range(len(point1)):
				diff += (point1[i] - point2[i]) ** 2
			return sqrt(diff)

		top_point_line = distance(self.plist[0], self.plist[1])
		diff_tops = abs(top_point_line - self.scale) * 6

		square_line = distance(self.plist[5], self.plist[13])
		diff_squares = abs(square_line - self.scale) * 12

		out_line = distance(self.plist[8], self.plist[9])
		diff_outs = abs(out_line - self.scale) * 4

		diff_total = diff_tops + diff_squares + diff_outs
		return diff_total * weight


	def angle_cost(self, weight):

		def angle(vec1, vec2):

			def magnitude(vec1):
				sum = 0
				for i in range(len(vec1)):
					sum += vec1[i] ** 2
				return sqrt(sum)

			numer = 0
			for i in range(len(vec1)):
				numer += vec1[i] * vec2[i]

			denom = magnitude(vec1) * magnitude(vec2)

			fraction = numer / denom

			return acos(fraction)

		def vectorize(point1, point2):
			vec = []
			for i in range(len(point1)):
				vec.append(point2[i] - point1[i])
			return vec

		sum_deviations = 0

		# for the pentagon
		s_pentagon = 108 * 2 * pi / 360

		top_edge_1 = vectorize(self.plist[0], self.plist[1])
		top_edge_2 = vectorize(self.plist[0], self.plist[2])
		top_angle = angle(top_edge_1, top_edge_2)

		top_edge = vectorize(self.plist[1], self.plist[0])
		side_edge = vectorize(self.plist[1], self.plist[13])
		side_angle = angle(top_edge, side_edge)

		side_edge_1 = vectorize(self.plist[13], self.plist[1])
		line_out_edge = vectorize(self.plist[13], self.plist[12])
		line_angle = angle(top_edge_1, line_out_edge)

		pentagon_devation = abs(top_angle - s_pentagon) + 2 * abs(side_angle - s_pentagon) + 2 * abs(line_angle - s_pentagon)
		sum_deviations += 6 * pentagon_devation

		# for the squares
		s_square = 90 * 2 * pi / 360

		left_edge = vectorize(self.plist[1], self.plist[11])
		right_edge = vectorize(self.plist[1], self.plist[13])
		top_angle = angle(left_edge, right_edge)

		top_edge = vectorize(self.plist[11], self.plist[1])
		bottom_edge = vectorize(self.plist[11], self.plist[5])
		edge_angle = angle(top_edge, bottom_edge)

		square_deviation = abs(top_angle - s_square) * 2 + abs(edge_angle - s_square) * 2
		sum_deviations += 3 * square_deviation

		return sum_deviations * weight


	def planarity_cost(self, weight):
		pass

		
		






















