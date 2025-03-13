import pygame as pg
from cooking_config import Config
import random


class Zombie:
    def __init__(self, idle_image):
        self.__position = (random.randint(0, Config.get('WIN_SIZE_W') - 1),
                           random.randint(0, Config.get('WIN_SIZE_H') - 1))
        self.screen = None

        # Load idle sprite sheet
        self.__idle_image = idle_image

        # Define frame properties (these need to be known beforehand)
        self.frame_width_idle = 128
        self.frame_height_idle = 128
        self.total_frames_idle = 6

        # Extract frames
        self.idle_frames = [
            pg.transform.scale(
                self.__idle_image.subsurface(i * self.frame_width_idle, 0, self.frame_width_idle, self.frame_height_idle),
                (Config.get('CHARACTER_SIZE') + 10, Config.get('CHARACTER_SIZE') + 10)
            )
            for i in range(self.total_frames_idle)
        ]

        self.current_frame = 0

        # Initialize zombie rectangle
        self.zombie_rect = self.idle_frames[0].get_rect(topleft=self.__position)
        self.zombie_sprite = self.idle_frames[0]

        self.speed = 2
        self.chasing = False

    def move_towards(self, target_x, target_y):
        """Move towards a given (x, y) target."""
        dx = target_x - self.zombie_rect.x
        dy = target_y - self.zombie_rect.y
        distance = max(1, (dx**2 + dy**2) ** 0.5)  # Prevent division by zero

        # Normalize direction and apply speed
        self.zombie_rect.x += self.speed * (dx / distance)
        self.zombie_rect.y += self.speed * (dy / distance)
        self.__position = (self.zombie_rect.x, self.zombie_rect.y)

    def chase_player(self, player):
        """Make the zombie chase the player."""
        player_x, player_y = player.get_position()
        self.move_towards(player_x, player_y)
        self.chasing = True

    def get_position(self):
        """Get the current position of the zombie"""
        return self.__position

    def set_screen(self, screen):
        self.screen = screen

    def draw(self):
        if self.screen:
            self.screen.blit(self.zombie_sprite, self.zombie_rect)
