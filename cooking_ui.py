import pygame as pg


class KitchenMap:
    def __init__(self):
        self.sprite_sheet = pg.image.load('images/kitchen16_tan.png')
        self.tile_size = 16

    def load_tiles(self):
        tiles = []
        for row in range(self.sprite_sheet.get_height() // self.tile_size):
            for col in range(self.sprite_sheet.get_width() // self.tile_size):
                tile = self.sprite_sheet.subsurface(col * self.tile_size, row * self.tile_size, self.tile_size, self.tile_size)
                tiles.append(tile)
        return tiles

    def get_tiles(self, x, y):
        tile = self.sprite_sheet.subsurface(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size)
        return tile

    def draw(self, screen):
        for row_idx, row in enumerate(Config.get('MAP')):
            for col_idx, tile in enumerate(row):
                screen.blit(self.get_tiles(tile[0], tile[1]), (col_idx * self.tile_size, row_idx * self.tile_size))

