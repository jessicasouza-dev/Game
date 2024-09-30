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

folder_path = os.path.dirname(__file__)
os.chdir(folder_path)

screen = scrn_mod.screen
temporary_screen_color = (252, 252, 252)
player_move_left = player_move_right = player_move_up = player_move_down = player_shoot = False


pygame.init()

floor_mod.create_floors()
player_mod.player_spawn()

# main loop
game_loop = True

while game_loop == True:
    screen.fill(temporary_screen_color)
    floor_mod.fill_floor_surfaces()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False
            pygame.quit()
        
        if event.type == pygame.KEYDOWN:
            #print('debug: key pressed')
            if event.key == pygame.K_a:
                player_move_left = True
                #print('debug: A press')
            if event.key == pygame.K_d:
                player_move_right = True
                #print('debug: D press')
            if event.key == pygame.K_w:
                player_move_up = True
                #print('debug: W press')
            if event.key == pygame.K_s:
                player_move_down = True
                #print('debug: S press')
            if event.key == pygame.K_SPACE:
                player_shoot = True
                #print('debug: spacebar press')
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player_move_left = False
                #print('debug: A release')
            if event.key == pygame.K_d:
                player_move_right = False
                #print('debug: D release')
            if event.key == pygame.K_w:
                player_move_up = False
                #print('debug: W release')
            if event.key == pygame.K_s:
                player_move_down = False
                #print('debug: S release')
            if event.key == pygame.K_SPACE:
                player_shoot = False
                #print('debug: spacebar release')

    player_mod.player_movement(player_move_left, player_move_right, player_move_up, player_move_down)
    for projectile in player_shots_mod.active_friendly_projectiles:
        projectile.move()
    
    player_mod.try_shooting(player_shoot)

    player_mod.player_render()

    # things rendered in any of the floor sub-screens go before this line
    floor_mod.render_floors()
    # things rendered in the entire screen go after this line

    for projectile in player_shots_mod.active_friendly_projectiles:
        projectile.render()  
    
    print(f'debug: number of player shots on screen: {len(player_shots_mod.active_friendly_projectiles)}')
    pygame.display.flip()
    pygame.time.Clock().tick(60)