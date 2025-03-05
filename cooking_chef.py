import pygame as pg
from pygame_functions import *
from cooking_config import Config


class Chef:
    def __init__(self):
        self.__position = (0, 0)
        self.chef_sprite = pg.image.load("images/Walk (1).png")  # Load the image as a surface
        self.chef_sprite = pg.transform.scale(self.chef_sprite, (
        Config.get('GRID_SIZE'), Config.get('GRID_SIZE')))  # Optional scaling if needed
        self.add_walk_images()

        # Create a rect for managing the sprite's position
        self.chef_rect = self.chef_sprite.get_rect()

    def add_walk_images(self):
        """Add walking images for animation"""
        self.walk_images = []
        for i in range(1, 16):
            image = pg.image.load(f"images/Walk ({i}).png")
            image = pg.transform.scale(image, (Config.get('GRID_SIZE'), Config.get('GRID_SIZE')))  # Optional scaling
            self.walk_images.append(image)

    def move(self, direction):
        """Move the chef in a specific direction"""
        x, y = self.__position
        if direction == 'UP':
            y -= 1
        elif direction == 'DOWN':
            y += 1
        elif direction == 'LEFT':
            x -= 1
        elif direction == 'RIGHT':
            x += 1

        # Ensure the chef doesn't move off-screen
        max_x = Config.get('WIN_SIZE_W') // Config.get('GRID_SIZE')
        max_y = Config.get('WIN_SIZE_H') // Config.get('GRID_SIZE')

        if 0 <= x < max_x and 0 <= y < max_y:
            self.__position = (x, y)
            self.update_sprite_position()

    def move_up(self):
        """Move up"""
        self.move('UP')

    def move_down(self):
        """Move down"""
        self.move('DOWN')

    def move_left(self):
        """Move left"""
        self.move('LEFT')

    def move_right(self):
        """Move right"""
        self.move('RIGHT')

    def update_sprite_position(self):
        """Update the sprite's position on the screen"""
        x, y = self.__position
        # Update the rect to move the sprite
        self.chef_rect.topleft = (x * Config.get('GRID_SIZE'), y * Config.get('GRID_SIZE'))
        # Clear the previous screen and draw the new sprite

        self.screen.blit(self.chef_sprite, self.chef_rect)
        pg.display.flip()

    def get_position(self):
        """Get the current position of the chef"""
        return self.__position

    def set_screen(self, screen):
        self.screen = screen
