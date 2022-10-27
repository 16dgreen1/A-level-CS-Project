import pygame
from Settings import *


class Button(pygame.sprite.Sprite):
    def __init__(self, game, idle_image_path, hover_image_path, x, y):
        self.game = game
        self.groups = game.buttons
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.idle_image = pygame.image.load(idle_image_path)
        self.hover_image = pygame.image.load(hover_image_path)
        self.image = self.idle_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

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
