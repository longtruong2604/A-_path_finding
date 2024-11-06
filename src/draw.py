from ast import Dict
import math
import pygame as pg

from src.config import (
    CELL_COLOR_EMPTY,
    CELL_COLOR_WALL,
    FONT_COLOR,
    FONT_SIZE,
    PATH_LINE_WIDTH,
)
from src.types import CellMark, CellType, Mode
from src.grid import CellGrid


def draw_board(surface: pg.Surface, grid: CellGrid, area: pg.Rect, mode: Mode):
    cell_font = pg.font.SysFont(pg.font.get_default_font(), FONT_SIZE)
    pg.draw.rect(surface, (0, 0, 0), area)  # color of the grid
    metrics = grid.metrics

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
            cell = grid.at([x, y])
            # Explicitly annotate the return type to indicate it's an RGB tuple
            cell_rect = metrics.cell_rect([x, y])
            cell_center = metrics.cell_center([x, y])

            pg.draw.rect(surface, colors.get(cell.type, (100, 100, 0)), cell_rect)

            if mode == Mode.Cost and cell.count != math.inf:
                count_text = cell_font.render(
                    str(round(cell.priority, 2)), True, FONT_COLOR
                )

                cell_x, cell_y, cell_width, cell_height = cell_rect
                text_width, text_height = count_text.get_rect().size

                text_x = cell_x + (cell_width - text_width) / 2
                text_y = cell_y + (cell_height - text_height) / 2

                surface.blit(count_text, (text_x, text_y))

            mark = marks.get(cell.mark, None)
            if mark is not None:
                pg.draw.rect(surface, mark, cell_rect, PATH_LINE_WIDTH)

            if mode == Mode.Arrow and cell.path_from is not None:
                cell.arrow.draw_arrow(surface, cell_center)


def draw_path(surface: pg.Surface, grid: CellGrid, path: list[tuple[int, int]]):
    metrics = grid.metrics
    for i in range(0, len(path) - 1):
        ctr_a = metrics.cell_center(path[i])
        ctr_b = metrics.cell_center(path[i + 1])
        pg.draw.line(surface, (120, 220, 0), ctr_a, ctr_b, PATH_LINE_WIDTH)
