import pygame as pg
from cooking_config import Config


class Chef:
    def __init__(self):
        self.__position = (Config.get('WIN_SIZE_W') // 2, Config.get('WIN_SIZE_H') // 2)  # Starting position at center

        self.speed = 3
        self.screen = None

        self.movement = {'UP': False, 'DOWN': False, 'LEFT': False, 'RIGHT': False}
        self.chef_rect = pg.Rect(self.__position[0], self.__position[1], Config.get('GRID_SIZE_W'), Config.get('GRID_SIZE_H'))
        self.reset()

    def reset(self):
        self.__position = (Config.get('WIN_SIZE_W') // 2, Config.get('WIN_SIZE_H') // 2)
        self.speed = 10
        self.chef_rect.topleft = self.__position

    def draw(self):
        if self.screen:
            pg.draw.rect(self.screen, Config.get('BLACK'), self.chef_rect)

    def move(self):
        # Update the animation based on movement
        if self.movement['UP']:
            self.chef_rect.y -= self.speed

        elif self.movement['DOWN']:
            self.chef_rect.y += self.speed

        elif self.movement['LEFT']:
            self.chef_rect.x -= self.speed

        elif self.movement['RIGHT']:
            self.chef_rect.x += self.speed

        # Keep the chef inside the screen
        self.chef_rect.x = max(0, self.chef_rect.x)
        self.chef_rect.x = min(Config.get('WIN_SIZE_W') - Config.get('GRID_SIZE_W'), self.chef_rect.x)
        self.chef_rect.y = max(0, self.chef_rect.y)
        self.chef_rect.y = min(Config.get('WIN_SIZE_H') - Config.get('GRID_SIZE_H'), self.chef_rect.y)
        self.__position = (self.chef_rect.x, self.chef_rect.y)

    def get_position(self):
        """Get the current position of the chef"""
        return self.__position

    def set_screen(self, screen):
        self.screen = screen
