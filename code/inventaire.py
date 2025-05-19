import pygame
from screen import Screen
from player import Player
from keylistener import KeyListener

class Inventaire:
    def __init__(self, screen_size, player):
        self.screen = Screen
        self.keylistener = KeyListener
        self.player = player
        self.items = []  
        self.images = []
        self.visible = False
        self.columns = 4
        self.rows = 3
        self.cell_size = 100
        self.padding = 10

        self.width = self.columns * self.cell_size + (self.columns + 1) * self.padding
        self.height = self.rows * self.cell_size + (self.rows + 1) * self.padding

        screen_w, screen_h = screen_size
        self.x = (screen_w - self.width) // 2
        self.y = (screen_h - self.height) // 2

        self.font = pygame.font.Font(None, 24)

    def toggle(self):
        self.visible = not self.visible

    def ajouter_item(self,liste_object_obtenue, item):
        if len(liste_object_obtenue) < self.columns * self.rows:
            if item == "truc":
                return
            image_item = f"enigma/assets/images/{item}.png"
            image = pygame.image.load(image_item)
            image = pygame.transform.scale(image, (self.cell_size - 10, self.cell_size - 10))  # Redimensionne l'image
            self.images.append(image)

    def draw(self, screen):
        if not self.visible:
            return
        if self.player.objets != []:
            print(self.player.objets)
            for objet in self.player.objets:
                self.ajouter_item(self.player.objets,objet)
        pygame.draw.rect(screen, (50, 50, 50), (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), 2)

        for index in range(len(self.items)):
            col = index % self.columns
            row = index // self.columns
            cx = self.x + self.padding + col * (self.cell_size + self.padding)
            cy = self.y + self.padding + row * (self.cell_size + self.padding)

            pygame.draw.rect(screen, (0, 0, 0), (cx, cy, self.cell_size, self.cell_size))
            pygame.draw.rect(screen, (255, 255, 255), (cx, cy, self.cell_size, self.cell_size), 2)

            image_rect = self.images[index].get_rect(center=(cx + self.cell_size // 2, cy + self.cell_size // 2))
            screen.blit(self.images[index], image_rect)


        for i in range(len(self.items), self.columns * self.rows):
            col = i % self.columns
            row = i // self.columns
            cx = self.x + self.padding + col * (self.cell_size + self.padding)
            cy = self.y + self.padding + row * (self.cell_size + self.padding)

            pygame.draw.rect(screen, (0, 0, 0), (cx, cy, self.cell_size, self.cell_size))
            pygame.draw.rect(screen, (255, 255, 255), (cx, cy, self.cell_size, self.cell_size), 2)
