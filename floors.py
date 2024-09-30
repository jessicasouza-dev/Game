import pygame
import screen as scrn_module

temporary_floor_color = (0, 0, 0)

floors_amount = 5

floor_size_y = scrn_module.screen.get_height() / (floors_amount + 1)
gap_size = (scrn_module.screen.get_height() - (floors_amount * floor_size_y)) / (floors_amount + 1)
floor_size_x = scrn_module.screen.get_width()

# array stores each layer as a surface type object
floors_list = []

# array stores the positional values of each layer as a rect object
floors_pos_list = []
# adds the layer values to the empty surfaces array
def create_floors():
    for n in range(floors_amount):
        floor_surface = pygame.Surface((floor_size_x, floor_size_y))
        floors_list.append(floor_surface)

        next_y = (n * (floor_size_y + gap_size)) + gap_size
        floor_position = pygame.Rect(scrn_module.left_limit, next_y, floor_size_x, floor_size_y)
        floors_pos_list.append(floor_position)

# blits the empty screens depicting each row to the main gameplay screen
# only call this function after all things that must be rendered in floor sub-screens have been rendered
def render_floors():
    for n in range(len(floors_list)):
        scrn_module.screen.blit(floors_list[n], floors_pos_list[n])

def fill_floor_surfaces():
    for n in range(len(floors_list)):
        floors_list[n].fill(temporary_floor_color)