import re
from collections import deque
from typing import (
    Deque,
    Tuple,
    Type,
    List,
    Optional,
)

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

Coordinates = Tuple[int, int]


class MazeContainer(object):
    """Maze container."""

    def __init__(
        self,
        maze: str
    ) -> None:
        """Initiate instance attributes."""
        self.maze = maze.strip()

        self.matrix: List = self.create_matrix()

    def create_matrix(self) -> List:
        """Create matrix from maze multi-line string."""
        return [list(s) for s in re.split(r'\n', self.maze)]


class Tree(object):
    """Maze path tree."""

    def __init__(self):
        """Initiate instance attributes."""
        self.forks = {}
        self.correct_paths: List = []

    @property
    def shortest_path(self) -> List:
        """Return longest path or one of multiple longest."""
        if self.correct_paths:
            return sorted(self.correct_paths, key=lambda l: len(l))[0]
        else:
            return []

    @property
    def longest_path(self) -> List:
        """Return shortest path or one of multiple shortest."""
        if self.correct_paths:
            return sorted(self.correct_paths, key=lambda l: len(l))[-1]
        else:
            return []


class Solver(object):
    """Maze explorer."""

    def __init__(
        self,
        maze_str: str,
        start: Coordinates,
        target: Coordinates,
        maze_class: Type[MazeContainer] = MazeContainer,
        tree_class: Type[Tree] = Tree
    ):
        """Initialize solver."""
        self.maze = maze_class(maze_str)
        self.tree = tree_class()

        self.start = start
        self.target = target

    def solve(self) -> None:
        """Solve maze."""
        self.explore_paths([self.start])

        correct_paths_count = len(self.tree.correct_paths)
        print(f"{correct_paths_count} correct paths found")
        if correct_paths_count > 1:
            print(f"Shortest path: {self.tree.shortest_path}")
            print(f"Longest path: {self.tree.longest_path}")
        elif correct_paths_count == 1:
            print(f"Correct path: {self.tree.correct_paths[0]}")

    def explore_paths(self, current_path: List) -> None:
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
            self.tree.correct_paths.append(current_path)
            self.backtrack(current_path)

        else:
            # backtrack to search for a new path
            self.backtrack(current_path)

    def get_available(
        self,
        coordinates: Coordinates
    ) -> Tuple[Deque, Coordinates]:
        """
        Return next_coordinates and other available options for coordinates.
        """
        available: Deque
        next_coordinates: Coordinates

        if coordinates in self.tree.forks:
            available = self.tree.forks[coordinates]
            next_coordinates = available.popleft()
            if not available:
                del self.tree.forks[coordinates]
        else:
            available = self.get_next_coordinates(coordinates)
            next_coordinates = available.popleft()
            if available:
                self.tree.forks[coordinates] = available

        return available, next_coordinates

    def backtrack(self, current_path: List) -> None:
        """
        Go back to previous available fork in current_path.
        """
        index = 0
        for c in reversed(current_path):
            if c in self.tree.forks:
                index = current_path.index(c)
                break
        if not index:
            return
        self.explore_paths(current_path[0:index+1])

    def get_next_coordinates(
        self,
        coordinates: Coordinates
    ) -> Deque:
        """
        Get possible next coordinates for given coordinates.
        """
        y, x = coordinates
        next_coordinates_queue: Deque = deque()

        for _y in (y - 1, y + 1):
            next_coordinates = self._check_cell(_y, x)
            if next_coordinates:
                next_coordinates_queue.append(next_coordinates)

        for _x in (x - 1, x + 1):
            next_coordinates = self._check_cell(y, _x)
            if next_coordinates:
                next_coordinates_queue.append(next_coordinates)

        return next_coordinates_queue

    def _check_cell(self, y: int, x: int) -> Optional[Coordinates]:
        """Check if a cell in self.matrix is blocked or open."""
        try:
            cell = self.maze.matrix[y][x]
        except IndexError:
            return
        if cell != '#':
            return (y, x)
