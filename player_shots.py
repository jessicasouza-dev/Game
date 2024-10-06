import pygame
import floors as floor_mod
import screen as screen_mod
import random
shots_temporary_color = (255, 100, 0)

screen = screen_mod.screen

# base shot stats and variables with current stats that can be modified during gameplay
BASE_DAMAGE = 100
BASE_DAMAGE_MODIFIER = 1
damage_value = BASE_DAMAGE
damage_modifier = BASE_DAMAGE_MODIFIER

BASE_SPEED = 30
speed_value = BASE_SPEED

BASE_COOLDOWN = 20 # cooldown counted in frames (60/sec)
cooldown_value = BASE_COOLDOWN

BASE_PIERCE = 0
pierce_value = BASE_PIERCE

BASE_BOUNCE = 0
bounce_value = BASE_BOUNCE

BASE_SIZE = floor_mod.floor_size_y/5
size_value = BASE_SIZE

BASE_INACCURACY = 0 #%
inaccuracy_value = BASE_INACCURACY

BASE_MULTISHOT = 1
multishot_value = BASE_MULTISHOT


active_friendly_projectiles = []

class player_projectile:

    rect = None

    def __init__(self, x_spawning_position, y_spawning_position, movement_direction):
        print('debug: attempting to shoot')

        self.speed = speed_value
        self.damage = damage_value * damage_modifier
        self.pierce = pierce_value
        self.bounce = bounce_value
        self.trajectory = movement_direction

        if inaccuracy_value != 0:
            self.inaccuracy_y = (speed_value * (1 + (random.randrange(inaccuracy_value * -1, inaccuracy_value) / 100))) / 10
            self.inaccuracy_y = random.uniform(self.inaccuracy_y * -1, self.inaccuracy_y)
            self.inaccuracy_x = random.uniform(self.inaccuracy_y * -1, self.inaccuracy_y)
            self.inaccuracy_x *= 10

        else:
            self.inaccuracy_x = 0
            self.inaccuracy_y = 0

        self.rect = pygame.Rect(0, 0, size_value, size_value)
        self.rect.centerx = x_spawning_position
        self.rect.centery = y_spawning_position
        for floor in floor_mod.floors_rect_list:
            if self.rect.colliderect(floor):
                self.original_layer = floor
        self.floors_pierced = [self.original_layer]

    def render(self):
        pygame.draw.rect(screen, shots_temporary_color, self.rect)
    
    def move(self):
        if self.trajectory == 'left':
            self.rect.centerx -= self.speed
        elif self.trajectory == 'right':
            self.rect.centerx += self.speed
        elif self.trajectory == 'up':
            self.rect.centery -= self.speed
        elif self.trajectory == 'down':
            self.rect.centery += self.speed
        self.rect.centerx += self.inaccuracy_x
        self.rect.centery += self.inaccuracy_y

        self.check_hit()
        #print('debug: moving a projectile')


    # conditions for projectile to lose pierce/bounce value or be destroyed
    def check_hit(self):
        # condition: reaching screen left border
        if self.rect.right < 0:
            if self.bounce > 0:
                if self.trajectory == 'right':
                    self.trajectory = 'left'
                elif self.trajectory == 'left':
                    self.trajectory = 'right'
                self.rect.right = 0
                self.bounce -= 1
            else: self.destroy()
        # condition: reaching screen right border
        if self.rect.left > screen.get_rect().right:
            if self.bounce > 0:
                if self.trajectory == 'right':
                    self.trajectory = 'left'
                elif self.trajectory == 'left':
                    self.trajectory = 'right'
                self.rect.left = screen.get_rect().right
                self.bounce -= 1
            else: self.destroy()
        
        #condition: reaching floor/ceiling
        for floor in floor_mod.floors_rect_list:
            if self.rect.colliderect(floor):
                if not floor in self.floors_pierced:
                    if self.pierce <= 0:
                        self.destroy()
                    else:
                        self.floors_pierced.append(floor)
                        self.pierce -= 1
                    
    def destroy(self):
        projectile = self
        if projectile in active_friendly_projectiles:
            index = active_friendly_projectiles.index(projectile)
            del active_friendly_projectiles[index]

    def kill(self, wave):
        projectile = self

        for enemy in wave.enemies:
            if self.rect.colliderect(enemy.rect):

                if enemy.life > 0:
                    enemy.get_hit(damage_value)
                elif enemy.life <= 0:
                    enemy.die()
                    wave.enemies.remove(enemy)

                if self.pierce <= 0:
                    self.destroy()
                else:
                    self.pierce -= 1