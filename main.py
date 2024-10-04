#Isabela Braga Dutra Buleje 
#João Pedro Telles Paes 2415310011
#Jessica Rodrigues de Souza
#2024

import pygame, sys
import screen as scrn_mod
import floors as floor_mod
import player_behavior as player_mod
import player_shots as player_shots_mod
import os
import enemy as enemy_mod
import life as life_mod
import wave_controller as wave_controller_mod
import wave as wave_mod
import button as button_mod

folder_path = os.path.dirname(__file__)
os.chdir(folder_path)

screen = scrn_mod.screen
temporary_screen_color = (252, 252, 252)
player_move_left = player_move_right = player_move_up = player_move_down = player_shoot = False


pygame.init()

floor_mod.create_floors()
player_mod.player_spawn()

#Temporary images
BG = pygame.image.load("assets/background.jpg")
BG = pygame.transform.scale(BG, (720, 720))
image = pygame.image.load("assets/button background.png")
image = pygame.transform.scale(image, (300, 100))


enemy = enemy_mod.Shooter(0, floor_mod.floors_bottom_y_list[1], enemy_mod.enemy_color_temporary, 5, screen, "right", player_mod.player_pos, 2)
enemy2 = enemy_mod.Enemy(0, floor_mod.floors_bottom_y_list[1], player_mod.player_color_temporary, 5, screen, "right", player_mod.player_pos, 2)
wave1 = wave_mod.Wave(1, enemy, 2, "Shooter")
wave2 = wave_mod.Wave(3, enemy2, 2, "Enemy")
wave3 = wave_mod.Wave(5, enemy2, 2, "Enemy")
waves = [wave1, wave2, wave3]

def get_font(size):
    return pygame.font.Font("assets\Love Roti.ttf",80)

def main_menu():
    pygame.display.set_caption("Menu")
    screen.blit(BG, (0,0))

    
    while True:
        menu_mouse_pos = pygame.mouse.get_pos()
    
        
        menu_text = get_font(100).render("Main Menu", True, scrn_mod.COLOR_BLACK)
        menu_rect = menu_text.get_rect(center = (350,200))
        
        play_button = button_mod.Button(image, pos = (350,350), 
                                        text_input = "PLAY", font = get_font, base_color = scrn_mod.COLOR_WHITE,
                                        hovering_color = scrn_mod.COLOR_WHITE)
        
        screen.blit(menu_text, menu_rect)
        play_button.update(screen)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(menu_mouse_pos):
                    game()
                
        pygame.display.update()
                 
        
def game():
    global player_move_left, player_move_right, player_move_up, player_move_down, player_shoot
    #main loop
    game_loop = True

    while game_loop == True:
        screen.fill(temporary_screen_color)
        floor_mod.render_floors()

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
        life_mod.show_life()
        player_mod.player_render()
        wave_controller_mod.control_waves(waves)

        for projectile in player_shots_mod.active_friendly_projectiles:
            projectile.render()
            projectile.kill(wave_controller_mod.current_wave)
            
        if life_mod.life == 0:
            wave1.restart_waves()
            life_mod.life = life_mod.max_life

        pygame.display.flip()
        pygame.time.Clock().tick(60)
        
main_menu()