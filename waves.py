import pygame

import enemy
import screen as scrn_mod
import floors as floor_mod
import player_behavior as player_mod
import random as random
import life as life_mod
import enemy as enemy_mod
import wave_controller as wave_controller_mod

cooldown = 60
is_restarting = True
delay = 5000

class Wave:
    def __init__(self, enemies_dictionary):
        super().__init__()

        self.last_restart_time = 0
        self.enemies_dictionary = enemies_dictionary
        self.enemies_dictionary_iteratable = self.enemies_dictionary.copy()
        self.spawn_delay = 1000
        self.last_spawn_time = 0
        self.enemies = []
        self.enemies_added = 0
        self.enemies_number = sum(enemies_dictionary.values())
        self.isActive = True

    def add_enemies(self):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_spawn_time < self.spawn_delay:
            return

        if self.enemies_added < self.enemies_number:

            enemy_class = random.choice(list(self.enemies_dictionary_iteratable.keys()))
            count = self.enemies_dictionary_iteratable[enemy_class]

            if count > 0:

                number = random.randint(0, len(floor_mod.floors_bottom_y_list) - 1)
                floor = floor_mod.floors_bottom_y_list[number]

                if enemy_class == 'Shooter':
                    enemy_instance = enemy.Shooter(0, floor, 5,
                                                    scrn_mod.screen, "right", player_mod.player_pos, number)
                elif enemy_class == 'Enemy':
                    enemy_instance = enemy.Enemy(0, floor, 5,
                                                 scrn_mod.screen, "right", player_mod.player_pos, number)
                elif enemy_class == 'Sniper':
                    enemy_instance = enemy.Sniper(0, floor, 5,
                                                   scrn_mod.screen, "right", player_mod.player_pos, number)

                self.enemies.append(enemy_instance)
                self.enemies_dictionary_iteratable[enemy_class] -= 1
                self.enemies_added += 1
                self.last_spawn_time = current_time

    def update(self):
        global is_restarting
        time = pygame.time.get_ticks()
        if self.isActive:

            self.add_enemies()

            for enemy in self.enemies:
                enemy.act()

            if len(self.enemies) == 0 and self.enemies_added == self.enemies_number:
                self.isActive = False
                is_restarting = False
                self.last_restart_time = time

    def restart_waves(self):
        global is_restarting
        global delay

        time = pygame.time.get_ticks()

        self.enemies_dictionary_iteratable = self.enemies_dictionary.copy()
        self.enemies.clear()
        self.last_spawn_time = 0
        self.enemies_added = 0
        self.enemies_number = sum(self.enemies_dictionary.values())

        print(f"{self.enemies_dictionary}")
        life_mod.life = life_mod.max_life
        player_mod.player_spawn()
        player_mod.player_render()

        self.last_restart_time = time

        is_restarting = True
