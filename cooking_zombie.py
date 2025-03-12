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
        self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        self.time_to_change_direction = random.randint(1, 5)
        self.time_to_pause_after_change = random.randint(10, 200)

    def move(self):
        """Move the zombie while keeping it inside the grid"""
        grid_w, grid_h = Config.get('GRID_COUNT_W'), Config.get('GRID_COUNT_H')
        char_size = Config.get('CHARACTER_SIZE')

        new_x, new_y = self.zombie_rect.x, self.zombie_rect.y

        if self.direction == 'UP':
            new_y = max(0, self.zombie_rect.y - self.speed)
        elif self.direction == 'DOWN':
            new_y = min(grid_h * char_size - self.zombie_rect.height, self.zombie_rect.y + self.speed)
        elif self.direction == 'LEFT':
            new_x = max(0, self.zombie_rect.x - self.speed)
        elif self.direction == 'RIGHT':
            new_x = min(grid_w * char_size - self.zombie_rect.width, self.zombie_rect.x + self.speed)

        # Apply the updated position
        self.zombie_rect.x, self.zombie_rect.y = new_x, new_y
        self.__position = (new_x, new_y)

    def wander(self):
        """Move the zombie randomly, changing direction if needed"""
        if self.time_to_pause_after_change > 0:
            self.time_to_pause_after_change -= 1
        elif self.time_to_change_direction > 0:
            self.time_to_change_direction -= 1
            self.move()
        else:
            self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
            self.time_to_change_direction = random.randint(50, 150)
            self.time_to_pause_after_change = random.randint(10, 30)

        self.move()

    def get_position(self):
        """Get the current position of the zombie"""
        return self.__position

    def set_screen(self, screen):
        self.screen = screen

    def draw(self):
        if self.screen:
            self.screen.blit(self.zombie_sprite, self.zombie_rect)
