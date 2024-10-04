import pygame
import floors as floor_mod
import player_behavior as player_mod
import player_shots as player_shots_mod
import screen as screen_mod
import random as random
import shot as shot_mod
import life as life_mod

enemy_color_temporary = (0, 0, 252)

current_direction = 'right'
enemy_pos = pygame.Rect(50, 50, 50, floor_mod.floor_size_y)

ENEMY_WIDTH = 32
ENEMY_HEIGHT = 64

cooldown = 0
sniper_cooldown = 0
delay = 100


class Enemy:
    def __init__(self, x, y, color, speed, surface, direction, player, current_layer):
        super().__init__()

        self.x = x
        self.y = y
        self.direction = direction
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.player = player
        self.color = color
        self.speed = speed
        self.surface = surface
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.current_layer = current_layer
        self.rect.centerx = x
        self.rect.centery = y

    def act(self):
        self.drawEnemy()
        self.wander()
        self.enemy_hit_player(self.player)
        self.see_player()

    def drawEnemy(self):
        pygame.draw.rect(self.surface, self.color, self.rect, width=0)

    def wander(self):
        if self.direction == 'right':
            self.x += self.speed
            if self.x + self.width >= screen_mod.screen.get_width():
                self.x = screen_mod.screen.get_width() - self.width
                self.direction = 'left'
        else:
            self.x -= self.speed
            if self.x <= 0:
                self.x = 0
                self.direction = 'right'

        # Update the rect's position
        self.rect.x = self.x
        self.rect.bottom = self.y

    def enemy_hit_player(self, player):
        if self.rect.colliderect(player) == True:
            player_mod.player_gets_hit()

    def die(self):
        self.rect = pygame.Rect(0, 0, 0, 0)

    def see_player(self):
        if self.current_layer == player_mod.current_layer and self.direction != player_mod.current_direction:
            print()


class Shooter(Enemy):
    def __init__(self, x, y, color, speed, surface, direction, player, current_layer):
        super().__init__(x, y, color, speed, surface, direction, player, current_layer)
        self.is_shooting = False

    def act(self):
        self.drawEnemy()
        self.wander()
        self.enemy_hit_player(self.player)
        self.see_player()

    def see_player(self):
        global cooldown
        if self.current_layer == player_mod.current_layer:

            if (self.direction == "right" and player_mod.player_pos.centerx >= self.x) or (
                    self.direction == "left" and player_mod.player_pos.centerx <= self.x):
                if cooldown == 0:
                    print('debug: enemy ready to shoot')
                    y = self.rect.centery
                    x = self.rect.centerx
                    shot_mod.active_projectiles.append(shot_mod.Shot(x, y, 15, self.surface, self.direction, self))
                    cooldown = 20
                else:
                    cooldown -= 1
        else:
            self.is_shooting = False
            #print('debug: enemy mot aiming')


class Sniper(Enemy):
    def __init__(self, x, y, color, speed, surface, direction, player, current_layer):
        super().__init__(x, y, color, speed, surface, direction, player, current_layer)
        self.is_shooting = False
        self.delay = 500
        self.last_time = 0
        self.last_time_walk = 0
        self.already_shot = False

        self.wandering = True
        self.shooting_at_player = False
        self.found_player = False

    def act(self):
        self.drawEnemy()
        self.wander()
        self.enemy_hit_player(self.player)
        self.see_player()

    def see_player(self):
        global cooldown
        current_time = pygame.time.get_ticks()
        distance = abs(self.x - player_mod.player_pos.x)

        if distance < 40 and self.current_layer != player_mod.current_layer and self.found_player == False:
            self.shooting_at_player = True
            self.wandering = False
            self.found_player = True
            print(f"debug: achou player ? {self.found_player}")

        if distance > 50 and self.current_layer != player_mod.current_layer and self.found_player == True:
            self.already_shot = False
            self.found_player = False
            print(f"debug: deixou o player em paz ? {self.found_player}")

        if self.already_shot:
            if current_time - self.last_time >= self.delay:
                self.wandering = True
                self.shooting_at_player = False
                self.last_time= current_time

        if self.shooting_at_player:
            self.wandering = False
            if current_time - self.last_time_walk >= self.delay:
                self.shoot()
                print(f"debug: atirou")
                self.already_shot = True
                self.last_time_walk = current_time

        else:
            self.wandering = True
            if current_time - self.last_time_walk >= self.delay:
                self.already_shot = False
                self.last_time_walk = current_time

        if self.wandering:
            self.speed = 5
        else:
            self.speed = 0

    def shoot(self):
        global sniper_cooldown
        current_time = pygame.time.get_ticks()

        if sniper_cooldown == 0:
            print('debug: enemy ready to shoot')
            y = self.rect.centery
            x = self.rect.centerx
            shot_mod.active_projectiles.append(shot_mod.VerticalShot(x, y, 15,
                                                                     self.surface, self.direction, self, player_mod))
            sniper_cooldown = 0
            self.last_time = current_time

        else:
            sniper_cooldown -= 1
