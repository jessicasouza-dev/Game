import pygame
import floors as floor_mod
import player_behavior as player_mod
import player_shots as player_shots_mod
import screen as screen_mod
import random as random
import life as life_mod

active_projectiles = []
screen = screen_mod.screen

fireshot_sprite_1 = pygame.image.load('assets/fire_goblin_sprites/fireshot-1.png')
fireshot_sprite_2 = pygame.image.load('assets/fire_goblin_sprites/fireshot-2.png')
fireshot_sprites = [fireshot_sprite_1, fireshot_sprite_2]

pygame.mixer.init()
sound_enemy = pygame.mixer.Sound('assets/synth-shot-fx-by-alien-i-trust-9-245434.mp3')

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
        self.rect = pygame.Rect(x, y, 50, 50)
        self.rect.centerx = x
        self.rect.centery = y
        self.damage = 25
        self.spritesheet = fireshot_sprites
        self.sprite_index = 0
        self.sprite = fireshot_sprite_1

    def update(self):
        self.render()
        self.move()
        self.hurt()

    def render(self):
        self.sprite = pygame.transform.scale(self.sprite, (50, 50))
        screen.blit(self.sprite, self.rect)

    def move(self):
        self.sprite_index = (self.sprite_index + 1) % 2
        self.sprite = fireshot_sprites[self.sprite_index]
        if self.trajectory == 'left':
            self.sprite = pygame.transform.flip(self.sprite, True, False)
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
            life_mod.lose_life(self.damage)
            self.destroy()


class VerticalShot(Shot):
    def __init__(self, x, y, speed, surface, direction, enemy, player):
        super().__init__(x, y, speed, surface, direction, enemy)
        self.player = player
        self.damage = 15

    def move(self):
        self.sprite_index = (self.sprite_index + 1) % 2
        self.sprite = fireshot_sprites[self.sprite_index]

        if self.player.current_layer >= self.enemy.current_layer:
            self.rect.centery += self.speed
            self.sprite = pygame.transform.rotate(self.sprite, 270)
        else:
            self.rect.centery -= self.speed
            self.sprite = pygame.transform.rotate(self.sprite, 90)

        if self.rect.top < screen.get_rect().top or self.rect.bottom > screen.get_rect().bottom:
            self.destroy()

