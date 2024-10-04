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

            if (self.direction == "right" and player_mod.player_pos.centerx >= self.x) or (self.direction == "left" and player_mod.player_pos.centerx <= self.x):
                if cooldown == 0:
                    print('debug: enemy ready to shoot')
                    y = self.rect.centery
                    x = self.rect.centerx
                    shot_mod.active_projectiles.append(shot_mod.Shot(x, y, 15, self.surface, self.direction, self))
                    cooldown = 60
                else:
                    cooldown -= 1
        else:
            self.is_shooting = False
            #print('debug: enemy mot aiming')

    def try_shooting(self):
        global cooldown
        # print('debug: running try_shooting function')
        if self.is_shooting == True:
            if cooldown == 0:
                #print('debug: enemy ready to shoot')
                #y = self.rect.centery
                #x = self.rect.centerx
                #shot_mod.active_projectiles.append(shot_mod.Shot(x, y, 5, self.surface, self.direction, self))
                cooldown = 30
        else:
            if cooldown >= 0:
                cooldown -= 1
