from Settings import *
import pygame
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game  # a reference to the game class
        self.groups = self.game.all_sprites  # a reference to the groups they're in
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
        x = mouse_pos_x - self.rect.centerx
        y = mouse_pos_y - self.rect.centery
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
        if mouse_pos_x < self.rect.centerx:
            self.rot_angle += 180
        # change the player
        self.image = pygame.transform.rotate(self.image_file, self.rot_angle % 360)
        self.rect = self.image.get_rect()
        self.rect.center = original_coords
        self.rotate_collide()

    def rotate_collide(self):
        walls = pygame.sprite.spritecollide(self, self.game.walls, False)
        if walls:
            for wall in walls:
                # finding how far the player is into the wall:
                # find if the player is above or below the wall an use the top or bottom of the player and wall depending on the result
                if self.rect.y < wall.rect.y:
                    # above
                    difference_y = wall.rect.y - self.rect.bottom
                else:
                    # below
                    difference_y = wall.rect.bottom - self.rect.y
                # find if the player is left or right of the wall and using the left or right of the player and wall depending on the result
                if self.rect.x > wall.rect.x:
                    # right
                    difference_x = wall.rect.right - self.rect.x
                else:
                    # left
                    difference_x = wall.rect.x - self.rect.right

                # move the player in the direction where the difference is smaller
                if abs(difference_x) < abs(difference_y):
                    self.rect.x += difference_x
                else:
                    self.rect.y += difference_y

    def move(self):
        if self.dx in [1, -1] and self.dy in [1, -1]:
            self.dx *= 0.7
            self.dy *= 0.7
        self.rect.x += self.dx * PLAYER_SPEED
        walls = pygame.sprite.spritecollide(self, self.game.walls, False)
        if walls:
            wall = walls[0]
            if wall.rect.x < self.rect.x:
                self.rect.x = wall.rect.x + wall.rect.width
            elif wall.rect.x > self.rect.x:
                self.rect.x = wall.rect.x - self.rect.width
        self.rect.y += self.dy * PLAYER_SPEED
        walls = pygame.sprite.spritecollide(self, self.game.walls, False)
        if walls:
            wall = walls[0]
            if wall.rect.y < self.rect.y:
                self.rect.y = wall.rect.y + wall.rect.height
            elif wall.rect.y > self.rect.y:
                self.rect.y = wall.rect.y - self.rect.height
        self.dx, self.dy = 0, 0

    def update(self):
        self.rotate()
        self.move()


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, game):
        self.game = game
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

