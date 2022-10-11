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
        self.x = x
        self.y = y
        self.rot_angle = 0
        self.dx = 0
        self.dy = 0
        self.camerax = x - WIDTH/2
        self.cameray = y - HEIGHT/2

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
                # how far the player has to move in each direction to not be colliding with the wall
                difference_y = wall.rect.y - self.rect.bottom if self.rect.y < wall.rect.y else wall.rect.bottom - self.rect.y
                difference_x = wall.rect.x - self.rect.right if self.rect.x < wall.rect.x else wall.rect.right - self.rect.x
                # move the player in the direction where the difference is smaller
                if abs(difference_x) < abs(difference_y):
                    self.rect.x += difference_x
                else:
                    self.rect.y += difference_y

    def move(self):
        originalx, originaly = self.rect.center
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
        self.camerax -= self.rect.centerx - originalx
        self.cameray -= self.rect.centery - originaly
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2

    def update(self):
        self.rotate()
        self.move()


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, game):
        self.game = game
        self.groups = game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y

    def update(self, player):
        self.rect.x = self.x + player.camerax
        self.rect.y = self.y + player.cameray
