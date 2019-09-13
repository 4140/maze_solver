import re
from collections import deque

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
        self.forks = {}

        self.explore_paths([self.start])

    def explore_paths(self, current_path):
        if not current_path:
            return

        coordinates = current_path[-1]

        if coordinates in self.forks:
            available = self.forks[coordinates]
            next_coordinates = available.popleft()
            if not available:
                del self.forks[coordinates]
        else:
            available = self.get_next_coordinates(coordinates)
            next_coordinates = available.popleft()
            if available:
                self.forks[coordinates] = available

        if (
            next_coordinates
            and next_coordinates in current_path
            and available
        ):
            # try next coordinates from queue for coordinates
            self.explore_paths(current_path)
        elif (
            next_coordinates
            and next_coordinates not in current_path
            and next_coordinates != self.target
        ):
            current_path.append(next_coordinates)
            self.explore_paths(current_path)
        elif next_coordinates and next_coordinates == self.target:
            current_path.append(next_coordinates)
            self.correct_paths.append(current_path)
            self.backtrack(current_path)

        else:
            self.backtrack(current_path)

    def backtrack(self, current_path):
        index = 0
        for c in reversed(current_path):
            if c in self.forks:
                index = current_path.index(c)
                break
        if not index:
            return
        self.explore_paths(current_path[0:index+1])

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
        next_coordinates_list = deque()
        for _y in (y - 1, y + 1):
            next_coordinates = check_cell(_y, x)
            if next_coordinates:
                next_coordinates_list.append(next_coordinates)
        for _x in (x - 1, x + 1):
            next_coordinates = check_cell(y, _x)
            if next_coordinates:
                next_coordinates_list.append(next_coordinates)

        return next_coordinates_list

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
