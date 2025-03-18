import pygame as pg
from cooking_config import Config


class Countertop:
    def __init__(self, x, y, width=300, height=60):
        self.rect = pg.Rect(x, y, width, height)  # Countertop position and size
        self.color = Config.get_config('BROWN')  # Color of the countertop (use a brown shade)
        self.texture_image = None  # Optional texture for countertop (if you want to use an image)

    def set_texture(self, texture_image_path):
        """Optional: Set a texture image for the countertop."""
        self.texture_image = pg.image.load(texture_image_path)
        self.texture_image = pg.transform.scale(self.texture_image, (self.rect.width, self.rect.height))

    def draw(self, screen):
        """Draw the countertop on the screen."""
        if self.texture_image:
            screen.blit(self.texture_image, self.rect.topleft)  # Draw the texture
        else:
            pg.draw.rect(screen, self.color, self.rect)  # Draw a solid color if no texture image

        # Optional: Add a border or details to make it look more realistic
        pg.draw.rect(screen, (0, 0, 0), self.rect, 3)  # Draw a black border around the countertop


# Usage
pg.init()

# Set up the screen
screen = pg.display.set_mode((800, 600))
pg.display.set_caption("Kitchen Countertop Example")

# Create the countertop object
countertop = Countertop(100, 300, 400, 80)
countertop.set_texture("images/countertop_texture.png")  # Optional: Use a texture image

# Game loop to draw the countertop
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Fill the screen with a background color
    screen.fill((255, 255, 255))  # White background

    # Draw the countertop
    countertop.draw(screen)

    # Update the screen
    pg.display.flip()

# Quit pygame
pg.quit()
