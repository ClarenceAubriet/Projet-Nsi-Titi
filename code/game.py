import pygame
from keylistener import KeyListener
from map import Map
from player import Player
from screen import Screen
from button import Button
from carte import Carte
from menu import Menu
from couleur import Couleur
from inventaire import Inventaire
from enigme import *

class Game:
    def __init__(self):
        self.running: bool = True
        self.screen: Screen = Screen()
        self.keylistener: KeyListener = KeyListener()
        self.map: Map = Map(self.screen)
        self.menu: Menu = Menu(self.screen)
        self.carte: Carte = Carte(self.screen)
        self.mode: str = "menu"
        self.couleur = Couleur()
        self.enigme_code = Enigme_code(self.screen)
        self.player: Player = Player(self.keylistener, self.screen, 700, 95)
        self.map.add_player(self.player)
        self.inventaire = Inventaire(self.screen.get_size(),self.player)
        self.buttons_menu: list = [Button(self.screen.get_size()[0] // 4 - 150, self.screen.get_size()[1] // 2.0, 225, 95,
                                           image="enigma/assets/images/button_play.png", action=lambda: self.changer_mode("game")),
                                   Button(self.screen.get_size()[0] // 4 - 125, self.screen.get_size()[1] // 1.5, 175, 75,
                                           image="enigma/assets/images/button_options.png", action=lambda: self.changer_mode("option_menu")),
                                   Button(self.screen.get_size()[0] // 4 - 125, self.screen.get_size()[1] // 1.25, 175, 75,
                                            image="enigma/assets/images/button_quit.png", action=lambda: self.changer_mode("quit")),
                                   Button(self.screen.get_size()[0] // 1.2, self.screen.get_size()[1] // 1.2, 140, 60,
                                           image="enigma/assets/images/button_credit.png",  action=lambda: self.changer_mode("credit")),
                                   Button(50 , self.screen.get_size()[1] - 150, 80, 80,
                                           image="enigma/assets/images/retour.png", action=lambda: self.changer_mode("menu")),
                                    ]
        self.button_musique: Button = Button(220, 275, 120, 35,
                                            text="On", action=lambda: self.toggle_musique(), couleur_bouton=self.couleur.GREEN)
        self.buttons_game: list = [Button(self.screen.get_size()[0]-80, 0, 80, 80,
                                           image="enigma/assets/images/options.png", action=lambda: self.changer_mode("option_game")),
                                   Button(self.screen.get_size()[0]-80, 80, 80, 80,
                                          image="enigma/assets/images/inventaire.png", action=self.inventaire.toggle),
                                   Button(0, self.screen.get_size()[1]-80, 80, 80,
                                           image="enigma/assets/images/carte.png", action=lambda: self.changer_mode("map"))
                                    ]
        self.button_retour_game: Button = Button(self.screen.get_size()[0]-80, 0, 80, 80,
                                                 image="enigma/assets/images/retour.png", action=lambda: self.changer_mode("game"))
        self.button_quitter_jeu:Button = Button(50, self.screen.get_size()[1] - 150, 140, 60,
                                            image="enigma/assets/images/button_quit.png", action=lambda: self.changer_mode("quit"))
        pygame.mouse.set_visible(False)
        self.curseur_img = pygame.transform.scale(pygame.image.load("enigma/assets/images/loupe.png").convert_alpha(),(32,32))
        self.curseur_doigt = pygame.transform.scale(pygame.image.load("enigma/assets/images/doigt.png").convert_alpha(),(32,32))
        pygame.mixer.init()
        pygame.mixer.music.load("enigma/assets/sound/backtrack_1.wav")
        pygame.mixer.music.play(-1)

    def toggle_musique(self):
        self.button_musique.toggle(self.button_musique)
        self.map.musique = not self.map.musique
        self.map.check_musique(self.map.current_map)


    def changer_mode(self,fonctionnalité):
        self.mode = fonctionnalité
        self.keylistener.clear()

    def run(self) -> None:
        while self.running:
            if self.mode == "menu":
                self.handle_input()
                self.screen.update()
                self.menu.draw_menu()
                for button in self.buttons_menu[:-1]:
                    button.draw(self.screen.display)

            elif self.mode == "option_menu":
                self.handle_input()
                self.screen.update()
                self.menu.draw_options()
                self.buttons_menu[-1].draw(self.screen.display)
                self.button_musique.draw(self.screen.display)

            elif self.mode == "credit":
                self.handle_input()
                self.screen.update()
                self.menu.draw_credits()
                self.buttons_menu[-1].draw(self.screen.display)

            elif self.mode == "game":
                self.handle_input()
                self.screen.update()
                self.map.update()
                self.map.player.inventaire_visible = self.inventaire.visible
                self.inventaire.draw(self.screen.get_display())
                for button in self.buttons_game:
                    button.draw(self.screen.display)
                if self.player.enigme_code_0 == True:
                    self.mode = "code_0"
                    self.player.enigme_code_0 = False
                elif self.player.enigme_code_1 == True:
                    self.mode = "code_1"
                    self.player.enigme_code_1 = False

            elif self.mode == "option_game":
                self.handle_input()
                self.screen.update()
                self.menu.draw_options()
                self.button_retour_game.draw(self.screen.display)
                self.button_musique.draw(self.screen.display)
                self.button_quitter_jeu.draw(self.screen.display)

            elif self.mode == "map":
                self.handle_input()
                self.screen.update()
                self.carte.update()
                self.button_retour_game.draw(self.screen.display)

            elif self.mode =="code_0":
                self.enigme_code.enigme = 0
                self.handle_input()
                self.screen.update()
                self.enigme_code.draw()
                for button in self.enigme_code.buttons:
                    button.draw(self.screen.display)
                self.button_retour_game.draw(self.screen.display)
                if self.enigme_code.win == True:
                    self.player.tp_pos = self.player.position
                    self.player.change_map = Collisions("switch", "labo1", pygame.Rect(0, 0, 0, 0), 0)
                    self.mode="game"
                    self.enigme_code.win = False

            elif self.mode =="code_1":
                self.enigme_code.enigme = 1
                self.handle_input()
                self.screen.update()
                self.enigme_code.draw()
                for button in self.enigme_code.buttons:
                    button.draw(self.screen.display)
                self.button_retour_game.draw(self.screen.display)
                if self.enigme_code.win2 == True:
                    self.player.tp_pos = self.player.position
                    self.player.change_map = Collisions("switch", "labo3", pygame.Rect(0, 0, 0, 0), 0)
                    self.mode="game"
                    self.enigme_code.win2 = False

            elif self.mode == "quit":
                pygame.mixer.music.stop
                pygame.quit()
                self.running = False
                return

            pos_curseur = pygame.mouse.get_pos()
            if self.mode.startswith("code"):
                self.screen.display.blit(self.curseur_doigt, (pos_curseur[0]-16, pos_curseur[1]-1))
            else:
                self.screen.display.blit(self.curseur_img, (pos_curseur[0]-5, pos_curseur[1]-5))
            pygame.display.flip()
        
    
    def handle_input(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            elif self.mode == "menu":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                    for button_menu in self.buttons_menu[:-1]:
                        button_menu.is_pressed()

            elif self.mode == "credit":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.buttons_menu[-1].is_pressed()

            elif self.mode == "option_menu":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.buttons_menu[-1].is_pressed()
                    self.button_musique.is_pressed()
                
            elif self.mode == "game":
                if event.type == pygame.KEYDOWN:
                    self.keylistener.add_key(event.key)

                elif event.type == pygame.KEYUP:
                    self.keylistener.remove_key(event.key)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.map.player.toggle_interaction(self.map.pnjs,self.map.enigmes)

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if not self.map.player.dialogue_actif:
                        for button in self.buttons_game:
                            button.is_pressed()

                    for pnj in self.map.pnjs:
                        if pnj.affiche_choix:
                            box_width = 350
                            box_height = 35
                            espacement = 10

                            dialogue_box_width = 600
                            dialogue_box_height = 150
                            dialogue_x = (self.screen.get_size()[0] - dialogue_box_width) // 2
                            dialogue_y = self.screen.get_size()[1] - dialogue_box_height - 30

                            start_x = dialogue_x + dialogue_box_width + 20
                            start_y = dialogue_y

                            for i, texte in enumerate(pnj.reponses):
                                rect = pygame.Rect(start_x, start_y + i * (box_height + espacement), box_width, box_height)
                                if rect.collidepoint(pygame.mouse.get_pos()):
                                    pnj.choix_selectionne = i
                                    pnj.affiche_choix = False
                                    if 0 <= i < len(pnj.repliques_reponse):
                                        pnj.dialogue_lignes = [pnj.repliques_reponse[i]]
                                        pnj.dialogue_index = 0
                                        pnj.dialogue_texte_affiche = ""
                                        pnj.affiche_dialogue = True
                                        pnj.reponses = []
                                        pnj.repliques_reponse = []
                                        self.map.player.dialogue_actif = True
                                    else:
                                        pnj.cacher_dialogue()
                                        self.map.player.dialogue_actif = False
                                    print(f"Réponse choisie : {texte}")

                                
            elif self.mode == "option_game":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.button_retour_game.is_pressed()
                    self.button_musique.is_pressed()
                    self.button_quitter_jeu.is_pressed()

            elif self.mode == "map":
                if event.type == pygame.MOUSEWHEEL:
                    curseur_x, curseur_y = pygame.mouse.get_pos()
                    position_map_avant = self.carte.screen_to_world((curseur_x, curseur_y))
                    zoom_précédente = self.carte.zoom
                    self.carte.zoom += event.y * self.carte.zoom_step
                    self.carte.zoom = max(self.carte.min_zoom, min(self.carte.max_zoom, self.carte.zoom))
                    if self.carte.zoom == zoom_précédente:
                        return
                    self.carte.map_layer.zoom = self.carte.zoom

                    position_map_après = self.carte.screen_to_world((curseur_x, curseur_y))

                    différence_x = position_map_après[0] - position_map_avant[0]
                    différence_y = position_map_après[1] - position_map_avant[1]

                    center_x = self.carte.camera_x + (self.screen.get_size()[0] / 2) / self.carte.map_layer.zoom
                    center_y = self.carte.camera_y + (self.screen.get_size()[1] / 2) / self.carte.map_layer.zoom

                    self.carte.camera_x = self.carte.camera_x- différence_x
                    self.carte.camera_y = self.carte.camera_y- différence_y

                    self.carte.group.center((center_x - différence_x, center_y - différence_y))
                
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.button_retour_game.is_pressed()

            elif self.mode.startswith("code"):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for bouton in self.enigme_code.buttons :
                        bouton.is_pressed()
                    self.button_retour_game.is_pressed()

                        