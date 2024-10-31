from __future__ import annotations  # For forward reference of CellGrid

import copy
import math
import random
import types

from src.constant import CellMark, CellType


class Cell:
    def __init__(self, type=CellType.Empty, pos=None):
        self.type = type
        self.count = math.inf
        self.mark = CellMark.No
        self.path_from: None | Cell = None
        self.pos = pos

    def __lt__(self, other):
        return self.count < other.count

    def is_start(self):
        return self.mark == CellMark.Start

    def is_end(self):
        return self.mark == CellMark.End

    def toggle_type(self):
        """Toggle cell type between Empty and Block."""
        self.type = CellType.Wall if self.type == CellType.Empty else CellType.Empty


class CellGrid:
    def __init__(self, board: list[list[Cell]], start=None, end=None):
        self.board = board
        self.set_start(start)
        self.set_end(end)

    def get_size(self) -> tuple[int, int]:
        """Returns the size of the grid as (width, height)."""
        return (len(self.board), len(self.board[0]))  # Using a tuple

    def at(self, pos: tuple[int, int]) -> Cell:
        """Returns the cell at a given position."""
        return self.board[pos[0]][pos[1]]

    def clone(self) -> CellGrid:
        """Creates a deep copy of the grid."""
        return CellGrid(copy.deepcopy(self.board))

    def clear_count(self, count: int) -> None:
        """Resets all cell counts to a specific value, typically used to clear path data."""
        for row in self.board:
            for cell in row:
                cell.count = count
                cell.path_from = None

    def set_start(self, pos: tuple[int, int]) -> None:
        """Sets the start cell."""
        self.start = pos
        self.at(pos).mark = CellMark.Start
        self.at(pos).count = 0

    def set_end(self, pos: tuple[int, int]) -> None:
        """Sets the end cell."""
        self.end = pos
        self.at(pos).mark = CellMark.End

    def get_start(self) -> Cell:
        """Sets the start cell."""
        return self.board[self.start[0]][self.start[1]]

    def get_end(self) -> Cell:
        """Sets the end cell."""
        return self.board[self.end[0]][self.end[1]]

    def get_neighbors(self, pos: tuple[int, int]) -> list[Cell]:
        """Returns a list of neighboring cells that are empty."""
        neighbors = []
        for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ncell_pos = add_point(pos, offset)
            if 0 <= ncell_pos[0] < len(self.board) and 0 <= ncell_pos[1] < len(
                self.board[0]
            ):
                ncell = self.at(ncell_pos)
                if ncell.type == CellType.Empty:
                    neighbors.append(ncell)
        return neighbors

    # def is_valid_point(self, pos):
    #     """Checks if a position is within grid boundaries."""
    #     size = self.get_size()
    #     return 0 <= pos[0] < size[0] and 0 <= pos[1] < size[1]


def init_maze(width: int, height: int):
    """Creates a maze with walls dividing the grid into four sections with some random openings."""
    board = [
        [Cell(type=CellType.Empty, pos=(x, y)) for y in range(height)]
        for x in range(width)
    ]

    # Adding walls in the middle row and column
    for x in range(width):
        board[x][height // 2].type = CellType.Wall
    for y in range(height):
        board[width // 2][y].type = CellType.Wall

    # Creating openings in the walls
    board[random.randint(0, width // 2 - 1)][height // 2].type = CellType.Empty
    board[random.randint(width // 2 + 1, width - 1)][height // 2].type = CellType.Empty
    board[width // 2][random.randint(0, height // 2 - 1)].type = CellType.Empty
    board[width // 2][random.randint(height // 2 + 1, height - 1)].type = CellType.Empty

    start = (random.randrange(0, width // 2), random.randrange(height // 2 + 1, height))
    # stack = [start]
    # visited = set()
    # visited.add(start)
    end = (random.randrange(width // 2 + 1, width), random.randrange(0, height // 2))
    board[start[0]][start[1]].mark = CellMark.Start
    board[end[0]][end[1]].mark = CellMark.End
    # Set the start cell to be empty
    board[start[0]][start[1]].type = CellType.Empty

    # while stack:
    #     current_x, current_y = stack.pop()

    #     # Get all potential neighbors by skipping one cell in between (for walls)
    #     unvisited_neighbors = []
    #     for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
    #         neighbor_x, neighbor_y = current_x + dx, current_y + dy

    #         # Check if the neighbor is within bounds and unvisited
    #         if (
    #             0 <= neighbor_x < width
    #             and 0 <= neighbor_y < height
    #             and (neighbor_x, neighbor_y) not in visited
    #         ):
    #             unvisited_neighbors.append((neighbor_x, neighbor_y))

    #     # If there are unvisited neighbors, proceed with backtracking steps
    #     if unvisited_neighbors:
    #         # Push the current cell back to the stack for further exploration
    #         stack.append((current_x, current_y))

    #         # Choose a random unvisited neighbor
    #         neighbor_x, neighbor_y = random.choice(unvisited_neighbors)

    #         # Remove the wall between the current cell and the chosen neighbor
    #         between_x, between_y = (
    #             (current_x + neighbor_x) // 2,
    #             (current_y + neighbor_y) // 2,
    #         )
    #         board[between_x][
    #             between_y
    #         ].type = CellType.Empty  # Make the wall between cells empty

    #         # Mark the neighbor as visited and push it to the stack
    #         visited.add((neighbor_x, neighbor_y))
    #         board[neighbor_x][
    #             neighbor_y
    #         ].type = CellType.Empty  # Make the neighbor cell empty
    #         stack.append((neighbor_x, neighbor_y))

    return types.SimpleNamespace(
        board=CellGrid(board, start, end),
        start=start,
        end=end,
    )


def add_point(pos_a: tuple[int, int], pos_b: tuple[int, int]) -> tuple[int, int]:
    """Adds two points represented as [x, y] coordinates."""
    return (pos_a[0] + pos_b[0], pos_a[1] + pos_b[1])
