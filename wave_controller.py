import pygame

import enemy
import screen as scrn_mod
import floors as floor_mod
import player_behavior as player_mod
import player_shots as player_shots_mod
import os
import enemy as enemy_mod
import waves
import waves as wave_mod
import life as life_mod
import power_ups as pwrup_mod

wave_config = {}

last_number = 0
current_wave = wave_mod.Wave(wave_config)
delay = 2500
last_time = 0

is_over = False

current_time = pygame.time.get_ticks()

is_power_picked = False

def control_waves(waves):
    global last_number
    global current_wave
    global delay
    global is_power_picked
    global last_time
    global wave_config
    global is_over
    global pwrup_selection

    time = pygame.time.get_ticks()
    wave_config = waves[last_number].enemies_dictionary

    if last_number >= 3:
        wave_mod.health_multiplier = pow(1.40, last_number - 2)
    else:
        wave_mod.health_multiplier = 1

    if last_number < len(waves):
        current_wave = waves[last_number]

        if current_wave.isActive == True:
            current_wave.update()
            is_power_picked = False
            pwrup_mod.pwrups_shuffled = False
        else:
            if last_number + 1 <= len(waves):

                if is_power_picked == False and wave_mod.is_restarting == False:
                    if pwrup_mod.pwrups_shuffled == False:
                        pwrup_mod.randomize_bundles()
                    pwrup_mod.pwrups_picked = False

                else:
                    if time - last_time >= delay:
                        last_number += 1
                        current_wave = waves[last_number]
                        last_time = time


        if last_number == len(waves) - 1 and current_wave.isActive == False:
            is_over = True

def change_last_number():
    global last_number
    last_number = 0