import copy
import random
import types

from src.constant import CellType, CellMark


class Cell:
    def __init__(self, type=CellType.Empty, pos=None):
        self.type = type
        self.count = 0
        self.mark = CellMark.No
        self.path_from = None
        self.pos = pos

    def is_start(self):
        print(self.mark, CellMark.Start)
        return self.mark == CellMark.Start

    def is_end(self):
        return self.mark == CellMark.End

    def toggle_type(self):
        """Toggle cell type between Empty and Block."""
        self.type = CellType.Wall if self.type == CellType.Empty else CellType.Empty


class CellGrid:
    def __init__(self, board, start=None, end=None):
        self.board = board
        self.start = start
        self.end = end

    def get_size(self) -> tuple[int, int]:
        """Returns the size of the grid as (width, height)."""
        return (len(self.board), len(self.board[0]))  # Using a tuple

    def at(self, pos) -> Cell:
        """Returns the cell at a given position."""
        return self.board[pos[0]][pos[1]]

    def clone(self):
        """Creates a deep copy of the grid."""
        return CellGrid(copy.deepcopy(self.board))

    def clear_count(self, count):
        """Resets all cell counts to a specific value, typically used to clear path data."""
        for row in self.board:
            for cell in row:
                cell.count = count
                cell.path_from = None

    def set_start(self, pos):
        """Sets the start cell."""
        self.start = pos
        self.at(pos).mark = CellMark.Start

    def set_end(self, pos):
        """Sets the end cell."""
        self.end = pos
        self.at(pos).mark = CellMark.End

    def get_start(self) -> Cell:
        """Sets the start cell."""
        return self.board[self.start[0]][self.start[1]]

    def get_end(self) -> Cell:
        """Sets the end cell."""
        return self.board[self.end[0]][self.end[1]]

    # def is_valid_point(self, pos):
    #     """Checks if a position is within grid boundaries."""
    #     size = self.get_size()
    #     return 0 <= pos[0] < size[0] and 0 <= pos[1] < size[1]


def init_maze(width: int, height: int):
    """Creates a maze with walls dividing the grid into four sections with some random openings."""
    board = [
        [Cell(type=CellType.Empty, pos=[x, y]) for y in range(height)]
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

    start = [random.randrange(0, width // 2), random.randrange(height // 2 + 1, height)]
    end = [random.randrange(width // 2 + 1, width), random.randrange(0, height // 2)]

    board[start[0]][start[1]].mark = CellMark.Start
    board[end[0]][end[1]].mark = CellMark.End
    return types.SimpleNamespace(
        board=CellGrid(board, start, end),
        start=start,
        end=end,
    )


def add_point(a, b):
    """Adds two points represented as [x, y] coordinates."""
    return [a[0] + b[0], a[1] + b[1]]
