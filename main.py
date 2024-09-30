#Isabela Braga Dutra Buleje 
#João Pedro Telles Paes 2415310011
#Jessica Rodrigues de Souza
#2024

import pygame
import screen as scrn_module
import floors as floor_module
import os

folder_path = os.path.dirname(__file__)
os.chdir(folder_path)

pygame.init()

floors = floor_module.Floors(rows = 5, columns = 1)
walls = floor_module.Walls()

# main loop
game_loop = True

while game_loop == True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False
            pygame.quit()
    
    floors.draw_floors()
    walls.draw_walls()
    pygame.display.flip()