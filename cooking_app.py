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
        self.__dict_keys = {pg.K_UP: 'UP',
                            pg.K_DOWN: 'DOWN',
                            pg.K_LEFT: 'LEFT',
                            pg.K_RIGHT: 'RIGHT'}

    def __user_event(self):
        for ev in pg.event.get():
            if ev.type == pg.QUIT:
                pg.quit()
                self.__running = False
            elif ev.type == pg.KEYDOWN:
                if ev.key == pg.K_UP:
                    self.__chef.move_up()
                elif ev.key == pg.K_DOWN:
                    self.__chef.move_down()
                elif ev.key == pg.K_LEFT:
                    self.__chef.move_left()
                elif ev.key == pg.K_RIGHT:
                    self.__chef.move_right()


    def run(self):
        while self.__running:
            self.__user_event()
            pg.display.flip()
            self.__clock.tick(Config.get('FPS'))
        pg.quit()

if __name__ == '__main__':
    app = GameApp()
    app.run()