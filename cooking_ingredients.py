from cooking_config import Config
import pygame as pg


class Ingredients:
    def __init__(self, x, y, ingredient_type):
        self.__position = (x, y)
        self.__ingredient_type = ingredient_type
        self.images = self.load_image(ingredient_type)

    def load_image(self, ingredient_type):
        """Loads the image for the ingredient based on its type."""
        image_map = {
            "pork": pg.transform.scale(pg.image.load("images/simply cooked/Raw food/pork3.png"),
                                       (Config.get('GRID_SIZE_W') * 2, Config.get('GRID_SIZE_W') * 2)),
            "bread": pg.transform.scale(pg.image.load("images/simply cooked/Cooked food/bread1.png"),
                                       (Config.get('GRID_SIZE_W') * 2, Config.get('GRID_SIZE_W') * 2)),
            "leek": pg.transform.scale(pg.image.load("images/FarmVeggies/Leek.png"),
                                       (Config.get('GRID_SIZE_W') * 2, Config.get('GRID_SIZE_W') * 2))

        }
        return image_map.get(ingredient_type, pg.Surface((50, 50)))

    def get_position(self):
        return self.__position

    def set_position(self, position):
        self.__position = position

    def draw(self, screen):
        """Draw ingredient at its default position."""
        self.draw_at(screen, self.__position[0] * Config.get('GRID_SIZE_W'),
                     self.__position[1] * Config.get('GRID_SIZE_H'))

    def draw_at(self, screen, x, y):
        """Draw ingredient at a specific position (e.g., inside the fridge)."""
        screen.blit(self.images, (x, y))  # Directly use self.__image to draw

class Menu:
    def __init__(self):
        self.__ingredients = [
            Ingredients(10, 10, "pork"),
            Ingredients(4, 10, "bread"),
            Ingredients(6, 10, "leek")
        ]

    def draw(self, screen):
        for ingredient in self.__ingredients:
            ingredient.draw(screen)


class Fridge:
    def __init__(self, x, y, chef):
        self.__x = x
        self.__y = y
        chef_x, chef_y = chef.get_position()
        self.__position = (self.__x, self.__y)
        self.__ingredients = [
            Ingredients(2, 10, "pork"),
            Ingredients(2, 4, "bread"),
            Ingredients(2, 8, "leek")
        ]
        self.is_open = False
        self.__dropped_ingredients = []
        self.__select_index = 0

    def toggle_fridge(self, chef):
        """Opens or closes the fridge."""
        fridge_x, fridge_y = self.__position
        chef_x, chef_y = chef.get_position()

        distance = abs(fridge_x - chef_x) + abs(fridge_y - chef_y)

        if distance <= 200:
            self.is_open = not self.is_open

    def move_selection(self, direction):
        """Moves selection up/down in the fridge."""
        if self.is_open:
            if direction == "UP":
                self.__select_index = (self.__select_index - 1) % len(self.__ingredients)
            elif direction == "DOWN":
                self.__select_index = (self.__select_index + 1) % len(self.__ingredients)

    def add_dropped_ingredient(self, ingredient):
        self.__dropped_ingredients.append(ingredient)

    def pick_ingredient(self):
        """Returns the currently selected ingredient for pickup."""
        if self.is_open and self.__ingredients:
            ingredient = self.__ingredients.pop(self.__select_index)
            if self.__select_index >= len(self.__ingredients):
                self.__select_index = len(self.__ingredients)
            return ingredient
        return None

    def put_ingredient_in_fridge(self, ingredient):
        """Puts the ingredient back into the fridge."""
        if self.is_open:
            self.__ingredients.append(ingredient)  # Add the ingredient back to the fridge
            ingredient.set_position(self.__position)

    def draw(self, screen):
        """Draws the fridge and its ingredients if open."""
        fridge_rect = pg.Rect(30, 30, 50, 90)  # Example fridge size
        pg.draw.rect(screen, Config.get('GRAY'), fridge_rect)  # Fridge background

        if self.is_open:
            for i, ingredient in enumerate(self.__ingredients):
                ingredient_x = 70 + (i * Config.get('GRID_SIZE_H') * 1.5)
                ingredient_y = 60
                ingredient.draw_at(screen, ingredient_x, ingredient_y)

        for ingredient in self.__dropped_ingredients:
            ingredient.draw_at(screen, ingredient.get_position()[0] * Config.get('GRID_SIZE_W'),
                               ingredient.get_position()[1] * Config.get('GRID_SIZE_H'))

