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
    MENU_ITEMS = ["sandwich", "egg fried", "chicken fried", "lamb fried"]

    def __init__(self, max_orders=3):
        self.font = pg.font.Font(None, 14)
        self.orders = deque()
        self.max_orders = max_orders

        self.__images = {
            item: pg.transform.scale(Config.get_image(item), (90, 90)) for item in self.MENU_ITEMS
        }

    def reset(self):
        self.orders = deque()

    def add_order(self):
        """Add a new random menu item to the queue."""
        if len(self.orders) < self.max_orders:
            menu_item = random.choice(self.MENU_ITEMS)
            order = {
                "name": menu_item,
                "start_time": pg.time.get_ticks(),
                "duration": 60000,
                "position": (800 - len(self.orders) * 150, 450)
            }
            self.orders.append(order)

    def update(self):
        """Remove expired orders from the queue."""
        current_time = pg.time.get_ticks()
        while self.orders and current_time - self.orders[0]["start_time"] >= self.orders[0]["duration"]:
            self.orders.popleft()  # Remove expired order

        if random.random() < 0.02:
            self.add_order()

    def draw(self, screen):
        """Render the menu orders."""

        for i, order in enumerate(self.orders):
            rect_x = 800 - i * 250  # Move each order left
            rect_y = 460

            pg.draw.rect(screen, Config.get_config('WHITE'), (rect_x, rect_y, 150, 150), border_radius=15)

            if order["name"] in self.__images:
                screen.blit(self.__images[order["name"]], (rect_x + 27, rect_y + 10))

            # Draw order name
            text = self.font.render(order["name"], True, Config.get_config('BLACK'))
            screen.blit(text, (rect_x + 50, rect_y + 110))


