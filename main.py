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
COLOR_GOLD = (255, 215, 0)
COLOR_DARK_BLUE = (7, 22, 46)
COLOR_BLUEISH_GREEN = (11, 128, 68)

folder_path = os.path.dirname(__file__)
os.chdir(folder_path)

screen = scrn_mod.screen
temporary_screen_color = (252, 252, 252)
player_move_left = player_move_right = player_move_up = player_move_down = player_shoot = spacebar = False

pygame.init()

pygame.mixer.init()
sound_player_shot = pygame.mixer.Sound('assets/laser-shot-ingame-230500.mp3')
sound_victory = pygame.mixer.Sound('assets/achievement-video-game-type-1-230515.mp3')

# victory text
victory_font = pygame.font.Font('PressStart2P.ttf', 20)
victory_text = victory_font.render('VICTORY!!!', True, COLOR_WHITE, COLOR_BLACK)
victory_text_rect = victory_text.get_rect()
victory_text_rect.center = (scrn_mod.screen.get_width() / 2, scrn_mod.screen.get_height() / 2)

floor_mod.create_floors()
player_mod.player_spawn()
power_up_mod.randomize_bundles()

DELAY = 5000

game_loop = True

wave_config1 = {
    'Shooter': 0,
    'Enemy': 20,
    'Sniper': 0
}

wave_config2 = {
    'Shooter': 20,
    'Enemy': 30,
    'Sniper': 0
}

wave_config3 = {
    'Shooter': 30,
    'Enemy': 40,
    'Sniper': 20
}

wave1 = wave_mod.Wave(wave_config1)
wave2 = wave_mod.Wave(wave_config2)
wave3 = wave_mod.Wave(wave_config3)
waves = [wave1, wave2, wave3]

shoot_direction = 'right'
sound_victory_played = False

BG = pygame.image.load("assets/bg2.png")
BG = pygame.transform.scale(BG, (720, 720))
image = pygame.image.load("assets/button background.png")
image = pygame.transform.scale(image, (300, 100))


def get_font_title(size):
    return pygame.font.Font("assets/fonts/Danger_Diabolik.ttf", size)

def get_font_button(size):
    return pygame.font.Font("assets/fonts/windows_command_prompt.ttf", size)



def main_menu():
    pygame.display.set_caption("Monster Mania")
    screen.blit(BG, (0, 0))

    while True:
        menu_mouse_pos = pygame.mouse.get_pos()

        monster_text = get_font_title(60).render("M o n s t e r", True, COLOR_BLUEISH_GREEN)
        monster_rect = monster_text.get_rect(center=(screen.get_width()/2, screen.get_height()/2 - 100))

        mania_text = get_font_title(60).render("M a n i a", True, COLOR_BLUEISH_GREEN)
        mania_rect = monster_text.get_rect(center=(monster_rect.centerx + mania_text.get_rect().width/4, monster_rect.y + 80))

        start_text = get_font_title(20).render("p r e s s   a n y   k e y   t o   s t a r t", True, COLOR_BLUEISH_GREEN)
        start_rect = start_text.get_rect(center=(screen.get_width() / 2, mania_rect.y + 200))

        #play_button = button_mod.Button(image, pos=(350, 350),text_input="PLAY", font=get_font_button(75), base_color=scrn_mod.COLOR_WHITE, hovering_color=scrn_mod.COLOR_WHITE)

        screen.blit(monster_text, monster_rect)
        screen.blit(mania_text, mania_rect)
        screen.blit(start_text, start_rect)
        #play_button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                game()

        pygame.display.update()


# main loop
def game():
    global player_move_down, player_move_left, player_move_right, player_move_up, player_shoot, sound_victory_played
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
                    sound_player_shot.play()
                    player_shoot = True
                if event.key == pygame.K_DOWN:
                    sound_player_shot.play()
                    shoot_direction = 'down'
                    player_shoot = True
                if event.key == pygame.K_LEFT:
                    sound_player_shot.play()
                    shoot_direction = 'left'
                    player_shoot = True
                if event.key == pygame.K_RIGHT:
                    sound_player_shot.play()
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

            if sound_victory_played == False:
                sound_victory.play()
                sound_victory_played = True

        for enemy in wave_controller_mod.current_wave.enemies:
            if enemy.life <= 0:
                enemy.die()
                wave_controller_mod.current_wave.enemies.remove(enemy)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

main_menu()
