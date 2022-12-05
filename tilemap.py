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

    def is_on_screen(self):
        return True if 0 < self.screen_x < WIDTH and 0 < self.screen_y < HEIGHT else False

    # spawns an enemy at the location of the spawner and set their health, damage and speed to a random value between bounds based on what wave it is
    def spawn(self):
        min_speed = min(SPEED_BOUNDS[0] * (WAVE_MULTIPLIER ** self.game.wave), MAX_SPEEDS[0])
        max_speed = min(SPEED_BOUNDS[1] * (WAVE_MULTIPLIER ** self.game.wave), MAX_SPEEDS[1])
        speed = random.uniform(min_speed, max_speed)

        damage = random.uniform(DAMAGE_BOUNDS[0], DAMAGE_BOUNDS[1])

        min_health = HEALTH_BOUNDS[0] * (WAVE_MULTIPLIER ** self.game.wave)
        max_health = HEALTH_BOUNDS[0] * (WAVE_MULTIPLIER ** self.game.wave)
        health = random.uniform(min_health, max_health)

        Enemy(self.game, self.x, self.y, speed, damage, health)


class Director:
    def __init__(self, game, start_spawners, all_spawners):
        self.game = game
        self.start_spawners = start_spawners
        self.all_spawners = all_spawners
        self.points = 0

    def update(self):
        if self.points > 0:
            self.spawn()
            self.points -= 1
        for i in self.start_spawners:
            i.update()
        for i in self.all_spawners:
            i.update()

    # picks a random point in the list of enemy spawners and moves through the list from there until it finds one that isn't on the screen
    @staticmethod
    def pick_spawner(spawner_list):
        spawn_index = random.randint(0, len(spawner_list)-1)
        while spawner_list[spawn_index].is_on_screen():
            spawn_index = spawn_index + 1 if spawn_index < len(spawner_list) - 1 else 0
        return spawner_list[spawn_index]

    def spawn(self):
        spawner_list = self.all_spawners
        if self.game.area_b_door.closed:
            spawner_list = self.start_spawners
        self.pick_spawner(spawner_list).spawn()
