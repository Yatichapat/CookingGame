import os
from file_game.cooking_config import Config
from file_game.cooking_ui import GameUI
import pygame as pg
import random
from collections import deque
import csv
from datetime import datetime


class Menu:
    __MENU_ITEMS = ["sandwich", "egg fried", "chicken fried", "lamb fried", "chicken drumstick fried",
                    "fish fried", "pork fried"]

    def __init__(self, max_orders=3):
        self.__font_menu = pg.font.Font(None, 14)
        self.__font_score = pg.font.Font(None, 42)
        self.__orders = deque()
        self.__max_orders = max_orders
        self.__serving_pad = None
        self.__score = 0

        # Tracking variables order
        self.__menu_appearance = {item: 0 for item in self.__MENU_ITEMS}  # How often each item appears as order
        self.__successful_orders = {item: 0 for item in self.__MENU_ITEMS}  # How often each was successfully served
        self.__session_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Tracking mistakes
        self.__detailed_mistakes = []
        self.__current_mistakes = 0

        self.__dish_preparation_times = []

        self.__images = {
            item: pg.transform.scale(Config.get_image(item), (90, 90)) for item in self.__MENU_ITEMS
        }
        self.__csv_file = "game_data/total_time_per_dish.csv"
        self.__session_id = self.__get_next_session_id()

    def __get_next_session_id(self):
        if not os.path.exists(self.__csv_file):
            return 1

        session_ids = []
        with open(self.__csv_file, 'r') as file:
            reader = csv.DictReader(file)  # <-- This ensures rows are dictionaries
            for row in reader:
                sid = row.get('session_id', '').strip()
                if sid.isdigit():
                    session_ids.append(int(sid))

        return max(session_ids, default=0) + 1

    def log_mistake(self, mistake_type="unknown", extra_info=None):
        self.__current_mistakes += 1
        self.__detailed_mistakes.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": mistake_type,
            "info": extra_info or ""
        })
        self.save_to_mistake()

    def serve_dish(self, plate):
        """Check if plate matches any order and calculate score"""
        if not self.__orders:
            self.log_mistake("no_orders", "No orders available")
            return 0

        # Find matching dish type
        prepared_type = None
        for ingredient in plate.get_ingredients():
            if ingredient.get_type() in self.__MENU_ITEMS:
                prepared_type = ingredient.get_type()
                break

        # If no valid menu item is found on the plate
        if prepared_type is None:
            self.log_mistake("wrong_dish", "No valid menu item on plate")
            return 0

        # Process matching order
        for order in list(self.__orders):
            if order["name"] == prepared_type:
                # Calculate points
                current_time = pg.time.get_ticks()
                elapsed_time = (current_time - order["start_time"]) / 1000
                time_remaining = order["duration"] - (pg.time.get_ticks() - order["start_time"])
                time_bonus = max(0, time_remaining // 1000)

                # Track dish preparation time
                self.__dish_preparation_times.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "dish_type": prepared_type,
                    "preparation_time_seconds": elapsed_time
                })

                # Remove fulfilled order
                self.__orders.remove(order)

                # Track successful order
                self.__successful_orders[prepared_type] += 1

                points = 10 + time_bonus
                self.__score += points
                Config.get_sound("served").play()  # Play sound for successful order

                return points

        # If we reach here, no matching order was found
        self.log_mistake("wrong_dish", f"served: {prepared_type}")
        return 0

    def reset(self):
        """Save session data before resetting"""
        self.__orders = deque()
        self.__score = 0
        self.__menu_appearance = {item: 0 for item in self.__MENU_ITEMS}
        self.__successful_orders = {item: 0 for item in self.__MENU_ITEMS}
        self.__session_id = self.__get_next_session_id()
        self.__session_start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__dish_preparation_times = []

        self.__current_mistakes = 0
        self.__detailed_mistakes = []

    def add_order(self):
        """Add a new random menu item to the queue."""
        if len(self.__orders) < self.__max_orders:
            menu_item = random.choice(self.__MENU_ITEMS)
            self.__menu_appearance[menu_item] += 1  # Track order appearance

            order = {
                "name": menu_item,
                "start_time": pg.time.get_ticks(),
                "duration": 60000,  # 60 seconds to complete
                "position": (800 - len(self.__orders) * 150, 450)
            }
            self.__orders.append(order)

    def update(self):
        """Remove expired orders and add new ones"""
        current_time = pg.time.get_ticks()
        while self.__orders and current_time - self.__orders[0]["start_time"] >= self.__orders[0]["duration"]:
            self.__orders.popleft()  # Remove expired order
            if not GameUI.game_over:
                self.__score -= 5  # Penalty for expired order

        if len(self.__orders) < self.__max_orders and random.random() < 0.05:
            self.add_order()

    def draw_score(self, screen):
        """Display current score on screen"""
        score_text = self.__font_score.render(f"Score: {self.__score}", True, Config.get_config('BLACK'))
        screen.blit(score_text, (10, 460))

    def get_score(self):
        return self.__score

    def draw(self, screen):
        """Render the menu orders."""
        current_time = pg.time.get_ticks()

        for i, order in enumerate(self.__orders):
            rect_x = 800 - i * 250  # Move each order left
            rect_y = 460
            order_width = 150
            order_height = 150

            pg.draw.rect(screen, Config.get_config('WHITE'), (rect_x, rect_y, 150, 150), border_radius=15)

            if order["name"] in self.__images:
                screen.blit(self.__images[order["name"]], (rect_x + 27, rect_y + 10))

            # Draw order name
            text = self.__font_menu.render(order["name"], True, Config.get_config('BLACK'))
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

    def save_to_mistake(self):
        file_name = "game_data/mistake.csv"
        try:
            file_exist = os.path.exists(file_name)

            with open(file_name, 'a', newline='') as csv_file:
                fieldnames = ['timestamp', 'mistake_type', 'info']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                if not file_exist:
                    writer.writeheader()

                for mistake in self.__detailed_mistakes:
                    writer.writerow({
                        'timestamp': mistake['timestamp'],
                        'mistake_type': mistake['type'],
                        'info': mistake['info']
                    })

        except Exception as e:
            print(f"Error saving detailed mistake log: {e}")

    def save_to_order_per_session(self, force_save=False):
        """Save statistics to CSV, with option to force immediate save"""
        # Only save if we have some successful orders or are forcing a save
        if not force_save:
            return

        filename = "game_data/order_per_session.csv"
        try:
            file_exists = os.path.exists(filename)

            with open(filename, 'a', newline='') as csvfile:
                fieldnames = ['session_start', 'session_end', 'total_score'] + self.__MENU_ITEMS
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if not file_exists:
                    writer.writeheader()

                record = {
                    'session_start': self.__session_start_time,
                    'session_end': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'total_score': self.__score,
                }

                # Add counts for each menu item
                for item in self.__MENU_ITEMS:
                    record[item] = self.__successful_orders[item]

                print("Saving session data:", record)  # Debug print
                writer.writerow(record)

        except Exception as e:
            print(f"Error saving menu statistics: {e}")

    def save_to_time_per_dish(self):
        file_name = "game_data/total_time_per_dish.csv"
        try:
            file_exist = os.path.exists(file_name)

            with open(file_name, 'a', newline='') as csv_file:
                fieldnames = ['timestamp', 'session_id', 'dish_type', 'preparation_time_seconds']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

                if not file_exist:
                    writer.writeheader()

                # Write all tracked preparation times to the CSV
                for record in self.__dish_preparation_times:
                    data = {
                        'timestamp': record['timestamp'],
                        'session_id': self.__session_id,
                        'dish_type': record['dish_type'],
                        'preparation_time_seconds': record['preparation_time_seconds']
                    }
                    writer.writerow(data)

                # Add debug print
                print(f"Saved {len(self.__dish_preparation_times)} dish preparation records to CSV")

                # Clear the preparation times after saving
                self.__dish_preparation_times = []

        except Exception as e:
            print(f"Error saving dish preparation time log: {e}")