import pygame as pg
from cooking_config import *


class KitchenMap:

    def __init__(self, screen):
        self.__tile_size = 60
        self.__screen = screen

        self.__grid_color = Config.get_config('GRAY')
        self.__background_color = Config.get_config('BACKGROUND')
        self.__sidebar_color = Config.get_config('PASTEL_GRAY')
        self.__sidebar_width = 220
        self.__line_color = Config.get_config('BLACK')

    def draw_tiles(self):
        window_width = Config.get_config('WIN_SIZE_W')
        window_height = Config.get_config('WIN_SIZE_H')

        for y in range(0, window_height, self.__tile_size):
            for x in range(0, window_width, self.__tile_size):
                if (x // self.__tile_size + y // self.__tile_size) % 2 == 0:
                    color = Config.get_config('PASTEL_BROWN')
                else:
                    color = Config.get_config('PASTEL_GRAY')
                pg.draw.rect(self.__screen, color, (x, y, self.__tile_size, self.__tile_size))

        for y in range(0, window_height, self.__tile_size):
            pg.draw.line(self.__screen, self.__grid_color, (0, y), (window_width, y), 4)  # Line width set to 4

        for x in range(0, window_width, self.__tile_size):
            pg.draw.line(self.__screen, self.__grid_color, (x, 0), (x, window_height), 4)  # Line width set to 4

    def draw_menu_block(self):
        window_width = Config.get_config('WIN_SIZE_W')
        window_height = Config.get_config('WIN_SIZE_H')

        pg.draw.rect(self.__screen, self.__sidebar_color,
                     (0, 0, self.__sidebar_width, window_height))  # Sidebar on the left

        pg.draw.line(self.__screen, self.__line_color,
                     (self.__sidebar_width, 0), (self.__sidebar_width, window_height), 4)  # Line width set to 4

    def draw_wall(self):
        wall_width = Config.get_config('WIN_SIZE_W')
        wall_height = 100

        wall_color = Config.get_config('GRAY_BLUE')
        pg.draw.rect(self.__screen, wall_color, (0, 0, wall_width, wall_height))

    def draw_counter_top(self):
        counter_top_image = pg.image.load("images/countertop.png")
        counter_top_image = pg.transform.scale(counter_top_image, (Config.get_config('WIN_SIZE_W') - 300, 80))

        counter_position = (350, 70)
        self.__screen.blit(counter_top_image, counter_position)

        counter_top_image2 = pg.image.load("images/countertop.png")
        counter_top_image2 = pg.transform.rotate(counter_top_image2,90)
        counter_top_image2 = pg.transform.scale(counter_top_image2, (100, Config.get_config('WIN_SIZE_H') - 200))

        counter_position2 = (935, 150)
        self.__screen.blit(counter_top_image2, counter_position2)

    def draw_red_button(self):
        red_button_image = pg.image.load('images/red_button.png')
        red_button_image = pg.transform.scale(red_button_image, (100, 100))

        red_button_position = (915, 300)
        self.__screen.blit(red_button_image, red_button_position)

    def draw_stove(self):
        stove_image = pg.image.load('images/stove.png')
        stove_image = pg.transform.scale(stove_image, (100, 100))

        stove_position = (490, 60)
        self.__screen.blit(stove_image, stove_position)

    def update(self):
        """Update the map by drawing tiles."""
        self.__screen.fill(self.__background_color)
        self.draw_tiles()
        self.draw_wall()
        self.draw_counter_top()
        self.draw_stove()
        self.draw_red_button()
        self.draw_menu_block()


class GameUI:
    game_over = False

    def __init__(self):
        self.__start_time = pg.time.get_ticks()
        self.__game_time = 60

    def reset(self):
        self.__start_time = pg.time.get_ticks()
        GameUI.game_over = False

    def update_time(self):
        elapsed_time = (pg.time.get_ticks() - self.__start_time) // 1000
        remaining_time = self.__game_time - elapsed_time

        if remaining_time <= 0:
            GameUI.game_over = True
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

    @staticmethod
    def draw_game_over(screen, final_score=0):
        """Display Game Over message with final score"""
        if GameUI.game_over:
            # Setup fonts
            large_font = pg.font.SysFont('Arial', 72, bold=True)
            medium_font = pg.font.SysFont('Arial', 48)
            button_font = pg.font.SysFont('Arial', 42)

            screen_width = Config.get_config('WIN_SIZE_W')
            screen_height = Config.get_config('WIN_SIZE_H')

            # Create semi-transparent overlay
            overlay = pg.Surface((screen_width, screen_height), pg.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # Semi-transparent black
            screen.blit(overlay, (0, 0))

            # Create main panel
            panel_rect = pg.Rect(
                screen_width // 2 - 250,
                screen_height // 2 - 200,
                500,
                400
            )
            pg.draw.rect(screen, Config.get_config('PASTEL_GRAY'), panel_rect, border_radius=15)
            pg.draw.rect(screen, Config.get_config('BLACK'), panel_rect, 3, border_radius=15)

            # Game Over text
            game_over_text = large_font.render("GAME OVER", True, Config.get_config('RED'))
            text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 3))
            screen.blit(game_over_text, text_rect)

            # Final Score text
            score_text = medium_font.render(f"Final Score: {final_score}", True, Config.get_config('BLACK'))
            score_rect = score_text.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(score_text, score_rect)

            # Button dimensions
            button_width = 200
            button_height = 60
            button_x = (screen_width - button_width) // 2  # Centered horizontally

            # Restart button (green)
            restart_button_rect = pg.Rect(button_x, screen_height // 2 + 80, button_width, button_height)
            pg.draw.rect(screen, (50, 200, 50), restart_button_rect, border_radius=10)
            pg.draw.rect(screen, Config.get_config('BLACK'), restart_button_rect, 2, border_radius=10)
            restart_text = button_font.render("Restart", True, Config.get_config('WHITE'))
            screen.blit(restart_text, restart_text.get_rect(center=restart_button_rect.center))

            # Exit button (red)
            exit_button_rect = pg.Rect(button_x, screen_height // 2 + 160, button_width, button_height)
            pg.draw.rect(screen, (200, 50, 50), exit_button_rect, border_radius=10)
            pg.draw.rect(screen, Config.get_config('BLACK'), exit_button_rect, 2, border_radius=10)
            exit_text = button_font.render("Exit", True, Config.get_config('WHITE'))
            screen.blit(exit_text, exit_text.get_rect(center=exit_button_rect.center))

            pg.display.flip()

            return restart_button_rect, exit_button_rect

    @staticmethod
    def draw_start_game(screen):
        """Display start screen with buttons centered."""
        if not GameUI.game_over:
            font = pg.font.SysFont(None, 72)
            button_font = pg.font.SysFont(None, 50)

            screen_width = Config.get_config('WIN_SIZE_W')
            screen_height = Config.get_config('WIN_SIZE_H')

            # Game title text
            title_text = font.render("Apocalypse Cooker", True, Config.get_config('BLACK'))
            title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 4))

            # Button dimensions
            button_width = 250
            button_height = 60
            button_x = (screen_width - button_width) // 2  # Centered horizontally

            # Define button positions
            restart_button_rect = pg.Rect(button_x, screen_height // 2 - 60, button_width, button_height)
            stat_button_rect = pg.Rect(button_x, screen_height // 2 + 20, button_width, button_height)
            exit_button_rect = pg.Rect(button_x, screen_height // 2 + 100, button_width, button_height)

            # Fill background
            screen.fill(Config.get_config('WHITE'))

            # Draw title
            screen.blit(title_text, title_rect)

            # Draw buttons
            for rect in [restart_button_rect, stat_button_rect, exit_button_rect]:
                pg.draw.rect(screen, Config.get_config('GRAY'), rect, border_radius=10)

            # Render and center button text
            restart_text = button_font.render("Start", True, Config.get_config('BLACK'))
            stat_text = button_font.render("Statistics", True, Config.get_config('BLACK'))
            exit_text = button_font.render("Exit", True, Config.get_config('BLACK'))

            screen.blit(restart_text, restart_text.get_rect(center=restart_button_rect.center))
            screen.blit(stat_text, stat_text.get_rect(center=stat_button_rect.center))
            screen.blit(exit_text, exit_text.get_rect(center=exit_button_rect.center))

            pg.display.flip()

            return restart_button_rect, stat_button_rect, exit_button_rect

