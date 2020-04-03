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
        valid_fill = lambda x: isinstance(x, int) or x == '◼' or x == '◻'
        return all(map(valid_fill, self.grid.values()))

    # given a coordinate in grid, shift function, and condition to continue,
    # retrieve coordinates traversed
    def traverse(self, coord, shift, condition):
        if coord in self.grid and condition(coord):
            return [coord] + self.traverse(shift(coord), shift, condition)
        return []

    def coords_seen(self, coord, condition):
        up    = lambda coord: (coord[0]    , coord[1] + 1)
        down  = lambda coord: (coord[0]    , coord[1] - 1)
        right = lambda coord: (coord[0] + 1, coord[1]    )
        left  = lambda coord: (coord[0] - 1, coord[1]    )
        look_up    = self.traverse(   up(coord),    up, condition)
        look_down  = self.traverse( down(coord),  down, condition)
        look_right = self.traverse(right(coord), right, condition)
        look_left  = self.traverse( left(coord),  left, condition)
        return [coord] + look_up + look_down + look_right + look_left

    def max_seen(self, coord):
        see_clear = lambda x: self.grid[x] == '◻'
        see_empty = lambda x: self.grid[x] == ' '
        see_hint  = lambda x: x in self.hints
        condition = lambda x: see_clear(x) or see_empty(x) or see_hint(x)
        return self.coords_seen(coord, condition)

    def min_seen(self, coord):
        see_clear = lambda x: self.grid[x] == '◻'
        see_hint  = lambda x: x in self.hints
        condition = lambda x: see_clear(x) or see_hint(x)
        return self.coords_seen(coord, condition)

    def sees_too_few(self, coord):
        return len(self.max_seen(coord)) < self.hints[coord]

    def sees_too_many(self, coord):
        return len(self.min_seen(coord)) > self.hints[coord]

    def disconnected_cave(self):
        def disconnected_cave_helper(coord):
            seen_coords.add(coord)
            for new_coord in self.within_range(coord, self.max_seen(coord), 1):
                if new_coord not in seen_coords:
                    disconnected_cave_helper(new_coord)
        start = list(self.hints)[0]
        seen_coords = set()
        disconnected_cave_helper(start)
        return len([x for x in self.grid.values() if x != '◼']) != len(seen_coords)

    def mistake(self, coord):
        wrong_sight = self.sees_too_few(coord) or self.sees_too_many(coord)
        return wrong_sight or self.disconnected_cave()

    def within_range(self, start, coords, dist):
        in_range = lambda x, y: abs(x[0] - y[0]) + abs(x[1] - y[1]) <= dist
        return [coord for coord in coords if in_range(start, coord)]

    def fill_empty(self, hint):
        update_grid = False
        visible = self.max_seen(hint)
        possible_empty_placements = len(visible)
        needed_empty_placements = self.hints[hint]
        leftover = possible_empty_placements - needed_empty_placements
        return update_grid

    def forcing_moves(self):
        update_grid = False
        for hint in self.hints:
            update_grid |= self.fill_empty(hint)
        return update_grid

    def heuristic_ordering(self):
        # return sorted(self.grid)
        # write a faster solver by first placing squares that hints can see
        # try for smaller hints first
        small_hints_first = sorted(self.hints, key = lambda x: -self.hints[x])
        ordering = []
        for hint in small_hints_first:
            visible = self.max_seen(hint)
            for coord in self.within_range(hint, visible, self.grid[hint] + 1):
                if coord not in ordering:
                    ordering.append(coord)
        for coord in sorted(self.grid):
            if coord not in ordering:
                ordering.append(coord)
        return ordering




    def solved(self):
        if any(i == ' ' for i in self.grid.values()):
            return False
        for coord in self.hints:
            if self.mistake(coord):
                return False
        return True


    def solve(self, debug=False):
        if debug:
            # time.sleep(0.1)
            print(self)
        if self.solved():
            return True
        if any(self.mistake(coord) for coord in self.hints):
            return False
        # update_grid = self.forcing_moves()
        # if update_grid:
            # return solve(self, debug=debug)

        coord = [x for x in self.heuristic_ordering() if self.grid[x] == ' '][0]
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
        # undo forcing moves

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
    (0,3) : 9,
    (4,3) : 13,
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
#
width = 10
height = 10
hints = {
    (0,0) : 2,
    (3,0) : 2,
    (6,0) : 8,
    (8,0) : 8,
    (9,1) : 4,
    (6,2) : 8,
    (0,3) : 6,
    (3,3) : 10,
    (7,3) : 10,
    (9,3) : 6,
    (4,4) : 14,
    (5,5) : 12,
    (0,6) : 6,
    (2,6) : 8,
    (6,6) : 12,
    (9,6) : 6,
    (3,7) : 6,
    (0,8) : 4,
    (1,9) : 12,
    (3,9) : 4,
    (6,9) : 4,
    (9,9) : 4,
}

c = Cave(hints, width, height)
print(c)
c.solve(debug=True)
print(c)
