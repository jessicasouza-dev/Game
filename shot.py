import pygame
import floors as floor_mod
import player_behavior as player_mod
import player_shots as player_shots_mod
import screen as screen_mod
import random as random
import life as life_mod

active_projectiles = []
screen = screen_mod.screen


class Shot:
    def __init__(self, x, y, speed, surface, direction, enemy):
        super().__init__()

        self.x = x
        self.y = y
        self.speed = speed
        self.surface = surface
        self.trajectory = direction
        self.enemy = enemy
        self.color = (255, 255, 255)
        self.rect = pygame.Rect(x, y, 10, 10)

    def update(self):
        self.render()
        self.move()
        self.hurt()

    def render(self):
        pygame.draw.rect(self.surface, self.color, self.rect)

    def move(self):
        if self.trajectory == 'left':
            self.rect.centerx -= self.speed
        elif self.trajectory == 'right':
            self.rect.centerx += self.speed

        if self.rect.right < 0 or self.rect.left > screen.get_rect().right:
            self.destroy()

    def destroy(self):
        if self in active_projectiles:
            active_projectiles.remove(self)

    def hurt(self):
        if self.rect.colliderect(player_mod.player_pos):
            life_mod.lose_life()
            self.destroy()


class VerticalShot(Shot):
    def __init__(self, x, y, speed, surface, direction, enemy, player):
        super().__init__(x, y, speed, surface, direction, enemy)
        self.player = player

    def move(self):
        if self.player.current_layer >= self.enemy.current_layer:
            self.rect.centery += self.speed
        else:
            self.rect.centery -= self.speed

        if self.rect.top < screen.get_rect().top or self.rect.bottom > screen.get_rect().bottom:
            self.destroy()
