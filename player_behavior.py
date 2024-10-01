import pygame
import floors as floor_mod
import player_shots as player_shots_mod
import screen as screen_mod

player_color_temporary = (0, 252, 0)

current_layer = 2

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

shooting_cooldown = 0
current_direction = 'right'

player = pygame.rect.Rect(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
player_pos = pygame.Rect(50, 50, 50, floor_mod.floor_size_y)

player_visible = True
screen = screen_mod.screen

def player_spawn():
    global current_layer

    player_pos.centerx = screen.get_width() / 2
    player_pos.bottom = floor_mod.floors_bottom_y_list[current_layer]
    current_layer = 2

def player_render():
    if player_visible == True:
        pygame.draw.rect(screen, player_color_temporary, player_pos)

def player_death():
    global player_pos

    player_pos = pygame.Rect(0, 0, 0, 0)


def player_movement(player_move_left, player_move_right, player_move_up, player_move_down):
    global current_layer
    global current_updown_cd
    global current_direction

    # if movement boolean values match, move player position
    if player_move_left == True and player_move_right == False:
        player_pos.x -= player_move_speed
        current_direction = 'left'
    if player_move_right == True and player_move_left == False:
        player_pos.x += player_move_speed
        current_direction = 'right'

    # if player is out of bounds, relocate to valid position
    if player_pos.left < screen.get_rect().left:
        player_pos.left = screen.get_rect().left
    if player_pos.right > screen.get_rect().right:
        player_pos.right = screen.get_rect().right

    # up/down movement, and handling of cooldown frames for said movement
    if current_updown_cd == 0:
        #print('debug: up/down movement possible')
        if player_move_up == True and player_move_down == False:
            #print('debug: attempting move up')
            if current_layer != 0:
                current_layer -= 1
                current_updown_cd = player_updown_cd
        if player_move_down == True and player_move_up == False:
            if current_layer != 4:
                current_layer += 1
                current_updown_cd = player_updown_cd
    else:
        current_updown_cd -= 1

    player_pos.bottom = floor_mod.floors_bottom_y_list[current_layer]

def try_shooting(is_shooting):
    global shooting_cooldown
    #print('debug: running try_shooting function')

    if shooting_cooldown == 0:
        if is_shooting:
            y = player_pos.centery
            player_shots_mod.active_friendly_projectiles.append(player_shots_mod.player_projectile(player_pos.centerx, y, current_direction))
            shooting_cooldown = player_shots_mod.cooldown_value
        #print('debug: player ready to shoot')
    else:
        shooting_cooldown -= 1
        #print(f'debug: frames until shot cooldown is over: {shooting_cooldown}')