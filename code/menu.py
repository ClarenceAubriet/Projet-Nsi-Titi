import pygame
from screen import Screen

from couleur import Couleur

class Menu:
    def __init__(self, screen: Screen):
        self.screen: Screen = screen
        self.fond_menu = pygame.image.load("enigma/assets/images/Fond_menu.jpeg")
        self.fond_autre = pygame.image.load("enigma/assets/images/Fond_autre.jpeg")
        self.fond_menu = pygame.transform.scale(self.fond_menu, self.screen.get_size())
        self.font = pygame.font.Font(None, 48)
        self.Musique = False
        self.couleur = Couleur()

    def draw_menu(self):
        self.screen.display.blit(self.fond_menu, (0, 0))

    def draw_credits(self):
        self.screen.display.blit(self.fond_autre, (0,-10))

        text = self.font.render("Paul est mort", True, self.couleur.WHITE)
        self.screen.display.blit(text, (50, 250))

    def draw_options(self):
        self.screen.display.blit(self.fond_autre, (0,-10))
        text1 = self.font.render("OPTIONS", True, self.couleur.RED)
        self.screen.display.blit(text1,(self.screen.get_size()[0]//2 - 100,100))
        text2 = self.font.render("Mouvements : ZQSD", True, self.couleur.WHITE)
        self.screen.display.blit(text2,(50,175))
        text3 = self.font.render("Interagir : E", True, self.couleur.WHITE)
        self.screen.display.blit(text3,(50,225))
        text4 = self.font.render("Musique :", True, self.couleur.WHITE)
        self.screen.display.blit(text4,(50,275))
