from __future__ import annotations  # For forward reference of CellGrid

import math

import pygame as pg

from src.config import (
    CELL_GAP,
    CELL_SIZE,
    MARGIN,
)
from src.types import ArrowDirection, CellMark, CellType
from src.ui import Arrow
from src.utils import add_point


class Cell:
    def __init__(self, type=CellType.Empty, pos=None):
        self.type = type
        self.count = math.inf
        self.priority = math.inf
        self.mark = CellMark.No
        self.path_from: None | Cell = None
        self.arrow: Arrow = None
        self.pos: None | tuple[int, int] = pos
        self.hidden = 0

    def __lt__(self, other):
        return self.count < other.count

    def is_start(self):
        return self.mark == CellMark.Start

    def is_end(self):
        return self.mark == CellMark.End

    def toggle_type(self):
        """Toggle cell type between Empty and Block."""
        self.type = CellType.Wall if self.type == CellType.Empty else CellType.Empty

    def update_cell(self, count, priority, path_from):
        self.count = count
        self.path_from = path_from
        self.priority = priority
        if path_from is not None:
            if path_from.pos[0] < self.pos[0]:
                self.arrow = Arrow(ArrowDirection.Left)
            elif path_from.pos[0] > self.pos[0]:
                self.arrow = Arrow(ArrowDirection.Right)
            elif path_from.pos[1] < self.pos[1]:
                self.arrow = Arrow(ArrowDirection.Up)
            elif path_from.pos[1] > self.pos[1]:
                self.arrow = Arrow(ArrowDirection.Down)


class GridMetrics:
    def __init__(self, area: tuple[int, int, int, int], grid: CellGrid):
        """Initialize grid metrics for positioning and spacing.

        Args:
            area (tuple[int, int, int, int]): Defines the (left, top, right, bottom) bounds of the grid area.
            grid: The grid grid, which provides its size with `get_size`.
        """
        # Grid area and spacing
        self.area = area
        self.left = area[0] + MARGIN  # Left boundary with gap
        self.top = area[1] + MARGIN  # Top boundary with gap
        self.width = area[2] - area[0] - 2 * MARGIN  # Width adjusted for gaps
        self.height = area[3] - area[1] - 2 * MARGIN  # Height adjusted for gaps

        # Grid dimensions
        self.pos_x, self.pos_y = grid.get_size()  # Unpack grid size as (num_x, num_y)

    def cell_rect(self, pos: tuple[int, int]) -> pg.Rect:
        """Get the rectangle of a cell at `pos`."""
        return pg.Rect(
            self.left + pos[0] * (CELL_SIZE + CELL_GAP),
            self.top + pos[1] * (CELL_SIZE + CELL_GAP),
            CELL_SIZE,
            CELL_SIZE,
        )

    def cell_center(self, pos: tuple[int, int]) -> tuple[int, int]:
        """Get the center of a cell at `pos`."""
        rect = self.cell_rect(pos)
        return rect.center


class CellGrid:
    def __init__(
        self,
        area: tuple[int, int, int, int],
        grid: list[list[Cell]],
        start=None,
        end=None,
    ):
        self.grid = grid
        self.set_start(start)
        self.set_end(end)
        self.metrics = GridMetrics(area, self)

    def get_size(self) -> tuple[int, int]:
        """Returns the size of the grid as (width, height)."""
        return (len(self.grid), len(self.grid[0]))  # Using a tuple

    def at(self, pos: tuple[int, int]) -> Cell:
        """Returns the cell at a given position."""
        return self.grid[pos[0]][pos[1]]

    def clear_count(self, count: int) -> None:
        """Resets all cell counts to a specific value, typically used to clear path data."""
        for row in self.grid:
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
        return self.grid[self.start[0]][self.start[1]]

    def get_end(self) -> Cell:
        """Sets the end cell."""
        return self.grid[self.end[0]][self.end[1]]

    def get_neighbors(self, pos: tuple[int, int]) -> list[Cell]:
        neighbors = []
        offsets = (
            [(0, -1), (-1, 0), (0, 1), (1, 0)]
            if (pos[0] + pos[1]) % 2
            else [(1, 0), (0, 1), (-1, 0), (0, -1)]
        )

        for offset in offsets:
            ncell_pos = add_point(pos, offset)
            if 0 <= ncell_pos[0] < len(self.grid) and 0 <= ncell_pos[1] < len(
                self.grid[0]
            ):
                ncell = self.at(ncell_pos)
                if ncell.type == CellType.Empty:
                    neighbors.append(ncell)
        return neighbors
