import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'point({}, {})'.format(self.x, self.y)

    def __mul__(self, rhs):
        if isinstance(rhs, Point):
            return Point(self.x * rhs.x, self.y * rhs.y)
        else:
            return Point(self.x * rhs, self.y * rhs)

    def __add__(self, rhs):
        if isinstance(rhs, Point):
            return Point(self.x + rhs.x, self.y + rhs.y)
        else:
            return Point(self.x + rhs, self.y + rhs)

    def rotate(self, angle, origin):
        ox, oy = origin.x, origin.y
        px, py = self.x, self.y

        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)

        return Point(int(round(qx)), int(round(qy)))
