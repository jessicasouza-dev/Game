#Isabela Braga Dutra Buleje 
#João Pedro Telles Paes 2415310011
#Jessica Rodrigues de Souza
#2024

import pygame
import screen as scrn_mod
import floors as floor_mod
import player_behavior as player_mod
import player_shots as player_shots_mod
import os
import shot as shot_mod
import enemy as enemy_mod
import life as life_mod
import wave_controller as wave_controller_mod
import power_ups as power_up_mod
import waves as wave_mod
import wave_controller as wave_controller_mod
import text_display as textbox_mod

folder_path = os.path.dirname(__file__)
os.chdir(folder_path)

screen = scrn_mod.screen
temporary_screen_color = (252, 252, 252)
player_move_left = player_move_right = player_move_up = player_move_down = player_shoot = spacebar = False

pygame.init()

floor_mod.create_floors()
player_mod.player_spawn()
power_up_mod.randomize_bundles()

# instant power ups for the purposes of testing
None


shoot_direction = 'right'

# main loop
game_loop = True

wave1 = wave_mod.Wave(wave_controller_mod.wave_config1)
waves = [wave1]

while game_loop == True:

    screen.fill(temporary_screen_color)
    floor_mod.render_floors()
    spacebar = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False
            pygame.quit()
        
        if event.type == pygame.KEYDOWN:
            # movement controls
            if event.key == pygame.K_a:
                player_move_left = True
            if event.key == pygame.K_d:
                player_move_right = True
            if event.key == pygame.K_w:
                player_move_up = True
            if event.key == pygame.K_s:
                player_move_down = True
            if event.key == pygame.K_SPACE:
                spacebar = True


            # directional shooting controls
            if event.key == pygame.K_UP:
                shoot_direction = 'up'
                player_shoot = True
            if event.key == pygame.K_DOWN:
                shoot_direction = 'down'
                player_shoot = True
            if event.key == pygame.K_LEFT:
                shoot_direction = 'left'
                player_shoot = True
            if event.key == pygame.K_RIGHT:
                shoot_direction = 'right'
                player_shoot = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player_move_left = False
            if event.key == pygame.K_d:
                player_move_right = False
            if event.key == pygame.K_w:
                player_move_up = False
            if event.key == pygame.K_s:
                player_move_down = False
            if event.key == pygame.K_SPACE:
                player_shoot = False
            if event.key == pygame.K_UP:
                player_shoot = False
            if event.key == pygame.K_DOWN:
                player_shoot = False
            if event.key == pygame.K_LEFT:
                player_shoot = False
            if event.key == pygame.K_RIGHT:
                player_shoot = False

    player_mod.player_movement(player_move_left, player_move_right, player_move_up, player_move_down)
    for projectile in player_shots_mod.active_friendly_projectiles:
        projectile.move()

    player_mod.try_shooting(player_shoot, shoot_direction)
    life_mod.show_life()
    player_mod.player_render()
    wave_controller_mod.control_waves(waves)
    if wave_controller_mod.pwrup_selection == True:
        power_up_mod.do_selection(spacebar)
        textbox_mod.display_powerup_info()

    for projectile in player_shots_mod.active_friendly_projectiles:
        projectile.render()
        projectile.kill(wave_controller_mod.current_wave)

    for projectile in shot_mod.active_projectiles:
        projectile.update()


    if life_mod.life == 0:
        wave_controller_mod.current_wave.restart_waves()
        life_mod.life = life_mod.max_life
        wave_controller_mod.change_last_number()

    pygame.display.flip()
    pygame.time.Clock().tick(60)