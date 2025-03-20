import pygame as pg
from cooking_config import Config
from cooking_chef import Chef
from cooking_zombie import Zombie
from cooking_ingredients import *
from cooking_ui import *
from cooking_tool import *


class GameApp:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Apocalypse Cooker')
        self.__screen = pg.display.set_mode((Config.get_config('WIN_SIZE_W'), Config.get_config('WIN_SIZE_H')))
        self.__kitchen_map = KitchenMap(self.__screen)

        self.__chef = Chef()

        self.__zombie1 = Zombie()

        self.__fridge = Fridge(200, 30, self.__chef)
        self.__pan = Pan(500, 40)
        self.__pot = Pot(800, 30)
        self.__plate = Plate(600, 50)
        self.__cutting_board = CuttingBoard(700, 50)

        self.__chef.set_screen(self.__screen)
        self.__zombie1.set_screen(self.__screen)
        self.__held_ingredient = None
        self.__held_tool = None
        self.__dropped_ingredient = []

        self.__clock = pg.time.Clock()
        self.__game_ui = GameUI()

        self.__restart_button_rect = None
        self.__exit_button_rect = None

        self.__running = True
        self.__start_game = False
        self.__menu = Menu()
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
                    if event.key == pg.K_LEFT:
                        self.__fridge.move_selection("LEFT")
                    elif event.key == pg.K_RIGHT:
                        self.__fridge.move_selection("RIGHT")
                    elif event.key == pg.K_RETURN:  # Pick ingredient
                        if self.__held_ingredient is None:
                            self.__held_ingredient = self.__fridge.pick_ingredient()

                        elif self.__held_ingredient and self.__fridge.is_open:
                            self.__fridge.put_ingredient_in_fridge(self.__held_ingredient)
                            self.__held_ingredient = None

                elif event.key == pg.K_RETURN and self.__held_ingredient and self.__fridge.is_open is False:
                    tool = self.is_near_tool()
                    if tool == 'pan':
                        self.__pan.put_ingredient_in_pan(self.__held_ingredient)
                        self.__pan.fry_ingredients()
                        self.__held_ingredient = None

                    elif tool == 'pot':
                        self.__pot.put_ingredient_in_pot(self.__held_ingredient)
                        self.__pot.boil_ingredients()
                        self.__held_ingredient = None

                    elif tool == 'cut':
                        self.__cutting_board.put_ingredient_in_cutting_board(self.__held_ingredient)
                        self.__cutting_board.cut_ingredients()
                        self.__held_ingredient = None

                    elif tool == 'plate':
                        self.__plate.add_ingredient(self.__held_ingredient)
                        self.__held_ingredient = None

                    else:
                        self.drop_food_to_the_world()

                elif event.key == pg.K_RETURN:
                    if self.__held_ingredient is None:
                        tool = self.is_near_tool()
                        if tool == 'pan' and self.__pan.is_ready_to_pick():
                            self.__held_ingredient = self.__pan.get_cooked_ingredients()

                        if tool == 'cut' and self.__cutting_board.is_ready_to_pick():
                            self.__held_ingredient = self.__cutting_board.get_cooked_ingredients()

                        if tool == 'plate':
                            # self.__held_ingredient = self.__plate.
                            pass

            if event.type in {pg.KEYDOWN, pg.KEYUP}:
                self.__chef.handle_input(event, self.__fridge.is_open)

    def restart_game(self):
        """Reset game state to restart"""
        GameUI.game_over = False
        self.__chef.reset()
        self.__zombie1.reset()
        self.__held_ingredient = None
        self.__menu.reset()
        self.__dropped_ingredient.clear()
        self.__game_ui.reset()

    def drop_food_to_the_world(self):
        """Drop the held ingredient"""
        if self.__held_ingredient:
            dropped_food = self.__held_ingredient
            dropped_food.set_position(self.__chef.get_position())

            self.__dropped_ingredient.append(dropped_food)
            self.__held_ingredient = None

    def is_near_tool(self):
        tools = {
            'pan': self.__pan,
            'pot': self.__pot,
            'cut': self.__cutting_board,
            'plate': self.__plate
        }
        chef_x, chef_y = self.__chef.get_position()
        nearest_tool = min(tools, key=lambda t: ((chef_x - tools[t].get_position()[0]) ** 2 +
                                                 (chef_y - tools[t].get_position()[1]) ** 2) ** 0.5)
        return nearest_tool if ((chef_x - tools[nearest_tool].get_position()[0]) ** 2 +
                                (chef_y - tools[nearest_tool].get_position()[1]) ** 2) ** 0.5 < 100 else None

    def update(self):
        """Update game logic"""

        self.__chef.move()
        # self.__zombie1.chase_player(self.__chef)
        self.__pan.fry_ingredients()
        self.__menu.update()
        self.__kitchen_map.update()

    def render(self):
        """Render game objects"""

        if GameUI.game_over:
            restart_button, exit_button = GameUI.draw_game_over(self.__screen)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    exit()

                elif event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()

                    if restart_button.collidepoint(mouse_pos):
                        self.restart_game()
                        GameUI.game_over = False
                        return

                    elif exit_button.collidepoint(mouse_pos):
                        pg.quit()
                        exit()
            return

        elif not self.__start_game:
            restart, stat, exit_ = GameUI.draw_start_game(self.__screen)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__running = False

                elif event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()

                    if restart.collidepoint(mouse_pos):
                        print("start button click")
                        self.__start_game = True
                        return

                    elif stat.collidepoint(mouse_pos):
                        # self.show_statistics()  # Function to display statistics
                        pass

                    elif exit_.collidepoint(mouse_pos):
                        pg.quit()
                        exit()
            return

        elif self.__start_game:
            self.__fridge.draw(self.__screen)
            self.__plate.draw(self.__screen)
            self.__pan.draw(self.__screen)
            self.__pot.draw(self.__screen)
            self.__cutting_board.draw(self.__screen)
            self.__chef.draw()
            self.__zombie1.draw()
            if self.__held_ingredient:
                x, y = self.__chef.get_position()
                self.__screen.blit(self.__held_ingredient.images, (x, y + 25))

            for ingredient in self.__dropped_ingredient:
                x, y = ingredient.get_position()
                ingredient.draw_at(self.__screen, x + 10, y)

            self.__menu.draw(self.__screen)
            self.__game_ui.draw_timer(self.__screen)

            pg.display.flip()

    def run(self):
        while self.__running:
            self.render()
            self.handle_events()
            self.update()
            self.__clock.tick(Config.get_config('FPS'))
        pg.quit()


if __name__ == '__main__':
    app = GameApp()
    app.run()
