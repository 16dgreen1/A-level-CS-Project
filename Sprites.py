from Settings import *
import pygame
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game  # a reference to the game class
        self.groups = self.game.all_sprites  # a reference to the
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image_file = pygame.image.load('images\\Player\\test.png')
        self.image = self.image_file
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.rot_angle = 0
        self.dx = 0
        self.dy = 0

    def rotate(self):
        original_coords = self.rect.center
        # AB = b - a
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        x = mouse_pos_x - self.rect.x
        y = mouse_pos_y - self.rect.y
        if x != 0:
            # angle between player and mouse
            self.rot_angle = math.degrees(math.atan(-y/x))
        else:
            # if the mouse is directly above or below (divide by 0)
            if mouse_pos_y < self.rect.y:
                self.rot_angle = 90
            else:
                self.rot_angle = -90
        # if the mouse is behind the player in terms of x
        if mouse_pos_x < self.rect.x:
            self.rot_angle += 180
        # change the player
        self.image = pygame.transform.rotate(self.image_file, self.rot_angle % 360)
        self.rect = self.image.get_rect()
        self.rect.center = original_coords

    def move(self):
        if self.dx in [1, -1] and self.dy in [1, -1]:
            self.dx *= 0.7
            self.dy *= 0.7
        self.rect.x += self.dx * PLAYER_SPEED
        self.rect.y += self.dy * PLAYER_SPEED
        self.dx, self.dy = 0, 0

    def update(self):
        self.rotate()
        self.move()
