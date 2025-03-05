class Config:
    __ALL_CONFIGS = {
        'WIN_SIZE_W': 1280,
        'WIN_SIZE_H': 660,
        'GRID_SIZE': 32,
        'GRID_COUNT_W': 64,
        'GRID_COUNT_H': 33,
        'FPS': 60,
        'BLACK': (0, 0, 0),
        'WHITE': (255, 255, 255),

    }

    @classmethod
    def get(cls, key, default=None):
        return cls.__ALL_CONFIGS[key]
