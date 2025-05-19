import pygame
import time

from couleur import Couleur

class Button:
    
    def __init__(self, x, y, width, height, text=None, image=None, action=None, couleur_bouton=None):
        self.button_sound = pygame.mixer.Sound("enigma/assets/sound/Boutonsound.wav")
        self.text = text
        if image!= None:
            self.image = pygame.image.load(image).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
        self.font = pygame.font.Font(None, 36)
        self.couleur = Couleur()
        self.couleur_bouton = couleur_bouton
        self.cooldown = 0.3
        self.current_time = None
        self.last_click_time = 0


    def draw(self, screen):
        if self.couleur_bouton:
            pygame.draw.rect(screen, self.couleur_bouton, self.rect)
        if self.text:
            text_surface = self.font.render(self.text, True, self.couleur.WHITE)
            text_rect = text_surface.get_rect()
            text_rect.center = self.rect.center
            screen.blit(text_surface, text_rect)
        else:
            screen.blit(self.image, self.rect)
    
    def is_pressed(self):
        pos = pygame.mouse.get_pos()
        self.current_time = time.time()
        if self.rect.collidepoint(pos):
            if self.current_time - self.last_click_time >= self.cooldown:
                self.last_click_time = self.current_time
                self.action()
                self.button_sound.play()

    def toggle(self, bouton):
        if bouton.text == "On":
            bouton.text = "Off"
            bouton.couleur_bouton = self.couleur.RED
        else:
            bouton.text = "On"
            bouton.couleur_bouton = self.couleur.GREEN