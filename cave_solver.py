import time

class Cave:
    def __init__(self, hints, width, height):
        # validate width and height
        if not isinstance(width, int):
            raise ValueError('Width {} is not an integer'.format(width))
        if not isinstance(height, int):
            raise ValueError('Height {} is not an integer').format(height)
        if width < 0:
            raise ValueError('Width {} is less than 0'.format(width))
        if height < 0:
            raise ValueError('Height {} is less than 0').format(height)

        # validate initial hints
        if len(hints) == 0:
            raise ValueError('We need at least 1 hint to have a puzzle')
        for (coords, val) in hints.items():
            if not isinstance(val, int):
                raise ValueError(
                'Improper clue {}, integer expected at {}'
                .format(val, coords))
            # if val <= 1:
            #     raise ValueError(
            #     'Improper clue {} must be an integer greater than 1 at {}'
            #     .format(val, coords))
            if coords[0] < 0 or coords[0] > width:
                raise ValueError(
                'Improper coords {} x-value must be an integer in [0, {}]'
                .format(coords, width))
            if coords[1] < 0 or coords[1] > height:
                raise ValueError(
                'Improper coords {} y-value must be an integer in [0, {}]'
                .format(coords, height))

        self.hints = hints
        # It would make sense to store the grid as a doubly nested list,
        # but it is easier to make sure x and y are in the intuitive directions
        # with a dict (also convenient to save hints)
        # Additionally all of our table values are in a nice flat data structure
        self.grid = {**self.hints}
        self.width = width
        self.height = height

        coords = [(x, y) for y in range(self.height) for x in range(self.width)]
        remaining = set(coords) - set(self.grid)
        for coord in remaining:
            self.grid[coord] = ' ' # we could use None - ' ' makes drawing nice


    def __str__(self):
        char_width = len(str(max([i for i in self.hints.values()])))
        top_line    = '┌' + '─' * ((char_width + 1) * width + 1) + '┐'
        bottom_line = '└' + '─' * ((char_width + 1) * width + 1) + '┘'
        body_lines  = []
        stringify = lambda x: str(x).rjust(char_width)
        for y in range(self.height):
            row = [stringify(self.grid[(x,y)]) for x in range(self.width)]
            body_lines.append('│ ' + ' '.join(row) + ' │')

        return top_line + '\n' + '\n'.join(body_lines) + '\n' + bottom_line

    def filled(self):
        valid_fill = lambda x: isinstance(x, int) or x == '◼' or val == '◻'
        return all(map(valid_fill, self.grid.values()))

    # given a coordinate in grid, shift function, and condition to continue,
    # count the number of coordinates traversed
    def traverse(self, coord, shift, condition):
        if coord in self.grid and condition(coord):
            return 1 + self.traverse(shift(coord), shift, condition)
        return 0

    def num_seen(self, coord, condition):
        up    = lambda coord: (coord[0]    , coord[1] + 1)
        down  = lambda coord: (coord[0]    , coord[1] - 1)
        right = lambda coord: (coord[0] + 1, coord[1]    )
        left  = lambda coord: (coord[0] - 1, coord[1]    )
        look_up    = self.traverse(   up(coord),    up, condition)
        look_down  = self.traverse( down(coord),  down, condition)
        look_right = self.traverse(right(coord), right, condition)
        look_left  = self.traverse( left(coord),  left, condition)
        return 1 + look_up + look_down + look_right + look_left

    def max_seen(self, coord):
        see_clear = lambda x: self.grid[x] == '◻'
        see_empty = lambda x: self.grid[x] == ' '
        see_hint  = lambda x: x in self.hints
        condition = lambda x: see_clear(x) or see_empty(x) or see_hint(x)
        return self.num_seen(coord, condition)

    def min_seen(self, coord):
        see_clear = lambda x: self.grid[x] == '◻'
        see_hint  = lambda x: x in self.hints
        condition = lambda x: see_clear(x) or see_hint(x)
        return self.num_seen(coord, condition)

    def sees_too_few(self, coord):
        return self.max_seen(coord) < self.hints[coord]

    def sees_too_many(self, coord):
        return self.min_seen(coord) > self.hints[coord]

    def disconnected_cave(self):
        return False

    def mistake(self, coord):
        wrong_sight = self.sees_too_few(coord) or self.sees_too_many(coord)
        return wrong_sight or self.disconnected_cave()

    def forcing_moves(self):
        for hint in self.hints:
            pass

    def heuristic_ordering(self):
        return sorted(self.grid)


    def solved(self):
        if any(i == ' ' for i in self.grid.values()):
            return False
        for coord in self.hints:
            if self.sees_too_few(coord) or self.sees_too_many(coord):
                return False
        return True


    def solve(self, debug=False):
        if debug:
            time.sleep(0.5)
            print(self)
        if self.solved():
            return True
        if any(self.mistake(coord) for coord in self.hints):
            return False
        self.forcing_moves()
        for coord in self.heuristic_ordering():
            if self.grid[coord] != ' ':
                continue
            self.grid[coord] = '◼'
            solution_shaded = self.solve(debug=debug)
            if solution_shaded:
                return True
            self.grid[coord] = '◻'
            solution_clear = self.solve(debug=debug)
            if solution_clear:
                return True
            self.grid[coord] = ' '
            return False

hints = {
    (0,1) : 3,
    (1,1) : 4,
    (2,1) : 3,
}
width  = 3
height = 2

hints = {
    (0,1) : 7,
    (0,3) : 5,
    (0,8) : 5,
    (0,9) : 3,
    (1,0) : 3,
    (1,5) : 7,
    (1,6) : 3,
    (3,0) : 13,
    (4,3) : 11,
    (5,1) : 5,
    (5,7) : 5,
    (6,1) : 9,
    (6,8) : 3,
    (7,5) : 9,
    (8,0) : 7,
    (8,6) : 7,
    (8,9) : 5,
    (9,0) : 5,
    (9,8) : 5,
}
hints = {
    (1,0) : 7,
    (3,0) : 5,
    (8,0) : 5,
    (9,0) : 3,
    (0,1) : 3,
    (5,1) : 7,
    (6,1) : 3,
    (0,3) : 13,
    (3,4) : 11,
    (1,5) : 5,
    (7,5) : 5,
    (1,6) : 9,
    (8,6) : 3,
    (5,7) : 9,
    (0,8) : 7,
    (6,8) : 7,
    (9,8) : 5,
    (0,9) : 5,
    (8,9) : 5,
}
width  = 10
height = 10

width = 5
height = 5
hints = {
    (0,0) : 7,
    (1,1) : 4,
    (1,4) : 3,
    (3,1) : 2,
    (3,3) : 1,
    (4,0) : 5,
    (4,2) : 1,
}

c = Cave(hints, width, height)
print(c)
c.solve(debug=True)
