import pygame as pg
import os


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

        "paper bag": "images/paperbag.png",
        "red button": "images/red_button.png",
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
            "chicken fried": "images/simply cooked/Cooked food/chiken1.png",

            "chicken to slice": "images/simply cooked/Raw food/chiken3.png",
            "chicken sliced": "images/simply cooked/Raw food/drumstick3.png",
            "chicken rotten": "images/simply cooked/Rotten food/chiken_rotten.png",

            "chicken drumstick fried": "images/simply cooked/Cooked food/drumstick1.png",
            "chicken drumstick rotten": "images/simply cooked/Rotten food/drumstick_rotten.png",

            "pork": "images/simply cooked/Raw food/pork3.png",
            "pork fried": "images/simply cooked/Cooked food/pork1.png",

            "fish": "images/simply cooked/Raw food/fish3.png",
            "fish fried": "images/simply cooked/Cooked food/fish1.png",

            "sandwich": "images/simply cooked/Cooked food/sandwich1.png",
            "tomato": "images/FarmVeggies/Tomato.png",
            "tomato sliced": "images/FarmVeggies/Tomatoslice.png",

            "cheese": "images/simply cooked/Cooked food/chees1.png",
            "cheese sliced": "images/simply cooked/Cooked food/cheese_slice.png",

            "lettuce": "images/FarmVeggies/lettuce.png",
            "lettuce sliced": "images/FarmVeggies/lettuceslice.png",

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

    __SOUND_CACHE = {}

    @classmethod
    def load_sounds(cls):
        """Pre-loads and caches all sounds"""
        if not pg.mixer.get_init():
            pg.mixer.init()

        sound_paths = {
            "click": "sounds/click.mp3",
            "game_start": "sounds/game_start_song.mp3",
            "trash": "sounds/trash.mp3",
            "cutting": "sounds/cutting.mp3",
            "finish_cooking": "sounds/finishcooking.mp3",
            "served": "sounds/handbell.mp3",
        }

        for name, path in sound_paths.items():
            try:
                sound = pg.mixer.Sound(path)
                # Set the volume for the sound
                if name == "game_start":
                    sound.set_volume(0.3)

                cls.__SOUND_CACHE[name] = sound
            except (FileNotFoundError, pg.error):
                print(f"Warning: Sound not found for {name}")
                # Create empty sounds as fallback
                cls.__SOUND_CACHE[name] = pg.mixer.Sound(buffer=bytes(44))

    @classmethod
    def get_sound(cls, sound_name):
        """Retrieve a sounds from the cache"""
        return cls.__SOUND_CACHE.get(sound_name, cls.__SOUND_CACHE.get("error"))  # Fallback to error sounds


# Ensure images are loaded before using them
Config.load_images()
Config.load_sounds()
