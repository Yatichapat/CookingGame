from cooking_config import Config
from cooking_ingredients import *
import pygame as pg


class Fridge:
    def __init__(self, x, y, chef):
        self.__x = x
        self.__y = y
        chef_x, chef_y = chef.get_position()
        self.__position = (self.__x, self.__y)
        self.__ingredients = [
            Ingredients(2, 10, "lamb"),
            Ingredients(2, 4, "bread"),
            Ingredients(2, 8, "leek"),
            Ingredients(2, 6, "egg"),
            Ingredients(4, 10, "chicken")
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
        elif self.__ingredients:
            ingredient = self.__ingredients
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

                if i == self.__select_index:
                    highlight_rect = pg.Rect(
                        ingredient_x + 5, ingredient_y + 5,
                        Config.get('GRID_SIZE_W') + 15, Config.get('GRID_SIZE_W') + 15
                    )
                    pg.draw.rect(screen, (0, 0, 0), highlight_rect, 3)

        for ingredient in self.__dropped_ingredients:
            ingredient.draw_at(screen, ingredient.get_position()[0] * Config.get('GRID_SIZE_W'),
                               ingredient.get_position()[1] * Config.get('GRID_SIZE_H'))


class Pan:
    def __init__(self, position=(500, 50)):
        self.__position = position
        self.__ingredients_on_pan = []

    def add_ingredient(self, ingredient):
        self.__ingredients_on_pan.append([ingredient, 0])

    def fry_ingredients(self):
        transformed_items = []
        """Cooks ingredients over time, transforming them if needed."""
        for i in range(len(self.__ingredients_on_pan)):  # Iterate by index
            ingredient, time_on_pan = self.__ingredients_on_pan[i]
            self.__ingredients_on_pan[i][1] += 1  # Increase cooking time

            # Transform egg → fried egg
            if ingredient.get_type() == "egg" and self.__ingredients_on_pan[i][1] >= 5:
                print("Fried egg is cooking!")
                fried_egg = Ingredients(*ingredient.get_position(), "egg_fried")
                self.__ingredients_on_pan[i][0] = fried_egg  # Update in-place
                transformed_items.append((ingredient, fried_egg))

            elif ingredient.get_type() == "lamb" and self.__ingredients_on_pan[i][1] >= 100:
                lamb_cooked = Ingredients(*ingredient.get_position(), "lamb_cooked")
                self.__ingredients_on_pan[i][0] = lamb_cooked
                transformed_items.append((ingredient, lamb_cooked))

            elif ingredient.get_type() == "chicken" and self.__ingredients_on_pan[i][1] >= 100:
                chicken_cooked = Ingredients(*ingredient.get_position(), "chicken_cooked")
                self.__ingredients_on_pan[i][0] = chicken_cooked
                transformed_items.append((ingredient, chicken_cooked))

            if self.__ingredients_on_pan[i][1] >= 200:
                print("Fried egg is ready!")

    def draw(self, screen):
        pan_x, pan_y = self.__position
        pan_image = pg.image.load("images/pan.png")
        pan_image = pg.transform.scale(pan_image, (90, 90))
        screen.blit(pan_image, (pan_x, pan_y))

        for ingredient, _ in self.__ingredients_on_pan:  # Fix unpacking
            ingredient.draw_at(screen, pan_x + 14, pan_y + 25)

    def get_ingredients_on_pan(self):
        return [item[0] for item in self.__ingredients_on_pan]

    def put_ingredient_in_pan(self, ingredient):
        self.add_ingredient(ingredient)

    def set_position(self, new_position):
        self.__position = new_position

    def get_position(self):
        return self.__position

    def get_cooked_ingredients(self):
        """Return cooked ingredients and remove them from the pan."""
        cooked = []

        for item in self.__ingredients_on_pan[:]:  # Iterate over a copy
            ingredient, time_on_pan = item
            if "_cooked" in ingredient.get_type() or "_fried" in ingredient.get_type():
                cooked.append(ingredient)
                self.__ingredients_on_pan.remove(item)

        return cooked


class Plate:
    def __init__(self, x, y):
        self.__position = (x, y)
        self.__ingredients = []

    def add_ingredient(self, ingredient):
        if len(self.__ingredients) < 3:
            self.__ingredients.append(ingredient)
        else:
            print("plate is full!")

    def remove_ingredient(self):
        if self.__ingredients:
            return self.__ingredients.pop()
        return None

    def is_complete_menu(self):
        if len(self.__ingredients) == 5:
            return (self.__ingredients[0].get_type() == "bread" and
                    self.__ingredients[1].get_type() == "cheese" and
                    self.__ingredients[2].get_type() == "lettuce" and
                    self.__ingredients[3].get_type() == "tomato" and
                    self.__ingredients[5].get_type() == "bread")
        return False

    def get_position(self):
        return self.__position

    def draw(self, screen):
        plate_x, plate_y = self.__position
        plate_image = pg.image.load("images/plate.png")
        plate_image = pg.transform.scale(plate_image, (80, 80))
        screen.blit(plate_image, (plate_x, plate_y))

    def set_position(self, position):
        self.__position = position

class Pot:
    def __init__(self, x, y):
        self.__position = (x, y)
