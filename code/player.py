import pygame

from entity import Entity
from keylistener import KeyListener
from screen import Screen
from Collisions import Collisions
from enigme import *

class Player(Entity):
    def __init__(self, keylistener: KeyListener, screen: Screen, x: int, y: int):
        super().__init__(keylistener, screen, x, y)
        self.dialogue_actif: bool = False
        self.objets = []        # inventaire de chaînes
        self.inventaire_visible = False        
        self.collisions: list[Collisions] | None = None
        self.switchs: list[Collisions] | None = None
        self.change_map: Collisions | None = None
        self.interactions: list[Collisions] | None = []
        self.tp_pos = None
        self.gare_liste = []
        self.enigme_code_0 = False
        self.enigme_code_1 = False

    def update(self) -> None:
        self.check_move()
        super().update()

    def check_move(self) -> None:
        if self.dialogue_actif or self.inventaire_visible:
            return
        elif self.animation_walk is False:
            temp_hitbox = self.hitbox.copy()
            if self.keylistener.key_pressed(pygame.K_q):
                temp_hitbox.x -= 16
                self.check_collisions_switchs(temp_hitbox)
                if not self.check_collisions_objet_fixe(temp_hitbox):
                    self.move_left()
            elif self.keylistener.key_pressed(pygame.K_d):
                temp_hitbox.x += 16
                self.check_collisions_switchs(temp_hitbox)
                if not self.check_collisions_objet_fixe(temp_hitbox):
                    self.move_right()
            elif self.keylistener.key_pressed(pygame.K_z):
                temp_hitbox.y -= 16
                self.check_collisions_switchs(temp_hitbox)
                if not self.check_collisions_objet_fixe(temp_hitbox):
                    self.move_up()
            elif self.keylistener.key_pressed(pygame.K_s):
                temp_hitbox.y += 16
                self.check_collisions_switchs(temp_hitbox)
                if not self.check_collisions_objet_fixe(temp_hitbox):
                    self.move_down()

    def add_switchs(self, switchs: list[Collisions]):
        self.switchs = switchs

    def add_collisions(self, collisions: list[Collisions]):
        self.collisions = collisions

    def check_collisions_objet_fixe(self, temp_hitbox):
        if self.collisions:
            for objets in self.collisions:
                if objets.check_collision(temp_hitbox):
                    if isinstance(objets, Caisse):
                        # Calcul du déplacement du joueur
                        dx = temp_hitbox.x - self.hitbox.x
                        dy = temp_hitbox.y - self.hitbox.y
                        # Tente de pousser la caisse
                        if objets.try_push(dx, dy, self.collisions):
                            return False  # Poussée réussie, pas un obstacle
                    self.collision()
                    return True
        return False

    def check_collisions_switchs(self, temp_hitbox):
        if self.switchs:
            for switch in self.switchs:
                if switch.check_collision(temp_hitbox):
                    if switch.name.startswith("gare"):
                        self.gare_liste.append(switch.name)
                        if len(self.gare_liste) > 6:
                            del self.gare_liste[0]
                        if self.gare_liste == ["gare0","gare1","gare0","gare2","gare3","gare0"]:
                            self.change_map = Collisions("switch", "gare_win", pygame.Rect(0, 0, 0, 0), 0)
                            return None
                    self.change_map = switch
        return None
    
    def toggle_interaction(self, pnjs: list, enigmes: list) -> None:
        for pnj in pnjs:
            if self.hitbox.colliderect(pnj.rect):
                if pnj.affiche_dialogue:
                    pnj.interagir(self)  # ← avance dans le dialogue
                    if not pnj.affiche_dialogue:
                        self.dialogue_actif = False  # dialogue terminé
                else:
                    pnj.interagir()  # ← démarre le dialogue
                    self.dialogue_actif = True
                break
        
        for enigme in enigmes:
             if self.hitbox.colliderect(enigme.rect):
                if enigme.event == "sound":
                    if isinstance(enigme, EnigmeMusique):
                        enigme.activer()
                    else:
                        enigme.sound()
                elif enigme.event == "on/off":
                    self.tp_pos = self.position
                    if enigme.map:
                        self.change_map = Collisions("switch", enigme.map, pygame.Rect(0, 0, 0, 0), 0)
                elif enigme.event == "reset":
                    self.change_map = Collisions("switch", "map0", pygame.Rect(0, 0, 0, 0), 0)
                elif enigme.event == "code_0":
                    self.enigme_code_0 = True
                elif enigme.event == "code_1":
                    self.enigme_code_1 = True
                    
    def possede(self, nom_objet: str) -> bool:
        return nom_objet in self.objets
