import pygame
import random
from Settings import *
from Sprites import *
from tilemap import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

    # handles events such as key presses
    def events(self):
        for event in pygame.event.get():
            # check if the x has been pressed then close the window if it has
            if event.type == pygame.QUIT:
                if self.running:
                    self.running = False

        # player movement
        k = pygame.key.get_pressed()
        if k[pygame.K_a]:
            self.player.dx -= 1
        if k[pygame.K_d]:
            self.player.dx += 1
        if k[pygame.K_w]:
            self.player.dy -= 1
        if k[pygame.K_s]:
            self.player.dy += 1

    # updates the objects
    def update(self):
        self.all_sprites.update()

    # draws the new screen and presents it to the player
    def draw(self):
        self.win.blit(self.map_image, (0, 0))
        self.all_sprites.draw(self.win)

        # after the screen has been drawn, display it to the player
        pygame.display.flip()

    def new(self):
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.player = Player(self, 512, 320)
        self.wall = Wall(300, 300, 32, 32, self)
        self.map = Tilemap('images\\Tilemap\\map1.tmx')
        self.map_image = self.map.make_map()
        self.map_rect = self.map_image.get_rect()
        self.run()

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()


g = Game()
g.running = True
while g.running:
    g.new()
