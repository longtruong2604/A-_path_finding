import pygame as pg
import sys
import math

from src.config import BOARD_SIZE, GRID_SIZE
from src.types import CellMark, Mode


def handle_keydown(self, event):
    """Handle keydown events for specific key actions."""
    if event.key == pg.K_ESCAPE:
        self.quit()
    elif event.key == pg.K_RIGHT:
        self.step += 1
        self.slider.set_value(self.step)
    elif event.key == pg.K_LEFT:
        self.step -= 1
        self.slider.set_value(self.step)
    elif event.key == pg.K_r:
        self.reset()
    elif event.key == pg.K_m:
        self.mode = Mode.Cost if self.mode == Mode.Arrow else Mode.Arrow


def start_drag(self):
    """Start a drag operation by toggling the initial cell and setting up for dragging."""
    mouse_x, mouse_y = pg.mouse.get_pos()
    self.mouse_held = True
    self.toggled_cells.clear()  # Clear the toggled cells set for a new drag
    if self.slider.on_slider(mouse_x, mouse_y):
        self.slider.is_dragging = True
        self.slider.handle_drag(self.screen, mouse_x, self.update_step)
        return

    pos_x, pos_y = (
        mouse_x // (BOARD_SIZE // GRID_SIZE),
        mouse_y // (BOARD_SIZE // GRID_SIZE),
    )

    if (pos_x >= GRID_SIZE) or (pos_y >= GRID_SIZE):
        return

    cell = self.grid.at((pos_x, pos_y))
    if cell:
        # Check if the cell is start or end, then begin dragging it
        if cell.is_start():
            self.dragging_start = True
        elif cell.is_end():
            self.dragging_end = True
        else:
            cell.toggle_type()
            self.cell_type = cell.type
            self.toggled_cells.add((pos_x, pos_y))  # Mark this cell as toggled


def end_drag(self):
    """End the drag operation and clear tracking data."""
    self.mouse_held = False
    self.cell_type = None
    self.slider.is_dragging = False
    self.dragging_start = False
    self.dragging_end = False
    self.toggled_cells.clear()


def drag_toggle(self):
    """Toggle cells as the mouse moves while holding down the button, or move start/end cell."""
    mouse_x, mouse_y = pg.mouse.get_pos()
    if self.slider.is_dragging:
        self.slider.handle_drag(self.screen, mouse_x, self.update_step)
        return

    pos_x = mouse_x // (BOARD_SIZE // GRID_SIZE)
    pos_y = mouse_y // (BOARD_SIZE // GRID_SIZE)

    if (pos_x >= GRID_SIZE) or (pos_y >= GRID_SIZE):
        return

    cell = self.grid.at((pos_x, pos_y))

    # If dragging start or end, update their positions
    if self.dragging_start:
        self.grid.get_start().count = math.inf
        self.grid.get_start().mark = CellMark.No  # Clear previous start cell
        self.grid.set_start((pos_x, pos_y))  # Move start to new position
    elif self.dragging_end:
        self.grid.get_end().mark = CellMark.No  # Clear previous start cell
        self.grid.set_end((pos_x, pos_y))  # Move end to new position
    elif (pos_x, pos_y) not in self.toggled_cells and cell:
        # Toggle type if it's a regular cell and not previously toggled
        if cell.type != self.cell_type:
            cell.toggle_type()
            self.toggled_cells.add((pos_x, pos_y))  # Mark this cell as toggled


def quit(self):
    """Quit the application."""
    pg.quit()
    sys.exit()
