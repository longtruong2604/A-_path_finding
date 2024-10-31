import math
import sys

import pygame as pg

from src.a_star import backtrack_to_start, fill_shortest_path
from src.config import (
    GAME_TITLE,
    GRID_SIZE,
    SCREEN_HEIGHT,
    BOARD_SIZE,
    SLIDER_HEIGHT,
    SLIDER_WIDTH,
)
from src.constant import CellMark
from src.grid import CellGrid, init_maze
from src.ui import Slider
from src.utils import draw_board, draw_path


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((BOARD_SIZE, SCREEN_HEIGHT))
        self.slider = Slider(
            (BOARD_SIZE - SLIDER_WIDTH) // 2,
            (BOARD_SIZE + SCREEN_HEIGHT - SLIDER_HEIGHT) // 2,
            SLIDER_WIDTH,
            SLIDER_HEIGHT,
        )
        pg.display.set_caption(GAME_TITLE)
        self.init_states()

    def register_state(self, state):
        """
        Register a state

        state: state object
        """
        self.states[type(state).__name__] = state

    def init_states(self):
        self.board: CellGrid = init_maze(
            GRID_SIZE, GRID_SIZE
        ).board  # 2D array of Cell objects
        self.path = None  # List of cell positions for the path
        self.mouse_held = False
        self.toggled_cells = set()  # Track toggled cells during drag
        self.cell_type = None
        self.dragging_start = False
        self.dragging_end = False
        self.steps = math.inf

        """
        # Initialize all the states
        #"""
        # self.state = None
        # self.states = {}
        # # iterate over __all__ states from states.py instantiate them
        # # and register to the self.states with state.name as the key and state instance
        # # as value
        # for State in map(states.__dict__.get, states.__all__):
        #     self.register_state(State(self))

        # # initialize the first state
        # first_state = list(self.states.keys())[0]
        # self.change_state(first_state)

    def change_state(self, state):
        """
        Change the current state

        state: name of the state to change to
        """
        if state in self.states.keys():
            # exit the current state
            if self.state:
                self.state.exit()
            # enter the new state
            self.state = self.states[state]
            self.state.enter()

    def loop(self):
        """Main application loop."""
        # start_time = pg.time.get_ticks()  # Record the start time

        while True:
            # elapsed_time = pg.time.get_ticks() - start_time
            # if elapsed_time >= 30:  # Check if 1 second (1000 ms) has passed
            #     break
            self.handle_events()
            self.draw(self.screen)
            fill_shortest_path(self.board, self.steps)
            self.path = backtrack_to_start(self.board.get_end())
            pg.display.update()

        self.quit()

    def handle_events(self):
        """Handle all incoming events."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            elif event.type == pg.KEYDOWN:
                self.handle_keydown(event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.start_drag()
            elif event.type == pg.MOUSEBUTTONUP:
                self.end_drag()
            elif event.type == pg.MOUSEMOTION and self.mouse_held:
                self.drag_toggle()

    def handle_keydown(self, event):
        """Handle keydown events for specific key actions."""
        if event.key == pg.K_ESCAPE:
            self.quit()
        elif event.key == pg.K_RIGHT:
            self.steps += 1
        elif event.key == pg.K_LEFT:
            self.steps -= 1
        elif event.key == pg.K_r:
            self.reset()

    def start_drag(self):
        """Start a drag operation by toggling the initial cell and setting up for dragging."""
        mouse_x, mouse_y = pg.mouse.get_pos()
        self.mouse_held = True
        self.toggled_cells.clear()  # Clear the toggled cells set for a new drag
        if self.slider.on_slider(mouse_x, mouse_y):
            print("on slider")
            self.slider.handle_event(self.screen, mouse_x, self.update_step)
            return
        pos_x = mouse_x // (BOARD_SIZE // GRID_SIZE)
        pos_y = mouse_y // (BOARD_SIZE // GRID_SIZE)

        cell = self.board.at((pos_x, pos_y))
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
        self.dragging_start = False
        self.dragging_end = False
        self.toggled_cells.clear()

    def drag_toggle(self):
        """Toggle cells as the mouse moves while holding down the button, or move start/end cell."""
        mouse_x, mouse_y = pg.mouse.get_pos()
        if self.slider.on_slider_hold(mouse_x, mouse_y):
            print("on slider hold")
            self.slider.handle_event(self.screen, mouse_x, self.update_step)
            return

        pos_x, pos_y = self.get_cell_position()
        cell = self.board.at((pos_x, pos_y))

        # If dragging start or end, update their positions
        if self.dragging_start:
            self.board.get_start().count = math.inf
            self.board.get_start().mark = CellMark.No  # Clear previous start cell
            self.board.set_start((pos_x, pos_y))  # Move start to new position
        elif self.dragging_end:
            self.board.get_end().mark = CellMark.No  # Clear previous start cell
            self.board.set_end((pos_x, pos_y))  # Move end to new position
        elif (pos_x, pos_y) not in self.toggled_cells and cell:
            # Toggle type if it's a regular cell and not previously toggled
            if cell.type != self.cell_type:
                cell.toggle_type()
                self.toggled_cells.add((pos_x, pos_y))  # Mark this cell as toggled

    def get_cell_position(self):
        """Calculate the cell position based on the current mouse position."""
        mouse_x, mouse_y = pg.mouse.get_pos()
        pos_x = mouse_x // (BOARD_SIZE // GRID_SIZE)
        pos_y = mouse_y // (BOARD_SIZE // GRID_SIZE)
        return pos_x, pos_y

    def quit(self):
        """Quit the application."""
        pg.quit()
        sys.exit()

    def draw(self, surface: pg.Surface):
        """Draw the board and any active paths."""
        if self.board is None:
            return
        draw_board(surface, surface.get_rect(), self.board)
        self.slider.draw(surface)
        # Uncomment if you want to draw paths
        if self.path is not None:
            draw_path(surface, surface.get_rect(), self.board, self.path)

    def update_step(self, new_steps):
        self.steps = new_steps
