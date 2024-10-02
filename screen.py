import pygame

screen_size = 720, 720
screen = pygame.display.set_mode(screen_size)

pygame.display.set_caption('Game')

background = pygame.Surface(screen.get_size())
background = background.convert()

bottom_limit = screen_size[1]
top_limit = 0
left_limit = 0
right_limit = screen_size[0]


COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (252, 252, 252)
COLOR_GREEN = (35, 142, 35)
COLOR_YELLOW = (252, 252, 0)
COLOR_ORANGE = (252, 165, 0)
COLOR_RED = (252, 0, 0)
COLOR_BLUE = (50, 153, 204)
