from ast import Dict
import pygame as pg
import math

from src.constant import CellType, CellMark
from src.config import (
    CELL_COLOR_EMPTY,
    CELL_COLOR_WALL,
    CELL_GAP,
    CELL_SIZE,
    LINE_WIDTH,
    MARGIN,
)
from src.grid import CellGrid


class BoardMetrics:
    def __init__(self, area: tuple[int, int, int, int], board: CellGrid):
        """Initialize board metrics for positioning and spacing.

        Args:
            area (tuple[int, int, int, int]): Defines the (left, top, right, bottom) bounds of the board area.
            board: The grid board, which provides its size with `get_size`.
        """
        # Board area and spacing
        self.area = area
        self.left = area[0] + MARGIN  # Left boundary with gap
        self.top = area[1] + MARGIN  # Top boundary with gap
        self.width = area[2] - area[0] - 2 * MARGIN  # Width adjusted for gaps
        self.height = area[3] - area[1] - 2 * MARGIN  # Height adjusted for gaps

        # Grid dimensions
        self.pos_x, self.pos_y = board.get_size()  # Unpack grid size as (num_x, num_y)

    def cell_rect(self, pos: tuple[int, int]) -> pg.Rect:
        """Get the rectangle of a cell at `pos`."""
        return pg.Rect(
            self.left + pos[0] * (CELL_SIZE + CELL_GAP),
            self.top + pos[1] * (CELL_SIZE + CELL_GAP),
            CELL_SIZE,
            CELL_SIZE,
        )


# surface = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
def draw_board(surface: pg.Surface, area: pg.Rect, board: CellGrid):
    cell_font = pg.font.SysFont(pg.font.get_default_font(), 25)
    pg.draw.rect(surface, (0, 0, 0), area)  # color of the board
    metrics = BoardMetrics(area, board)

    colors: Dict[CellType, tuple[int, int, int]] = {
        CellType.Empty: CELL_COLOR_EMPTY,
        CellType.Wall: CELL_COLOR_WALL,
    }
    marks: Dict[CellMark, tuple[int, int, int]] = {
        CellMark.Start: (0, 255, 0),
        CellMark.End: (255, 0, 0),
    }
    for y in range(0, metrics.pos_y):
        for x in range(0, metrics.pos_x):
            cell = board.at([x, y])
            # Explicitly annotate the return type to indicate it's an RGB tuple
            clr: tuple[int, int, int] = colors.get(cell.type, (100, 100, 0))
            cell_rect = metrics.cell_rect([x, y])

            pg.draw.rect(surface, clr, cell_rect)

            if cell.count != math.inf:
                count_text = cell_font.render(str(cell.count), True, (255, 255, 255))

                cell_x, cell_y, cell_width, cell_height = cell_rect
                text_width, text_height = count_text.get_rect().size

                text_x = cell_x + (cell_width - text_width) / 2
                text_y = cell_y + (cell_height - text_height) / 2

                surface.blit(count_text, (text_x, text_y))

            mark = marks.get(cell.mark, None)
            if mark is not None:
                pg.draw.rect(surface, mark, cell_rect, LINE_WIDTH)


def draw_path(
    surface: pg.Surface, area: pg.Rect, board: CellGrid, path=[(0, 1), (1, 2)]
):
    metrics = BoardMetrics(area, board)
    for i in range(0, len(path) - 1):
        ctr_a = metrics.cell_rect(path[i]).center
        ctr_b = metrics.cell_rect(path[i + 1]).center
        pg.draw.line(surface, (120, 220, 0), ctr_a, ctr_b, LINE_WIDTH)
