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

last_number = 0
current_wave = wave_mod.Wave(1, enemy, 2, "Enemy")
delay = 10000
last_time = 0

current_time = pygame.time.get_ticks()

def control_waves(waves):
    global last_number
    global current_wave
    global delay
    global last_time

    time = pygame.time.get_ticks()

    if last_number + 1 <= len(waves) - 1:
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
        print("wave acabou")
        
def change_last_number():
    global last_number
    last_number = 0