import pygame

screen_size = 600, 760
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Game')

background = pygame.Surface(screen.get_size())
background = background.convert()

bottom_limit = screen_size[1]
top_limit = 0