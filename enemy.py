import pygame
import floors as floor_mod
import player_behavior as player_mod
import player_shots as player_shots_mod
import screen as screen_mod
import random as random
import shot as shot_mod

enemy_color_temporary = (0, 0, 252)

enemy_pos = pygame.Rect(50, 50, 50, floor_mod.floor_size_y)

ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50

cooldown = 0
sniper_cooldown = 0
delay = 50

pygame.mixer.init()
sound_enemy = pygame.mixer.Sound('assets/smw_bowser_fire.wav')
sound_enemy_dead = pygame.mixer.Sound('assets/goblin-death-clash-of-clans.mp3')
sound_enemy_dead.set_volume(0.25)

screen_width = screen_mod.screen.get_width()



class Enemy:
    def __init__(self, x, y, speed, surface, direction, player, current_layer, health, spritesheet):
        super().__init__()

        self.y = y
        self.direction = direction
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        
        if random.choice(["left", "right"]) == "left":
            self.x = 0
            self.direction = 'right' 
        else:
            self.x = screen_width - self.width 
            self.direction = 'left' 
                   
        self.player = player
        self.color = (0, 0, 128)
        self.speed = speed
        self.usual_speed = speed
        self.damage = 20
        self.surface = surface
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.current_layer = current_layer
        self.rect.centerx = self.x
        self.rect.centery = self.y - (self.height - 25)
        self.life = health
        self.spritesheet = spritesheet
        self.sprite_index = 0
        self.sprite = self.spritesheet[self.sprite_index]
        self.sprite_change_timer = 3
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
        if self.direction == 'left':
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
        self.delay = 600
        self.cooldown = 0  
        self.last_time = pygame.time.get_ticks()  
        self.life = health
        self.spritesheet = spritesheet
        self.time = 20
        self.shoot_windup = 20
        self.current_shoot_windup = 20
        self.shoot_startup = False
        self.saw_player = False

    def act(self):
        self.drawEnemy()
        self.wander()
        self.color = (230, 230, 250)
        self.enemy_hit_player(self.player)
        self.see_player()

        if self.cooldown > 0:
            self.cooldown -= pygame.time.get_ticks() - self.last_time
            if self.cooldown < 0:
                self.cooldown = 0  

        self.last_time = pygame.time.get_ticks()
        
    def see_player(self):
        if self.current_layer == player_mod.current_layer:

            if (self.direction == "right" and player_mod.player_pos.centerx >= self.x) or (
                    self.direction == "left" and player_mod.player_pos.centerx <= self.x):
                self.shoot_startup = True

        if self.shoot_startup == True:
            self.speed = 0
            if not self.current_shoot_windup == 0:
                self.current_shoot_windup -= 1
            else:
                self.shoot()
                self.shoot_startup = False
                self.current_shoot_windup = self.shoot_windup
                self.speed = self.usual_speed

    def shoot(self):
        y = self.rect.top
        x = self.rect.centerx
        sound_enemy.play()
        shot_mod.active_projectiles.append(shot_mod.Shot(x, y, 15, self.surface, self.direction, self))
        self.cooldown = self.delay


class Sniper(Enemy):
    def __init__(self, x, y, speed, surface, direction, player, current_layer, health, spritesheet):
        super().__init__(x, y, speed, surface, direction, player, current_layer, health, spritesheet)
        self.is_shooting = False
        self.delay = 1450
        self.color = (255, 0, 0)
        self.last_time = 0
        self.last_time_walk = 0
        self.already_shot = False
        self.life = health
        self.spritesheet = spritesheet
        self.wandering = True
        self.shooting_at_player = False
        self.found_player = False
        self.shoot_windup = 20
        self.current_shoot_windup = 20
        self.shoot_startup = False
        self.saw_player = False

    def act(self):
        self.drawEnemy()
        self.wander()
        self.enemy_hit_player(self.player)
        self.see_player()

    def see_player(self):
        global sniper_cooldown
        current_time = pygame.time.get_ticks()
        distance = abs(self.x - player_mod.player_pos.x)

        if ((distance < 20 and self.current_layer != player_mod.current_layer)
            or (distance > 50 and self.shooting_at_player)):
            self.wandering = False
            self.shoot_startup = True
            
        if self.shoot_startup:
            if not self.current_shoot_windup == 0:
                self.current_shoot_windup -= 1
                self.speed = 0
            else:
                sound_enemy.play()
                self.shoot()
                self.shoot_startup = False
                self.current_shoot_windup = self.shoot_windup
                self.speed = self.usual_speed

        self.last_time = current_time

    def shoot(self):
        y = self.rect.centery
        x = self.rect.centerx
        shot_mod.active_projectiles.append(shot_mod.VerticalShot(x, y, 30,
                                                             self.surface, self.direction, self, player_mod))