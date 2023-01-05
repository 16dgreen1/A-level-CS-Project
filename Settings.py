
# window settings

WIDTH = 1024
HEIGHT = 640
FPS = 60

# menu settings
START_BUTTON_IMAGES = ["images\\Menu\\Start Button\\start button idle.png", "images\\Menu\\Start Button\\start button hover.png"]
START_BUTTON_POS = (WIDTH/2, 320)
MAIN_QUIT_BUTTON_IMAGES = ["images\\Menu\\Quit Button\\quit button idle.png", "images\\Menu\\Quit Button\\quit button hover.png"]
MAIN_QUIT_BUTTON_POS = (WIDTH / 2, 470)
NO_BUTTON_IMAGES = ["images\\Menu\\Quit popup\\No button\\no button idle.png", "images\\Menu\\Quit popup\\No button\\no button hover.png"]
YES_BUTTON_IMAGES = ["images\\Menu\\Quit popup\\Yes button\\yes button idle.png", "images\\Menu\\Quit popup\\Yes button\\yes button hover.png"]
RESUME_BUTTON_IMAGES = ["images\\Menu\\Pause popup\\Quit button\\quit button idle.png", "images\\Menu\\Pause popup\\Quit button\\quit button hover.png"]
POPUP_QUIT_BUTTON_IMAGES = ["images\\Menu\\Pause popup\\Resume button\\resume button idle.png", "images\\Menu\\Pause popup\\Resume button\\resume button hover.png"]
POPUP_HEIGHT = 200
POPUP_WIDTH = 440
POPUP_TEXT_POS = (WIDTH/2, 260)
YES_BUTTON_POS = (387, 370)
NO_BUTTON_POS = (637, 370)

# player settings
PLAYER_SPEED = 5
PLAYER_HEALTH = 1000
CURRENCY_ON_HIT = 5
CURRENCY_ON_DEATH = 30
PLAYER_SPRITES = ['images\\Player\\frame1.png', 'images\\Player\\frame2.png', 'images\\Player\\frame3.png', 'images\\Player\\frame2.png']

# tilemap
TILESIZE = 32
DOOR_IMAGE = "images\\Tilemap\\Door.png"

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

# items
ITEM_SPRITES = {
    "handgun": "images\\Weapons\\handgun\\sprite.png",
    "assault rifle": "images\\Weapons\\assault rifle\\sprite.png",
    "smg": "images\\Weapons\\smg\\sprite.png",
    "lmg": "images\\Weapons\\chain gun\\sprite.png",
    "revolver": "images\\Weapons\\revolver\\sprite.png",
    "sniper rifle": "images\\Weapons\\sniper rifle\\sprite.png",
    "shotgun": "images\\Weapons\\shotgun\\sprite.png"
}
