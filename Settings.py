import pygame

# window settings

WIDTH = 1920
HEIGHT = 1080
FPS = 60

# menu settings
START_BUTTON_IMAGES = ["images\\Menu\\Start Button\\start button idle.png", "images\\Menu\\Start Button\\start button hover.png"]
START_BUTTON_POS = (WIDTH/2, HEIGHT/2 - 150)
SCORE_BUTTON_IMAGES = ["images\\Menu\\Score Button\\score button idle.png", "images\\Menu\\Score Button\\score button hover.png"]
SCORE_BUTTON_POS = (WIDTH/2, HEIGHT/2)
MAIN_QUIT_BUTTON_IMAGES = ["images\\Menu\\Quit Button\\quit button idle.png", "images\\Menu\\Quit Button\\quit button hover.png"]
MAIN_QUIT_BUTTON_POS = (WIDTH/2, HEIGHT/2 + 150)
CLOSE_BUTTON_IMAGES = ["images\\Menu\\Close Button\\close button idle.png", "images\\Menu\\Close Button\\close button hover.png"]
CLOSE_BUTTON_POS = (WIDTH/2, HEIGHT-75)
SCOREBOARD_OFFSET_X = 100
SCOREBOARD_OFFSET_Y = 100
CONTINUE_BUTTON_IMAGES = ["images\\Menu\\Continue Button\\continue button idle.png", "images\\Menu\\Continue Button\\continue button hover.png"]
CONTINUE_BUTTON_POS = (WIDTH/2, HEIGHT/2 + 300)
NO_BUTTON_IMAGES = ["images\\Menu\\Quit popup\\No button\\no button idle.png", "images\\Menu\\Quit popup\\No button\\no button hover.png"]
YES_BUTTON_IMAGES = ["images\\Menu\\Quit popup\\Yes button\\yes button idle.png", "images\\Menu\\Quit popup\\Yes button\\yes button hover.png"]
RESUME_BUTTON_IMAGES = ["images\\Menu\\Pause popup\\Quit button\\quit button idle.png", "images\\Menu\\Pause popup\\Quit button\\quit button hover.png"]
POPUP_QUIT_BUTTON_IMAGES = ["images\\Menu\\Pause popup\\Resume button\\resume button idle.png", "images\\Menu\\Pause popup\\Resume button\\resume button hover.png"]
POPUP_HEIGHT = 200
POPUP_WIDTH = 440
POPUP_TEXT_POS = (WIDTH/2, HEIGHT/2 - 60)
YES_BUTTON_POS = (WIDTH/2 - 125, HEIGHT/2 + 50)
NO_BUTTON_POS = (WIDTH/2 + 125, HEIGHT/2 + 50)

# player settings
PLAYER_SPEED = 5
PLAYER_HEALTH = 1000
CURRENCY_ON_HIT = 5
CURRENCY_ON_DEATH = 30
PLAYER_SPRITES = ['images\\Player\\frame1.png', 'images\\Player\\frame2.png', 'images\\Player\\frame3.png', 'images\\Player\\frame2.png']

# tilemap
TILESIZE = 32
DOOR_IMAGE = "images\\Tilemap\\Door.png"
CHEST_CLOSED_IMAGE = "images\\Tilemap\\chest_closed.png"
CHEST_OPEN_IMAGE = "images\\Tilemap\\chest_open.png"
ITEMS = []

# colour RGB values
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
DARK_GREY = (50, 50, 50)
BACKGROUND_COLOUR = (107, 123, 57)

# enemy settings
ENEMY_SPRITES = ['images\\Enemy\\frame1.png', 'images\\Enemy\\frame2.png', 'images\\Enemy\\frame3.png', 'images\\Enemy\\frame2.png']
ENEMY_HIT_SPRITE = 'images\\Enemy\\hit.png'
SPEED_BOUNDS = [1, 2]
MAX_SPEEDS = [3, 5.5]
HEALTH_BOUNDS = [90, 150]
DAMAGE_BOUNDS = [5, 15]

# wave settings
WAVE_MULTIPLIER = 1.05
WAVE_TIME = 3600
WAVE_POINTS = 20

# HUD
HEALTHBAR_WIDTH = 300
HEALTHBAR_HEIGHT = 15
HEALTHBAR_OFFSET = 25
RELOAD_X = WIDTH/2 - 40
RELOAD_Y = HEIGHT/2 - 40
RELOAD_WIDTH = 80
RELOAD_HEIGHT = 10
CURRENCY_X = 43
CURRENCY_Y = 47
COIN_POS = (30, 57)
COIN_RADIUS = 5
INTERACT_POS = (WIDTH/2, HEIGHT - 100)
ITEM_BORDER_HEIGHT = 100
ITEM_BORDER_WIDTH = 160
ITEM_BORDER_OFFSET_X = 60

# items
ITEMS = ["handgun", "assault rifle", "smg", "chain gun", "revolver", "sniper rifle", "shotgun"]
ITEM_SPRITES = {
    "handgun": "images\\Weapons\\handgun\\sprite.png",
    "assault rifle": "images\\Weapons\\assault rifle\\sprite.png",
    "smg": "images\\Weapons\\smg\\sprite.png",
    "chain gun": "images\\Weapons\\chain gun\\sprite.png",
    "revolver": "images\\Weapons\\revolver\\sprite.png",
    "sniper rifle": "images\\Weapons\\sniper rifle\\sprite.png",
    "shotgun": "images\\Weapons\\shotgun\\sprite.png"
}
AMMO_SPRITES = {
    "handgun": "images\\Weapons\\handgun\\ammo.png",
    "assault rifle": "images\\Weapons\\assault rifle\\ammo.png",
    "smg": "images\\Weapons\\smg\\ammo.png",
    "chain gun": "images\\Weapons\\chain gun\\ammo.png",
    "revolver": "images\\Weapons\\revolver\\ammo.png",
    "sniper rifle": "images\\Weapons\\sniper rifle\\ammo.png",
    "shotgun": "images\\Weapons\\shotgun\\ammo.png"
}
