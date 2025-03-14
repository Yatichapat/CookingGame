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
            "lamb": pg.transform.scale(pg.image.load("images/simply cooked/Raw food/lamb3.png"),
                                       (Config.get('GRID_SIZE_W') * 2, Config.get('GRID_SIZE_W') * 2)),
            "lamb_cooked": pg.transform.scale(pg.image.load("images/simply cooked/Cooked food/lamb1.png"),
                                              (Config.get('GRID_SIZE_W') * 2, Config.get('GRID_SIZE_W') * 2)),
            "bread": pg.transform.scale(pg.image.load("images/simply cooked/Cooked food/bread1.png"),
                                        (Config.get('GRID_SIZE_W') * 2, Config.get('GRID_SIZE_W') * 2)),
            "leek": pg.transform.scale(pg.image.load("images/FarmVeggies/Leek.png"),
                                       (Config.get('GRID_SIZE_W') * 2, Config.get('GRID_SIZE_W') * 2)),

            "egg": pg.transform.scale(pg.image.load("images/simply cooked/Raw food/egg3.png"),
                                      (Config.get('GRID_SIZE_W') * 2, Config.get('GRID_SIZE_W') * 2)),
            "egg_fried": pg.transform.scale(pg.image.load("images/simply cooked/Cooked food/egg1.png"),
                                        (Config.get('GRID_SIZE_W') * 2, Config.get('GRID_SIZE_W') * 2)),

            "chicken": pg.transform.scale(pg.image.load("images/simply cooked/Raw food/chiken3.png"),
                                        (Config.get('GRID_SIZE_W') * 2, Config.get('GRID_SIZE_W') * 2)),
            "chicken_cooked": pg.transform.scale(pg.image.load("images/simply cooked/Raw food/chiken3.png"),
                                        (Config.get('GRID_SIZE_W') * 2, Config.get('GRID_SIZE_W') * 2)),

            "sandwich": pg.transform.scale(pg.image.load("images/simply cooked/Cooked food/sandwich1.png"),
                                        (Config.get('GRID_SIZE_W') * 2, Config.get('GRID_SIZE_W') * 2)),


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

    def get_type(self):
        return self.__ingredient_type

    def set_type(self, ingredient_type):
        self.__ingredient_type = ingredient_type
        self.images = self.load_image(ingredient_type)

    def draw_at(self, screen, x, y):
        """Draw ingredient at a specific position (e.g., inside the fridge)."""
        screen.blit(self.images, (x, y))  # Directly use self.__image to draw

class Menu:
    def __init__(self, menu_type):
        self.__menu = [
            Ingredients(10, 10, "sandwich"),
            Ingredients(4, 10, "egg_fried"),
            Ingredients(5, 10, "chicken_cooked")
        ]
        self.__menu_type = menu_type

    def get_type(self):
        return self.__menu_type

    def draw(self, screen):
        for ingredient in self.__menu:
            ingredient.draw(screen)
