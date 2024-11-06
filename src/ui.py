import math
import pygame as pg
from src.config import (
    ARROW_COLOR,
    ARROW_SIZE,
    CELL_SIZE,
    SLIDER_BAR_COLOR,
    SLIDER_THUMB_COLOR,
    SLIDER_THUMB_SIZE,
)
from src.types import ArrowDirection


class Slider:
    """
    Lớp đại diện cho thanh trượt số bước.

    Attributes:
        circle_x (float): Vị trí x của nút kéo trên của sổ.
        value (int): Giá trị hiện tại của thanh trượt đi từ 0 -> số bước tối đa
        is_dragging (bool): Trạng thái đang kéo của nút.
        sliderRect (pg.Rect): Khu vực chứa thanh trượt.
        intervals (int): Số khoảng chia trên thanh trượt, bằng với số bước tối đa.
        interval_width (float): Độ rộng của mỗi khoảng trên thanh trượt.
    """

    def __init__(self, x, y, w, h, intervals=100):
        self.circle_x = x
        self.value = 0
        self.is_dragging = False
        self.sliderRect = pg.Rect(x, y, w, h)
        self.intervals = intervals
        self.interval_width = w / intervals

    def draw(self, screen):
        """
        Vẽ thanh trượt và nút kéo lên màn hình dựa vào giá trị hiện tại.
        """
        pg.draw.rect(screen, SLIDER_BAR_COLOR, self.sliderRect)

        self.circle_x = (
            self.sliderRect.x + (self.value / self.intervals) * self.sliderRect.w
        )

        pg.draw.circle(
            screen,
            SLIDER_THUMB_COLOR,
            (int(self.circle_x), int(self.sliderRect.h / 2 + self.sliderRect.y)),
            SLIDER_THUMB_SIZE,
        )

    def set_intervals(self, intervals):
        """
        Lấy giá trị hiện tại của thanh trượt.
        """
        self.intervals = intervals
        self.interval_width = self.sliderRect.w / intervals

    def get_value(self):
        return self.value

    def set_value(self, num):
        self.value = max(
            0, min(num, self.intervals)
        )  # Ensure the value is within 0 to intervals
        self.circle_x = (
            self.sliderRect.x + (self.value / self.intervals) * self.sliderRect.w
        )

    def update_value(self, x):
        """
        Cập nhật giá trị của thanh trượt dựa trên vị trí x của nút kéo.
        Dùng để cập nhật giá trị khi nút kéo được kéo.
        Dùng trong hàm handle_drag.
        """
        if x < self.sliderRect.x:
            self.value = 0
        elif x > self.sliderRect.x + self.sliderRect.w:
            self.value = self.intervals
        else:
            self.value = int(
                (x - self.sliderRect.x) / float(self.sliderRect.w) * self.intervals
            )

    def snap_to_interval(self, x):
        """
        Làm tròn vị trí x của nút kéo đến điểm gần nhất trong các khoảng.
        """
        relative_x = x - self.sliderRect.x
        snapped_x = round(relative_x / self.interval_width) * self.interval_width
        return int(self.sliderRect.x + snapped_x)

    def on_slider(self, x, y):
        """
        Kiểm tra xem vị trí x, y có nằm trong thanh trượt hoặc nút kéo.
        """
        return (
            self.on_slider_hold(x, y)
            or self.sliderRect.x <= x <= self.sliderRect.x + self.sliderRect.w
            and self.sliderRect.y <= y <= self.sliderRect.y + self.sliderRect.h
        )

    def on_slider_hold(self, x, y):
        """Kiểm tra xem nút kéo có đang bị giữ không."""
        return (
            (x - self.circle_x) ** 2
            + (y - (self.sliderRect.y + self.sliderRect.h / 2)) ** 2
        ) <= SLIDER_THUMB_SIZE**2

    def handle_drag(self, x, event=None):
        """Xử lý việc kéo nút, cập nhật giá trị dựa vào vị trí x"""
        self.circle_x = self.snap_to_interval(x)
        self.update_value(self.circle_x)

        if event is not None and callable(event):
            event(self.value)


class Arrow:
    """
    Lớp đại diện cho mũi tên chỉ hướng trong một ô trên lưới.

    Attributes:
        direction (ArrowDirection): Hướng của mũi tên (Right, Left, Up, Down).
    """

    def __init__(self, direction: ArrowDirection) -> None:
        self.direction = direction

    def draw_arrow(self, surface, cell_center):
        """
        Vẽ mũi tên bên trong ô theo hướng `direction`.
        """
        half_size = CELL_SIZE / 4
        if self.direction == ArrowDirection.Right:
            arrow_start = (cell_center[0] - half_size, cell_center[1])
            arrow_end = (cell_center[0] + half_size, cell_center[1])
        elif self.direction == ArrowDirection.Left:
            arrow_start = (cell_center[0] + half_size, cell_center[1])
            arrow_end = (cell_center[0] - half_size, cell_center[1])
        elif self.direction == ArrowDirection.Up:
            arrow_start = (cell_center[0], cell_center[1] + half_size)
            arrow_end = (cell_center[0], cell_center[1] - half_size)
        elif self.direction == ArrowDirection.Down:
            arrow_start = (cell_center[0], cell_center[1] - half_size)
            arrow_end = (cell_center[0], cell_center[1] + half_size)
        else:
            return

        pg.draw.line(surface, ARROW_COLOR, arrow_start, arrow_end, ARROW_SIZE)

        angle = math.atan2(arrow_end[1] - arrow_start[1], arrow_end[0] - arrow_start[0])
        arrow_length = 8
        arrow_angle = math.pi / 6

        left_point = (
            arrow_end[0] - arrow_length * math.cos(angle + arrow_angle),
            arrow_end[1] - arrow_length * math.sin(angle + arrow_angle),
        )
        right_point = (
            arrow_end[0] - arrow_length * math.cos(angle - arrow_angle),
            arrow_end[1] - arrow_length * math.sin(angle - arrow_angle),
        )

        pg.draw.polygon(surface, ARROW_COLOR, [arrow_end, left_point, right_point])
