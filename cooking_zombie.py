import pygame as pg
from cooking_config import Config
import random


class Zombie:
    def __init__(self):
        self.__position = (random.randint(0, Config.get_config('WIN_SIZE_W') - 1),
                           random.randint(0, Config.get_config('WIN_SIZE_H') - 1))
        self.screen = None

        self.__image = pg.transform.scale(pg.image.load("images/Zombie_1/Walk_still.png"), (30,70))
        self.zombie_rect = self.__image.get_rect(topleft=self.__position)
        self.__speed = 4
        self.__chasing = False
        self.__last_attack_time = 0

    def move_towards(self, target_x, target_y):
        """Move towards a given (x, y) target."""
        dx = target_x - self.zombie_rect.x
        dy = target_y - self.zombie_rect.y
        distance = max(0.1, (dx**2 + dy**2) ** 0.5)  # Prevent division by zero

        # Normalize direction and apply speed
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

    def get_position(self):
        """Get the current position of the zombie"""
        return self.__position

    def set_screen(self, screen):
        self.screen = screen

    def draw(self):
        if self.screen:
            self.screen.blit(self.__image, self.zombie_rect)
