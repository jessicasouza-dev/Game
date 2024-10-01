import pygame
import screen as scrn_module

temporary_floor_color = (0, 0, 0)

floors_amount = 5

floor_size_y = scrn_module.screen.get_height() / (floors_amount + 1)
gap_size = (scrn_module.screen.get_height() - (floors_amount * floor_size_y)) / (floors_amount + 1)
floor_size_x = scrn_module.screen.get_width()

# array storing positional information about each layer as rect values
floors_rect_list = []

# array storing only the bottom y positional value of each layer for easier access in other functions and mechanics
# basically a list with the coordinates of the ground of each floor
floors_bottom_y_list = []

def create_floors():
    for n in range(floors_amount):
        next_y = (n * (floor_size_y + gap_size)) + gap_size
        floor_position = pygame.Rect(scrn_module.left_limit, next_y, floor_size_x, floor_size_y)
        floors_rect_list.append(floor_position)
        floors_bottom_y_list.append(floor_position.bottom)

# blits the empty screens depicting each row to the main gameplay screen
# only call this function after all things that must be rendered in floor sub-screens have been rendered
def render_floors():
    for n in range(len(floors_rect_list)):
        pygame.draw.rect(scrn_module.screen, temporary_floor_color, floors_rect_list[n])