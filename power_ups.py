import pygame
import player_shots as shots_mod
import floors as floor_mod
import player_behavior as player_mod
import life as life_mod
import math

def powerup_damageup():
    # +10% damage, additively
    # size up slightly
    # shot flight speed down slightly
    shots_mod.damage_value += 20
    if shots_mod.size_value * 1.1 <= floor_mod.floor_size_y * 0.8:
        shots_mod.size_value *= 1.1
    shots_mod.speed_value *= 0.9

def powerup_firerateup():
    # -25% shot cooldown, multiplicative
    shots_mod.cooldown_value *= 0.75
    round(shots_mod.cooldown_value)

def powerup_multishot():
    # +1 or +33% projectiles per shot, at the cost of -33% damage, multiplicative
    if shots_mod.multishot_value >= 3:
        shots_mod.multishot_value += round(shots_mod.multishot_value * 0.34)
    else:
        shots_mod.multishot_value += 1

    shots_mod.size_value *= 0.90
    shots_mod.damage_modifier *= 0.67
    shots_mod.inaccuracy_value += 1

def powerup_pierceup():
    # increases how many times each shot can go through an enemy/floor without beind destroyed
    shots_mod.pierce_value += 1

def powerup_move_speed():
    # +25% player sideways movement speed, additively
    player_mod.player_move_speed += player_mod.PLAYER_BASE_SPEED * 0.25
    round(player_mod.player_move_speed)

def powerup_climb_speed():
    # -20% up/down between floors movement cooldown, additively, down to a minimum of 5 frames
    player_mod.player_updown_cd -= player_mod.BASE_UPDOWN_CD * 0.2
    if player_mod.player_updown_cd < 5:
        player_mod.player_updown_cd = 5

def powerup_instaheal():
    #heal 30% of maximum health, rounded up
    life_mod.life += life_mod.max_life * 0.3
    life_mod.life = math.ceil(life_mod.life)
    if life_mod.life > life_mod.max_life:
        life_mod.life = life_mod.max_life

def powerup_full_heal():
    #heal back to maximum health
    life_mod.life = life_mod.max_life

def powerup_health_boost():
    #increase maximum health by 25, also heals by 25
    life_mod.max_life += 25
    life_mod.life += 25