import pygame as pg
from cooking_config import *
import math


class Serving:
    def __init__(self, x, y, screen, menu):
        self.__position = (x, y)
        self.__plates = []
        self.__pad_rect = pg.Rect(x, y, 50, 100)  # Fixed size to match draw_pad
        self.__screen = screen
        self.__serve_timer = 0
        self.__serving = False
        self.__menu = menu
        self.__current_plate = None
        self.__last_serve_time = 0
        self.__last_serve_success = False
        self.__last_serve_points = 0

    def add_plate(self, plate):
        """Add plate to serving pad and start serving process"""
        if len(self.__plates) > 3:
            return False
        plate_offset = 25 * len(self.__plates)  # Dynamic spacing
        plate.set_position((
            self.__position[0] + plate_offset,
            self.__position[1] + 10
        ))

        self.__plates.append(plate)
        self.__serving = True
        self.__serve_timer = pg.time.get_ticks()
        return True

    def update(self):
        """Handle automatic serving after delay"""
        if self.__serving:  # 2 second delay
            self.serve()
            self.__serving = False

    def draw_pad(self):
        """Enhanced visual feedback with progress bar"""
        # Base pad
        pg.draw.rect(
            self.__screen,
            Config.get_config('PASTEL_BLUE'),
            (self.__position[0], self.__position[1], 100, 50),
            border_radius=8
        )

    def serve(self):
        """Enhanced order validation with feedback"""
        if not self.__plates:
            return None

        served_plate = self.__plates.pop(0)
        points = self.__menu.serve_dish(served_plate)

        # Visual feedback flags
        self.__last_serve_time = pg.time.get_ticks()
        self.__last_serve_success = points > 0
        self.__last_serve_points = points

        return points

    def draw_feedback(self):
        """Draw floating score text"""
        if hasattr(self, '__last_serve_time') and \
                (pg.time.get_ticks() - self.__last_serve_time) < 1000:
            text_color = (0, 255, 0) if self.__last_serve_success else (255, 0, 0)
            text = f"+{self.__last_serve_points}" if self.__last_serve_success else "Wrong Order!"

            font = pg.font.Font(None, 24)
            text_surface = font.render(text, True, text_color)

            # Animate upward
            y_offset = min(50, (pg.time.get_ticks() - self.__last_serve_time) // 20)
            self.__screen.blit(
                text_surface,
                (self.__position[0] + 5, self.__position[1] - y_offset)
            )

    # def calculate_score(self, plate):
    #     """More sophisticated scoring considering combinations"""
    #     ingredients = [ing.get_type() for ing in plate.get_ingredients()]
    #     base_score = 0
    #     bonus = 1.0
    #
    #     # Base values
    #     type_values = {
    #         'fried': 10,
    #         'sliced': 7,
    #         'raw': 3
    #     }
    #
    #     # Combination bonuses
    #     if 'chicken' in ingredients and 'egg' in ingredients:
    #         bonus *= 1.5
    #     if len(ingredients) >= 3:
    #         bonus *= 1.3
    #
    #     # Calculate total
    #     for ing in ingredients:
    #         for type_, value in type_values.items():
    #             if type_ in ing:
    #                 base_score += value
    #                 break
    #
    #     return int(base_score * bonus)

    def get_position(self):
        return self.__position
