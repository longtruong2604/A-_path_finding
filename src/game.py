import pygame as pg

from src.a_star import a_star, backtrack_to_start
from src.config import (
    BOARD_SIZE,
    GAME_TITLE,
    GRID_SIZE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SLIDER_HEIGHT,
    SLIDER_WIDTH,
)
from src.draw import draw_board, draw_path
from src.events import drag_toggle, end_drag, handle_keydown, quit, start_drag
from src.grid import CellGrid
from src.map_generation import gen_grid, get_random_empty_cell
from src.types import Mode
from src.ui import Logger, Slider


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption(GAME_TITLE)
        self.grid: CellGrid = self.init_grid(GRID_SIZE, GRID_SIZE)
        self.slider = Slider(
            (BOARD_SIZE - SLIDER_WIDTH) // 2,
            (BOARD_SIZE + SCREEN_HEIGHT - SLIDER_HEIGHT) // 2,
            SLIDER_WIDTH,
            SLIDER_HEIGHT,
        )
        self.logger = Logger()  # Khởi tạo Logger
        self.path = None  # Đường đi từ vị trí đầu đến cuối
        self.mouse_held = False
        self.step = 0  # Bước đi trong quá trình tìm đường
        self.mode = Mode.Cost  # Chế độ hiển thị mặc định

    def loop(self):
        while True:
            self.handle_events()
            self.max_steps = a_star(self.grid, self.step, self.logger)
            # Tìm số bước đi đến đích
            self.step = min(
                self.step, self.max_steps
            )  # Đảm bảo bước hiện tại không vượt quá số bước đến đích

            self.slider.set_intervals(self.max_steps)
            self.slider.set_value(self.step)
            # Cập nhật thanh trượt dựa vào số bước đi hiện tại và số bước đi đến đích
            self.draw(self.screen)
            self.path = backtrack_to_start(self.grid.get_end())
            pg.display.update()

    def handle_events(self):
        """
        Xử lý các sự kiện đầu vào từ người dùng như nhấn phím, nhấp chuột và kéo chuột.
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit(self)
            elif event.type == pg.KEYDOWN:
                handle_keydown(self, event)
            elif event.type == pg.MOUSEBUTTONDOWN:
                start_drag(self)
            elif event.type == pg.MOUSEBUTTONUP:
                end_drag(self)
            elif event.type == pg.MOUSEMOTION and self.mouse_held:
                drag_toggle(self)

    def draw(self, surface: pg.Surface):
        """
        Vẽ lưới và các đường đi, cũng như hiển thị thanh trượt trên màn hình.
        """
        if self.grid is None:
            return
        draw_board(surface, self.grid, surface.get_rect(), self.mode)
        if self.slider is not None:
            self.slider.draw(surface)
        # Vẽ đường đi nếu có
        if self.path is not None:
            draw_path(surface, self.grid, self.path)

        # Vẽ thông tin logger
        self.logger.draw_log(surface)

    def init_grid(self, width: int, height: int):
        """
        Khởi tạo lưới cho trò chơi, tạo các ô trống và đặt ô bắt đầu và ô kết thúc.

        Parameters:
            width (int): Chiều rộng của lưới.
            height (int): Chiều cao của lưới.

        Returns:
            CellGrid: Đối tượng lưới chứa các ô và các cài đặt.
        """
        grid = gen_grid(width, height)
        # Sinh bản đồ một cách ngẫu nhiên

        start, end = (get_random_empty_cell(grid), get_random_empty_cell(grid))
        # Sinh ô bắt đầu và ô kết thúc

        return CellGrid(self.screen.get_rect(), grid, start, end)

    def update_step(self, x):
        self.step = x

    def reset(self):
        """
        Tạo một lưới mới với các cài đặt ngẫu nhiên.
        """
        self.grid: CellGrid = self.init_grid(GRID_SIZE, GRID_SIZE)
        self.slider = Slider(
            (BOARD_SIZE - SLIDER_WIDTH) // 2,
            (BOARD_SIZE + SCREEN_HEIGHT - SLIDER_HEIGHT) // 2,
            SLIDER_WIDTH,
            SLIDER_HEIGHT,
        )

        self.path = None  # Đường đi từ vị trí đầu đến cuối
        self.mouse_held = False
        self.step = 0  # Bước đi trong quá trình tìm đường
        self.mode = Mode.Cost  # Chế độ hiển thị mặc định
