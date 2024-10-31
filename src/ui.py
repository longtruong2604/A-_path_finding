import pygame as pg
from src.config import SLIDER_BAR_COLOR, SLIDER_THUMB_COLOR, SLIDER_THUMB_SIZE


class Slider:
    def __init__(self, x, y, w, h, intervals=100):
        self.circle_x = x
        self.value = 0
        self.sliderRect = pg.Rect(x, y, w, h)
        self.intervals = intervals
        self.interval_width = w / intervals  # Calculate interval width

    def draw(self, screen):
        pg.draw.rect(screen, SLIDER_BAR_COLOR, self.sliderRect)
        pg.draw.circle(
            screen,
            SLIDER_THUMB_COLOR,
            (self.circle_x, int(self.sliderRect.h / 2 + self.sliderRect.y)),
            SLIDER_THUMB_SIZE,
        )

    def get_value(self):
        return self.value

    def set_value(self, num):
        self.value = num

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

    def handle_event(self, screen, x, event=None):
        """Handle slider movement by snapping to intervals and updating value."""
        # Snap the thumb to the nearest interval
        self.circle_x = self.snap_to_interval(x)
        # Update the value based on the new thumb position
        self.update_value(self.circle_x)
        # Redraw the slider with the updated thumb position
        self.draw(screen)

        # Call the event callback if provided
        if event is not None and callable(event):
            print(self.value)
            event(self.value)
