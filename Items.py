import pygame
from Settings import *
import math
import random


class ItemPlaced(pygame.sprite.Sprite):
    def __init__(self, game, x, y, item):
        self.game = game
        self.groups = game.items
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = item.image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.item = item
        self.interact_type = "weapon"

    def update(self):
        self.rect.x = self.x + self.game.player.camerax
        self.rect.y = self.y + self.game.player.cameray

    # returns the distance between the player and the door
    def distance_to(self, sprite):
        return math.sqrt((sprite.rect.centerx - self.rect.centerx)**2 + (sprite.rect.centery - self.rect.centery)**2)

    # checks if thew player is close enough to the door to interact with it
    def is_interact_distance(self, player):
        return True if self.distance_to(player) <= 100 else False

    # handles what happens when the player interacts with the item
    def interact(self):
        if self.game.player.held_item.stored_ammo + self.game.player.held_item.clip_ammo > 0:
            item_swap = self.item
            self.item = self.game.player.held_item
            self.game.player.held_item = item_swap
            self.image = self.item.image
        else:
            self.game.player.held_item = self.item
            self.kill()


class ItemHeld:
    def __init__(self, database_item, rarity):
        self.name = database_item[0]
        self.image = pygame.image.load(ITEM_SPRITES[self.name])
        self.damage = database_item[1]
        self.shot_delay = database_item[2]
        self.spread = database_item[3]
        self.bullet_speed = database_item[4]
        self.bullets_at_once = database_item[5]
        self.is_auto = database_item[6]
        self.clip_size = database_item[7]
        self.clip_ammo = self.clip_size
        self.stored_ammo = database_item[8] - self.clip_ammo
        self.reload_time = database_item[9]
        self.rarity = rarity
