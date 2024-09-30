import pygame
import floors as floor_mod

player_color_temporary = (0, 252, 0)

current_surface = 3

# player sizes
PLAYER_WIDTH = 32
PLAYER_HEIGHT = 64

# player movement speed, could be changed by power-ups once those are implemented
PLAYER_BASE_SPEED = 5
player_move_speed = PLAYER_BASE_SPEED

# player cooldown time in frames for moving up or down layers, also possible to change
# initially 1/2 of a second
BASE_UPDOWN_CD = 30
player_updown_cd = BASE_UPDOWN_CD
current_updown_cd = 0

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
    global current_updown_cd
    surface = floor_mod.floors_list[current_surface]

    # handle cooldown frames for up/down movement

    # if movement boolean values match, move player position
    if player_move_left == True and player_move_right == False:
        player_pos.x -= player_move_speed
    if player_move_right == True and player_move_left == False:
        player_pos.x += player_move_speed

    # if player is out of bounds, relocate to valid position
    if player_pos.left < surface.get_rect().left:
        player_pos.left = surface.get_rect().left
    if player_pos.right > surface.get_rect().right:
        player_pos.right = surface.get_rect().right

    if current_updown_cd == 0:
        #print('debug: up/down movement possible')
        if player_move_up == True and player_move_down == False:
            #print('debug: attempting move up')
            if current_surface != 0:
                current_surface -= 1
                current_updown_cd = player_updown_cd
        if player_move_down == True and player_move_up == False:
            if current_surface != 4:
                current_surface += 1
                current_updown_cd = player_updown_cd
    else:
        current_updown_cd -= 1