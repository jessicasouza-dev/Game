#Isabela Braga Dutra Buleje 
#João Pedro Telles Paes 2415310011
#Jessica Rodrigues de Souza
#2024

import pygame
import screen as scrn_mod
import floors as floor_mod
import player_behavior as player_mod
import os

folder_path = os.path.dirname(__file__)
os.chdir(folder_path)

temporary_screen_color = (252, 252, 252)
player_move_left = player_move_right = player_move_up = player_move_down = False

pygame.init()

floor_mod.create_floors()
player_mod.player_spawn()

# main loop
game_loop = True

while game_loop == True:
    scrn_mod.screen.fill(temporary_screen_color)

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
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player_move_left = False
                #print('debug: A release')
            if event.key == pygame.K_d:
                player_move_right = False
                #print('debug: D release')

    player_mod.player_movement(player_move_left, player_move_right, player_move_up, player_move_down)

    player_mod.player_render()
    floor_mod.render_floors()
    floor_mod.fill_floor_surfaces()
    pygame.display.flip()

    pygame.time.Clock().tick(60)