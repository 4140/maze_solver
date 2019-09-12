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

        self.nodes = {}
        self.target_nodes = []
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

        return self.nodes.get((coordinates, parent_coordinates))

    def add_node(self, node):
        node_repr = node.coordinates
        if node.parent_node:
            parent_node_repr = node.parent_node.coordinates
        else:
            parent_node_repr = None

        if not self.nodes.get((node_repr, parent_node_repr)):
            self.nodes[(node_repr, parent_node_repr)] = node
        else:
            print(f'COLISION: {(node_repr, parent_node_repr)}')

        if not node.parent_node:
            self.add_root(node)
        if node.coordinates == self.target:
            self.target_nodes.append(node)

    def create_node(self, coordinates, tree, parent_node=None, **kwargs):

        if not (
            self.get_node(coordinates, parent_node)
            or (
                parent_node
                and parent_node.parent_node
                and parent_node.parent_node.coordinates == coordinates
            )
        ):
            node = Node(coordinates, tree, parent_node, **kwargs)
            self.add_node(node)
            return node

    def add_root(self, node):
        if not self.root_node:
            self.root_node = node
        else:
            print(f'COLISION root: {(node.coordinates, node.parent_node)}')

    def build_tree(self):
        queue = deque(self.root_node.get_children())

        while queue:
            node = queue.pop()
            queue.extend(node.get_children())

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
        self.tree.create_node(self.start, self.tree)

    def solver(self):
        return self.tree.get_correct_paths()

    def create_matrix(self):
        return [list(s) for s in re.split(r'\n', self.maze)]
