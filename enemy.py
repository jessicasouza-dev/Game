import pygame
import floors as floor_mod
import player_behavior as player_mod
import player_shots as player_shots_mod
import screen as screen_mod
import random as random

enemy_color_temporary = (0, 0, 252)

current_direction = 'right'
enemy_pos = pygame.Rect(50, 50, 50, floor_mod.floor_size_y)

ENEMY_WIDTH = 32
ENEMY_HEIGHT = 64


class Enemy:
    def __init__(self, x, y, color, speed, surface, direction, player):
        super().__init__()

        self.direction = direction
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.x = x
        self.y = y
        self.player = player
        self.color = enemy_color_temporary
        self.speed = speed
        self.surface = surface
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def act(self):
        self.drawEnemy()
        self.wander()
        self.kill(self.player)

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

    def kill(self, player):
        if self.rect.colliderect(player):
            player_mod.player_death()

    def die(self):
        self.rect = pygame.Rect(0, 0, 0, 0)


class Wave:
    def __init__(self, enemies_number, enemy, subwaves):
        super().__init__()

        self.spawn_delay = 120
        self.wave_delay = 360
        self.last_spawn_time = 0
        self.last_wave_time = 0
        self.enemies = []
        self.enemies_number = enemies_number
        self.enemy = enemy
        self.subwaves = subwaves
        self.enemies_per_sub_wave = enemies_number // subwaves
        self.current_wave = 0

    def add_enemies(self):

        for i in range(self.enemies_per_sub_wave):
            if self.spawn_delay >= 120:
                number = random.randint(0, len(floor_mod.floors_bottom_y_list)-1)
                floor = floor_mod.floors_bottom_y_list[number]
                enemy_instance = Enemy(self.enemy.x, floor, self.enemy.color, self.enemy.speed, self.enemy.surface, self.enemy.direction, self.enemy.player)
                self.enemies.append(enemy_instance)
                print(f"enemy n° {i+1}")
                self.spawn_delay = 0
            else:
                self.spawn_delay += 1



    def control_waves(self):
        if self.wave_delay == 360:
            if self.current_wave < self.subwaves:
                print(f"wave n° {self.current_wave}")
                self.add_enemies()
                self.current_wave += 1
                self.wave_delay = 0
        else:
            self.wave_delay += 1


    def update(self):
        self.control_waves()
        for enemy in self.enemies:
            enemy.act()




