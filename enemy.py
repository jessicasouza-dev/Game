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

ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50

cooldown = 0
sniper_cooldown = 0
delay = 100

pygame.mixer.init()
sound_enemy = pygame.mixer.Sound('assets/synth-shot-fx-by-alien-i-trust-9-245434.mp3')
sound_enemy_dead = pygame.mixer.Sound('assets/goblin-death-clash-of-clans.mp3')
sound_enemy_dead.set_volume(0.25)




class Enemy:
    def __init__(self, x, y, speed, surface, direction, player, current_layer, health, spritesheet):
        super().__init__()

        self.x = x
        self.y = y
        self.direction = direction
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.player = player
        self.color = (0, 0, 128)
        self.speed = speed
        self.usual_speed = speed
        self.damage = 20
        self.surface = surface
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.current_layer = current_layer
        self.rect.centerx = x
        self.rect.centery = y
        self.life = health
        self.spritesheet = spritesheet
        self.sprite_index = 0
        self.sprite = self.spritesheet[self.sprite_index]
        self.sprite_change_timer = 6
        self.shots_hit = []

    def act(self):
        self.drawEnemy()
        self.wander()
        self.enemy_hit_player(self.player)

    def drawEnemy(self):
        self.sprite = pygame.transform.scale(self.sprite, (ENEMY_WIDTH, ENEMY_HEIGHT))
        screen_mod.screen.blit(self.sprite, self.rect)

    def wander(self):
        #update sprite
        if self.sprite_change_timer <= 0:
            self.sprite_index = (self.sprite_index + 1) % 2
            self.sprite_change_timer = random.randint(6, 12)
        else:
            self.sprite_change_timer -= 1
        self.sprite = self.spritesheet[self.sprite_index]

        if self.direction == 'right':
            self.x += self.speed
            if self.x + self.width >= screen_mod.screen.get_width():
                self.x = screen_mod.screen.get_width() - self.width
                self.direction = 'left'
        else:
            self.sprite = pygame.transform.flip(self.sprite, True, False)
            self.x -= self.speed
            if self.x <= 0:
                self.x = 0
                self.direction = 'right'

        # Update the rect's position
        self.rect.x = self.x
        self.rect.bottom = self.y

    def enemy_hit_player(self, player):
        if self.rect.colliderect(player) == True:
            player_mod.player_gets_hit(self.damage)

    def die(self):
        player_shots_mod.explosion(self.rect.centerx, self.rect.centery)
        self.rect = pygame.Rect(0, 0, 0, 0)
        sound_enemy_dead.play()

    def get_hit(self, damage):
        self.life = self.life - damage


class Shooter(Enemy):
    def __init__(self, x, y, speed, surface, direction, player, current_layer, health, spritesheet):
        super().__init__(x, y, speed, surface, direction, player, current_layer, health, spritesheet)
        self.is_shooting = False
        self.delay = 500
        self.last_time = 0
        self.already_shot = False
        self.switch = False
        self.life = health
        self.spritesheet = spritesheet
        self.time = 90
        self.saw_player = False

    def act(self):
        self.drawEnemy()
        self.wander()
        self.color = (230, 230, 250)
        self.enemy_hit_player(self.player)
        self.see_player()

    def see_player(self):

        if self.current_layer == player_mod.current_layer:
            if (self.direction == "right" and player_mod.player_pos.centerx >= self.x) or (
                    self.direction == "left" and player_mod.player_pos.centerx <= self.x):

                if self.time > 0 and self.saw_player == False:
                    self.speed = 0
                    self.time -= 1

                if self.time == 0:
                    self.shoot()


        if self.time < 90 and self.time != 0:
            self.time -= 1

        if self.time < 0:
            self.time = 0

        if self.time == 0:
            self.speed = self.usual_speed
            self.saw_player = True

    def shoot(self):
        global cooldown
        if cooldown == 0:
            y = self.rect.top
            x = self.rect.centerx
            sound_enemy.play()
            shot_mod.active_projectiles.append(shot_mod.Shot(x, y, 15, self.surface, self.direction, self))
            cooldown = 20
        elif cooldown != 0:
            cooldown -= 1



class Sniper(Enemy):
    def __init__(self, x, y, speed, surface, direction, player, current_layer, health, spritesheet):
        super().__init__(x, y, speed, surface, direction, player, current_layer, health, spritesheet)
        self.is_shooting = False
        self.delay = 500
        self.color = (255, 0, 0)
        self.last_time = 0
        self.last_time_walk = 0
        self.already_shot = False
        self.life = health
        self.spritesheet = spritesheet
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

        if distance < 20 and self.current_layer != player_mod.current_layer and self.found_player == False:
            self.shooting_at_player = True
            self.wandering = False
            self.found_player = True

        if distance > 50 and self.current_layer != player_mod.current_layer and self.found_player == True:
            self.already_shot = False
            self.found_player = False

        if self.already_shot:
            if current_time - self.last_time >= self.delay:
                self.wandering = True
                self.shooting_at_player = False
                self.last_time= current_time

        if self.shooting_at_player:
            self.wandering = False
            if current_time - self.last_time_walk >= self.delay:
                self.shoot()
                sound_enemy.play()
                self.already_shot = True
                self.last_time_walk = current_time

        else:
            self.wandering = True
            if current_time - self.last_time_walk >= self.delay:
                self.already_shot = False
                self.last_time_walk = current_time

        if self.wandering:
            self.speed = self.usual_speed
        else:
            self.speed = 0

    def shoot(self):
        global sniper_cooldown
        current_time = pygame.time.get_ticks()

        if sniper_cooldown == 0:
            y = self.rect.centery
            x = self.rect.centerx
            shot_mod.active_projectiles.append(shot_mod.VerticalShot(x, y, 15,
                                                                     self.surface, self.direction, self, player_mod))
            sniper_cooldown = 0
            self.last_time = current_time

        else:
            sniper_cooldown -= 1
