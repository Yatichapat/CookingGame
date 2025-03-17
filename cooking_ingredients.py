from cooking_config import Config
import pygame as pg


class Ingredients:
    def __init__(self, x, y, ingredient_type):
        self.__position = (x, y)
        self.__ingredient_type = ingredient_type
        self.images = Config.get_image(ingredient_type)

    def get_position(self):
        return self.__position

    def set_position(self, position):
        self.__position = position

    def draw(self, screen):
        """Draw ingredient at its default position."""
        self.draw_at(screen, self.__position[0] * Config.get_config('GRID_SIZE_W'),
                     self.__position[1] * Config.get_config('GRID_SIZE_H'))

    def get_type(self):
        return self.__ingredient_type

    def set_type(self, ingredient_type):
        self.__ingredient_type = ingredient_type
        self.images = Config.get_image(ingredient_type)

    def draw_at(self, screen, x, y):
        """Draw ingredient at a specific position (e.g., inside the fridge)."""
        screen.blit(self.images, (x, y))  # Directly use self.__image to draw


class Menu:
    def __init__(self, duration=5000, position=(870, 570), background_position=(800,450)):  # Menu lasts 5 seconds
        self.duration = duration
        self.font = pg.font.Font(None, 24)
        self.remaining_time = duration
        self.position = position
        self.active = True
        self.background = Config.get_config('MESSAGE_BACKGROUND')
        self.background_position = background_position

        self.start_time = pg.time.get_ticks()

    def update(self):
        """Reduce time based on the elapsed time (dt)."""
        if self.active:
            elapsed_time = pg.time.get_ticks() - self.start_time
            self.remaining_time = max(self.duration - elapsed_time, 0)
            if self.remaining_time <= 0:
                self.active = False  # Hide menu when time runs out

    def draw(self, screen):
        """Render the menu if active."""

        if self.active:
            screen.blit(self.background, self.background_position)
            text = self.font.render(f"Menu: {self.remaining_time // 1000}s", True, Config.get_config('BLACK'))
            screen.blit(text, self.position)


