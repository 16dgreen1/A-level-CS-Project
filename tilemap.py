import pygame
from Settings import *
import pytmx
from Sprites import *
import random


# taken from https://www.youtube.com/watch?v=QIXyj3WeyZM&list=PLsk-HSGFjnaGQq7ybM8Lgkh5EMxUWPm2i&index=12
class Tilemap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pygame.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface


# objects that are placed around the map and will spawn enemies
class Spawner:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.screen_x = x
        self.screen_y = y

    def update(self):
        self.screen_x = self.x + self.game.player.camerax
        self.screen_y = self.y + self.game.player.cameray

    # spawns an enemy at the location of the spawner  game, x, y, speed, damage, health
    def spawn(self):
        Enemy(self.game, self.x, self.y, random.randint(2, 4), random.randint(5, 15), random.randint(7, 13))
