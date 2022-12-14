import pygame
import random
import sqlite3
from Settings import *
from Sprites import *
from Items import *
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
        self.item_connector = sqlite3.connect("item.db")
        self.item_cursor = self.item_connector.cursor()

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
        self.quit_popup = Popup(self, "Are you wsure you want to quit?", NO_BUTTON_IMAGES, YES_BUTTON_IMAGES)
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.player.interact()

            # making the player shoot if the mouse has been pressed this frame and the gun is not auto
            if event.type == pygame.MOUSEBUTTONDOWN and self.player.held_item.is_auto == 'False':
                self.player.shoot()

        # making the player shoot whenever the mouse is being held down if the gun is auto
        if pygame.mouse.get_pressed(5)[0] and self.player.held_item.is_auto == 'True':
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
        if self.wave_timer > 0:
            self.wave_timer -= 1
        else:
            self.wave += 1
            self.wave_timer = WAVE_TIME * (WAVE_MULTIPLIER ** self.wave)
            self.director.points += WAVE_POINTS * (WAVE_MULTIPLIER ** self.wave)
            self.player.wave_text_time = 140
        self.director.update()
        self.projectiles.update()
        self.all_sprites.update()
        self.walls.update()
        self.out_of_bounds.update()
        self.items.update()

    # draws the new screen and presents it to the player
    def draw(self):
        self.win.fill(BACKGROUND_COLOUR)
        self.win.blit(self.map_image, (self.player.camerax, self.player.cameray))
        self.doors.draw(self.win)
        self.items.draw(self.win)
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
        self.out_of_bounds = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.item_cursor.execute("SELECT * FROM items WHERE name='handgun'")
        self.player = Player(self, 672, 736, ItemHeld(self.item_cursor.fetchall()[0]))
        self.projectiles_list = []
        self.start_spawner_list = []
        self.spawner_list = []
        self.map = Tilemap('images\\Tilemap\\map1.tmx')
        self.map_image = self.map.make_map()
        self.map_rect = self.map_image.get_rect()
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'Wall':
                Wall(tile_object.x, tile_object.y, tile_object.width, tile_object.height, self)
            if tile_object.name == 'Door':
                cost = int(math.sqrt((tile_object.x)**2 + (tile_object.y)**2)//5)
                if tile_object.type == "area b":
                    self.area_b_door = Door(self, tile_object.x, tile_object.y, tile_object.width < tile_object.height, cost)
                else:
                    Door(self, tile_object.x, tile_object.y, tile_object.width < tile_object.height, cost)
            if tile_object.name == "Out of bounds":
                Bounds(tile_object.x, tile_object.y, tile_object.width, tile_object.height, self)
            if tile_object.name == "spawner":
                if tile_object.type == "A":
                    self.start_spawner_list.append(Spawner(self, tile_object.x, tile_object.y))
                self.spawner_list.append(Spawner(self, tile_object.x, tile_object.y))
        self.wave = 0
        self.wave_timer = 0
        self.director = Director(self, self.start_spawner_list, self.spawner_list)
        self.director.points = 0
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
g.item_connector.close()
