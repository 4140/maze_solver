import re

maze = """
###########
#         #
# ##### ###
→   #     #
### # ### #
#     #   #
# ##### ###
# #   #   @
# ### #####
#         #
###########
"""


class Tree(object):

    def __init__(self, matrix, start, target):
        self.matrix = matrix
        self.start = start
        self.target = target

        self.correct_paths = []
        self.deadends = []
        self.generators = {}

        self.explore_paths([self.start])

    def explore_paths(self, current_path, explored=[]):
        if not current_path:
            return

        coordinates = current_path[-1]
        explored.append(coordinates)

        if coordinates not in self.generators:
            self.generators[coordinates] = self.get_next_coordinates(
                coordinates
            )
        gen = self.generators.get(coordinates)
        next_coordinates = next(gen, None)

        if next_coordinates and next_coordinates in explored:
            # try next coordinates from generator
            self.explore_paths(current_path, explored)
        elif next_coordinates and next_coordinates != self.target:
            current_path.append(next_coordinates)
            self.explore_paths(current_path, explored)
        elif next_coordinates and next_coordinates == self.target:
            current_path.append(next_coordinates)
            self.correct_paths.append(current_path)
            self.explore_paths(current_path[0:-1], explored)
        else:
            self.deadends.append(coordinates)
            self.explore_paths(current_path[0:-1], explored)

    def get_next_coordinates(self, coordinates):
        def check_cell(y, x):
            try:
                cell = self.matrix[y][x]
            except IndexError:
                return
            if (
                cell != '#'
                and not (y, x) in self.deadends
            ):

                return (y, x)

        y, x = coordinates
        for _y in (y - 1, y + 1):
            next_coordinates = check_cell(_y, x)
            if next_coordinates:
                yield next_coordinates
        for _x in (x - 1, x + 1):
            next_coordinates = check_cell(y, _x)
            if next_coordinates:
                yield next_coordinates

    @property
    def shortest_path(self):
        return sorted(self.correct_paths, key=lambda l: len(l))[0]

    @property
    def longest_path(self):
        return sorted(self.correct_paths, key=lambda l: len(l))[-1]


class MazeSolver(object):

    def __init__(self, start, target, maze):
        self.maze = maze.strip()
        self.start = start
        self.target = target

        self.matrix = self.create_matrix()
        self.tree = Tree(self.matrix, self.start, self.target)

    def create_matrix(self):
        return [list(s) for s in re.split(r'\n', self.maze)]
