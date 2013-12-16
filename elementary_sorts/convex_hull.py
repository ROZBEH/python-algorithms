# -*- coding: utf-8 -*-
import math
from shuffle import shuffle


class Point2D(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def ccw(self, a, b):
        """
        Determines how points a, b and c (self) are connected.
        -1 - clockwise
        1 - counter-clockwise
        0 - collinear
        """
        area = (b.x - a.x) * (self.y - a.y) - (b.y - a.y) * (self.x - a.x)
        if area < 0:
            # clockwise turn
            return -1
        elif area > 0:
            # counter-clockwise turn
            return 1
        else:
            # collinear
            return 0

    def polar_angle(self, x, y):
        return math.atan2(self.y - y, self.x - x)

    def __repr__(self):
        return 'Point2D({}, {})'.format(self.x, self.y)


def convex_hull(points):
        # sort points by y coordinate (find the lowest one)
        points.sort(key=lambda p: p.y)
        lowest_point = points[0]
        # sort by polar angle with respect to the first (also lowest) point
        points.sort(key=lambda p: p.polar_angle(lowest_point.y, lowest_point.x))
        hull = list()
        # the first point is definitely on hull
        hull.append(points[0])
        # the second point is the current top
        hull.append(points[1])

        for i in xrange(2, len(points)):
            top = hull.pop()
            while points[i].ccw(hull[-1], top) <= 0:
                top = hull.pop()
            hull.append(top)
            hull.append(points[i])

        return hull

if __name__ == '__main__':
    ps = [(7, 1), (7, 2), (9, 3), (4, 5), (2, 8), (-4, 7), (-6, 4), (-2, 5), (-5, -2), (-1, -4), (2, -1),
          (5, -2)]

    shuffle(ps)
    arbitrary_points = [Point2D(x, y) for x, y in ps]
    print convex_hull(arbitrary_points)

