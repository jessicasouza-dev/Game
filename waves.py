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
health_multiplier = 1

# load enemy sprites
crawler_sprite_1 = pygame.image.load('assets/crawler_goblin_sprites/goblin_1.png')
crawler_sprite_2 = pygame.image.load('assets/crawler_goblin_sprites/goblin_2.png')
crawler_sprites = [crawler_sprite_1, crawler_sprite_2]

firegob_sprite_1 = pygame.image.load('assets/fire_goblin_sprites/fire goblin-1.png')
firegob_sprite_2 = pygame.image.load('assets/fire_goblin_sprites/fire goblin-2.png')
firegob_sprites = [firegob_sprite_1, firegob_sprite_2]

sniper_sprite_1 = pygame.image.load('assets/sniper_goblin_sprites/sniper goblin-1.png')
sniper_sprite_2 = pygame.image.load('assets/sniper_goblin_sprites/sniper goblin-2.png')
sniper_sprites = [sniper_sprite_1, sniper_sprite_2]

class Wave:
    def __init__(self, enemies_dictionary):
        super().__init__()

        self.last_restart_time = 0
        self.enemies_dictionary = enemies_dictionary
        self.enemies_dictionary_iteratable = self.enemies_dictionary.copy()
        self.spawn_delay = 500
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
                    enemy_instance = enemy.Shooter(0, floor, random.randint(2, 3),
                                                    scrn_mod.screen, "right", player_mod.player_pos, number, 250 * health_multiplier, firegob_sprites)
                elif enemy_class == 'Enemy':
                    enemy_instance = enemy.Enemy(0, floor, random.randint(4, 5),
                                                 scrn_mod.screen, "right", player_mod.player_pos, number, 300 * health_multiplier, crawler_sprites)
                elif enemy_class == 'Sniper':
                    enemy_instance = enemy.Sniper(0, floor, random.randint(2, 4),
                                                   scrn_mod.screen, "right", player_mod.player_pos, number, 400 * health_multiplier, sniper_sprites)

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

