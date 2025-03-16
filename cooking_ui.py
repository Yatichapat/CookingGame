import pygame as pg
from cooking_config import *


class KitchenMap:
    def __init__(self, screen):
        self.__tile_size = 60  # Size of each grid square
        self.__screen = screen

        self.GRID_COLOR = Config.get_config('BROWN')  # Color for grid lines
        self.BACKGROUND_COLOR = Config.get_config('BACKGROUND')  # Background color for the screen

    def draw_tiles(self):
        """Draw grid tiles on the screen with alternating colors."""
        # Get the window size from the config
        window_width = Config.get_config('WIN_SIZE_W')
        window_height = Config.get_config('WIN_SIZE_H')

        # Draw alternating tiles (black and white)
        for y in range(0, window_height, self.__tile_size):
            for x in range(0, window_width, self.__tile_size):
                # Alternate between black and white squares
                if (x // self.__tile_size + y // self.__tile_size) % 2 == 0:
                    color = (255, 255, 255)  # White
                else:
                    color = (0, 0, 0)  # Black
                # Draw each square
                pg.draw.rect(self.__screen, color, (x, y, self.__tile_size, self.__tile_size))

        # Draw horizontal grid lines (thicker lines)
        for y in range(0, window_height, self.__tile_size):
            pg.draw.line(self.__screen, self.GRID_COLOR, (0, y), (window_width, y), 4)  # Line width set to 4

        # Draw vertical grid lines (thicker lines)
        for x in range(0, window_width, self.__tile_size):
            pg.draw.line(self.__screen, self.GRID_COLOR, (x, 0), (x, window_height), 4)  # Line width set to 4

    def update(self):
        """Update the map by drawing tiles."""
        self.__screen.fill(self.BACKGROUND_COLOR)  # Fill the screen with background color
        self.draw_tiles()  # Draw the grid
