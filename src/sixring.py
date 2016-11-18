import numpy as np
from math import sin, cos, radians
from johnson import Johnson
from transform import rotate


class SixRing:

	def __init__(self):
		self.ring = []

		for i in range(6):
			solid = Johnson()

			solid.translate(solid.scale * sin(radians(60*i)), solid.scale * cos(radians(60*i)), 0)

			rotation = rotate(60 * i, [0, 0, 1])
			for i in range(len(solid.plist)):
				solid.plist[i] = np.dot(rotation, solid.plist[i])

			ring.append(solid)


	def redraw(self):
		for johnson in self.ring:
			johnson.redraw()


