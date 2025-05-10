from file_game.cooking_config import Config
from file_game.cooking_ingredients import Ingredients
from file_game.cooking_menu import Menu
import pygame as pg
import os
import csv
from datetime import datetime


class Fridge:
    def __init__(self, x, y, chef):
        self.__position = (x, y)
        self.__ingredients = {}
        self.__selected_ingredient = None

        self.is_open = False
        self.__dropped_ingredients = []
        self.__select_index = 0
        self.__usage_data = []  # Stores ingredient usage records
        self.__csv_file = "game_data/ingredient_used.csv"
        self.__initialize_csv()
        self.__session_id = self.__get_next_session_id()

    def __initialize_csv(self):
        """Create CSV file with headers if it doesn't exist"""
        if not os.path.exists(self.__csv_file):
            with open(self.__csv_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["session_id", "id",
                                "timestamp", "ingredient", "action", "quantity"])

    def __record_usage(self, ingredient, action, quantity=1):
        """Record ingredient usage to memory and CSV"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        record = {
            "session_id": self.__session_id,
            "id": len(self.__usage_data) + 1,
            "timestamp": timestamp,
            "ingredient": ingredient,
            "action": action,  # "Taken" or "Returned"
            "quantity": quantity
        }

        self.__usage_data.append(record)

        # Append to CSV file
        with open(self.__csv_file, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=record.keys())
            writer.writerow(record)

    def reset(self):
        """Reset fridge to initial state and create new session"""
        self.is_open = False
        self.__select_index = 0
        self.__ingredients.clear()
        self.__session_id = self.__get_next_session_id()

        ingredients_to_add = [
            ("lamb", 1),
            ("bread", 1),
            ("leek", 1),
            ("egg", 1),
            ("chicken", 1),
            ("lettuce", 1),
            ("tomato", 1),
            ("cheese", 1),
            ("fish", 1),
            ("pork", 1)
        ]

        for ingredient_type, quantity in ingredients_to_add:
            if quantity > 0:
                self.__ingredients[ingredient_type] = quantity

    def toggle_fridge(self, chef):
        """Opens or closes the fridge."""
        fridge_x, fridge_y = self.__position
        chef_x, chef_y = chef.get_position()

        distance = abs(fridge_x - chef_x) + abs(fridge_y - chef_y)

        if distance <= 200:
            self.is_open = not self.is_open

        if not self.is_open:
            chef._update_movement_from_states()

    def move_selection(self, direction):
        """Moves selection up/down in the fridge."""
        if self.is_open:
            if direction == "LEFT":
                self.__select_index = (self.__select_index - 1) % len(self.__ingredients)
            elif direction == "RIGHT":
                self.__select_index = (self.__select_index + 1) % len(self.__ingredients)
            elif direction == 'UP':
                self.__select_index = (self.__select_index - 4) % len(self.__ingredients)
            elif direction == 'DOWN':
                self.__select_index = (self.__select_index + 4) % len(self.__ingredients)

    def add_dropped_ingredient(self, ingredient):
        self.__dropped_ingredients.append(ingredient)

    def pick_ingredient(self):
        """Returns the currently selected ingredient for pickup."""
        if self.is_open and self.__ingredients:
            # Get a list of the ingredient types
            ingredient_types = list(self.__ingredients.keys())

            # Make sure the select index is valid
            if self.__select_index >= len(ingredient_types):
                self.__select_index = len(ingredient_types) - 1

            # Get the ingredient type at the current selection
            if self.__select_index >= 0 and self.__select_index < len(ingredient_types):
                ingredient_type = ingredient_types[self.__select_index]

                # Decrement the quantity
                self.__ingredients[ingredient_type] -= 1

                # If quantity reaches zero, remove the ingredient type
                if self.__ingredients[ingredient_type] <= 0:
                    del self.__ingredients[ingredient_type]

                # Record usage and create a new ingredient to return
                self.__record_usage(ingredient_type, "Taken")
                return Ingredients(*self.__position, ingredient_type)

        return None

    def put_ingredient_in_fridge(self, ingredient):
        """Add ingredient to fridge with quantity tracking"""
        ingredient_type = ingredient.get_type()
        if ingredient_type in self.__ingredients:
            # Increment quantity if ingredient already exists
            self.__ingredients[ingredient_type] += 1
        else:
            # Add new ingredient with quantity 1
            self.__ingredients[ingredient_type] = 1
            # Set position to the corner of the screen
            corner_position = (10, 10)  # Top-left corner with a small margin
            ingredient.set_position(corner_position)

    def draw(self, screen):
        """Draws the fridge and its ingredients if open."""
        fridge_x, fridge_y = self.__position
        fridge_image = pg.image.load("images/fridge.png")
        fridge_image = pg.transform.scale(fridge_image, (150, 150))
        screen.blit(fridge_image, (fridge_x, fridge_y))

        if self.is_open:
            # Start positions in the corner
            x_start = 10  # Left margin
            y_start = 10  # Top margin

            x_offset = x_start
            y_offset = y_start

            # Maximum items per row
            items_per_row = 4
            item_count = 0

            ingredient_types = list(self.__ingredients.keys())

            for i, ingredient_type in enumerate(ingredient_types):
                quantity = self.__ingredients[ingredient_type]

                # Calculate position for current ingredient
                current_x = x_start + (i % items_per_row) * 50
                current_y = y_start + (i // items_per_row) * 50

                # Create a temporary ingredient for display
                example_ingredient = Ingredients(
                    current_x, current_y, ingredient_type
                )

                # Draw the ingredient icon
                example_ingredient.draw_at(screen, current_x, current_y)

                # Draw quantity next to it
                font = pg.font.SysFont('Arial', 18, bold=True)
                quantity_text = font.render(f"x{quantity}", True, Config.get_config("BLACK"))
                screen.blit(quantity_text, (current_x + 30, current_y + 5))

                # Draw highlight rectangle for selected ingredient
                if i == self.__select_index:
                    highlight_rect = pg.Rect(
                        current_x, current_y,
                        Config.get_config('GRID_SIZE_W') + 15, Config.get_config('GRID_SIZE_W') + 15
                    )
                    pg.draw.rect(screen, (0, 0, 0), highlight_rect, 3)

    def get_position(self):
        """Returns the position of the fridge."""
        return self.__position

    def __get_next_session_id(self):
        if not os.path.exists(self.__csv_file):
            return 1

        session_ids = []
        with open(self.__csv_file, 'r') as file:
            reader = csv.DictReader(file)  # <-- This ensures rows are dictionaries
            for row in reader:
                sid = row.get('session_id', '').strip()
                if sid.isdigit():
                    session_ids.append(int(sid))

        return max(session_ids, default=0) + 1


class Equipments:
    def __init__(self, x, y, image_path):
        self.__position = (x, y)
        self.__ingredients = []
        self.__image_path = image_path

        # Tracking cooking sound
        self.__is_cooking = False
        self.__cooking_sound_playing = False


    def clear(self):
        return self.__ingredients.clear()

    def add_ingredient(self, ingredient):
        """Adds an ingredient to the cooking tool and starts the timer."""
        start_time = pg.time.get_ticks()  # Start time when the ingredient is added
        self.__ingredients.append([ingredient, start_time, False])

    def cook_ingredients(self):
        """Cooks ingredients based on real-time duration."""
        transformed_items = []
        current_time = pg.time.get_ticks()
        new_ingredients = []

        # Check if there are ingredients being cooked
        self.__is_cooking = any(
            ingredient_data[0].get_type() in ["egg", "lamb", "chicken", "chicken sliced", "fish", "pork"]
            for ingredient_data in self.__ingredients
        )

        # Handle cooking sound
        if self.__is_cooking:
            if not self.__cooking_sound_playing:
                Config.get_sound('pan_cooking').play(-1)  # -1 for looping
                self.__cooking_sound_playing = True
        else:
            if self.__cooking_sound_playing:
                Config.get_sound('pan_cooking').stop()
                self.__cooking_sound_playing = False

        for ingredient_data in self.__ingredients:
            # Safely unpack the data regardless of length
            ingredient = ingredient_data[0]
            start_time = ingredient_data[1]
            sound_played = ingredient_data[2] if len(ingredient_data) >= 3 else False
            elapsed_time = (current_time - start_time) / 1000
            transformed = None

            # FRYING LOGIC (primarily for Pan)
            if isinstance(self, Pan):
                # Check if this ingredient is newly transformed and needs sound
                newly_transformed = False
                self.__is_cooking = True

                if ingredient.get_type() == "egg" and elapsed_time >= 0:
                    transformed = Ingredients(*ingredient.get_position(), "egg fried")
                    newly_transformed = True
                elif ingredient.get_type() == "lamb" and elapsed_time >= 8:
                    transformed = Ingredients(*ingredient.get_position(), "lamb fried")
                    newly_transformed = True
                elif ingredient.get_type() == "chicken" and elapsed_time >= 8:
                    transformed = Ingredients(*ingredient.get_position(), "chicken fried")
                    newly_transformed = True
                elif ingredient.get_type() == "chicken sliced" and elapsed_time >= 8:
                    transformed = Ingredients(*ingredient.get_position(), "chicken drumstick fried")
                    newly_transformed = True
                elif ingredient.get_type() == "fish" and elapsed_time >= 8:
                    transformed = Ingredients(*ingredient.get_position(), "fish fried")
                    newly_transformed = True
                elif ingredient.get_type() == "pork" and elapsed_time >= 8:
                    transformed = Ingredients(*ingredient.get_position(), "pork fried")
                    newly_transformed = True

                # Play sound only if newly transformed and sound not played yet
                if newly_transformed and not sound_played:
                    Config.get_sound("finish_cooking").play()
                    sound_played = True

            # SLICING LOGIC (primarily for CuttingBoard)
            elif isinstance(self, CuttingBoard):
                if ingredient.get_type() == "tomato" and elapsed_time >= 0:
                    Config.get_sound("cutting").play()
                    transformed = Ingredients(*ingredient.get_position(), "tomato sliced")
                elif ingredient.get_type() == "lettuce" and elapsed_time >= 0:
                    Config.get_sound("cutting").play()
                    transformed = Ingredients(*ingredient.get_position(), "lettuce sliced")
                elif ingredient.get_type() == "cheese" and elapsed_time >= 0:
                    Config.get_sound("cutting").play()
                    transformed = Ingredients(*ingredient.get_position(), "cheese sliced")
                elif ingredient.get_type() == "chicken" and elapsed_time >= 0:
                    Config.get_sound("cutting").play()
                    transformed = Ingredients(*ingredient.get_position(), "chicken sliced")
                elif ingredient.get_type() == "bread" and elapsed_time >= 0:
                    Config.get_sound("cutting").play()
                    transformed = Ingredients(*ingredient.get_position(), "bread sliced")
                elif ingredient.get_type() == "chicken to slice" and elapsed_time >= 0:
                    Config.get_sound("cutting").play()
                    transformed = Ingredients(*ingredient.get_position(), "chicken sliced")

            if transformed:
                transformed_items.append((ingredient, transformed))
                new_ingredients.append([transformed, start_time, True])  # Mark sound as played
            else:
                new_ingredients.append([ingredient, start_time, sound_played])

        self.__ingredients = new_ingredients

    def get_cooked_ingredients(self):
        """Returns cooked ingredients and removes them from the tool."""
        for item in self.__ingredients[:]:
            ingredient = item[0]  # Access the first element directly
            if "cooked" in ingredient.get_type() or "fried" in ingredient.get_type():
                self.__ingredients.remove(item)  # Remove from the pan
                # Check if no more ingredients are being cooked
                if not any(
                        i[0].get_type() in ["egg", "lamb", "chicken", "chicken sliced", "fish", "pork"]
                        for i in self.__ingredients):
                    self.__is_cooking = False
                    if self.__cooking_sound_playing:
                        Config.get_sound('pan_cooking').stop()
                        self.__cooking_sound_playing = False
                return ingredient  # Return only one ingredient

            if "sliced" in ingredient.get_type():
                self.__ingredients.remove(item)  # Remove from the cutting board
                return ingredient
        return None

    def is_ready_to_pick(self):
        """Checks if all ingredients are cooked and ready to be picked."""
        for item in self.__ingredients:
            ingredient = item[0]  # Access the first element directly
            if ingredient.get_type() in ["egg", "lamb", "chicken"]:
                return False
        return True

    def take_tool(self):
        """Picks up cooked ingredients but keeps the pan in place."""
        cooked_food = self.get_cooked_ingredients()
        return cooked_food if cooked_food else None

    def draw(self, screen):
        """Draws the tool and its ingredients."""
        tool_x, tool_y = self.__position
        tool_image = pg.image.load(self.__image_path)
        tool_image = pg.transform.scale(tool_image, (90, 90))
        screen.blit(tool_image, (tool_x, tool_y))

        # Draw all ingredients on the tool
        for ingredient_data in self.__ingredients:
            ingredient = ingredient_data[0]
            start_time = ingredient_data[1]
            ingredient.draw_at(screen, tool_x + 14, tool_y + 25)

            if not isinstance(self, CuttingBoard):
                current_time = pg.time.get_ticks()
                elapsed_time = (current_time - start_time) / 1000

                ingredient_type = ingredient.get_type()
                total_time = 0
                if ingredient_type == "egg":
                    total_time = 0
                elif ingredient_type in ["lamb", "chicken", "chicken sliced", "fish", "pork"]:
                    total_time = 8
                else:
                    continue

                progress = min(max(elapsed_time / total_time, 0), 1)

                # Bar background (red)
                pg.draw.rect(screen, Config.get_config("RED"), (tool_x + 7, tool_y, 50, 5), border_radius=3)

                # Bar progress (green)
                pg.draw.rect(screen, Config.get_config("GREEN"), (tool_x + 7, tool_y, 50 * progress, 5),
                             border_radius=3)

    def set_position(self, new_position):
        self.__position = new_position

    def get_position(self):
        return self.__position


class Pan(Equipments):
    def __init__(self, x, y):
        super().__init__(x, y, "images/pan.png")

    def fry_ingredients(self):
        return self.cook_ingredients()  # Adjust frying logic if needed

    def put_ingredient_in_pan(self, ingredient):
        self.add_ingredient(ingredient)


class CuttingBoard(Equipments):
    def __init__(self, x, y):
        super().__init__(x, y, "images/cutting.png")

    def put_ingredient_in_cutting_board(self, ingredient):
        self.add_ingredient(ingredient)

    def cut_ingredients(self):
        return self.cook_ingredients()


class Plate:
    def __init__(self, x, y):
        self.__position = (x, y)
        self.__ingredients = []  # List to store ingredients on the plate

    def clear(self):
        return self.__ingredients.clear()

    def add_ingredient(self, ingredient):
        """Add an ingredient to the plate."""
        if len(self.__ingredients) < 5:  # Limit the number of ingredients on the plate
            self.__ingredients.append(ingredient)
            self.check_and_transform()
            return True  # Ingredient added successfully
        else:
            return False  # Plate is full

    def remove_ingredient(self):
        """Remove and return the last ingredient added to the plate."""
        if self.__ingredients:
            return self.__ingredients.pop()
        return None

    def is_complete_menu(self):
        """Check if the plate contains a complete dish (e.g., sandwich)."""
        sandwich_required = {"bread sliced", "cheese sliced", "lettuce sliced", "tomato sliced"}
        ingredient_types = {ingredient.get_type() for ingredient in self.__ingredients}
        return sandwich_required.issubset(ingredient_types)

    def check_and_transform(self):
        """Check if the plate contains a complete dish and transform it."""
        if self.is_complete_menu():
            self.__ingredients.clear()
            sandwich = Ingredients(*self.__position, "sandwich")
            self.__ingredients.append(sandwich)

    def get_position(self):
        """Get the position of the plate."""
        return self.__position

    def draw(self, screen):
        """Draw the plate and its ingredients on the screen."""
        plate_x, plate_y = self.__position
        plate_image = pg.image.load("images/plate.png")
        plate_image = pg.transform.scale(plate_image, (80, 80))  # Plate size
        screen.blit(plate_image, (plate_x, plate_y))

        # Draw ingredients on the plate in a grid-like layout
        for i, ingredient in enumerate(self.__ingredients):
            row = i // 2  # Two ingredients per row
            col = i % 2
            ingredient_x = plate_x + 20  # Adjust spacing as needed
            ingredient_y = plate_y + 10 + row
            screen.blit(ingredient.images, (ingredient_x, ingredient_y))

    def pick_up_plate(self):
        if not self.__ingredients:  # Don't pick up empty plates
            return None

        new_plate = Plate(*self.__position)
        new_plate.__ingredients = self.__ingredients.copy()
        self.__ingredients.clear()  # Clear the original plate
        return new_plate

    def set_position(self, position):
        """Set the position of the plate."""
        self.__position = position

    def get_ingredients(self):
        """Get the list of ingredients on the plate."""
        return self.__ingredients

    def draw_at(self, screen, x, y):
        """Draw the plate and its ingredients at the specified position."""
        # Temporarily store the original position
        original_position = self.__position
        # Update position for drawing
        self.__position = (x, y)
        # Use the existing draw method
        self.draw(screen)
        # Restore the original position
        self.__position = original_position

class TrashBin:
    def __init__(self, x, y):
        self.__position = (x, y)
        self.__menu = Menu()
        self.__image = pg.image.load("images/trashbin.png")
        self.__image = pg.transform.scale(self.__image, (100, 100))
        self.__throw = []

    def draw(self, screen):
        screen.blit(self.__image, self.__position)

    def get_position(self):
        return self.__position

    def throw_into_bin(self, ingredient):
        """Throw an ingredient into the trash bin."""
        self.__throw.append(ingredient.get_type())
        Config.get_sound("trash").play()
        self.__menu.log_mistake("throw away", f"served: {ingredient.get_type()}")
