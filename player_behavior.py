import pygame
import floors as floor_mod

player_color_temporary = (0, 252, 0)

current_surface = 3

#player sizes
PLAYER_WIDTH = 32
PLAYER_HEIGHT = 64

#player movement speed, could be changed by power-ups once those are implemented
player_move_speed = 5

player = pygame.rect.Rect(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
player_pos = pygame.Rect(50, 50, 50, 50)

player_visible = True

def player_spawn():
    global current_surface
    surface = floor_mod.floors_list[current_surface]

    player_pos.centerx = surface.get_width() / 2
    player_pos.bottom = surface.get_height()
    current_surface = 2

def player_render():
    surface = floor_mod.floors_list[current_surface]
    if player_visible == True:
        pygame.draw.rect(surface, player_color_temporary, player_pos)


def player_movement(player_move_left, player_move_right, player_move_up, player_move_down):
    global current_surface
    surface = floor_mod.floors_list[current_surface]

    # if movement boolean values match, move player position
    if player_move_left == True and player_move_right == False:
        player_pos.x -= player_move_speed
    if player_move_right == True and player_move_left == False:
        player_pos.x += player_move_speed

    # if player is out of bounds, relocate to valid position
    if player.left < surface.get_rect().left:
        player.left = surface.get_rect().left
    if player.left > surface.get_rect().right:
        player.left = surface.get_rect().right