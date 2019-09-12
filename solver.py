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

    def __init__(self, matrix, target):
        self.matrix = matrix
        self.target = target

        self.root_node = None
        self.paths = []
        self.correct_paths = []

    def get_correct_paths(self):
        self.build_tree()
        for node in self.target_nodes:
            path = [parent.coordinates for parent in node]
            self.correct_paths.append(path[::-1])

    def get_node(self, coordinates, parent_node):
        if isinstance(parent_node, tuple):
            parent_coordinates = parent_node
        elif isinstance(parent_node, Node):
            parent_coordinates = parent_node.coordinates
        else:
            parent_coordinates = None

    def get_next_coordinates(self, coordinates):
        def check_cell(y, x):
            try:
                cell = self.tree.matrix[y][x]
            except IndexError:
                return
            if cell != '#':

                return coordinates

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
        self.tree = Tree(self.matrix, self.target)

    def solver(self):
        return self.tree.get_correct_paths()

    def create_matrix(self):
        return [list(s) for s in re.split(r'\n', self.maze)]
