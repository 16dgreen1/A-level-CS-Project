from Settings import *
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = 0
        self.dy = 0

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
