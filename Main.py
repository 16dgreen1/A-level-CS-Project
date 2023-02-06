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
        self.score_font = pygame.font.SysFont("calibri", 60)
        self.item_connector = sqlite3.connect("item.db")
        self.item_cursor = self.item_connector.cursor()
        self.score_connector = sqlite3.connect("scoreboard.db")
        self.score_cursor = self.score_connector.cursor()

    def main_menu(self):
        self.buttons = pygame.sprite.Group()
        self.start_button = Button(self, self.buttons, START_BUTTON_IMAGES, START_BUTTON_POS)
        self.score_button = Button(self, self.buttons, SCORE_BUTTON_IMAGES, SCORE_BUTTON_POS)
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
                    self.name_menu()
                    self.menu_open = False

                # if the scoreboard button is pressed, show the player teh scoreboard
                elif self.score_button.is_hover():
                    self.score_menu()

    def menu_update(self):
        self.buttons.update()

    def menu_draw(self):
        self.win.fill(BLACK)
        self.buttons.draw(self.win)

        # flip the screen once everything has drawn
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

    def score_menu(self):
        # draw the player's names on the scoreboard
        self.score_cursor.execute("SELECT name FROM scores ORDER BY score DESC LIMIT 10")
        names = [i[0] for i in self.score_cursor.fetchall()]
        self.player_text_images = [self.score_font.render("Player:", True, WHITE)]
        self.player_text_rects = [self.player_text_images[0].get_rect()]
        self.player_text_rects[0].topleft = (SCOREBOARD_OFFSET_X, SCOREBOARD_OFFSET_Y)

        # finds the longest name to put the scores next to so that the scores do not overlap the names
        highest_x = self.player_text_rects[0].right
        for i in range(1, 11):
            self.player_text_images.append(self.score_font.render("{}: {}".format(i, names[i-1]), True, WHITE))
            self.player_text_rects.append(self.player_text_images[i].get_rect())
            self.player_text_rects[i].topleft = (SCOREBOARD_OFFSET_X, SCOREBOARD_OFFSET_Y + 65*i)
            if self.player_text_rects[i].right > highest_x:
                highest_x = self.player_text_rects[i].right

        # draw the scores on the scoreboard next to the player names
        self.score_cursor.execute("SELECT score FROM scores ORDER BY score DESC LIMIT 10")
        scores = [i[0] for i in self.score_cursor.fetchall()]
        self.score_text_images = [self.score_font.render("Score:", True, WHITE)]
        self.score_text_rects = [self.score_text_images[0].get_rect()]
        self.score_text_rects[0].topleft = (highest_x + 50, SCOREBOARD_OFFSET_Y)
        for i in range(1, 11):
            self.score_text_images.append(self.score_font.render("{}".format(scores[i-1]), True, WHITE))
            self.score_text_rects.append(self.score_text_images[i].get_rect())
            self.score_text_rects[i].topleft = (highest_x + 75, SCOREBOARD_OFFSET_Y + 65*i)

        # setup and start the game loop
        self.win.fill(BLACK)
        pygame.display.flip()
        self.score_buttons = pygame.sprite.Group()
        self.close_button = Button(self, self.score_buttons, CLOSE_BUTTON_IMAGES, CLOSE_BUTTON_POS)
        self.scoreboard_open = True
        while self.scoreboard_open:
            self.score_events()
            self.score_update()
            self.score_draw()

    def score_events(self):
        for event in pygame.event.get():
            # check if the x has been pressed then close the window if it has
            if event.type == pygame.QUIT:
                if self.running:
                    self.running, self.playing, self.scoreboard_open = False, False, False

            if event.type == pygame.MOUSEBUTTONUP:
                if self.close_button.is_hover():
                    self.scoreboard_open = False

    def score_update(self):
        self.score_buttons.update()

    def score_draw(self):
        self.win.fill(BLACK)

        for i in range(11):
            self.win.blit(self.player_text_images[i], self.player_text_rects[i])
        for i in range(11):
            self.win.blit(self.score_text_images[i], self.score_text_rects[i])

        self.score_buttons.draw(self.win)
        pygame.display.flip()

    def name_menu(self):
        self.name_buttons = pygame.sprite.Group()
        self.continue_button = Button(self, self.name_buttons, CONTINUE_BUTTON_IMAGES, CLOSE_BUTTON_POS)
        self.name_open = True
        self.typed_name = ""
        while self.name_open:
            self.name_events()
            self.name_update()
            self.name_draw()

    def name_events(self):
        for event in pygame.event.get():
            # check if the x has been pressed then close the window if it has
            if event.type == pygame.QUIT:
                if self.running:
                    self.running, self.name_open = False, False
            if event.type == pygame.MOUSEBUTTONUP:
                if self.continue_button.is_hover():
                    self.player_name = self.typed_name if self.typed_name else ' '
                    self.name_open = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.typed_name = self.typed_name[:-1]
                else:
                    self.typed_name += event.unicode

    def name_update(self):
        self.name_image = self.score_font.render(self.typed_name, True, WHITE)
        self.name_rect = self.name_image.get_rect()
        self.name_rect.center = (WIDTH/2, HEIGHT/2)
        self.name_buttons.update()

    def name_draw(self):
        self.win.fill(BLACK)
        title_image = self.score_font.render("Enter your name:", True, WHITE)
        title_rect = title_image.get_rect()
        title_rect.midtop = (WIDTH/2, 100)
        self.win.blit(title_image, title_rect)
        self.name_buttons.draw(self.win)
        self.win.blit(self.name_image, self.name_rect)
        pygame.display.flip()

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
        self.interactable_obstacles.draw(self.win)
        self.items.draw(self.win)
        self.all_sprites.draw(self.win)
        self.projectiles.draw(self.win)
        for interactable in self.interactable_obstacles:
            interactable.draw_price(self.player)
        self.player.draw_hud()

        # after the screen has been drawn, display it to the player
        pygame.display.flip()

    def new(self):
        self.mouse_down = False
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.interactable_obstacles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.out_of_bounds = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.item_cursor.execute("SELECT * FROM items WHERE name='handgun'")
        self.player = Player(self, 672, 736, ItemHeld(self.item_cursor.fetchall()[0]), self.player_name)
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
            if tile_object.name == "Chest":
                cost = int(math.sqrt((tile_object.x)**2 + (tile_object.y)**2)//2)
                Chest(self, tile_object.x + TILESIZE/2, tile_object.y + TILESIZE/2, int(tile_object.type), cost)
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

        # add the player's score to the scoreboard:
        self.score_cursor.execute("INSERT INTO scores VALUES ('{}', {})".format(self.player.name, self.player.score))
        self.score_connector.commit()


g = Game()
g.running = True
while g.running:
    g.main_menu()
    if g.running:
        g.new()
g.item_connector.close()
