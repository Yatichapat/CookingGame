import time
import os
from cooking_config import Config
import pygame as pg
import random
from collections import deque
import csv
from datetime import datetime


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
        self.font_menu = pg.font.Font(None, 14)
        self.font_score = pg.font.Font(None, 42)
        self.orders = deque()
        self.max_orders = max_orders
        self.__serving_pad = None
        self.__score = 0

        self.__completed_dishes = []
        self.__session_start = time.time()
        self.__current_minute = 0
        self.__dishes_this_minute = 0
        self.__last_save_time = time.time()

        self.__images = {
            item: pg.transform.scale(Config.get_image(item), (90, 90)) for item in self.MENU_ITEMS
        }

    def serve_dish(self, plate):
        """Check if plate matches any order and calculate score"""
        if not self.orders:
            return 0

            # Find matching dish type
        prepared_type = None
        for ingredient in plate.get_ingredients():
            if ingredient.get_type() in self.MENU_ITEMS:
                prepared_type = ingredient.get_type()
                break

        if not prepared_type:
            return 0

        # Process matching order
        for order in self.orders:
            if order["name"] == prepared_type:
                # Calculate points
                time_remaining = order["duration"] - (pg.time.get_ticks() - order["start_time"])
                time_bonus = max(0, time_remaining // 1000)

                # Remove fulfilled order
                self.orders.remove(order)

                points = 10 + time_bonus
                self.__score += points

                # Update minute tracking
                self._update_minute_tracking()
                return points

        return 0

    def _update_minute_tracking(self):
        """Internal method to handle minute-by-minute tracking"""
        current_time = time.time()
        elapsed_minutes = int((current_time - self.__session_start) / 60)

        # If new minute, save previous minute's data
        if elapsed_minutes > self.__current_minute:
            self.__completed_dishes.append({
                'minute': self.__current_minute,
                'dishes': self.__dishes_this_minute,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            self.__current_minute = elapsed_minutes
            self.__dishes_this_minute = 0

            # Auto-save every 1 minutes
            if elapsed_minutes % 1 == 0:
                self.save_to_order_per_minute()

        self.__dishes_this_minute += 1

    def reset(self):
        self.orders = deque()
        self.__score = 0
        self.save_to_order_per_minute()

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
        """Remove expired orders and add new ones"""
        current_time = pg.time.get_ticks()
        while self.orders and current_time - self.orders[0]["start_time"] >= self.orders[0]["duration"]:
            self.orders.popleft()  # Remove expired order
            # Penalty for expired order?
            self.__score -= 5

        if len(self.orders) < self.max_orders and random.random() < 0.02:
            self.add_order()

    def draw_score(self, screen):
        """Display current score on screen"""
        score_text = self.font_score.render(f"Score: {self.__score}", True, Config.get_config('BLACK'))
        screen.blit(score_text, (10, 460))

    def get_score(self):
        return self.__score

    def draw(self, screen):
        """Render the menu orders."""
        current_time = pg.time.get_ticks()

        for i, order in enumerate(self.orders):
            rect_x = 800 - i * 250  # Move each order left
            rect_y = 460
            order_width = 150
            order_height = 150

            pg.draw.rect(screen, Config.get_config('WHITE'), (rect_x, rect_y, 150, 150), border_radius=15)

            if order["name"] in self.__images:
                screen.blit(self.__images[order["name"]], (rect_x + 27, rect_y + 10))

            # Draw order name
            text = self.font_menu.render(order["name"], True, Config.get_config('BLACK'))
            screen.blit(text, (rect_x + 50, rect_y + 110))

            time_elapsed = current_time - order["start_time"]
            progress = 1.0 - min(1.0, time_elapsed / order["duration"])

            # Time bar dimensions
            bar_width = 130
            bar_height = 8
            bar_x = rect_x + 10
            bar_y = rect_y + 130

            # Draw time bar background
            pg.draw.rect(screen, (100, 100, 100),
                         (bar_x, bar_y, bar_width, bar_height),
                         border_radius=4)

            # Draw time remaining (green)
            pg.draw.rect(screen, Config.get_config('GREEN'),
                         (bar_x, bar_y, int(bar_width * progress), bar_height),
                         border_radius=4)

    def save_to_order_per_minute(self, force_save=False):
        """Save statistics to CSV, with option to force immediate save"""
        if not self.__completed_dishes and not force_save:
            return

        filename = "order_per_minute.csv"
        try:
            file_exists = os.path.exists(filename)

            with open(filename, 'a', newline='') as csvfile:
                fieldnames = ['timestamp', 'minute', 'dishes', 'score']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if not file_exists:
                    writer.writeheader()

                for record in self.__completed_dishes:
                    writer.writerow({
                        'timestamp': record['timestamp'],
                        'minute': record['minute'],
                        'dishes': record['dishes'],
                    })

            # Clear saved records
            self.__completed_dishes = []
            self.__last_save_time = time.time()

        except Exception as e:
            print(f"Error saving dish stats: {e}")

