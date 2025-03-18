from cooking_config import Config
import pygame as pg
import random
from collections import deque


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
    MENU_ITEMS = ["sandwich", "egg_fried", "chicken_cooked"]

    def __init__(self, duration=5000, position=(870, 570), background_position=(800,450)):  # Menu lasts 5 seconds
        self.duration = duration
        self.font = pg.font.Font(None, 24)
        self.remaining_time = duration
        self.position = position

        self.active = True
        self.background = Config.get_config('MESSAGE_BACKGROUND')
        self.background_position = background_position

        self.start_time = pg.time.get_ticks()
        self.orders = deque()

    def add_order(self):
        if len(self.orders) < 3:
            menu_item = random.choice(self.MENU_ITEMS)
            order = {
                "name": menu_item,
                "start_time": pg.time.get_ticks(),
                "duration": 10000,  # Each order lasts 5 seconds
                "position": (50, 50 + len(self.orders) * 40)  # Stack vertically
            }
            self.orders.append(order)

    def update(self):
        current_time = pg.time.get_ticks()
        while self.orders and current_time - self.orders[0]["start_time"] >= self.orders[0]["duration"]:
            self.orders.popleft()  # Remove expired order

        if random.random() < 0.02:
            self.add_order()

    def draw(self, screen):
        """Render the menu if active."""

        for i, order in enumerate(self.orders):
            screen.blit(self.background, self.background_position)

            text = self.font.render(order["name"], True, Config.get_config('BLACK'))
            screen.blit(text, (870 - i * 300, 570))  # Update positions dynamically



