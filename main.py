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
import shot as shot_mod
import enemy as enemy_mod
import life as life_mod
import wave_controller as wave_controller_mod
import power_ups as power_up_mod
import waves as wave_mod
import wave_controller as wave_controller_mod
import text_display as textbox_mod
import button as button_mod

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

folder_path = os.path.dirname(__file__)
os.chdir(folder_path)

screen = scrn_mod.screen
temporary_screen_color = (252, 252, 252)
player_move_left = player_move_right = player_move_up = player_move_down = player_shoot = spacebar = False

pygame.init()

# victory text
victory_font = pygame.font.Font('PressStart2P.ttf', 20)
victory_text = victory_font .render('VICTORY!!!', True, COLOR_WHITE, COLOR_BLACK)
victory_text_rect = victory_text.get_rect()
victory_text_rect.center = (scrn_mod.screen.get_width()/2, scrn_mod.screen.get_height()/2)

floor_mod.create_floors()
player_mod.player_spawn()
power_up_mod.randomize_bundles()

DELAY = 5000

game_loop = True

wave_config1 = {
    'Shooter': 10,
    'Enemy': 15,
    'Sniper': 5
}

wave_config2 = {
    'Shooter': 15,
    'Enemy': 20,
    'Sniper': 10
}

wave_config3 = {
    'Shooter': 20,
    'Enemy': 25,
    'Sniper': 15
}

wave1 = wave_mod.Wave(wave_config1)
wave2 = wave_mod.Wave(wave_config2)
wave3 = wave_mod.Wave(wave_config2)
waves = [wave1]


shoot_direction = 'right'

BG = pygame.image.load("assets/background.jpg")
BG = pygame.transform.scale(BG, (720, 720))
image = pygame.image.load("assets/button background.png")
image = pygame.transform.scale(image, (300, 100))

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
                                        text_input = "PLAY", font = get_font(75), base_color = scrn_mod.COLOR_WHITE,
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
     

# main loop
def game():
    global player_move_down, player_move_left, player_move_right, player_move_up, player_shoot
    global game_loop, shoot_direction
    while game_loop == True:

        time = pygame.time.get_ticks()

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

        if wave_controller_mod.is_power_picked == False and wave_controller_mod.current_wave.isActive == False and wave_controller_mod.is_over == False and wave_mod.is_restarting == False:
            power_up_mod.do_selection(spacebar)
            textbox_mod.display_powerup_info()

        for projectile in player_shots_mod.active_friendly_projectiles:
            projectile.render()
            projectile.kill(wave_controller_mod.current_wave)

        for projectile in shot_mod.active_projectiles:
            projectile.update()

        if life_mod.life == 0:

            if time - DELAY > wave_controller_mod.current_wave.last_restart_time:
                wave_controller_mod.current_wave.restart_waves()
                life_mod.life = life_mod.max_life
                wave_controller_mod.change_last_number()

        if wave_controller_mod.is_over == True:
            screen.fill(COLOR_BLACK)
            screen.blit(victory_text, victory_text_rect)

        pygame.display.flip()
        pygame.time.Clock().tick(60)
main_menu()