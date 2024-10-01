import pygame
import floors as floor_mod
import player_shots as player_shots_mod
import screen as screen_mod

enemy_color_temporary = (0, 0, 252)

current_direction = 'right'
enemy_pos = pygame.Rect(50, 50, 50, floor_mod.floor_size_y)

ENEMY_WIDTH = 32
ENEMY_HEIGHT = 64

class Enemy:
    def __init__(self, x, y, color, speed, surface, direction):
        super().__init__()

        self.direction = direction
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.x = 0
        self.y = 0
        self.color = enemy_color_temporary
        self.speed = speed
        self.surface = surface
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.drawEnemy()
        self.wander()

    def drawEnemy(self):
        pygame.draw.rect(self.surface, self.color, self.rect, width=0)

    def wander(self):
        # Move the enemy in the current direction
        if self.direction == 'right':
            self.x += self.speed
            if self.x + self.width >= screen_mod.screen.get_width():  # Check if the enemy reaches the right edge
                self.x = screen_mod.screen.get_width() - self.width  # Set to the edge
                self.direction = 'left'  # Change direction to left
        else:  # Moving left
            self.x -= self.speed
            if self.x <= 0:  # Check if the enemy reaches the left edge
                self.x = 0  # Set to the edge
                self.direction = 'right'  # Change direction to right

        # Update the rect's position
        self.rect.x = self.x

    def kill(self, rect):
        if self.rect.colliderect(rect):
            print("KILL")

