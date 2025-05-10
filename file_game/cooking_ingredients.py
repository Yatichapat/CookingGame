from file_game.cooking_config import Config


class Ingredients:
    def __init__(self, x, y, ingredient_type):
        self.__position = (x, y)
        self.__ingredient_type = ingredient_type
        self.images = Config.get_image(ingredient_type)
        self.__time_used = 0

    def get_position(self):
        return self.__position

    def set_position(self, position):
        self.__position = position

    def draw(self, screen):
        """Draw ingredient at its default position."""
        self.draw_at(screen, self.__position[0] * Config.get_config('GRID_SIZE_W'),
                     self.__position[1] * Config.get_config('GRID_SIZE_H'))

    def get_type(self):
        return self.__ingredient_type

    def set_type(self, ingredient_type):
        self.__ingredient_type = ingredient_type
        self.images = Config.get_image(ingredient_type)

    def draw_at(self, screen, x, y):
        """Draw ingredient at a specific position (e.g., inside the fridge)."""
        screen.blit(self.images, (x, y))  # Directly use self.__image to draw

    def increment_usage(self):
        self.__time_used += 1
        return self.__time_used

    def get_usage_count(self):
        return self.__time_used
