from berin.shapes import regular_polygon
from random import choice
from collections import namedtuple


GridElement = namedtuple("GridElement", "x, y, i, j")

class GridElement(object):

    def __init__(self, x, y, i, j, w, h, grid):
        self.x, self.y = x, y
        self.i, self.j = i, j
        self.width, self.height = w, h
        self.grid = grid


class BaseGrid(object):

    def __init__(self, x, y, num_rows, grid_elem_size):
        self.grid_x = x
        self.grid_y = y
        self.num_rows = num_rows
        self.grid_elem_size = grid_elem_size

    def get_grid_positions(self):
        grid_width_limit = self.grid_x + self.num_rows * self.grid_elem_size
        grid_height_limit = self.grid_y + self.num_rows * self.grid_elem_size

        x_positions = []
        acc = self.grid_x
        while acc < grid_width_limit:
            x_positions.append(acc)
            acc += self.grid_elem_size

        y_positions = []
        acc = self.grid_y
        while acc < grid_width_limit:
            y_positions.append(acc)
            acc += self.grid_elem_size

        for i, x in enumerate(x_positions):
            for j, y in enumerate(y_positions):
                yield GridElement(x, y, i, j, self.grid_elem_size, self.grid_elem_size, self)


class VirtualGrid(BaseGrid):

    def draw(self, func, *f_args, **f_kwargs):
        for grid_elem in self.get_grid_positions():
            with pushMatrix():
                translate(grid_elem.x, grid_elem.y)
                self.draw_elem(grid_elem, func, *f_args, **f_kwargs)

    def draw_elem(self, grid_elem, func, *f_args, **f_kwargs):
        func(*f_args, **f_kwargs)


class DiagonalsOnlyGrid(VirtualGrid):

    def draw_elem(self, grid_elem, func, *f_args, **f_kwargs):
        diff = abs(grid_elem.i - grid_elem.j)
        if not diff or grid_elem.i + grid_elem.j == self.num_rows - 1:
            func(*f_args, **f_kwargs)


class RandomPositioningGrid(VirtualGrid):

    def __init__(self, *args, **kwargs):
        self.percent = kwargs.pop('percent')
        super(RandomPositioningGrid, self).__init__(*args, **kwargs)

    def draw_elem(self, grid_elem, func, *f_args, **f_kwargs):
        if random(1) > self.percent:
            func(*f_args, **f_kwargs)


class OddLinesGrid(VirtualGrid):

    def draw_elem(self, grid_elem, func, *f_args, **f_kwargs):
        if grid_elem.j % 2:
            func(*f_args, **f_kwargs)


class EvenColumnsGrid(VirtualGrid):

    def draw_elem(self, grid_elem, func, *f_args, **f_kwargs):
        if not grid_elem.i % 2:
            func(*f_args, **f_kwargs)
