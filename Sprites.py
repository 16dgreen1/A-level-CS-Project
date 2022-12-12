from Settings import *
import pygame
import math


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game  # a reference to the game class
        self.groups = self.game.all_sprites  # a reference to the groups they're in
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.animation_frames = [pygame.image.load(PLAYER_SPRITES[i]).convert_alpha() for i in range(len(PLAYER_SPRITES))]
        self.current_frame = 0
        self.image = self.animation_frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.spawn = (x, y)
        self.x = x
        self.y = y
        self.rot_angle = 0
        self.dx = 0
        self.dy = 0
        self.camerax = -x + WIDTH / 2
        self.cameray = -y + HEIGHT / 2
        self.health = PLAYER_HEALTH
        self.gun_cooldown = 0
        self.animation_cooldown = 10
        self.currency = 0
        self.wave_text_time = 0

    def rotate(self):
        original_coords = self.rect.center
        # AB = b - a
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        x = mouse_pos_x - self.rect.centerx
        y = mouse_pos_y - self.rect.centery
        if x != 0:
            # angle between player and mouse
            self.rot_angle = math.degrees(math.atan(-y / x))
        else:
            # if the mouse is directly above or below (divide by 0)
            if mouse_pos_y < self.rect.y:
                self.rot_angle = 90
            else:
                self.rot_angle = -90
        # if the mouse is behind the player in terms of x
        if mouse_pos_x < self.rect.centerx:
            self.rot_angle += 180
        # rotate the sprite and change it if the animation cooldown is 0
        if self.animation_cooldown <= 0:
            self.animation_cooldown = 10
            self.current_frame = self.current_frame + 1 if self.current_frame < len(self.animation_frames) - 1 else 0
        else:
            self.animation_cooldown -= 1
        self.image = pygame.transform.rotate(self.animation_frames[self.current_frame], self.rot_angle % 360)
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
        original_x, original_y = self.rect.center
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
        self.camerax -= self.rect.centerx - original_x
        self.cameray -= self.rect.centery - original_y
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2

    # the player gets pushed back when they get hit by an enemy
    def hit_move(self, enemy):
        difference_x = self.rect.centerx - enemy.rect.centerx
        difference_y = self.rect.centery - enemy.rect.centery
        enemy_distance = math.sqrt(difference_x ** 2 + difference_y ** 2)
        self.dx, self.dy = 5 * (difference_x / enemy_distance), 5 * (difference_y / enemy_distance)
        self.move()
        self.dx, self.dy = 0, 0

    def draw_hud(self):
        self.draw_health_bar()
        self.draw_currency()
        self.draw_interact()
        # when a new wave start, flash the new wave on screen to the player
        if str(self.wave_text_time // 10) in ["13", "12", "9", "8", "5", "4", "1", "0"] and self.wave_text_time > 0:
            self.draw_wave()

    def draw_health_bar(self):
        full_bar = pygame.Rect(HEALTHBAR_OFFSET, HEALTHBAR_OFFSET, HEALTHBAR_WIDTH, HEALTHBAR_HEIGHT)
        current_bar = pygame.Rect(HEALTHBAR_OFFSET, HEALTHBAR_OFFSET, int(HEALTHBAR_WIDTH * self.health / PLAYER_HEALTH), HEALTHBAR_HEIGHT)
        pygame.draw.rect(self.game.win, DARK_GREY, full_bar)
        pygame.draw.rect(self.game.win, RED, current_bar)

    def draw_currency(self):
        currency_text = self.game.font.render("x {}".format(self.currency), True, BLACK)
        currency_rect = currency_text.get_rect()
        currency_rect.topleft = (CURRENCY_X, CURRENCY_Y)
        self.game.win.blit(currency_text, currency_rect)
        pygame.draw.circle(self.game.win, YELLOW, COIN_POS, 7.5)

    def draw_wave(self):
        wave_text = self.game.font.render("Wave {}".format(self.game.wave), True, RED)
        wave_text_rect = wave_text.get_rect()
        wave_text_rect.center = (WIDTH/2, HEIGHT/2 - 100)
        self.game.win.blit(wave_text, wave_text_rect)

    def closest_interactable(self):
        current_door = False
        for door in self.game.doors:
            if door.is_interact_distance(self):
                if not current_door:
                    current_door = door
                elif door.distance_to(self) < current_door.distance_to(self):
                    current_door = door
        return current_door

    def draw_interact(self):
        interactable = self.closest_interactable()
        if interactable:
            interact_text = self.game.font.render("press E to interact with the {}".format(self.closest_interactable().interact_type), True, WHITE)
            interact_rect = interact_text.get_rect()
            interact_rect.midbottom = INTERACT_POS
            self.game.win.blit(interact_text, interact_rect)

    # finds the closest thing that the player can interact with and interact with it
    def interact(self):
        interactable = self.closest_interactable()
        if interactable:
            if interactable.interact_type == "door":
                if interactable.cost <= self.currency:
                    interactable.interact()
                    self.currency -= interactable.cost
                else:
                    # if the player cannot afford the door or chest, the cost text will flash red
                    interactable.is_red = 10

    def shoot(self):
        if self.gun_cooldown <= 0:
            self.game.projectiles_list.append(Projectile(self.game, WIDTH / 2, HEIGHT / 2, self.rot_angle, 15, 5, 30))
            self.gun_cooldown = 20

    def update(self):
        self.rotate()
        self.move()
        # move the player back to spawn when they move out of bounds
        if pygame.sprite.spritecollide(self, self.game.out_of_bounds, False):
            self.x, self.y = self.spawn
            self.camerax, self.cameray = -self.x + WIDTH / 2, -self.y + HEIGHT / 2
        self.gun_cooldown -= 1 if self.gun_cooldown > 0 else 0
        if self.health <= 0:
            self.game.playing = False
        if self.wave_text_time > 0:
            self.wave_text_time -= 1


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, game):
        self.game = game
        self.groups = game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y

    def update(self):
        self.rect.x = self.x + self.game.player.camerax
        self.rect.y = self.y + self.game.player.cameray
        pygame.sprite.spritecollide(self, self.game.projectiles, True)


class Bounds(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, game):
        self.game = game
        self.groups = game.out_of_bounds
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y

    def update(self):
        self.rect.x = self.x + self.game.player.camerax
        self.rect.y = self.y + self.game.player.cameray


class Enemy(pygame.sprite.Sprite):

    def __init__(self, game, x, y, speed, damage, health):
        self.game = game
        self.groups = game.all_sprites, game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.animation_frames = [pygame.image.load(ENEMY_SPRITES[i]).convert_alpha() for i in range(len(ENEMY_SPRITES))]
        self.hit_sprite = pygame.image.load(ENEMY_HIT_SPRITE).convert_alpha()
        self.current_frame = 0
        self.image = self.animation_frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.spawn = (x, y)
        self.position_x = x
        self.position_y = y
        self.speed = speed
        self.damage = damage
        self.health = health
        self.animation_cooldown = 10
        self.hit_sprite_duration = 0
        self.rot_angle = 0

    def move(self):
        hit_player = False
        dx = math.cos(self.rot_angle)
        dy = -(math.sin(self.rot_angle))
        self.rect.x += dx * self.speed
        collisions = pygame.sprite.spritecollide(self, self.game.walls, False) + pygame.sprite.spritecollide(self, self.game.all_sprites, False)
        for collision in collisions:
            if collision != self:
                if collision.rect.x < self.rect.x:
                    self.rect.x = collision.rect.x + collision.rect.width
                elif collision.rect.x > self.rect.x:
                    self.rect.x = collision.rect.x - self.rect.width
                if collision == self.game.player:
                    self.game.player.health -= self.damage
                    self.game.player.hit_move(self)
                    hit_player = True
        self.rect.y += dy * self.speed
        collisions = pygame.sprite.spritecollide(self, self.game.walls, False) + pygame.sprite.spritecollide(self, self.game.all_sprites, False)
        for collision in collisions:
            if collision != self:
                if collision.rect.y < self.rect.y:
                    self.rect.y = collision.rect.y + collision.rect.height
                elif collision.rect.y > self.rect.y:
                    self.rect.y = collision.rect.y - self.rect.height
                if collision == self.game.player and not hit_player:
                    self.game.player.health -= self.damage
                    self.game.player.hit_move(self)
        bullet_collisions = pygame.sprite.spritecollide(self, self.game.projectiles, False)
        if bullet_collisions:
            for bullet in bullet_collisions:
                self.health -= bullet.damage
                self.game.player.currency += CURRENCY_ON_HIT
                bullet.kill()
                if self.health <= 0:
                    self.game.player.currency += CURRENCY_ON_DEATH
                    self.kill()
                    break
                else:
                    self.hit_sprite_duration = 5

    def rotate(self):
        original_coords = self.rect.center
        player_pos_x, player_pos_y = self.game.player.rect.center
        # AB = b - a
        x = player_pos_x - self.rect.centerx
        y = player_pos_y - self.rect.centery
        if x != 0:
            # angle between enemy and player
            self.rot_angle = math.atan(-y / x)
        else:
            # if the player is directly above or below (divide by 0)
            if player_pos_y < self.rect.y:
                self.rot_angle = math.radians(90)
            else:
                self.rot_angle = math.radians(-90)
        # if the player is behind the enemy in terms of x
        if player_pos_x < self.rect.centerx:
            self.rot_angle += math.radians(180)
        # change the enemy
        if self.animation_cooldown <= 0:
            self.animation_cooldown = 10
            self.current_frame = self.current_frame + 1 if self.current_frame < len(self.animation_frames) - 1 else 0
        else:
            self.animation_cooldown -= 1
        if self.hit_sprite_duration > 0:
            self.hit_sprite_duration -= 1
        self.image = pygame.transform.rotate(self.animation_frames[self.current_frame], math.degrees(self.rot_angle) % 360) if self.hit_sprite_duration <= 0 else pygame.transform.rotate(self.hit_sprite, math.degrees(self.rot_angle) % 360)
        self.rect = self.image.get_rect()
        self.rect.center = original_coords
        self.rotate_collide()

    def rotate_collide(self):
        collisions = pygame.sprite.spritecollide(self, self.game.walls, False)
        if collisions:
            for collision in collisions:
                if collision != self:
                    # how far the enemy has to move in each direction to not be colliding with the wall/player/other enemy
                    difference_y = collision.rect.y - self.rect.bottom if self.rect.y < collision.rect.y else collision.rect.bottom - self.rect.y
                    difference_x = collision.rect.x - self.rect.right if self.rect.x < collision.rect.x else collision.rect.right - self.rect.x
                    # move the enemy in the direction where the difference is smaller
                    if abs(difference_x) < abs(difference_y):
                        self.rect.x += difference_x
                    else:
                        self.rect.y += difference_y

    def update(self):
        original_pos_x, original_pos_y = self.rect.centerx, self.rect.centery
        self.rotate()
        self.move()
        # teleport the enemy back to spawn when they move out of bounds
        if pygame.sprite.spritecollide(self, self.game.out_of_bounds, False):
            self.position_x, self.position_y = self.spawn
        else:
            self.position_x += self.rect.centerx - original_pos_x
            self.position_y += self.rect.centery - original_pos_y
        self.rect.centerx = self.position_x + self.game.player.camerax
        self.rect.centery = self.position_y + self.game.player.cameray


class Projectile(pygame.sprite.Sprite):
    def __init__(self, game, x, y, rot_angle, speed, size, damage):
        self.game = game
        self.groups = game.projectiles
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface((size, size))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.x, self.y = x - self.game.player.camerax, y - self.game.player.cameray
        self.rot_angle = rot_angle
        self.speed = speed
        self.damage = damage
        self.dx, self.dy = math.cos(math.radians(self.rot_angle)), -(math.sin(math.radians(self.rot_angle)))

    # move forward then collide with walls and enemies
    def update(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        self.rect.x = self.x + self.game.player.camerax
        self.rect.y = self.y + self.game.player.cameray


class Door(pygame.sprite.Sprite):
    def __init__(self, game, x, y, is_tall, cost):
        self.game = game
        self.groups = game.doors, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.image.load(DOOR_IMAGE)
        if is_tall:
            self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.cost = cost
        self.interact_type = "door"
        self.is_red = 0
        self.closed = True

    def update(self):
        self.rect.x = self.x + self.game.player.camerax
        self.rect.y = self.y + self.game.player.cameray
        pygame.sprite.spritecollide(self, self.game.projectiles, True)
        if self.is_red > 0:
            self.is_red -= 1

    # returns the distance between the player and the door
    def distance_to(self, sprite):
        return math.sqrt((sprite.rect.centerx - self.rect.centerx)**2 + (sprite.rect.centery - self.rect.centery)**2)

    # checks if thew player is close enough to the door to interact with it
    def is_interact_distance(self, player):
        return True if self.distance_to(player) <= 100 else False

    # shows the price of the door if the player is close enough
    def draw_price(self, player):
        player_distance = math.sqrt((player.rect.centerx - self.rect.centerx)**2 + (player.rect.centery - self.rect.centery)**2)
        if player_distance <= 200:
            if self.is_red <= 0:
                text_colour = WHITE
                coin_colour = YELLOW
            else:
                text_colour = RED
                coin_colour = RED
            price_text = self.game.font.render("   x {}".format(self.cost), True, text_colour)
            price_rect = price_text.get_rect()
            price_rect.bottomleft = self.rect.topleft
            self.game.win.blit(price_text, price_rect)
            pygame.draw.circle(self.game.win, coin_colour, (self.rect.x, self.rect.y - 12.5), 7.5)

    # called when the player interacts with the door
    def interact(self):
        self.closed = False
        self.kill()
