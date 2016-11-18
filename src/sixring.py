import numpy as np
from math import sin, cos, radians, sqrt
from johnson import Johnson
from transform import rotate


class SixRing:

    def __init__(self):
        self.ring = []

        for _ in range(1):
            self.ring.append(Johnson())

        self.redraw()


    def redraw(self):
        for i in range(len(self.ring)):
            solid = self.ring[i]
            solid.redraw()

            # rotation = rotate(- 60 * i, [0, 0, 1])
            # for k in range(len(solid.points)):
            #     solid.points[k] = np.dot(rotation, solid.points[k])

            # d = sqrt(3) / 2.0 * solid.scale + solid.line_out
            # solid.translate(d * sin(radians(60*i)), d * cos(radians(60*i)), 0)


    def stats(self):
        l_cost, a_cost, p_cost, t_cost = 0, 0, 0, 0

        for solid in self.ring:
            cost = solid.cost()
            l_cost += cost[0]
            a_cost += cost[1]
            p_cost += cost[2]
            t_cost += cost[3]

        l_cost /= len(self.ring)
        a_cost /= len(self.ring)
        p_cost /= len(self.ring)
        t_cost /= len(self.ring)

        return 'length cost: ' + str(l_cost), 'angle cost: ' + str(a_cost), \
               'planarity cost: ' + str(p_cost), 'total cost: ' + str(t_cost)


    def adjust_top_height(self, num):
        for solid in self.ring:
            solid.top_height += num * solid.scale_factor


    def adjust_square_tip_up(self, num):
        for solid in self.ring:
            solid.square_tip_up += num * solid.scale_factor


    def adjust_line_out(self, num):
        for solid in self.ring:
            solid.line_out += num * solid.scale_factor


    def adjust_alpha(self, num):
        for solid in self.ring:
            if num > 0:
                solid.alpha *= solid.weight_factor
            else:
                sold.alpha /= solid.weight_factor


    def adjust_beta(self, num):
        for solid in self.ring:
            if num > 0:
                solid.beta *= solid.weight_factor
            else:
                sold.beta /= solid.weight_factor


    def adjust_gamma(self, num):
        for solid in self.ring:
            if num > 0:
                solid.gamma *= solid.weight_factor
            else:
                sold.gamma /= solid.weight_factor


    def take_step(self):
        for solid in self.ring:
            solid.take_step()


















