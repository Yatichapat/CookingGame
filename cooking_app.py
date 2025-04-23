import time

import pygame as pg
from cooking_config import Config
from cooking_chef import Chef
from cooking_zombie import Zombie
from cooking_ingredients import *
from cooking_served import Serving
from cooking_ui import *
from cooking_tool import *
from cooking_groceries import Groceries
from cooking_stat import StatsWindow


class GameApp:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Apocalypse Cooker')
        self.__screen = pg.display.set_mode((Config.get_config('WIN_SIZE_W'), Config.get_config('WIN_SIZE_H')))
        self.__kitchen_map = KitchenMap(self.__screen)

        self.__chef = Chef()

        self.__zombie1 = Zombie()

        self.__fridge = Fridge(190, 30, self.__chef)
        self.__pan = Pan(500, 38)
        # self.__pot = Pot(800, 30)
        self.__plate = Plate(600, 50)
        self.__cutting_board = CuttingBoard(700, 50)
        self.__trash = TrashBin(270, 70)

        self.__chef.set_screen(self.__screen)
        self.__zombie1.set_screen(self.__screen)

        self.__held_ingredient = None
        self.__held_plate = None
        self.__held_bag = None
        self.__plate_pick = False

        self.__dropped_ingredient = []
        self.__dropped_plate = []

        self.__clock = pg.time.Clock()
        self.__game_ui = GameUI()

        self.__restart_button_rect = None
        self.__exit_button_rect = None

        self.__running = True
        self.__start_game = False

        self.__menu = Menu()
        self.__serving = Serving(945, 150, self.__screen, self.__menu)
        self.__groceries = Groceries(self.__screen)

        self.movement = {'UP': False, 'DOWN': False, 'LEFT': False, 'RIGHT': False}
        self.__final_score = 0

        self.__orders_complete_this_session = 0
        self.__all_sessions_order = []

    def handle_events(self):
        """Handle user input"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.__chef.save_keystrokes_to_csv()
                self.__running = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_e:
                    if self.__held_bag:

                        self.__groceries.release_at_fridge(
                            self.__fridge.get_position(), self.__fridge)
                        self.__held_bag = False

                    else:
                        self.__fridge.toggle_fridge(self.__chef)

                # Check if the fridge is open and handle ingredient selection
                elif self.__fridge.is_open:
                    if event.key == pg.K_a:
                        self.__fridge.move_selection("LEFT")
                    elif event.key == pg.K_d:
                        self.__fridge.move_selection("RIGHT")
                    elif event.key == pg.K_w:
                        self.__fridge.move_selection("UP")
                    elif event.key == pg.K_s:
                        self.__fridge.move_selection("DOWN")
                    elif event.key == pg.K_RETURN:
                        if self.__held_ingredient is None:
                            self.__held_ingredient = self.__fridge.pick_ingredient()
                        elif self.__held_ingredient and self.__fridge.is_open:
                            self.__fridge.put_ingredient_in_fridge(self.__held_ingredient)
                            self.__held_ingredient = None

                elif event.key == pg.K_RETURN:
                    tool = self.is_near_tool()

                    # First try to pick up dropped items if not holding anything
                    if self.__held_ingredient is None and self.__held_plate is None:
                        # Try to pick up dropped plate first (since it might contain ingredients)
                        for plate in self.__dropped_plate[:]:
                            if self.is_near_dropped_item(plate.get_position()):
                                self.__held_plate = plate
                                self.__dropped_plate.remove(plate)
                                break

                        # If no plate was picked up, try to pick up ingredient
                        if self.__held_plate is None:
                            for ingredient in self.__dropped_ingredient[:]:
                                if self.is_near_dropped_item(ingredient.get_position()):
                                    self.__held_ingredient = ingredient
                                    self.__dropped_ingredient.remove(ingredient)
                                    break

                    # Handle held ingredient
                    if self.__held_ingredient:
                        if tool == 'pan':
                            self.__pan.put_ingredient_in_pan(self.__held_ingredient)
                            self.__held_ingredient = None

                        elif tool == 'cut':
                            self.__cutting_board.put_ingredient_in_cutting_board(self.__held_ingredient)
                            self.__cutting_board.cook_ingredients()
                            self.__held_ingredient = None

                        elif tool == 'plate':
                            self.__plate.add_ingredient(self.__held_ingredient)
                            self.__held_ingredient = None

                        elif tool == 'trash':
                            self.__trash.throw_into_bin(self.__held_ingredient)
                            self.__held_ingredient = None

                        elif tool == 'pad':
                            if self.__held_plate:
                                if self.__serving.add_plate(self.__held_plate):
                                    self.__held_plate = None
                                else:
                                    self.__serving.serve()

                            # If carrying something, drop it first
                            if self.__held_ingredient:
                                self.drop_food_to_the_world()
                                self.__held_ingredient = None

                    # Only spawn bag if not already carrying one and no bag exists
                    elif not self.__held_bag and not self.__groceries.has_active_bag() and tool == 'red button':
                        self.__groceries.spawn_bag()
                        self.__held_ingredient = None  # Clear held ingredient after spawning bag

                    # Handle held plate
                    elif self.__held_plate:
                        if tool == 'pad':
                            if self.__serving.add_plate(self.__held_plate):
                                self.__held_plate = None
                            else:
                                self.__serving.serve()
                        elif tool == 'trash':
                            self.__held_plate = None
                        else:
                            self.drop_all_to_the_world()
                    # Handle held bag
                    elif self.__held_bag:
                        # Drop bag at current position
                        self.__groceries.drop_bag(*self.__chef.get_position())
                        self.__held_bag = False

                    # Handle empty hands (interact with tools)
                    else:
                        if tool == 'pan' and self.__pan.is_ready_to_pick():
                            self.__held_ingredient = self.__pan.get_cooked_ingredients()

                        elif tool == 'cut' and self.__cutting_board.is_ready_to_pick():
                            self.__held_ingredient = self.__cutting_board.get_cooked_ingredients()

                        elif tool == 'plate':
                            if not self.__plate_pick:
                                self.__plate_pick = True
                                self.__held_plate = self.__plate.pick_up_plate()
                            else:
                                self.__plate_pick = False

                        if tool == 'paper bag':
                            if self.__held_bag:
                                # Drop the bag
                                self.__groceries.drop_bag(*self.__chef.get_position())
                                self.__held_bag = False

                            else:
                                # Try to pick up bag
                                if self.__groceries.pick_up_bag(self.__chef.get_position()):
                                    self.__held_bag = True

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
        self.__plate.clear()
        self.__pan.clear()
        self.__cutting_board.clear()
        self.__fridge.reset()
        self.__start_game = True
        self.__final_score = 0

    def drop_food_to_the_world(self):
        """Drop the held ingredient"""
        if self.__held_ingredient:
            dropped_food = self.__held_ingredient
            chef_x, chef_y = self.__chef.get_position()
            # Store the absolute position, not relative to chef
            dropped_food.set_position((chef_x, chef_y))

            self.__dropped_ingredient.append(dropped_food)
            self.__held_ingredient = None

    def drop_all_to_the_world(self):
        if self.__held_plate:
            dropped_plate = self.__held_plate
            chef_x, chef_y = self.__chef.get_position()
            # Store the absolute position, not relative to chef
            dropped_plate.set_position((chef_x, chef_y))

            self.__dropped_plate.append(dropped_plate)
            self.__held_plate = None

    def is_near_dropped_item(self, item_position):
        chef_x, chef_y = self.__chef.get_position()
        # Increase the pickup radius slightly to make it easier
        distance = ((chef_x - item_position[0]) ** 2 + (chef_y - item_position[1]) ** 2) ** 0.5
        return distance < 75

    def is_near_tool(self):
        tools = {
            'pan': self.__pan,
            'cut': self.__cutting_board,
            'plate': self.__plate,
            'trash': self.__trash,
            'pad': self.__serving,
            'fridge': self.__fridge,
            'red button': self.__groceries.get_red_button_position(),
        }

        # Special handling for paper bag if it exists
        if self.__groceries.has_active_bag() and not self.__groceries.is_bag_carried():
            tools['paper bag'] = self.__groceries.get_bag_position()

        chef_x, chef_y = self.__chef.get_position()

        # Find nearest tool
        nearest_tool = None
        min_distance = float('inf')

        for tool_name, tool in tools.items():
            if tool is None:
                continue

            # Handle both tool objects and position tuples
            if hasattr(tool, 'get_position'):
                tool_x, tool_y = tool.get_position()
            else:  # For paper bag position tuple
                tool_x, tool_y = tool

            distance = ((chef_x - tool_x) ** 2 + (chef_y - tool_y) ** 2) ** 0.5

            if distance < min_distance:
                min_distance = distance
                nearest_tool = tool_name

        return nearest_tool if min_distance <= 100 else None

    def update(self):
        """Update game logic"""

        self.__chef.move()
        self.__zombie1.chase_player(self.__chef)
        self.__pan.fry_ingredients()
        self.__menu.update()
        self.__kitchen_map.update()
        self.__serving.update()

    def render(self):
        """Render game objects"""

        if GameUI.game_over:
            self.__final_score = self.__menu.get_score()
            restart_button, exit_button = GameUI.draw_game_over(self.__screen, self.__final_score)
            self.__start_game = False

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__menu.save_to_order_per_session(force_save=True)
                    pg.quit()
                    Config.get_sound("click").play()
                    exit()

                elif event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()

                    if restart_button.collidepoint(mouse_pos):
                        # sounds play
                        Config.get_sound("click").play()

                        # Only save when game is exiting
                        self.__menu.save_to_order_per_session(force_save=True)
                        self.__chef.save_keystrokes_to_csv()
                        self.restart_game()
                        return

                    elif exit_button.collidepoint(mouse_pos):
                        # sounds play
                        Config.get_sound("click").play()

                        # Only save when game is exiting
                        self.__menu.save_to_order_per_session(force_save=True)
                        self.__chef.save_keystrokes_to_csv()
                        pg.quit()
                        exit()
            return

        elif not self.__start_game:
            start, stat, exit_ = GameUI.draw_start_game(self.__screen)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    # sounds play
                    Config.get_sound("click").play()
                    self.__running = False

                elif event.type == pg.MOUSEBUTTONDOWN:
                    mouse_pos = pg.mouse.get_pos()

                    if start.collidepoint(mouse_pos):
                        # sounds play
                        Config.get_sound("click").play()

                        self.__start_game = True
                        self.restart_game()
                        return

                    elif stat.collidepoint(mouse_pos):
                        # sounds play
                        Config.get_sound("click").play()

                        StatsWindow()

                    elif exit_.collidepoint(mouse_pos):
                        # sounds play
                        Config.get_sound("click").play()

                        # Only save when game is exiting
                        self.__menu.save_to_order_per_session(force_save=True)
                        self.__chef.save_keystrokes_to_csv()
                        self.__start_game = False
                        GameUI.game_over = False
                        self.__running = False
                        pg.quit()
            return

        elif self.__start_game:
            self.__fridge.draw(self.__screen)
            self.__trash.draw(self.__screen)
            self.__plate.draw(self.__screen)
            self.__pan.draw(self.__screen)
            self.__cutting_board.draw(self.__screen)

            self.__serving.draw_pad()

            self.__chef.draw()
            self.__zombie1.draw()

            self.__groceries.draw_red_button()
            self.__groceries.draw_bag()

            if self.__held_ingredient:
                x, y = self.__chef.get_position()
                self.__screen.blit(self.__held_ingredient.images, (x, y + 25))

            for ingredient in self.__dropped_ingredient:
                x, y = ingredient.get_position()
                ingredient.draw_at(self.__screen, x + 10, y)

            for plate in self.__dropped_plate:
                x, y = plate.get_position()
                plate.draw_at(self.__screen, x + 10, y)

            if self.__held_plate:
                x, y = self.__chef.get_position()
                self.__held_plate.set_position((x + 10, y))
                self.__held_plate.draw(self.__screen)

            if self.__held_bag:
                x, y = self.__chef.get_position()
                self.__screen.blit(self.__groceries.get_bag_image(), (x + 10, y))

            self.__menu.draw(self.__screen)
            self.__menu.draw_score(self.__screen)
            self.__game_ui.draw_timer(self.__screen)
            self.__serving.draw_feedback()

            pg.display.flip()

    def run(self):
        while self.__running:
            if not self.__start_game and not GameUI.game_over:
                self.render()
            else:
                self.render()
                self.handle_events()
                self.update()
            self.__clock.tick(Config.get_config('FPS'))

        pg.quit()


