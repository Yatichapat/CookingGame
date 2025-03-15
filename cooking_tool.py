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
        return None

    def put_ingredient_in_fridge(self, ingredient):
        """Puts the ingredient back into the fridge."""
        if self.is_open:
            self.__ingredients.append(ingredient)  # Add the ingredient back to the fridge
            ingredient.set_position(self.__position)

    def draw(self, screen):
        """Draws the fridge and its ingredients if open."""
        fridge_x, fridge_y = self.__position
        fridge_image = pg.image.load("images/fridge.png")
        fridge_image = pg.transform.scale(fridge_image, (150, 150))
        screen.blit(fridge_image, (fridge_x, fridge_y))

        if self.is_open:
            for i, ingredient in enumerate(self.__ingredients):
                ingredient_x = 70 + (i * Config.get_config('GRID_SIZE_H') * 1.5)
                ingredient_y = 60
                ingredient.draw_at(screen, ingredient_x, ingredient_y)

                if i == self.__select_index:
                    highlight_rect = pg.Rect(
                        ingredient_x + 5, ingredient_y + 5,
                        Config.get_config('GRID_SIZE_W') + 15, Config.get_config('GRID_SIZE_W') + 15
                    )
                    pg.draw.rect(screen, (0, 0, 0), highlight_rect, 3)

        for ingredient in self.__dropped_ingredients:
            ingredient.draw_at(screen, ingredient.get_position()[0] * Config.get_config('GRID_SIZE_W'),
                               ingredient.get_position()[1] * Config.get_config('GRID_SIZE_H'))


class Tools:
    def __init__(self, x, y, image_path):
        self.__position = (x, y)
        self.__ingredients = []  # List of (ingredient, start_time)
        self.__image_path = image_path

    def add_ingredient(self, ingredient):
        """Adds an ingredient to the cooking tool and starts the timer."""
        start_time = pg.time.get_ticks()  # Start time when the ingredient is added
        self.__ingredients.append([ingredient, start_time])

    def cook_ingredients(self):
        """Cooks ingredients based on real-time duration."""
        transformed_items = []
        current_time = pg.time.get_ticks()  # Get the current time

        for i in range(len(self.__ingredients)):
            ingredient, start_time = self.__ingredients[i]
            elapsed_time = (current_time - start_time) / 1000  # Time cooked in seconds

            # Cooking transformations based on elapsed time
            if ingredient.get_type() == "egg":
                cooked_ingredient = Ingredients(*ingredient.get_position(), "egg_fried")
                self.__ingredients[i][0] = cooked_ingredient  # Replace the raw ingredient
                transformed_items.append((ingredient, cooked_ingredient))
                if elapsed_time >= 5:
                    print(f"Egg is ready! Cooked in {elapsed_time:.1f} seconds.")

            elif ingredient.get_type() == "lamb" and elapsed_time >= 8:
                cooked_ingredient = Ingredients(*ingredient.get_position(), "lamb_cooked")
                self.__ingredients[i][0] = cooked_ingredient
                transformed_items.append((ingredient, cooked_ingredient))
                print(f"Lamb is ready! Cooked in {elapsed_time:.1f} seconds.")

            elif ingredient.get_type() == "chicken" and elapsed_time >= 8:
                cooked_ingredient = Ingredients(*ingredient.get_position(), "chicken_cooked")
                self.__ingredients[i][0] = cooked_ingredient
                transformed_items.append((ingredient, cooked_ingredient))
                print(f"Chicken is ready! Cooked in {elapsed_time:.1f} seconds.")

        return transformed_items

    def get_cooked_ingredients(self):
        """Returns cooked ingredients and removes them from the tool."""
        cooked = []
        for item in self.__ingredients[:]:
            ingredient, _ = item
            if "_cooked" in ingredient.get_type() or "_fried" in ingredient.get_type():
                cooked.append(ingredient)
                self.__ingredients.remove(item)
        return cooked

    def is_ready_to_pick(self):
        """Checks if all ingredients are cooked and ready to be picked."""
        for ingredient, start_time in self.__ingredients:
            if ingredient.get_type() in ["egg", "lamb", "chicken"]:
                return False
        return True

    def take_tool(self):
        """Picks up the tool if all ingredients are cooked."""
        if self.is_ready_to_pick():
            cooked_food = [ingredient for ingredient, _ in self.__ingredients]
            self.__ingredients.clear()  # Clear the ingredients after taking them
            return cooked_food
        return None

    def draw(self, screen):
        """Draws the tool and its ingredients."""
        tool_x, tool_y = self.__position
        tool_image = pg.image.load(self.__image_path)
        tool_image = pg.transform.scale(tool_image, (90, 90))
        screen.blit(tool_image, (tool_x, tool_y))

        # Draw all ingredients on the tool
        for ingredient, _ in self.__ingredients:
            ingredient.draw_at(screen, tool_x + 14, tool_y + 25)

    def set_position(self, new_position):
        self.__position = new_position

    def get_position(self):
        return self.__position


class Pan(Tools):
    def __init__(self, x, y):
        super().__init__(x, y, "images/pan.png")

    def fry_ingredients(self):
        return self.cook_ingredients()  # Adjust frying logic if needed

    def put_ingredient_in_pan(self, ingredient):
        self.add_ingredient(ingredient)


class Pot(Tools):
    def __init__(self, x, y):
        super().__init__(x, y, "images/pot.png")

    def boil_ingredients(self):
        return self.cook_ingredients()  # Adjust boiling logic if needed

    def put_ingredient_in_pot(self, ingredient):
        self.add_ingredient(ingredient)


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