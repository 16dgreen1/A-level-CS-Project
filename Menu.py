import pygame
from Settings import *


class Button(pygame.sprite.Sprite):
    def __init__(self, game, groups, images, pos):
        self.game = game
        self.groups = groups
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.idle_image = pygame.image.load(images[0])
        self.hover_image = pygame.image.load(images[1])
        self.image = self.idle_image
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        if self.is_hover():
            self.image = self.hover_image
        else:
            self.image = self.idle_image

    def is_pressed(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y) and pygame.mouse.get_pressed(5)[0]:
            return True
        else:
            return False

    def is_hover(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y):
            return True
        else:
            return False


class Popup:
    def __init__(self, game, text, no_button_images, yes_button_images):
        self.game = game
        self.text = text
        self.buttons = pygame.sprite.Group()
        self.no_button = Button(self.game, self.buttons, no_button_images, NO_BUTTON_POS)
        self.yes_button = Button(self.game, self.buttons, yes_button_images, YES_BUTTON_POS)
        self.popup_background = pygame.Surface((POPUP_WIDTH, POPUP_HEIGHT))
        self.popup_background.fill(DARK_GREY)
        self.yes_pressed = False
        self.no_pressed = False

    def menu_loop(self):
        self.menu_events()
        self.menu_update()
        self.menu_draw()

    def menu_events(self):
        for event in pygame.event.get():
            # check if the x has been pressed then close the window if it has
            if event.type == pygame.QUIT:
                if self.game.running:
                    self.game.running, self.game.playing, self.game.popup_open, self.game.menu_open = False, False, False, False
            # check if the mouse has been clicked and check which button, if any has bee clicked
            if event.type == pygame.MOUSEBUTTONUP:

                if self.no_button.is_hover():
                    self.no_pressed = True

                if self.yes_button.is_hover():
                    self.yes_pressed = True

    def menu_update(self):
        self.buttons.update()

    def menu_draw(self):
        self.game.win.blit(self.popup_background, (WIDTH/2 - POPUP_WIDTH/2, HEIGHT/2 - POPUP_HEIGHT/2))
        self.buttons.draw(self.game.win)
        popup_text = self.game.font.render(self.text, True, RED)
        popup_text_rect = popup_text.get_rect()
        popup_text_rect.center = POPUP_TEXT_POS
        self.game.win.blit(popup_text, popup_text_rect)

        # after drawing objects, flip te screen
        pygame.display.flip()
