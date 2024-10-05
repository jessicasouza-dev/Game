import pygame

import enemy
import screen as scrn_mod
import floors as floor_mod
import player_behavior as player_mod
import player_shots as player_shots_mod
import os
import enemy as enemy_mod
import waves as wave_mod
import life as life_mod
import power_ups as pwrup_mod

wave_config = {}

last_number = 0
current_wave = wave_mod.Wave(wave_config)
delay = 10000
last_time = 0

current_time = pygame.time.get_ticks()

pwrup_selection = False

wave_config1 = {
    'Shooter': 1,
    'Enemy': 0,
    'Sniper': 1
}

def control_waves(waves):
    global last_number
    global current_wave
    global delay
    global last_time
    global wave_config
    global pwrup_selection

    time = pygame.time.get_ticks()
    wave_config = waves[last_number].enemies_dictionary

    if last_number < len(waves):
        current_wave = waves[last_number]

        if current_wave.isActive == True:
            current_wave.update()
        else:
            if last_number + 1 <= len(waves) - 1 and time - last_time >= delay:
                print(time)
                print(last_time)
                last_number += 1
                current_wave = waves[last_number]
                last_time = time

        if last_number == len(waves) - 1 and current_wave.isActive == False:
            if pwrup_mod.pwrups_shuffled == False:
                pwrup_mod.randomize_bundles()
            pwrup_selection = True
            pwrup_mod.pwrups_picked = False
        else:
            pwrup_selection = False

def change_last_number():
    global last_number
    last_number = 0