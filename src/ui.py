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
    def __init__(self, x, y, w, h, intervals=100):
        self.circle_x = x
        self.value = 0
        self.is_dragging = False
        self.sliderRect = pg.Rect(x, y, w, h)
        self.intervals = intervals
        self.interval_width = w / intervals

    def draw(self, screen):
        # Draw the slider bar
        pg.draw.rect(screen, SLIDER_BAR_COLOR, self.sliderRect)

        # Calculate the x position of the thumb based on the current value
        self.circle_x = (
            self.sliderRect.x + (self.value / self.intervals) * self.sliderRect.w
        )

        # Draw the slider thumb based on the calculated `circle_x` position
        pg.draw.circle(
            screen,
            SLIDER_THUMB_COLOR,
            (int(self.circle_x), int(self.sliderRect.h / 2 + self.sliderRect.y)),
            SLIDER_THUMB_SIZE,
        )

    def set_intervals(self, intervals):
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
        """Update value based on thumb position within slider range."""
        if x < self.sliderRect.x:
            self.value = 0
        elif x > self.sliderRect.x + self.sliderRect.w:
            self.value = self.intervals
        else:
            self.value = int(
                (x - self.sliderRect.x) / float(self.sliderRect.w) * self.intervals
            )

    def snap_to_interval(self, x):
        """Snap x position to the nearest interval."""
        # Calculate position relative to the slider's start position
        relative_x = x - self.sliderRect.x
        # Find the nearest interval by rounding to the closest multiple of interval width
        snapped_x = round(relative_x / self.interval_width) * self.interval_width
        # Calculate the absolute x position
        return int(self.sliderRect.x + snapped_x)

    def on_slider(self, x, y):
        """Check if a given x, y position is within the slider or thumb area."""
        return (
            self.on_slider_hold(x, y)
            or self.sliderRect.x <= x <= self.sliderRect.x + self.sliderRect.w
            and self.sliderRect.y <= y <= self.sliderRect.y + self.sliderRect.h
        )

    def on_slider_hold(self, x, y):
        """Check if the thumb is being held."""
        return (
            (x - self.circle_x) ** 2
            + (y - (self.sliderRect.y + self.sliderRect.h / 2)) ** 2
        ) <= SLIDER_THUMB_SIZE**2

    def handle_drag(self, screen, x, event=None):
        """Handle slider movement by snapping to intervals and updating value."""
        # Snap the thumb to the nearest interval
        self.circle_x = self.snap_to_interval(x)
        # Update the value based on the new thumb position
        self.update_value(self.circle_x)
        # Redraw the slider with the updated thumb position
        self.draw(screen)

        # Call the event callback if provided
        if event is not None and callable(event):
            event(self.value)


class Arrow:
    def __init__(self, direction: ArrowDirection) -> None:
        self.direction = direction

    def draw_arrow(self, surface, cell_center):
        """Draw an arrow inside the cell at `cell_pos` pointing in the given `direction`."""
        # Get the center and half-size of the cell for arrow drawing
        half_size = CELL_SIZE / 4  # Arrow length
        # Calculate end points of arrow line based on direction
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
            return  # Exit if direction is not valid

        # Draw arrow line
        pg.draw.line(surface, ARROW_COLOR, arrow_start, arrow_end, ARROW_SIZE)

        # Draw arrowhead
        angle = math.atan2(arrow_end[1] - arrow_start[1], arrow_end[0] - arrow_start[0])
        arrow_length = 8  # Length of arrowhead wings
        arrow_angle = math.pi / 6  # 30 degrees for arrowhead

        # Calculate points for the arrowhead
        left_point = (
            arrow_end[0] - arrow_length * math.cos(angle + arrow_angle),
            arrow_end[1] - arrow_length * math.sin(angle + arrow_angle),
        )
        right_point = (
            arrow_end[0] - arrow_length * math.cos(angle - arrow_angle),
            arrow_end[1] - arrow_length * math.sin(angle - arrow_angle),
        )

        # Draw the arrowhead
        pg.draw.polygon(surface, ARROW_COLOR, [arrow_end, left_point, right_point])
