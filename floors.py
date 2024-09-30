import pygame
import screen as scrn_module

floor_width = scrn_module.screen.get_width() 
floor_height = 15

wall_width = 14
wall_height = scrn_module.screen.get_height()

surface = scrn_module.screen
color_white = (255, 255, 255)

rows = 6
intermediate_rows = rows - 2

total_height_of_floors = rows * floor_height
available_space = scrn_module.bottom_limit - scrn_module.top_limit - (2 * floor_height)

gap = available_space // (intermediate_rows + 1)

class Floors:
    #Creates different floors with equal gaps between them
    def __init__(self, rows, columns):
        self.width = floor_width
        self.height = floor_height
        self.color = color_white
        self.rows = rows
        self.columns = columns
        self.surface = scrn_module.screen
        self.floors = [] 
        self.create_floors()
        
    def create_floors(self):
        first_y = scrn_module.top_limit
        rect = pygame.Rect(0, first_y, self.width, self.height)
        self.floors.append(rect)
        
        last_y = scrn_module.bottom_limit - floor_height
        rect = pygame.Rect(0, last_y, self.width, self.height)
        self.floors.append(rect)
        
        for i in range(self.rows):
            y = scrn_module.top_limit + floor_height + i * gap
            rect = pygame.Rect(0, y, self.width, self.height)
            self.floors.append(rect)
            
    def draw_floors(self):
        for rect in self.floors:
            pygame.draw.rect(self.surface, self.color, rect, width = 0)

class Walls:
    # Makes the Left and Right Walls
    def __init__(self):
        self.width = wall_width
        self.height = wall_height
        self.color = color_white
        self.surface = scrn_module.screen
        self.walls = [] 
        self.create_walls()
        
    def create_walls(self):
        left_wall_rect = pygame.Rect(0, 0, self.width, self.height)
        self.walls.append(left_wall_rect)
        
        right_wall_x = scrn_module.screen.get_width() - self.width
        right_wall_rect = pygame.Rect(right_wall_x, 0, self.width, self.height)
        self.walls.append(right_wall_rect)
        
    def draw_walls(self):
        for rect in self.walls:
            pygame.draw.rect(self.surface, self.color, rect, width = 0)