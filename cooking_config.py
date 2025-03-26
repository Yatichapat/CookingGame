import pygame as pg


class Config:
    __ALL_CONFIGS = {
        'WIN_SIZE_W': 1000,
        'WIN_SIZE_H': 630,
        'GRID_SIZE_W': 22,
        'GRID_SIZE_H': 44,
        'GRID_COUNT_W': 64,
        'GRID_COUNT_H': 33,
        'FPS': 60,
        'BLACK': (0, 0, 0),
        'WHITE': (255, 255, 255),
        'GREEN': (119, 206, 112),
        'RED': (255, 0, 0),
        'BROWN': (165, 42, 42),
        'PASTEL_BLUE': (162, 191, 254),
        'GRAY': (128, 128, 128),
        'GRAY_BLUE': (202, 209, 211),
        'PASTEL_BROWN': (175, 175, 158),
        'PASTEL_GRAY': (220, 220, 213),
        'BACKGROUND': (249, 234, 211),
        'CHARACTER_SIZE': 100,
        'MESSAGE_BACKGROUND': pg.transform.scale(pg.image.load("images/message.png"),(200, 200)),
    }

    __IMAGE_CACHE = {}

    @classmethod
    def get_config(cls, key, default=None):
        return cls.__ALL_CONFIGS.get(key, default)

    @classmethod
    def load_images(cls):
        """Pre-loads and caches all ingredient images."""
        image_paths = {
            "lamb": "images/simply cooked/Raw food/lamb3.png",
            "lamb fried": "images/simply cooked/Cooked food/lamb1.png",

            "bread": "images/simply cooked/Cooked food/bread1.png",
            "bread sliced": "images/simply cooked/Cooked food/bread_sliced.png",
            "leek": "images/FarmVeggies/Leek.png",

            "egg": "images/simply cooked/Raw food/egg3.png",
            "egg fried": "images/simply cooked/Cooked food/egg1.png",

            "chicken": "images/simply cooked/Raw food/chiken3.png",
            "chicken to slice": "images/simply cooked/Raw food/chiken3.png",
            "chicken sliced": "images/simply cooked/Raw food/drumstick3.png",

            "chicken fried": "images/simply cooked/Cooked food/chiken1.png",
            "chicken drumstick fried": "images/simply cooked/Cooked food/drumstick1.png",

            "sandwich": "images/simply cooked/Cooked food/sandwich1.png",
            "tomato": "images/FarmVeggies/Tomato.png",
            "tomato sliced": "images/FarmVeggies/Tomatoslice.png",

            "cheese": "images/simply cooked/Cooked food/chees1.png",
            "cheese sliced": "images/simply cooked/Cooked food/cheese_slice.png",

            "lettuce": "images/FarmVeggies/lettuce.png",
            "lettuce sliced": "images/FarmVeggies/lettuceslice.png"

        }

        for ingredient, path in image_paths.items():
            try:
                image = pg.image.load(path)
                scaled_image = pg.transform.scale(
                    image,
                    (cls.get_config('GRID_SIZE_W') * 2, cls.get_config('GRID_SIZE_W') * 2)
                )
                cls.__IMAGE_CACHE[ingredient] = scaled_image
            except FileNotFoundError:
                print(f"Warning: Image not found for {ingredient}, using placeholder.")
                cls.__IMAGE_CACHE[ingredient] = pg.Surface((50, 50))  # Placeholder

    @classmethod
    def get_image(cls, ingredient_type):
        """Retrieve an image from the cache."""
        return cls.__IMAGE_CACHE.get(ingredient_type, pg.Surface((50, 50)))  # Default placeholder


# Ensure images are loaded before using them
Config.load_images()
