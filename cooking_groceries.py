import pygame as pg
import random
from cooking_config import Config
from cooking_ingredients import Ingredients


class Groceries:
    def __init__(self, screen):
        self.__screen = screen
        self.__active_bag = None
        self.__bag_carried = False
        self.__bag_spawn = False

        # Load images with error handling
        try:
            self.__button_img = pg.image.load(Config.get_config('red button')).convert_alpha()
            self.__button_img = pg.transform.scale(self.__button_img, (100, 100))
        except:
            print("Error loading button image - creating placeholder")
            self.__button_img = pg.Surface((100, 100))
            self.__button_img.fill((255, 0, 0))  # Red placeholder

        try:
            self.__bag_img = pg.image.load(Config.get_config('paper bag')).convert_alpha()
            self.__bag_img = pg.transform.scale(self.__bag_img, (60, 80))  # Smaller for carrying
        except:
            print("Error loading bag image - creating placeholder")
            self.__bag_img = pg.Surface((60, 80))
            self.__bag_img.fill((200, 150, 100))  # Brown placeholder

        self.button_rect = pg.Rect(915, 300, 100, 100)

    def spawn_bag(self):
        """Create a new grocery bag at specified position"""
        if not self.__active_bag and not self.__bag_carried:
            self.__active_bag = {
                'rect': pg.Rect(self.button_rect.x + 20,  # Position right of button
                                self.button_rect.y - 50, 60, 80),
                'image': self.__bag_img,
                'contents': self.generate_contents()
            }
            self.__bag_spawn = True

    def draw_red_button(self):
        """Draw the red button on screen"""
        self.__screen.blit(self.__button_img, self.button_rect)

    def generate_contents(self):
        groceries = ["lamb", "bread", "egg", "chicken", "tomato", "lettuce", "cheese", "pork", "fish"]
        return groceries

    def draw_bag(self):
        """Draw the bag at its position or carried by chef"""
        if self.__active_bag and not self.__bag_carried:
            self.__screen.blit(self.__active_bag['image'],
                               self.__active_bag['rect'])

    def pick_up_bag(self, chef_pos):
        """Check if chef can pick up the bag"""
        if self.__active_bag and not self.__bag_carried:
            bag_center = (
                self.__active_bag['rect'].x + self.__active_bag['rect'].width // 2,
                self.__active_bag['rect'].y + self.__active_bag['rect'].height // 2
            )
            distance = ((chef_pos[0] - bag_center[0]) ** 2 +
                        (chef_pos[1] - bag_center[1]) ** 2) ** 0.5
            if distance < 100:  # Within pickup range
                self.__bag_carried = True
                return True
        return False

    def drop_bag(self, x, y):
        """Drop the bag at specified position with contents"""
        if self.__bag_carried:
            self.__active_bag = {
                'rect': pg.Rect(x, y, 60, 80),
                'image': self.__bag_img,
                'contents': self.__active_bag['contents']  # Keep the same contents
            }
            self.__bag_carried = False
            return True
        return False

    def release_at_fridge(self, fridge_pos, fridge):
        """Release ingredients when bag reaches fridge"""
        if not self.__bag_carried or not self.__active_bag:
            return []

        # Add each grocery item to the fridge
        for item in self.__active_bag['contents']:
            # Create ingredient and add to fridge
            fridge.put_ingredient_in_fridge(Ingredients(0, 0, item))

        # Play sound effect when adding to fridge
        try:
            Config.get_sound("fridge_door").play()
        except:
            pass  # If sound doesn't exist, ignore

        self.__bag_carried = False
        self.__active_bag = None
        return []

    def get_bag_position(self):
        """Get current bag position (world or carried)"""
        if self.__bag_carried:
            return None  # Position is handled by chef when carried
        if self.__active_bag:
            return (self.__active_bag['rect'].x, self.__active_bag['rect'].y)
        return None

    def get_red_button_position(self):
        """Get the position of the red button"""
        return self.button_rect.topleft

    def has_active_bag(self):
        return self.__active_bag is not None

    def is_bag_carried(self):
        return self.__bag_carried

    def get_bag_image(self):
        return self.__bag_img
