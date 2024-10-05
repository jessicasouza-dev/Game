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
delay = 5000
last_time = 0

current_time = pygame.time.get_ticks()

is_power_picked = False

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
            print(f"debug wave: IS ACTIVE power picked is {is_power_picked}")
            current_wave.update()
        else:
            if last_number + 1 <= len(waves) - 1:

                if is_power_picked == False:
                    print(f"debug if: power picked is {is_power_picked}")
                    if pwrup_mod.pwrups_shuffled == False:
                        pwrup_mod.randomize_bundles()
                    pwrup_mod.pwrups_picked = False

                else:
                    print(f"debug else: power picked is {is_power_picked}")
                    last_number += 1
                    current_wave = waves[last_number]
                    last_time = time


        if last_number == len(waves) - 1 and current_wave.isActive == False:
            print("waves acabaram")

def change_last_number():
    global last_number
    last_number = 0