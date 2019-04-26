from contextlib import contextmanager

@contextmanager
def draw_at_center():
    """
    Move the 0, 0 to the center of the sketch
    """
    try:
        translate(width/2, height/2)
        yield
    finally:
        pass


def polar_coordinate(x0, y0, r, angle):
    x = x0 + r * cos(angle)
    y = y0 + r * sin(angle)

    return PVector(x, y)
