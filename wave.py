import pygame

import enemy
import screen as scrn_mod
import floors as floor_mod
import player_behavior as player_mod
import random as random
import life as life_mod




class Wave:
    def __init__(self, enemies_number, enemy, wave_number, enemy_class):
        super().__init__()

        self.spawn_delay = 900
        self.last_spawn_time = 0
        self.enemies = []
        self.enemies_number = enemies_number
        self.enemy = enemy
        self.current_wave = 0
        self.enemy_class = enemy_class
        self.wave_number = wave_number
        self.enemies_added = 0
        self.isActive = True

    def add_enemies(self):

        number = random.randint(0, len(floor_mod.floors_bottom_y_list) - 1)
        floor = floor_mod.floors_bottom_y_list[number]
        if self.enemy_class == 'Shooter':
            enemy_instance = enemy.Shooter(
                self.enemy.x, floor, self.enemy.color, self.enemy.speed,
                self.enemy.surface, self.enemy.direction, self.enemy.player, number
            )
            self.enemies.append(enemy_instance)
        elif self.enemy_class == 'Enemy':
            enemy_instance = enemy.Enemy(
                self.enemy.x, floor, self.enemy.color, self.enemy.speed,
                self.enemy.surface, self.enemy.direction, self.enemy.player, number
            )
            self.enemies.append(enemy_instance)
        print(f"new enemy {self.enemies_added + 1}")
        self.enemies_added += 1

    def update(self):
        if self.isActive:
            current_time = pygame.time.get_ticks()

            if current_time - self.last_spawn_time >= self.spawn_delay and self.enemies_added < self.enemies_number:
                self.add_enemies()
                self.last_spawn_time = current_time

            for enemy in self.enemies:
                enemy.act()

            if len(self.enemies) == 0 and self.enemies_added > 0:
                self.isActive = False

    def restart_waves(self):
        self.enemies.clear()
        self.last_spawn_time = 0
        self.enemies_added = 0

        life_mod.life = life_mod.max_life
        player_mod.player_spawn()
        player_mod.player_render()

        self.last_restart_time = pygame.time.get_ticks()

