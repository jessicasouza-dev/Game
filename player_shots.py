import pygame
import floors as floor_mod
import screen as screen_mod

shots_temporary_color = (255, 100, 0)

screen = screen_mod.screen

# base shot stats and variables with current stats that can be modified during gameplay
BASE_DAMAGE = 100
damage_value = BASE_DAMAGE 

BASE_SPEED = 20
speed_value = BASE_SPEED

BASE_COOLDOWN = 30 # cooldown counted in frames (60/sec)
cooldown_value = BASE_COOLDOWN

BASE_PIERCE = 0
pierce_value = BASE_PIERCE

BASE_BOUNCE = 5
bounce_value = BASE_BOUNCE

BASE_SIZE = floor_mod.floor_size_y/5
size_value = BASE_SIZE


active_friendly_projectiles = []

class player_projectile:

    rect = None

    def __init__(self, x_spawning_position, y_spawning_position, movement_direction):
        print('debug: attempting to shoot')
        self.speed = speed_value
        self.damage = damage_value
        self.pierce = pierce_value
        self.bounce = bounce_value
        self.trajectory = movement_direction
        self.rect = pygame.Rect(0, 0, size_value, size_value)
        self.rect.centerx = x_spawning_position
        self.rect.centery = y_spawning_position

    def render(self):
        pygame.draw.rect(screen, shots_temporary_color, self.rect)
    
    def move(self):
        if self.trajectory == 'left':
            self.rect.centerx -= self.speed
        elif self.trajectory == 'right':
            self.rect.centerx += self.speed

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
                    
    def destroy(self):
        projectile = self
        index = active_friendly_projectiles.index(projectile)
        del active_friendly_projectiles[index]