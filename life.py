import pygame
import player_shots as player_shots_mod
import enemy as players_shots_mod
import player_behavior as player_mod
import screen as scrn_mod


life = 100

def show_life():
    global life
    life_font = pygame.font.Font(None, 80)
    life_text = life_font.render(f"Life: {life}", True, scrn_mod.COLOR_WHITE, scrn_mod.COLOR_BLACK)
    life_text_rect = life_text.get_rect()
    life_text_rect.center = (scrn_mod.screen.get_width() - 120, 50)
    
    
    scrn_mod.screen.blit(life_text, life_text_rect)
    
def lose_life():
    global life
    life -= 20
    if life == 0 or life < 0:
        player_mod.player_death()
        life = 0
        