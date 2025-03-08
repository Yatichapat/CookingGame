import pygame as pg
from cooking_config import Config
from cooking_chef import Chef


class GameApp:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Apocalypse Cooker')
        self.__screen = pg.display.set_mode((Config.get('WIN_SIZE_W'), Config.get('WIN_SIZE_H')))
        self.__screen.fill(Config.get('WHITE'))
        self.__chef = Chef()
        self.__chef.set_screen(self.__screen)
        self.__clock = pg.time.Clock()
        self.__running = True
        self.__last_move_time = 0
        self.__speed = 0
        self.movement = {'UP': False, 'DOWN': False, 'LEFT': False, 'RIGHT': False}

    def handle_events(self):
        """Handle user input"""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.__running = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
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

    def update(self):
        """Update game logic"""
        self.__chef.move()

    def render(self):
        """Render game objects"""
        self.__screen.fill(Config.get('WHITE'))  # Clear screen
        self.__screen.blit(self.__chef.chef_sprite, self.__chef.chef_rect)  # Draw chef
        pg.display.flip()

    def run(self):
        while self.__running:
            self.handle_events()
            self.update()
            self.render()
            self.__clock.tick(Config.get('FPS'))
        pg.quit()


if __name__ == '__main__':
    app = GameApp()
    app.run()
