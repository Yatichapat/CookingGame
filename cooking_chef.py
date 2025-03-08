import pygame as pg
from cooking_config import Config


class Chef:
    def __init__(self):
        self.__position = (Config.get('WIN_SIZE_W') // 2, Config.get('WIN_SIZE_H') // 2)  # Starting position at center

        self.__walk_images = []
        self.__idle_images = []  # To store idle images
        self.current_frame = 0
        self.add_walk_images()
        self.add_idle_images()  # Add idle images

        self.chef_sprite = self.__idle_images[self.current_frame]  # Default to idle sprite
        self.chef_rect = self.chef_sprite.get_rect()
        self.chef_rect.center = self.__position

        self.speed = 4

        self.movement = {'UP': False, 'DOWN': False, 'LEFT': False, 'RIGHT': False}
        self.screen = None
        self.facing_left = None

    def draw(self):
        if self.screen:
            self.screen.blit(self.chef_sprite, self.chef_rect)

    def add_walk_images(self):
        """Add walking images for animation"""
        for i in range(1, 16):
            image = pg.image.load(f"images/Walk ({i}).png")
            image = pg.transform.scale(image, (Config.get('CHARACTER_SIZE'), Config.get('CHARACTER_SIZE')))
            self.__walk_images.append(image)

    def add_idle_images(self):
        """Add idle images for standing still animation"""
        for i in range(1, 6):  # Assuming there are 5 idle frames
            image = pg.image.load(f"images/Idle ({i}).png")
            image = pg.transform.scale(image, (Config.get('CHARACTER_SIZE'), Config.get('CHARACTER_SIZE')))
            self.__idle_images.append(image)

    def move(self):
        # Update the animation based on movement
        if self.movement['UP']:
            self.chef_rect.y -= self.speed
            self.update_sprite(self.__walk_images, flip=self.facing_left)

        elif self.movement['DOWN']:
            self.chef_rect.y += self.speed
            self.update_sprite(self.__walk_images, flip=self.facing_left)

        elif self.movement['LEFT']:
            self.chef_rect.x -= self.speed
            self.update_sprite(self.__walk_images, flip=True)
            self.facing_left = True

        elif self.movement['RIGHT']:
            self.chef_rect.x += self.speed
            self.update_sprite(self.__walk_images)
            self.facing_left = False

        else:
            # If no movement, use the idle animation
            self.update_sprite(self.__idle_images, flip=self.facing_left)

    def update_sprite(self, sprite_list, flip=False):
        """Update the sprite animation"""
        self.current_frame = (self.current_frame + 1) % len(sprite_list)
        sprite = sprite_list[self.current_frame]

        if flip:
            self.chef_sprite = pg.transform.flip(sprite, True, False)
        else:
            self.chef_sprite = sprite

    def animate_walk(self):
        """Animate walking by cycling through frames"""
        self.current_frame = (self.current_frame + 1) % len(self.__walk_images)
        self.chef_sprite = self.__walk_images[self.current_frame]

    def update_sprite_position(self):
        if self.screen:
            self.screen.blit(self.chef_sprite, self.chef_rect)

    def get_position(self):
        """Get the current position of the chef"""
        return self.__position

    def set_screen(self, screen):
        self.screen = screen
