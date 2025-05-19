import pygame
import random

from button import Button
from couleur import Couleur
from screen import Screen
from Collisions import Collisions
from entity import Entity

class Enigme:
    def __init__(self, nom, x, y, width, height, event, map = None):
        self.rect = pygame.Rect(x, y, width, height)
        self.event = event
        self.nom = nom
        self.sound_test = []
        self.sound_victoire = []
        self.liste_victoire = []
        self.button_sound1 = [pygame.mixer.Sound("enigma/assets/sound/son1.wav"),1]
        self.button_sound2 = [pygame.mixer.Sound("enigma/assets/sound/son2.wav"),2]
        self.button_sound3 = [pygame.mixer.Sound("enigma/assets/sound/son3.wav"),3]
        self.button_sound4 = [pygame.mixer.Sound("enigma/assets/sound/son4.wav"),4]
        self.button_sound5 = [pygame.mixer.Sound("enigma/assets/sound/son5.wav"),5]
        self.son=[self.button_sound1,self.button_sound2,self.button_sound3,self.button_sound4,self.button_sound5]
        self.sequence_en_cours = False
        self.map = map
        self.win_musique = False

    def sound(self):
        if self.nom == "musique aléatoire":
            self.index_son = 0
            self.sound_victoire = []
            self.liste_victoire = []
            for _ in range(5):
                son_choisie=random.choice(self.son)
                self.sound_victoire.append(son_choisie[0])
                self.liste_victoire.append(son_choisie[1])
            self.canal = pygame.mixer.Channel(0)
            self.sequence_en_cours = True
            self.sound_test = []

    def ajouter_son(self, valeur):
        self.sound_test.append(valeur)
        if len(self.sound_test) > 5:
            del self.sound_test[0]
        if self.sound_test == self.liste_victoire and self.win_musique == False:
            print("🎉 Énigme réussie ! 🎉")
            self.win_musique = True

    def mise_a_jour_sequence_sonore(self):
        if self.sequence_en_cours:
            if not self.canal.get_busy() and self.index_son < len(self.sound_victoire):
                self.canal.play(self.sound_victoire[self.index_son])
                self.index_son += 1
            elif self.index_son >= len(self.sound_victoire):
                self.sequence_en_cours = False

class EnigmeMusique:
    def __init__(self, numero, x, y, width, height, enigme_cible, event):
        self.event = event
        self.numero = numero 
        self.rect = pygame.Rect(x, y, width, height)
        self.enigme_cible = enigme_cible
        self.son = pygame.mixer.Sound(f"enigma/assets/sound/son{numero}.wav")

    def activer(self):
        self.son.play()
        self.enigme_cible.ajouter_son(self.numero)

class Caisse(Entity,Collisions):
    def __init__(self, screen: Screen, x: int, y: int):
        super().__init__(keylistener=None, screen=screen, x=x+16, y=y+16)
        self.image = pygame.image.load("enigma/assets/sprite/caisse_enigme.png").convert_alpha()
        self.base_y = y
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(x+16, y+16)
        self.rect.center = self.position
        self.hitbox = pygame.Rect(0, 0, 32, 32)
        self.hitbox.midbottom = self.rect.midbottom
        self.liste_test_plaque = []
        self.win = False

    def update(self):  
        self.rect.center = self.position
        self.hitbox.midbottom = self.rect.midbottom

    def try_push(self, dx: int, dy: int, obstacles: list[Collisions]) -> bool:
        future_hitbox = self.hitbox.copy()
        future_hitbox.x += dx
        future_hitbox.y += dy

        for obstacle in obstacles:
            if obstacle is not self and obstacle.check_collision(future_hitbox):
                return False

        self.position.x += dx
        self.position.y += dy
        self.rect.center = self.position
        self.hitbox.midbottom = self.rect.midbottom
        return True
    
    def test_plaque(self,numero,activation,nb_plaques):
        if len(self.liste_test_plaque) != nb_plaques:
            for _ in range(nb_plaques):
                self.liste_test_plaque.append(False)
        self.liste_test_plaque[numero]=activation
        if self.liste_test_plaque.count(True) == nb_plaques and self.win==False:
            self.win=True
            print("win")
        return

    def check_collision(self, obj_hitbox: pygame.Rect) -> bool:
        return self.hitbox.colliderect(obj_hitbox) 

class Plaque(): 
    def __init__(self, numero, x, y, width, height, enigme_cible, event):
        self.event = event
        self.numero = numero
        self.rect = pygame.Rect(x, y, width, height)
        self.enigme_cible = enigme_cible
        self.activation = False
        
    def update(self, player, caisses, nb_plaques):
        self.activation = any(caisse.hitbox.colliderect(self.rect) for caisse in caisses) or player.hitbox.colliderect(self.rect)
        self.enigme_cible.test_plaque(self.numero,self.activation,nb_plaques)

class Enigme_code:
    def __init__(self, screen: Screen):
        self.fond_autre = pygame.image.load("enigma/assets/images/Fond_autre.jpeg")
        self.cadre = pygame.image.load("enigma/assets/images/cadre.png")
        self.enigme = 0
        self.screen: Screen = screen
        self.couleur = Couleur()
        self.font = pygame.font.Font(None, 48)
        self.win = False
        self.win2 = False
        self.ecran =  pygame.image.load("enigma/assets/images/ecran_enigme_code.png").convert_alpha()
        self.cases = [pygame.Rect(self.screen.get_size()[0]/2-140, 200, 80, 50),
                      pygame.Rect(self.screen.get_size()[0]/2-40, 200, 80, 50),
                      pygame.Rect(self.screen.get_size()[0]/2+60, 200, 80, 50)
                      ]
        self.cases2 = [pygame.Rect(self.screen.get_size()[0]/2-40-150, 200, 80, 50),
                      pygame.Rect(self.screen.get_size()[0]/2-40-50, 200, 80, 50),
                      pygame.Rect(self.screen.get_size()[0]/2-40+50, 200, 80, 50),
                      pygame.Rect(self.screen.get_size()[0]/2-40+150, 200, 80, 50)
                      ]
        self.buttons = [(Button((self.screen.get_size()[0]/2-100)+ ((i - 1) % 3) * 100 - 50, 355 + ((i - 1) // 3) * 100, 100, 100,
                                image=f"enigma/assets/images/button_{i}.png", action=lambda chiffre=str(i): self.ajouter(chiffre))) for i in range(1,10)]
        self.buttons.append(Button(self.screen.get_size()[0]/2-50, 355 + 3 * 100, 100, 100,
                                image="enigma/assets/images/button_0.png", action=lambda: self.ajouter("0")))
        self.buttons.append((Button(self.screen.get_size()[0]/2-150, 355 + 3 * 100, 100, 100,
                                image="enigma/assets/images/button_suppr.png", action=lambda: self.suppr())))
        self.buttons.append((Button(self.screen.get_size()[0]/2+50, 355 + 3 * 100, 100, 100,
                                image="enigma/assets/images/button_validate.png", action=lambda: self.tester())))
        
        self.case_values = ["", "", ""]
        self.case_values2 = ["", "", "", ""]

    def suppr(self):
        if self.enigme == 0:
            for i in range(1,4):
                if self.case_values[-i]:
                    self.case_values[-i] = ""
                    break
        elif self.enigme == 1:
            for i in range(1,5):
                if self.case_values2[-i]:
                    self.case_values2[-i] = ""
                    break

    def ajouter(self,chiffre):
        if self.enigme == 0:
            for i in range(3):
                if not self.case_values[i]:
                    self.case_values[i] = chiffre
                    break
        elif self.enigme == 1: 
            for i in range(4):
                if not self.case_values2[i]:
                    self.case_values2[i] = chiffre
                    break
    
    def tester(self):
        if self.enigme == 0:
            if self.case_values == ['6', '9', '4']:
                self.win=True
            self.case_values = ["", "", ""]

        elif self.enigme == 1:
            if self.case_values2 == ['2', '1', '7', '8']:
                self.win2=True
            self.case_values2 = ["", "", "", ""]

    def draw(self):
        self.screen.display.blit(self.fond_autre, (0,-10))
        if self.enigme == 0:
            self.cadre = pygame.transform.scale(self.cadre, (410, 685))
            self.ecran = pygame.transform.scale(self.ecran, (350, 210))
            self.screen.display.blit(self.cadre, (self.screen.get_size()[0]/2-205, 100, 410, 685))
            self.screen.display.blit(self.ecran, (self.screen.get_size()[0]/2-175, 130, 350, 210))
            for i, case in enumerate(self.cases):
                pygame.draw.rect(self.screen.display,self.couleur.RED, case, 2)
                value = self.case_values[i] if self.case_values[i] else ""
                text = self.font.render(value, True, self.couleur.WHITE)
                self.screen.display.blit(text, (case.x + 30, case.y + 10))

        elif self.enigme == 1:
            self.cadre = pygame.transform.scale(self.cadre, (530, 730))
            self.ecran = pygame.transform.scale(self.ecran, (450, 270))
            self.screen.display.blit(self.cadre, (self.screen.get_size()[0]/2-265, 70, 510, 730))
            self.screen.display.blit(self.ecran, (self.screen.get_size()[0]/2-225, 100, 450, 270))
            for i, case in enumerate(self.cases2):
                pygame.draw.rect(self.screen.display,self.couleur.RED, case, 2)
                value = self.case_values2[i] if self.case_values2[i] else ""
                text = self.font.render(value, True, self.couleur.WHITE)
                self.screen.display.blit(text, (case.x + 30, case.y + 10))







