import pygame
import random
from Settings import *
from Sprites import *
from Menu import *
from tilemap import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.font.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("calibri", 24)

    def main_menu(self):
        self.buttons = pygame.sprite.Group()
        self.start_button = Button(self, self.buttons, START_BUTTON_IMAGES, START_BUTTON_POS)
        self.quit_button = Button(self, self.buttons, MAIN_QUIT_BUTTON_IMAGES, MAIN_QUIT_BUTTON_POS)
        self.menu_open = True
        while self.menu_open:
            self.menu_events()
            self.menu_update()
            self.menu_draw()

    def menu_events(self):
        for event in pygame.event.get():
            # check if the x has been pressed then close the window if it has
            if event.type == pygame.QUIT:
                if self.running:
                    self.running, self.menu_open = False, False

            # check if the mouse has been clicked and then check what button, if any the mouse is above
            if event.type == pygame.MOUSEBUTTONUP:

                # if the quit button is pressed, close the window
                if self.quit_button.is_hover():
                    self.quit_menu()

                # if the start button is pressed, close the menu
                elif self.start_button.is_hover():
                    self.menu_open = False

    def menu_update(self):
        self.buttons.update()

    def menu_draw(self):
        self.win.fill(BLACK)
        self.buttons.draw(self.win)

        # flip teh screen once everything has drawn
        pygame.display.flip()

    def quit_menu(self):
        self.quit_popup = Popup(self, "Are you sure you want to quit?", NO_BUTTON_IMAGES, YES_BUTTON_IMAGES)
        self.popup_open = True
        while self.popup_open:
            self.quit_popup.menu_loop()
            if self.quit_popup.yes_pressed:
                self.running, self.playing, self.menu_open, self.popup_open = False, False, False, False
            if self.quit_popup.no_pressed:
                self.popup_open = False

    def pause_menu(self):
        self.pause_popup = Popup(self, "Paused", RESUME_BUTTON_IMAGES, POPUP_QUIT_BUTTON_IMAGES)
        self.popup_open = True
        while self.popup_open:
            self.pause_popup.menu_loop()
            if self.pause_popup.no_pressed:
                self.playing, self.menu_open, self.popup_open = False, False, False
            if self.pause_popup.yes_pressed:
                self.popup_open = False

    # handles events such as key presses
    def events(self):
        for event in pygame.event.get():
            # check if the x has been pressed then close the window if it has
            if event.type == pygame.QUIT:
                if self.running:
                    self.running, self.playing = False, False

        # making the player shoot whenever the mouse is being clicked
        if pygame.mouse.get_pressed(5)[0]:
            self.player.shoot()

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
        if k[pygame.K_ESCAPE]:
            self.pause_menu()

    # updates the objects
    def update(self):
        self.projectiles.update()
        self.all_sprites.update()
        self.walls.update(self.player)

    # draws the new screen and presents it to the player
    def draw(self):
        self.win.blit(self.map_image, (self.player.camerax, self.player.cameray))
        self.doors.draw(self.win)
        self.all_sprites.draw(self.win)
        self.projectiles.draw(self.win)
        for door in self.doors:
            door.draw_price(self.player)
        self.player.draw_hud()

        # after the screen has been drawn, display it to the player
        pygame.display.flip()

    def new(self):
        self.mouse_down = False
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.doors = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.player = Player(self, 672, 736)
        self.enemy_list = [Enemy(self, 256, 256, 4, 25, 10), Enemy(self, 320, 1280, 4, 25, 10)]
        self.projectiles_list = []
        self.map = Tilemap('images\\Tilemap\\map1.tmx')
        self.map_image = self.map.make_map()
        self.map_rect = self.map_image.get_rect()
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'Wall':
                Wall(tile_object.x, tile_object.y, tile_object.width, tile_object.height, self)
            if tile_object.name == 'Door':
                Door(self, tile_object.x, tile_object.y, tile_object.width < tile_object.height, 10)
        self.run()

    def run(self):
        self.playing = True if self.running else False
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()


g = Game()
g.running = True
while g.running:
    g.main_menu()
    g.new()
