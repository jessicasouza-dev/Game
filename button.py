import pygame, sys
import screen as scrn_mod

screen = scrn_mod.screen

#Main menu code, not executed yet
#Temporary images
BG = pygame.image.load("assets/background.jpg")
BG = pygame.transform.scale(BG, (720, 720))
image = pygame.image.load("assets/button background.png")
image = pygame.transform.scale(image, (300, 100))

def get_font(size):
    return pygame.font.Font("assets\Love Roti.ttf",80)

def main_menu():
    pygame.display.set_caption("Menu")
    screen.blit(BG, (0,0))

    
    while True:
        menu_mouse_pos = pygame.mouse.get_pos()
    
        
        menu_text = get_font(100).render("Main Menu", True, scrn_mod.COLOR_BLACK)
        menu_rect = menu_text.get_rect(center = (350,200))
        
        play_button = Button(image, pos = (350,350), 
                                        text_input = "PLAY", font = get_font(75), base_color = scrn_mod.COLOR_WHITE,
                                        hovering_color = scrn_mod.COLOR_WHITE)
        
        screen.blit(menu_text, menu_rect)
        play_button.update(screen)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(menu_mouse_pos):
                    game()
                
        pygame.display.update()
     
class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = pygame.font.Font(None, 75)
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
            
        self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center = (self.x_pos, self.y_pos))
        
    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
        
    def check_for_input(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def change_color(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)