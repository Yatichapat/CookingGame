import pygame as pg
from cooking_config import Config
from cooking_chef import Chef
from cooking_zombie import Zombie
from cooking_ingredients import *
from cooking_tool import *


class GameApp:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Apocalypse Cooker')
        self.__screen = pg.display.set_mode((Config.get('WIN_SIZE_W'), Config.get('WIN_SIZE_H')))
        # self.__screen.fill(Config.get('WHITE'))

        self.__chef = Chef()

        self.__zombie = Zombie(pg.image.load("images/Zombie_1/Idle.png"))

        self.__fridge = Fridge(10, 10, self.__chef)
        self.__pan = Pan()
        self.__plate = Plate(600, 50)

        self.__chef.set_screen(self.__screen)
        self.__zombie.set_screen(self.__screen)
        self.__held_ingredient = None
        self.__dropped_ingredient = []

        self.__clock = pg.time.Clock()
        self.__running = True
        self.movement = {'UP': False, 'DOWN': False, 'LEFT': False, 'RIGHT': False}

    def handle_events(self):
        """Handle user input"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.__running = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.__fridge.toggle_fridge(self.__chef)

                elif self.__fridge.is_open:  # Fridge interactions
                    if event.key == pg.K_UP:
                        self.__fridge.move_selection("UP")
                    elif event.key == pg.K_DOWN:
                        self.__fridge.move_selection("DOWN")
                    elif event.key == pg.K_RETURN:  # Pick ingredient
                        if self.__held_ingredient is None:
                            self.__held_ingredient = self.__fridge.pick_ingredient()

                        elif self.__held_ingredient and self.__fridge.is_open:
                            self.__fridge.put_ingredient_in_fridge(self.__held_ingredient)
                            self.__held_ingredient = None

                elif event.key == pg.K_RETURN and self.__held_ingredient and self.__fridge.is_open is False:
                    if self.is_near_pan():
                        self.__pan.put_ingredient_in_pan(self.__held_ingredient)
                        self.__pan.fry_ingredients()
                        self.__held_ingredient = None
                    elif self.is_near_pan() and self.__held_ingredient is None:
                        cooked_ingredients = self.__pan.get_cooked_ingredients()
                        self.__held_ingredient = cooked_ingredients.pop()

                    else:
                        self.drop_food_to_the_world()

                elif event.key == pg.K_UP:
                    self.__chef.movement['UP'] = True
                elif event.key == pg.K_DOWN:
                    self.__chef.movement['DOWN'] = True
                elif event.key == pg.K_LEFT:
                    self.__chef.movement['LEFT'] = True
                elif event.key == pg.K_RIGHT:
                    self.__chef.movement['RIGHT'] = True

            elif event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    self.__chef.movement['UP'] = False
                elif event.key == pg.K_DOWN:
                    self.__chef.movement['DOWN'] = False
                elif event.key == pg.K_LEFT:
                    self.__chef.movement['LEFT'] = False
                elif event.key == pg.K_RIGHT:
                    self.__chef.movement['RIGHT'] = False

    def drop_food_to_the_world(self):
        """Drop the held ingredient"""
        if self.__held_ingredient:
            dropped_food = self.__held_ingredient
            dropped_food.set_position(self.__chef.get_position())

            self.__dropped_ingredient.append(dropped_food)
            self.__held_ingredient = None

    def is_near_pan(self):
        if self.__held_ingredient is None:
            chef_x, chef_y = self.__chef.get_position()
            pan_x, pan_y = self.__pan.get_position()

            distance = ((chef_x - pan_x) ** 2 + (chef_y - pan_y) ** 2) ** 0.5
            return distance < 100

    def update(self):
        """Update game logic"""
        self.__chef.move()
        self.__zombie.chase_player(self.__chef)
        self.__pan.fry_ingredients()

    def render(self):
        """Render game objects"""
        self.__screen.fill(Config.get('WHITE'))  # Clear screen

        self.__fridge.draw(self.__screen)
        self.__plate.draw(self.__screen)
        self.__pan.draw(self.__screen)
        if self.__held_ingredient:
            self.__screen.blit(self.__held_ingredient.images, self.__chef.get_position())

        for ingredient in self.__dropped_ingredient:
            x, y = ingredient.get_position()
            ingredient.draw_at(self.__screen, x + 10, y)

        self.__chef.draw()
        self.__zombie.draw()

        pg.display.flip()

    def run(self):
        while self.__running:
            self.render()
            self.handle_events()
            self.update()
            self.__clock.tick(Config.get('FPS'))
        pg.quit()


if __name__ == '__main__':
    app = GameApp()
    app.run()
