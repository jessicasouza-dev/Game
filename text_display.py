import pygame
import power_ups as pwrup_mod
import player_behavior as player_mod
import wave_controller as wave_control_mod
import floors as floor_mod
import screen as screen_mod

screen = screen_mod.screen
upgrade_textbox_font = pygame.font.Font('assets\3_Minecraft-Bold.otf')
textbox_color = (64, 0, 20)

powerup_textbox_firsthalf = pygame.Rect(0, 0, 0, 0)
powerup_textbox_secondhalf = pygame.Rect(0, 0, 0, 0)

def display_powerup_info():

    text_1 = pwrup_mod.display_text_1
    text_2 = pwrup_mod.display_text_2

    powerup_textbox_firsthalf.width = floor_mod.floor_size_x / 3
    powerup_textbox_secondhalf.width = floor_mod.floor_size_x / 3
    powerup_textbox_firsthalf.height = floor_mod.floor_size_y * (3/4)
    powerup_textbox_secondhalf.height = floor_mod.floor_size_y * (3/4)
    powerup_textbox_firsthalf.right = floor_mod.floor_size_x / 2 - 10
    powerup_textbox_secondhalf.left = floor_mod.floor_size_x / 2 + 10
    if player_mod.player_pos.centery < floor_mod.floors_bottom_y_list[3]:
        powerup_textbox_firsthalf.bottom = floor_mod.floors_bottom_y_list[4]
        powerup_textbox_secondhalf.bottom = floor_mod.floors_bottom_y_list[4]
    else:
        powerup_textbox_firsthalf.bottom = floor_mod.floors_bottom_y_list[0]
        powerup_textbox_secondhalf.bottom = floor_mod.floors_bottom_y_list[0]
    
    pygame.draw.rect(screen, textbox_color, powerup_textbox_firsthalf)
    pygame.draw.rect(screen, textbox_color, powerup_textbox_secondhalf)