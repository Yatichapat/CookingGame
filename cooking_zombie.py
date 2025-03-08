import pygame as pg
from cooking_config import Config
import random


class Zombie:
    def __init__(self):
        self.__position = (random.randint(0, Config.get('WIN_SIZE_W') - 1),
                           random.randint(0, Config.get('WIN_SIZE_H') - 1))

        try:
            self.__walk_image = pg.image.load("images/Zombie_1/Walk.png")
        except pg.error as e:
            print("Error loading image:", e)
            exit()

        self.frame_width = 128
        self.frame_height = 128
        self.total_frames = 10

        self.frames = [
            pg.transform.scale(
                self.__walk_image.subsurface(i * self.frame_width, 0, self.frame_width, self.frame_height),
                (Config.get('CHARACTER_SIZE'), Config.get('CHARACTER_SIZE'))
            )
            for i in range(self.total_frames)
        ]

        self.current_frame = 0
        self.zombie_sprite = self.frames[self.current_frame]
        self.zombie_rect = self.zombie_sprite.get_rect()
        self.zombie_rect.topleft = self.__position

        self.speed = 2
        self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        self.time_to_change_direction = random.randint(300, 600)
        self.time_to_pause_after_change = random.randint(400, 600)

    def wander(self):
        """Move the zombie randomly"""
        if self.time_to_change_direction <= 0:
            self.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
            self.time_to_change_direction = random.randint(10, 50)
            self.time_to_pause_after_change = random.randint(5, 20)
        else:
            self.time_to_change_direction -= 1

        if self.direction == 'UP':
            self.zombie_rect.y -= self.speed
        elif self.direction == 'DOWN':
            self.zombie_rect.y += self.speed
        elif self.direction == 'LEFT':
            self.zombie_rect.x -= self.speed
        elif self.direction == 'RIGHT':
            self.zombie_rect.x += self.speed

        self.__position = (self.zombie_rect.x, self.zombie_rect.y)  # Update position
        self.animate_wander()

    def animate_wander(self):
        """Animate the zombie by cycling through frames"""
        self.current_frame = (self.current_frame + 1) % self.total_frames
        self.zombie_sprite = self.frames[self.current_frame]

    def get_position(self):
        """Get the current position of the zombie"""
        return self.__position

    def set_screen(self, screen):
        if screen is not None:
            self.screen = screen

    def draw(self):
        if self.screen:
            self.screen.blit(self.zombie_sprite, self.zombie_rect)