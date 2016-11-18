import numpy as np 
from math import sqrt, pi, acos


class Johnson:

    edges = [
                # top edges
                [0,1],
                [0,2],
                [0,3],

                #bottom edges
                [4,5],
                [4,6],
                [4,7],

                # line outs
                [8,9],
                [10,11],
                [12,13],

                #top edges to line outs
                [1,11],
                [3,10],
                [1,13],
                [2,12],
                [2,9],
                [3,8],

                #bottom edges to line outs
                [5,11],
                [5,13],
                [6,9],
                [6,12],
                [7,8],
                [7,10],
            ]

    # for interactive scaling
    scale_factor, weight_factor = 0.05, 1.05


    def __init__(self):
        self.points = []

        self.scale = 1.2
        # CHANGEABLE PARAMETERS
        self.top_height = 1.75 * self.scale
        self.square_tip_up = 1.0 * self.scale
        self.line_out = 1.5 * self.scale

        # to make square faces planar for ring
        numer = 3*self.scale**2 +4*sqrt(3)*self.line_out*self.scale + 4*self.line_out**2
        self.square_tip_out = sqrt(numer) / 4.0
        

        # cost function weights
        self.alpha, self.beta, self.gamma = 150, 150, 30

        # for gradient descent
        self.wiggle_size, self.step_size = 10e-5, 0.5
        self.prev_cost, self.cost_change = None, None


    def translate(self, x, y, z):
        for i in range(len(self.points)):
            curr = self.points[i]
            self.points[i] = [curr[0] + x, curr[1] + y, curr[2] + z]


    def redraw(self):
        # to make square faces planar for ring
        numer = 3*self.scale**2 +4*sqrt(3)*self.line_out*self.scale + 4*self.line_out**2
        self.square_tip_out = sqrt(numer) / 4.0

        del self.points[:]
        

        # top half top point
        self.points.append([0, 0, self.top_height])

        # calculations for top and bottom halves
        x_dist = sqrt(3) * self.square_tip_out / 2.0
        y_dist = self.square_tip_out / 2.0

        # top half corner top points
        self.points.append([0, self.square_tip_out, self.square_tip_up])
        self.points.append([-x_dist, -y_dist, self.square_tip_up])
        self.points.append([x_dist, -y_dist, self.square_tip_up])


        # bottom half bottom point
        self.points.append([0, 0, -self.top_height])

        # bottom half corner bottom points
        self.points.append([0, self.square_tip_out, -self.square_tip_up])
        self.points.append([-x_dist, -y_dist, -self.square_tip_up])
        self.points.append([x_dist, -y_dist, -self.square_tip_up])

        # calculations for connector line points
        x_offset = self.scale / 4.0
        y_offset = self.scale * sqrt(3) / 4.0
        x_coord = self.line_out * sqrt(3) / 2.0
        y_coord = self.line_out / 2.0

        # bottom bar connector line points
        self.points.append([self.scale/2.0, -self.line_out, 0])
        self.points.append([-self.scale/2.0, -self.line_out, 0])

        # wing connector line points
        self.points.append([x_coord + x_offset, y_coord - y_offset, 0])
        self.points.append([x_coord - x_offset, y_coord + y_offset, 0])
        self.points.append([-x_coord - x_offset, y_coord - y_offset, 0])
        self.points.append([-x_coord + x_offset, y_coord + y_offset, 0])


    def take_step(self):

        #handle first two calls to set up comparisons for future
        if self.prev_cost == None:
            self.prev_cost = self.cost()[3]

        elif self.cost_change == None:
            self.gradient_descent()
            cost = self.cost()[3]
            self.cost_change = (self.prev_cost - cost) / self.step_size
            self.prev_cost = cost


        # take most beneficial step
        else:
            self.gradient_descent()
            cost = self.cost()[3]
            decrease = (self.prev_cost - cost) / self.step_size

            if abs(self.prev_cost - cost) < 0.5:
                print('Finished optimizing! Final values are:')
                print('tz: ' + str(self.top_height), 'rc: ' + str(self.square_tip_out), \
                    'hc: ' + str(self.square_tip_up), 'ex: ' + str(self.line_out))


            if decrease < 0:
                self.step_size /= 1.03

            # if step is better than last step
            elif decrease > self.cost_change:
                self.step_size *= 1
                # self.step_size *= 1.01

            # if step is not as good but still beneficial
            else:
                self.step_size /= 1.01
                self.wiggle_size /= 1.001

            self.cost_change, self.prev_cost = decrease, cost


    def gradient_descent(self):
        self.redraw()
        norm_cost = self.cost()[3]

        # figure out contribution to cost function by each parameter
        self.top_height += self.wiggle_size
        self.redraw()
        top_height_cost = self.cost()[3] - norm_cost
        top_height_step = top_height_cost * self.step_size * -1
        self.top_height -= self.wiggle_size

        self.square_tip_up += self.wiggle_size
        self.redraw()
        square_tip_up_cost = self.cost()[3] - norm_cost
        square_tip_up_step = square_tip_up_cost * self.step_size * -1
        self.square_tip_up -= self.wiggle_size

        self.line_out += self.wiggle_size
        self.redraw()
        line_out_cost = self.cost()[3] - norm_cost
        line_out_step = line_out_cost * self.step_size * -1
        self.line_out -= self.wiggle_size


        # take gradient descent step in direction of most decrease
        self.top_height += top_height_step
        self.square_tip_up += square_tip_up_step
        self.line_out += line_out_step

        self.redraw()


    def stats(self):
        l_cost, a_cost, p_cost, t_cost = self.cost()

        return 'length cost: ' + str(l_cost), 'angle cost: ' + str(a_cost), \
               'planarity cost: ' + str(p_cost), 'total cost: ' + str(t_cost)


    def cost(self):
        a, b, c = self.length_cost(), self.angle_cost(), self.planarity_cost()
        t = a + b + c
        return (a, b, c, t)


    def length_cost(self):

        def distance(point1, point2):
            diff = 0
            for i in range(len(point1)):
                diff += (point1[i] - point2[i]) ** 2
            return sqrt(diff)


        top_point_line = distance(self.points[0], self.points[1])
        diff_tops = abs(top_point_line - self.scale) * 6

        square_line = distance(self.points[5], self.points[13])
        diff_squares = abs(square_line - self.scale) * 12

        out_line = distance(self.points[8], self.points[9])
        diff_outs = abs(out_line - self.scale) * 4

        diff_total = diff_tops + diff_squares + diff_outs
        return diff_total * self.alpha


    def angle_cost(self):

        def angle(vec1, vec2):

            def magnitude(vec):
                sum = 0
                for i in range(len(vec)):
                    sum += vec[i] ** 2
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

        # for the pentagons
        s_pentagon = 108 * 2 * pi / 360

        top_edge_1 = vectorize(self.points[0], self.points[1])
        top_edge_2 = vectorize(self.points[0], self.points[2])
        top_angle = angle(top_edge_1, top_edge_2)

        top_edge = vectorize(self.points[1], self.points[0])
        side_edge = vectorize(self.points[1], self.points[13])
        side_angle = angle(top_edge, side_edge)

        side_edge_1 = vectorize(self.points[13], self.points[1])
        line_out_edge = vectorize(self.points[13], self.points[12])
        line_angle = angle(top_edge_1, line_out_edge)

        pentagon_devation = abs(top_angle - s_pentagon) + 2 * abs(side_angle - s_pentagon) \
                            + 2 * abs(line_angle - s_pentagon)
        sum_deviations += 6 * pentagon_devation


        # for the squares
        s_square = 90 * 2 * pi / 360

        left_edge = vectorize(self.points[1], self.points[11])
        right_edge = vectorize(self.points[1], self.points[13])
        top_angle = angle(left_edge, right_edge)

        top_edge = vectorize(self.points[11], self.points[1])
        bottom_edge = vectorize(self.points[11], self.points[5])
        edge_angle = angle(top_edge, bottom_edge)

        square_deviation = abs(top_angle - s_square) * 2 + abs(edge_angle - s_square) * 2
        sum_deviations += 3 * square_deviation

        return sum_deviations * self.beta


    def planarity_cost(self):

        def best_fit_plane(points):
            a, b, c = 0, 0, 0
            p = (0, 0, 0)
            n = len(points)

            for i in range(n):
                a += (points[i][1] - points[(i+1) % n][1]) * (points[i][2] + points[(i+1) % n][2])
                b += (points[i][2] - points[(i+1) % n][2]) * (points[i][0] + points[(i+1) % n][0])
                c += (points[i][0] - points[(i+1) % n][0]) * (points[i][1] + points[(i+1) % n][1])
                p = tuple(p[x] + points[i][x] for x in range(len(p)))

            p = tuple(p[x] / n for x in range(len(p)))

            d = -a * p[0] - b * p[1] - c * p[2]

            return (a, b, c, d)


        def distance(point, plane):
            d = abs(plane[0]*point[0] + plane[1]*point[1] + plane[2]*point[2] + plane[3])
            d /= sqrt(plane[0]**2 + plane[1]**2 + plane[2]**2)
            return d


        def cost(points):
            planarity = 0
            plane = best_fit_plane(points)
            for point in self.points:
                planarity += distance(point, plane)
            return planarity


        p_list = [self.points[0], self.points[1], self.points[3], self.points[11], self.points[10]]
        pentagon = cost(p_list) * 6
        s_list = [self.points[2], self.points[6], self.points[9], self.points[12]]
        square = cost(s_list) * 4

        return (pentagon + square) * self.gamma


# for reference, best values: 'tz: 2.14374626606', 'rc: 1.86108676884', 'hc: 1.41201738716', 'ex: 2.20796050939'

        






















