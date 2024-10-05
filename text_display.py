import pygame
import power_ups as pwrup_mod
import player_behavior as player_mod
import wave_controller as wave_control_mod
import floors as floor_mod
import screen as screen_mod

screen = screen_mod.screen
textbox_color = (64, 0, 20)

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)


def display_powerup_info():
    text_1 = pwrup_mod.display_text_1
    text_2 = pwrup_mod.display_text_2

    power_font = pygame.font.Font('PressStart2P.ttf', 16)

    power_text_1 = power_font.render(text_1, True, COLOR_WHITE, COLOR_BLACK)
    power_text_rect_1 = power_text_1.get_rect()
    power_text_rect_1.center = (floor_mod.floor_size_x / 2, floor_mod.floors_bottom_y_list[4])


    power_text_2 = power_font.render(text_2, True, COLOR_WHITE, COLOR_BLACK)
    power_text_rect_2 = power_text_2.get_rect()
    power_text_rect_2.center = (
    floor_mod.floor_size_x / 2, power_text_rect_1.bottom + 20)


    if player_mod.player_pos.centery < floor_mod.floors_bottom_y_list[3]:
        power_text_rect_1.top = floor_mod.floors_bottom_y_list[3] + floor_mod.gap_size + 20
        power_text_rect_2.top = power_text_rect_1.bottom + 20
    else:
        power_text_rect_1.bottom = floor_mod.floors_bottom_y_list[0] - floor_mod.gap_size - 20
        power_text_rect_2.bottom = power_text_rect_1.bottom + 20

    screen.blit(power_text_1, power_text_rect_1)
    screen.blit(power_text_2, power_text_rect_2)
