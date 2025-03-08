import pygame as pg


class Config:
    __ALL_CONFIGS = {
        'WIN_SIZE_W': 1280,
        'WIN_SIZE_H': 660,
        'GRID_SIZE': 32,
        'GRID_COUNT_W': 64,
        'GRID_COUNT_H': 33,
        'FPS': 50,
        'FPS_Z': 20,
        'BLACK': (0, 0, 0),
        'WHITE': (255, 255, 255),
        'BACKGROUND': (0, 0, 0),
        'CHARACTER_SIZE': 100

    }

    @classmethod
    def get(cls, key, default=None):
        return cls.__ALL_CONFIGS[key]
