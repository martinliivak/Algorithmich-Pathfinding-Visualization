from random import randrange


class Maze(object):
    """
    Based on the work done in theJollySin's maze library https://github.com/theJollySin/mazelib

    This is a master object meant to hold a rectangular, 2D maze.
    This object includes the methods used to generate and solve the maze, as well as the start and end points.
    """

    def __init__(self):
        self.generator = None
        self.grid = None
        self.start = None
        self.end = None

    def generate(self):
        """ public method to generate a new maze, and handle some clean-up """
        if self.generator is None:
            raise UnboundLocalError('No maze-generation algorithm has been set.')
        else:
            self.grid = self.generator.generate()
            self.start = None
            self.end = None

    def generate_entrances(self, start_outer=True, end_outer=True):
        """ Generate maze entrances.
            Entrances can be on the walls, or inside the maze.
        """
        if start_outer and end_outer:
            self._generate_outer_entrances()
        elif not start_outer and not end_outer:
            self._generate_inner_entrances()
        elif start_outer:
            self.start, self.end = self._generate_opposite_entrances()
        else:
            self.end, self.start = self._generate_opposite_entrances()

        # the start and end shouldn't be right next to each other
        if abs(self.start[0] - self.end[0]) + abs(self.start[1] - self.end[1]) < 2:
            self.generate_entrances(start_outer, end_outer)

    def _generate_outer_entrances(self):
        """ Generate maze entrances, along the outer walls. """
        H = self.grid.shape[0]
        W = self.grid.shape[1]

        start_side = randrange(4)

        # maze entrances will be on opposite sides of the maze.
        if start_side == 0:
            self.start = (0, randrange(1, W, 2))  # North
            self.end = (H - 1, randrange(1, W, 2))
        elif start_side == 1:
            self.start = (H - 1, randrange(1, W, 2))  # South
            self.end = (0, randrange(1, W, 2))
        elif start_side == 2:
            self.start = (randrange(1, H, 2), 0)  # West
            self.end = (randrange(1, H, 2), W - 1)
        else:
            self.start = (randrange(1, H, 2), W - 1)  # East
            self.end = (randrange(1, H, 2), 0)

    def _generate_inner_entrances(self):
        """ Generate maze entrances, randomly within the maze. """
        H = self.grid.height
        W = self.grid.width

        self.start = (randrange(1, H, 2), randrange(1, W, 2))
        end = (randrange(1, H, 2), randrange(1, W, 2))

        # make certain the start and end points aren't the same
        while end == self.start:
            end = (randrange(1, H, 2), randrange(1, W, 2))

        self.end = end

    def _generate_opposite_entrances(self):
        """ Generate one inner and one outer entrance. """
        H = self.grid.height
        W = self.grid.width

        start_side = randrange(4)

        # pick a side for the outer maze entrance
        if start_side == 0:
            first = (0, randrange(1, W, 2))  # North
        elif start_side == 1:
            first = (H - 1, randrange(1, W, 2))  # South
        elif start_side == 2:
            first = (randrange(1, H, 2), 0)  # West
        else:
            first = (randrange(1, H, 2), W - 1)  # East

        # create an inner maze entrance
        second = (randrange(1, H, 2), randrange(1, W, 2))

        return (first, second)

    def tostring(self, entrances=False, solutions=False):
        """ Return a string representation of the maze. """
        if self.grid is None:
            return ''

        # build the walls of the grid
        txt = []
        for row in self.grid:
            txt.append(''.join(['#' if cell else ' ' for cell in row]))

        # insert the start and end points
        if entrances and self.start and self.end:
            r, c = self.start
            txt[r] = txt[r][:c] + 'S' + txt[r][c+1:]
            r, c = self.end
            txt[r] = txt[r][:c] + 'E' + txt[r][c+1:]

        return '\n'.join(txt)

    def __str__(self):
        """ display maze walls, entrances, and solutions, if available """
        return self.tostring(True, True)

    def __repr__(self):
        return self.__str__()