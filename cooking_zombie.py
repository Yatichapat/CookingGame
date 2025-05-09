import pygame as pg
from cooking_config import Config
import random


class Zombie:
    def __init__(self, delay_time=3000):
        self.__position = (self.spawn_offscreen(Config.get_config('WIN_SIZE_W'), Config.get_config('WIN_SIZE_H')))
        self.screen = None

        self.__image = pg.transform.scale(pg.image.load("images/Zombie_1/Walk_still.png"), (30,70))
        self.zombie_rect = self.__image.get_rect(topleft=self.__position)
        self.__speed = 2
        self.__chasing = False
        self.__last_attack_time = 0

        self.__spawn_time = pg.time.get_ticks()
        self.__delay_time = delay_time

    def reset(self):
        self.__position = (self.spawn_offscreen(Config.get_config('WIN_SIZE_W'), Config.get_config('WIN_SIZE_H')))
        self.__speed = 2
        self.__chasing = False
        self.zombie_rect = self.__image.get_rect(topleft=self.__position)

        self.__spawn_time = pg.time.get_ticks()
        self.__delay_time = 3000

    def spawn_offscreen(self, screen_width, screen_height):
        """Randomly generates a spawn position outside the screen."""
        side = random.choice(["left", "right", "top", "bottom"])

        if side == "left":
            return -50, random.randint(0, screen_height)
        elif side == "right":
            return screen_width + 50, random.randint(0, screen_height)
        elif side == "top":
            return random.randint(0, screen_width), -50
        else:
            return random.randint(0, screen_width), screen_height + 50

    def move_towards(self, target_x, target_y):
        """Move towards a given (x, y) target."""

        dx = target_x - self.zombie_rect.x
        dy = target_y - self.zombie_rect.y
        distance = max(0.1, (dx**2 + dy**2) ** 0.5)  # Prevent division by zero

        # Normalize direction and apply speed
        current_time = pg.time.get_ticks()
        if current_time - self.__spawn_time < self.__delay_time:
            return

        self.zombie_rect.x += self.__speed * (dx / distance)
        self.zombie_rect.y += self.__speed * (dy / distance)
        self.__position = (self.zombie_rect.x, self.zombie_rect.y)

    def chase_player(self, player):
        """Make the zombie chase the player."""
        player_x, player_y = player.get_position()
        self.move_towards(player_x, player_y)
        self.__chasing = True
        self.attack(player)

    def attack(self, player):
        current_time = pg.time.get_ticks()
        if current_time - self.__last_attack_time >= 1000:
            if self.zombie_rect.colliderect(player.get_rect()):
                player.take_damage(10)
                self.__last_attack_time = current_time
                return True
        return False

    def get_position(self):
        """Get the current position of the zombie"""
        return self.__position

    def set_screen(self, screen):
        self.screen = screen

    def draw(self):
        if self.screen:
            self.screen.blit(self.__image, self.zombie_rect)
