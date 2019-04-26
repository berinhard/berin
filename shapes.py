from random import choice

def regular_polygon(x, y, radius, n_sides, angle_rotation=0, draw=True, end_shape_mode=0):
    """
    Draw a regular polygon with the center located at x, y.

    Parameters:
    - x: center's X coordinate
    - y: center's Y coordinate
    - radius: distance between the center and the vertexes
    - n_sides: number of sides
    - angle_rotation (in radians): initial rotation to the polygon
    - draw: if True, draw the polygon. if False, returns the polygon vertexes coordinates as PVectors
    """
    section_angle = TWO_PI / n_sides
    angles = [section_angle * i for i in range(n_sides)]

    points = []
    for angle in angles:
        p = PVector(
            x + cos(angle + angle_rotation) * radius,
            y + sin(angle + angle_rotation) * radius,
        )
        points.append(p)

    if draw:
        draw_shape(points, end_shape_mode=end_shape_mode)
    else:
        return points


def draw_shape(points, end_shape_mode=0, vertex_func=None):
    """
    Draw a shape given a list of points as PVectors

    Parameters:
    - points: shape points;
    - end_shape_mode (defaults to None): value passed to Processing's endShape() method;
    - vertex_func (defaults to vertex): which vertex function should be used for the points;
    """
    vertex_func = vertex_func or vertex
    beginShape()
    for p in points:
        vertex_func(p.x, p.y)
    endShape(end_shape_mode)


def lines_intersection(p1, p2, p3, p4):
    """
    p1 and p2 are points from line 1 while p3 and p4 are points from line 2
    """
    x1, y1 = p1.x, p1.y
    x2, y2 = p2.x, p2.y
    x3, y3 = p3.x, p3.y
    x4, y4 = p4.x, p4.y

    try:
        uA = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1));
        uB = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1));
    except ZeroDivisionError:
        return

    if not(0 <= uA <= 1 and 0 <= uB <= 1):
        return

    x = x1 + uA * (x2 - x1)
    y = y1 + uA * (y2- y1)

    return PVector(x, y)


class IntersectionLine():

    def __init__(self, p1, p2, l_color=None):
        self.p1, self.p2 = p1, p2
        self.color = l_color
        self.inter_lines = []

    def __eq__(self, other):
        return self.p1 == other.p1 and self.p2 == other.p2

    def line_size(self):
        return abs(dist(self.p1.x, self.p1.y, self.p2.x, self.p2.y))

    def display(self):
        if self.color:
            stroke(self.color)
        line(self.p1.x, self.p1.y, self.p2.x, self.p2.y)

    def get_intersection(self, other_line):
        return lines_intersection(self.p1, self.p2, other_line.p1, other_line.p2)

    def add_line_intersection(self, inter_line):
        if not inter_line:
            return
        self.inter_lines.append(inter_line)
