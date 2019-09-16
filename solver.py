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
    """
    Tree object building and containing paths.
    """

    def __init__(self, maze, start, target):
        """
        Initiate instance attributes.
        """
        self.maze = maze.strip()
        self.start = start
        self.target = target

        self.correct_paths = []
        self.forks = {}

        self.matrix = self.create_matrix()
        self.explore_paths([self.start])

    def explore_paths(self, current_path):
        """
        Explore possible paths from self.start to self.target.

        Called recursively until no options to start a new path are left.
        """
        if not current_path:
            return

        coordinates = current_path[-1]
        available, next_coordinates = self.get_available(coordinates)

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
            # continue on path
            current_path.append(next_coordinates)
            self.explore_paths(current_path)

        elif next_coordinates and next_coordinates == self.target:
            # save path and backtrack to start a new one
            current_path.append(next_coordinates)
            self.correct_paths.append(current_path)
            self.backtrack(current_path)

        else:
            # backtrack to search for a new path
            self.backtrack(current_path)

    def get_available(self, coordinates):
        """
        Return next_coordinates and other available options for coordinates.
        """
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

        return available, next_coordinates

    def backtrack(self, current_path):
        """
        Go back to previous available fork in current_path.
        """
        index = 0
        for c in reversed(current_path):
            if c in self.forks:
                index = current_path.index(c)
                break
        if not index:
            return
        self.explore_paths(current_path[0:index+1])

    def get_next_coordinates(self, coordinates):
        """
        Get possible next coordinates for given coordinates.
        """
        def check_cell(y, x):
            """
            Check if a cell in self.matrix is blocked or open.
            """
            try:
                cell = self.matrix[y][x]
            except IndexError:
                return
            if cell != '#':
                return (y, x)

        y, x = coordinates
        next_coordinates_queue = deque()

        for _y in (y - 1, y + 1):
            next_coordinates = check_cell(_y, x)
            if next_coordinates:
                next_coordinates_queue.append(next_coordinates)

        for _x in (x - 1, x + 1):
            next_coordinates = check_cell(y, _x)
            if next_coordinates:
                next_coordinates_queue.append(next_coordinates)

        return next_coordinates_queue

    def create_matrix(self):
        """Create matrix from maze multi-line string."""
        return [list(s) for s in re.split(r'\n', self.maze)]

    @property
    def shortest_path(self):
        return sorted(self.correct_paths, key=lambda l: len(l))[0]

    @property
    def longest_path(self):
        return sorted(self.correct_paths, key=lambda l: len(l))[-1]
