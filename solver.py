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
        self.correct_paths = []

    def get_correct_paths(self):
        self.build_tree()
        for node in self.target_nodes:
            path = [parent.coordinates for parent in node]
            self.correct_paths.append(reversed(path))

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

    def create_node(self, *args, **kwargs):
        try:
            node = Node(*args, **kwargs)
            self.add_node(node)
            return node
        except Exception as e:
            print(e)

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


class Node(object):
    def __init__(
        self,
        coordinates,
        tree,
        root_node=None,
        parent_node=None,
        is_visited=False,
    ):
        if tree.get_node(coordinates, parent_node):
            raise Exception(f'COLISION init: {(coordinates, parent_node)}')

        self.coordinates = coordinates
        self.tree = tree
        self.root_node = root_node or self
        self.parent_node = parent_node
        self.is_visited = is_visited

        self.is_target = self.coordinates == self.tree.target
        self.is_root = not parent_node

        self.iter_next = self

    def __str__(self):
        return str(self.coordinates)

    def __iter__(self):
        return self

    def __next__(self):
        if self.iter_next:
            _next = self.iter_next
            self.iter_next = _next.parent_node
            return _next
        else:
            raise StopIteration

    def get_children(self):
        children = []

        def get_child_node(y, x):
            try:
                cell = self.tree.matrix[y][x]
            except IndexError:
                return
            if (
                cell != '#'
                and not self.tree.get_node((y, x), self)
                and not (
                    self.parent_node
                    and ((y, x) == self.parent_node.coordinates)
                )
            ):
                node = self.tree.create_node(
                    (y, x),
                    self.tree,
                    root_node=self.root_node,
                    parent_node=self,
                )
                return node

        y, x = self.coordinates
        for _y in (y - 1, y + 1):
            node = get_child_node(_y, x)
            if node:
                children.append(node)
        for _x in (x - 1, x + 1):
            node = get_child_node(y, _x)
            if node:
                children.append(node)
        return children


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
