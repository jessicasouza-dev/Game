import pygame
import player_shots as player_shots_mod
import enemy as enemy_mod
import player_behavior as player_mod
import screen as scrn_mod
import floors as floor_mod

life = 100
max_life = 100

def show_life():
    global life, max_life
    bar_width = 200
    bar_height = 30
    bar_x = scrn_mod.screen.get_width() - 250 
    bar_y = 50 

    current_bar_width = int((life / max_life) * bar_width)
    
    life_color = scrn_mod.COLOR_GREEN
    background_color = scrn_mod.COLOR_RED

    pygame.draw.rect(scrn_mod.screen, background_color, (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(scrn_mod.screen, life_color, (bar_x, bar_y, current_bar_width, bar_height))

    life_font = pygame.font.Font(None, 30)
    life_text = life_font.render(f"Life: {life}", True, scrn_mod.COLOR_WHITE, scrn_mod.COLOR_BLACK)
    scrn_mod.screen.blit(life_text, (bar_x + 60, bar_y - 20))
    
    
    
def lose_life():
    global life
    life -= 20
    if life == 0 or life < 0:
        life = 0
        