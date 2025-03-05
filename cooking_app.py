import pygame as pg
from cooking_config import Config


class GameApp:
    def __init__(self):
        pg.init()
        self.__screen = pg.display.set_mode((Config.get('WIN_SIZE_W'), Config.get('WIN_SIZE_H')))
        self.__screen.fill(Config.get('WHITE'))
        self.__clock = pg.time.Clock()
        self.__running = True

    def run(self):
        while self.__running:
            for ev in pg.event.get():
                if ev.type == pg.QUIT:
                    pg.quit()
                    self.__running = False
            pg.display.flip()
            self.__clock.tick(Config.get('FPS'))
        pg.quit()

if __name__ == '__main__':
    app = GameApp()
    app.run()