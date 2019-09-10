import re
from collections import deque
from operator import xor

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


class MazeSolver(object):

    def __init__(self, start, target, maze):
        self.maze = maze.strip()
        self.start = start
        self.target = target

        self.matrix = self.create_matrix()
        self.queue = deque()
        self.queue.append(self.start)

    def solver(self):
        visited = []

        while self.queue:
            coordinates = self.queue.pop()
            visited.append(coordinates)
            self.matrix[coordinates[0]][coordinates[1]] = len(visited)

            if coordinates == self.target:
                return visited

            self.collect_nodes(coordinates, visited)
        return ':-('

    def get_ranges(self, coordinates):
        y, x = coordinates
        y_start = y - 1 if y > 0 else y
        x_start = x - 1 if x > 0 else x
        y_end = y + 2 if y + 1 < len(self.matrix) else y + 1
        x_end = x + 2 if x + 1 < len(self.matrix[0]) else x + 1

        return range(y_start, y_end), range(x_start, x_end)

    def collect_nodes(self, coordinates, visited=[]):
        neighbors = self.check_neighbors(coordinates, visited)

        if neighbors:
            self.queue.append(neighbors.popleft())
        else:
            return

        self.queue.extendleft(neighbors)

    def check_neighbors(self, coordinates, visited=[]):
        y, x = coordinates
        range_y, range_x = self.get_ranges(coordinates)
        neighbors = deque()

        for _y in range_y:
            for _x in range_x:
                _coordinates = (_y, _x)
                if (
                    xor(y == _y, x == _x)
                    and self.matrix[_y][_x] != '#'
                    and _coordinates not in visited
                    and _coordinates not in self.queue
                ):
                    neighbors.append(_coordinates)
        return neighbors

    def create_matrix(self):
        return [list(s) for s in re.split(r'\n', self.maze)]
