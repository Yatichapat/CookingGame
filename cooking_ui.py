import pygame as pg
from cooking_config import *


class KitchenMap:
    def __init__(self, screen):
        self.__tile_size = 60  # Size of each grid square
        self.__screen = screen

        self.GRID_COLOR = Config.get_config('GRAY')  # Color for grid lines
        self.BACKGROUND_COLOR = Config.get_config('BACKGROUND')  # Background color for the screen
        self.SIDEBAR_COLOR = Config.get_config('PASTEL_GRAY')  # Color for the sidebar
        self.SIDEBAR_WIDTH = 220  # Width of the sidebar (set to 200 pixels)
        self.__line_color = Config.get_config('BLACK')

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
                    color = Config.get_config('PASTEL_BROWN')
                else:
                    color = Config.get_config('PASTEL_GRAY')
                # Draw each square
                pg.draw.rect(self.__screen, color, (x, y, self.__tile_size, self.__tile_size))

        # Draw horizontal grid lines (thicker lines)
        for y in range(0, window_height, self.__tile_size):
            pg.draw.line(self.__screen, self.GRID_COLOR, (0, y), (window_width, y), 4)  # Line width set to 4

        # Draw vertical grid lines (thicker lines)
        for x in range(0, window_width, self.__tile_size):
            pg.draw.line(self.__screen, self.GRID_COLOR, (x, 0), (x, window_height), 4)  # Line width set to 4

    def draw_menu_block(self):
        """Draw the sidebar (menu block) on the left side of the screen."""
        window_width = Config.get_config('WIN_SIZE_W')
        window_height = Config.get_config('WIN_SIZE_H')

        # Draw the rectangle (menu block) on the left side of the screen
        pg.draw.rect(self.__screen, self.SIDEBAR_COLOR,
                     (0, 0, self.SIDEBAR_WIDTH, window_height))  # Sidebar on the left

        # Draw a line on the right edge of the sidebar
        pg.draw.line(self.__screen, self.__line_color,
                     (self.SIDEBAR_WIDTH, 0), (self.SIDEBAR_WIDTH, window_height), 4)  # Line width set to 4

    def update(self):
        """Update the map by drawing tiles."""
        self.__screen.fill(self.BACKGROUND_COLOR)  # Fill the screen with background color
        self.draw_tiles()  # Draw the grid
        self.draw_menu_block()


class GameUI:
    def __init__(self):
        self.__game_over = False
        self.__start_time = pg.time.get_ticks()
        self.__game_time = 60

    def update_time(self):
        elapsed_time = (pg.time.get_ticks() - self.__start_time) // 1000
        remaining_time = self.__game_time - elapsed_time

        if remaining_time <= 0:
            self.__game_over = True
            remaining_time = 0
        return remaining_time

    def draw_timer(self, screen):
        remaining_time = self.update_time()
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        time_text = f"{minutes:02}: {seconds:02}"

        font = pg.font.SysFont(None, 48)
        timer_surface = font.render(time_text, True, Config.get_config('BLACK'))  # White color
        screen.blit(timer_surface, (10, 550))  # Draw timer at top-left corner

    def draw_game_over(self, screen):
        # Display Game Over message
        font = pg.font.SysFont(None, 72)
        game_over_text = font.render("Game Over", True, (255, 0, 0))  # Red color
        screen.blit(game_over_text, (300, 250))  # Center the text on the screen

