import time
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
        self.__chef_sprite_original = pg.transform.scale(pg.image.load("images/player.png"), (40, 80))
        self.__chef_sprite = self.__chef_sprite_original
        self.__chef_rect = self.__chef_sprite.get_rect(center=self.__position)
        self.__facing_left = False

        self.__keystrokes = 0
        self.__dish_start_time = None

    def reset(self):
        self.__position = (Config.get_config('WIN_SIZE_W') // 2, Config.get_config('WIN_SIZE_H') // 2)
        self.__chef_rect.topleft = self.__position
        self.__chef_health = self.__max_health
        self.__chef_sprite = self.__chef_sprite_original
        self.__facing_left = False
        self.movement = {'UP': False, 'DOWN': False, 'LEFT': False, 'RIGHT': False}

        self.__keystrokes = 0
        self.__dish_start_time = None

    def draw(self):
        if self.__screen:
            self.__screen.blit(self.__chef_sprite, self.__chef_rect.topleft)  # Draw sprite
            self.draw_health_bar()

    def move(self):
        """Update chef's position and sprite orientation"""
        prev_x, prev_y = self.__chef_rect.topleft  # Store previous position

        if self.movement['UP']:
            self.__chef_rect.y -= self.__speed
        if self.movement['DOWN']:
            self.__chef_rect.y += self.__speed
        if self.movement['LEFT']:
            self.__chef_rect.x -= self.__speed
            if not self.__facing_left:
                self.__facing_left = True
                self.update_sprite(flip=True)
        if self.movement['RIGHT']:
            self.__chef_rect.x += self.__speed
            if self.__facing_left:
                self.__facing_left = False
                self.update_sprite(flip=False)

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
        if fridge_open:
            # Ignore movement input if fridge is open
            return

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                self.movement['UP'] = True
            elif event.key == pg.K_DOWN:
                self.movement['DOWN'] = True
            elif event.key == pg.K_LEFT:
                self.movement['LEFT'] = True
            elif event.key == pg.K_RIGHT:
                self.movement['RIGHT'] = True

        elif event.type == pg.KEYUP:
            if event.key == pg.K_UP:
                self.movement['UP'] = False
            elif event.key == pg.K_DOWN:
                self.movement['DOWN'] = False
            elif event.key == pg.K_LEFT:
                self.movement['LEFT'] = False
            elif event.key == pg.K_RIGHT:
                self.movement['RIGHT'] = False

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