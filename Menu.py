import pygame
from Settings import *


class Button(pygame.sprite.Sprite):
    def __init__(self, game, images, x, y):
        self.game = game
        self.groups = game.buttons
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.idle_image = pygame.image.load(images[0])
        self.hover_image = pygame.image.load(images[1])
        self.image = self.idle_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y):
            self.image = self.hover_image
        else:
            self.image = self.idle_image

    def is_pressed(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (self.rect.collidepoint(mouse_x, mouse_y)) and pygame.mouse.get_pressed(3)[0]:
            return True
        else:
            return False
