from datetime import datetime
import time
import csv
import os
import pygame as pg
from cooking_config import Config
from cooking_ui import GameUI


class Chef:
    def __init__(self):
        self.__position = (Config.get_config('WIN_SIZE_W') // 2, Config.get_config('WIN_SIZE_H') // 2)  # Center position
        self.__speed = 10
        self.__screen = None

        self.__font = pg.font.Font(None, 24)
        self.__max_health = 100
        self.__chef_health = self.__max_health
        self.__health_bar_width = 130
        self.__health_bar_height = 10
        self.__health_bar_color = Config.get_config('GREEN')
        self.__background_color = Config.get_config('WHITE')
        self.__held_plate = None

        self.movement = {'UP': False, 'DOWN': False, 'LEFT': False, 'RIGHT': False}
        self.__key_states = {
            pg.K_w: False,
            pg.K_s: False,
            pg.K_a: False,
            pg.K_d: False
        }

        self.__key_initial_press = {
            pg.K_w: False,
            pg.K_s: False,
            pg.K_a: False,
            pg.K_d: False
        }

        self.__chef_sprite_original = pg.transform.scale(pg.image.load("images/player.png"), (40, 80))
        self.__chef_sprite = self.__chef_sprite_original
        self.__chef_rect = self.__chef_sprite.get_rect(center=self.__position)

        self.__facing_left = False

        self.__keystrokes = {
            pg.K_w: 0,  # UP
            pg.K_s: 0,  # DOWN
            pg.K_a: 0,  # LEFT
            pg.K_d: 0  # RIGHT
        }
        self.__last_log_time = time.time()
        self.__dish_start_time = None

    def reset(self):
        self.__position = (Config.get_config('WIN_SIZE_W') // 2, Config.get_config('WIN_SIZE_H') // 2)
        self.__chef_rect.topleft = self.__position
        self.__chef_health = self.__max_health
        self.__chef_sprite = self.__chef_sprite_original
        self.__facing_left = False
        self.movement = {'UP': False, 'DOWN': False, 'LEFT': False, 'RIGHT': False}

        self.__keystrokes = {key: 0 for key in self.__key_states}
        for key in self.__key_states:
            self.__key_states[key] = False
            self.__key_initial_press[key] = False
            self.__keystrokes[key] = 0

        self.__dish_start_time = None

    def draw(self):
        if self.__screen:
            self.__screen.blit(self.__chef_sprite, self.__chef_rect.topleft)  # Draw sprite
            self.draw_health_bar()

    def move(self):
        """Update chef's position and sprite orientation"""
        if self.movement['UP']:
            self.__chef_rect.y -= self.__speed

        if self.movement['DOWN']:
            self.__chef_rect.y += self.__speed

        if self.movement['LEFT']:
            self.__chef_rect.x -= self.__speed

        if self.movement['RIGHT']:
            self.__chef_rect.x += self.__speed

        # Keep the chef inside the screen boundaries
        self.__chef_rect.x = max(220, min(self.__chef_rect.x, Config.get_config('WIN_SIZE_W') - 100))
        self.__chef_rect.y = max(100, min(self.__chef_rect.y, Config.get_config('WIN_SIZE_H') - Config.get_config('GRID_SIZE_H')))

        self.__position = self.__chef_rect.topleft  # Update position after movement

    def get_position(self):
        """Get the current position of the chef"""
        return self.__position

    def set_screen(self, screen):
        self.__screen = screen

    def handle_input(self, event, fridge_open):
        """Handle keyboard input for movement"""
        if event.type == pg.KEYDOWN:
            if event.key in self.__key_states and not self.__key_initial_press[event.key]:
                self.__key_states[event.key] = True
                self.__keystrokes[event.key] += 1
                self.__key_initial_press[event.key] = True

                if not fridge_open:
                    self._update_movement_from_states()

        elif event.type == pg.KEYUP:
            if event.key in self.__key_states:
                self.__key_states[event.key] = False
                self.__key_initial_press[event.key] = False

                if not fridge_open:
                    self._update_movement_from_states()

    def _update_movement_from_states(self):
        """Update movement flags based on current key states"""
        self.movement['UP'] = self.__key_states[pg.K_w]
        self.movement['DOWN'] = self.__key_states[pg.K_s]
        self.movement['LEFT'] = self.__key_states[pg.K_a]
        self.movement['RIGHT'] = self.__key_states[pg.K_d]

        # Update sprite direction if needed
        if self.movement['LEFT'] and not self.__facing_left:
            self.__facing_left = True
            self.update_sprite(flip=True)
        elif self.movement['RIGHT'] and self.__facing_left:
            self.__facing_left = False
            self.update_sprite(flip=False)

    def update_sprite(self, flip=False):
        """Flip sprite when changing direction"""
        self.__chef_sprite = pg.transform.flip(self.__chef_sprite_original, flip, False)

    def draw_health_bar(self):
        x, y = 10, 500
        pg.draw.rect(self.__screen, self.__background_color, (x, y, self.__health_bar_width, self.__health_bar_height))

        # Calculate the width of the health bar based on the player's current health
        health_width = (self.__chef_health / self.__max_health) * self.__health_bar_width
        if health_width <= 0:
            GameUI.game_over = True
            GameUI.draw_game_over(self.__screen)

        # Draw the filled rectangle representing the player's health
        pg.draw.rect(self.__screen, self.__health_bar_color, (x, y, health_width, self.__health_bar_height))
        text = self.__font.render(f"Health", True, Config.get_config('BLACK'))
        self.__screen.blit(text, (x + 140, y - 4))

    def take_damage(self, damage):
        self.__chef_health = max(0, self.__chef_health - damage)
        if self.__chef_health <= 0:
            GameUI.game_over = True

    def heal(self, amount):
        self.__chef_health = min(self.__max_health, self.__chef_health + amount)

    def get_rect(self):
        return self.__chef_rect

    def pick_up_plate(self, plate):
        """Pick up a plate and its ingredients."""
        if not self.__held_plate:
            self.__held_plate = plate

    def save_keystrokes_to_csv(self):
        """Save keystrokes to a CSV file with timestamp and movement data.

        Creates a new file if it doesn't exist, or appends to existing file.
        Logs only when the specified time interval has passed.
        """
        filename = "keystroke_per_dish.csv"
        try:
            current = datetime.now()
            file_exists = os.path.exists(filename)

            # Initialize last_id
            last_id = 0

            # Read existing records if file exists
            if file_exists:
                with open(filename, 'r') as csvfile:
                    reader = csv.DictReader(csvfile)
                    records = list(reader)
                    if records:
                        # Convert string IDs to integers for comparison
                        last_id = max(int(record['id']) for record in records)

            # Open file in append mode
            with open(filename, 'a', newline='') as csvfile:
                fieldnames = [
                    'timestamp',
                    'up',
                    'down',
                    'left',
                    'right',
                    'total_key',
                    'id',
                ]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                if not file_exists:
                    writer.writeheader()

                record = {
                    'id': last_id + 1,
                    'timestamp': current.strftime("%Y-%m-%d %H:%M:%S"),
                    'up': self.__keystrokes[pg.K_w],
                    'down': self.__keystrokes[pg.K_s],
                    'left': self.__keystrokes[pg.K_a],
                    'right': self.__keystrokes[pg.K_d],
                    'total_key': sum(self.__keystrokes.values())
                }

                self.__last_log_time = current
                print("Saving session data:", record)  # Debug print
                writer.writerow(record)

        except IOError as e:
            print(f"Error writing to CSV file: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
