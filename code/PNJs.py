import pygame
import sys

from couleur import Couleur

ETATS_PNJ = {}

class PNJ:
    def __init__(self, nom, x, y, width, height, dialogue_lignes: list[str]):
        self.nom = nom
        self.etat = ETATS_PNJ.get(nom, 0)
        self.rect = pygame.Rect(x, y, width, height)
        self.dialogues_par_etat = {0: dialogue_lignes}
        self.reponses_par_etat = {}
        self.repliques_par_etat = {}
        self.dialogue_index = 0
        self.affiche_dialogue = False
        self.dialogue_texte_affiche = ""
        self.temps_derniere_lettre = 0
        self.lettre_intervalle = 20
        self.couleur = Couleur()
        self.reponses_par_etat[0] = []  # les réponses pour l'état initial
        self.repliques_par_etat[0] = []  # les répliques associées
        self.affiche_choix = False
        self.choix_selectionne = -1



    def update_dialogue(self):
        if not self.affiche_dialogue:
            return

        maintenant = pygame.time.get_ticks()

        if self.dialogue_index < len(self.dialogue_lignes):
            ligne = self.dialogue_lignes[self.dialogue_index]
            if len(self.dialogue_texte_affiche) < len(ligne):
                if maintenant - self.temps_derniere_lettre > self.lettre_intervalle:
                    self.dialogue_texte_affiche += ligne[len(self.dialogue_texte_affiche)]
                    self.temps_derniere_lettre = maintenant

    def interagir(self, joueur=None):
        
        if joueur :
            if self.nom == "ARNOLD" :
                if self.etat == 0 and self.choix_selectionne == 1:
                    joueur.objets.append("caisse")   # donne l’objet
                    self.etat = 1                     # bloque la remise à une seule fois
                    ETATS_PNJ[self.nom] = self.etat
                elif self.etat == 0 and (self.choix_selectionne == 0 or self.choix_selectionne == 2):
                    self.etat = 4
                    ETATS_PNJ[self.nom] = self.etat
                elif self.etat == 4 :
                    self.etat = 0
                    ETATS_PNJ[self.nom] = self.etat
                elif self.etat == 1 and joueur.possede("caisse"):
                    self.etat = 1
                    ETATS_PNJ[self.nom] = self.etat
                elif self.etat == 1 and not joueur.possede("caisse"):
                    self.etat = 2
                    ETATS_PNJ[self.nom] = self.etat
                elif self.etat == 2 and self.choix_selectionne in (0,1,2):
                    self.etat = 3
                    ETATS_PNJ[self.nom] = self.etat
                elif self.etat == 2:
                    self.etat = 2
                    ETATS_PNJ[self.nom] = self.etat

            elif self.nom == "ROSSIER":
                if self.etat == 0 :
                    self.etat = 1
                    ETATS_PNJ[self.nom] = self.etat

            elif self.nom == "JUSTIN":
                if self.etat == 0 :
                    self.etat = 1
                    ETATS_PNJ[self.nom] = self.etat

            elif self.nom == "CHLOE":
                if self.etat == 0 :
                    self.etat = 1
                    ETATS_PNJ[self.nom] = self.etat

            elif self.nom == "PABLO":
                if self.etat == 0 :
                    self.etat = 1
                    ETATS_PNJ[self.nom] = self.etat

            elif self.nom == "MARTIN":
                joueur.objets.append("truc")
                if self.etat == 0 :
                    self.etat = 1
                    ETATS_PNJ[self.nom] = self.etat

            elif self.nom == "NATHAN":
                if not joueur.possede("truc"):
                    self.etat = 0
                    ETATS_PNJ[self.nom] = self.etat
                elif self.etat == 0 and joueur.possede("truc") :
                    self.etat = 1
                    self.cacher_dialogue()
                    ETATS_PNJ[self.nom] = self.etat
                elif self.etat == 1 :
                    self.etat = 1
                    ETATS_PNJ[self.nom] = self.etat


            elif self.nom == "ZIMA":
                if self.etat == 0:
                    self.etat = 1
                    ETATS_PNJ[self.nom] = self.etat
                elif joueur.possede("pioche") and self.etat in (0, 1):
                    self.etat = 2
                    self.cacher_dialogue()
                    joueur.objets.remove("pioche")
                    ETATS_PNJ[self.nom] = self.etat
                elif self.etat == 2 :
                    self.etat = 3
                    ETATS_PNJ[self.nom] = self.etat
                elif self.etat == 3 :
                    self.etat = 3
                    ETATS_PNJ[self.nom] = self.etat

            elif self.nom == "POT MYSTERE" :
                if self.etat == 0 :
                    self.etat = 1
                    joueur.objets.append("pioche")
                    ETATS_PNJ[self.nom] = self.etat
                elif joueur.possede("pioche"):
                    self.etat = 1
                    ETATS_PNJ[self.nom] = self.etat

            elif self.nom == "VITRINE ":
                if joueur.possede("pioche"):
                    return
                joueur.objets.append("Clé")

            elif self.nom == "FRANCOIS" :
                if not joueur.possede("poisson") and not joueur.possede("Clé") :
                    self.etat = 0
                    ETATS_PNJ[self.nom] = self.etat
                elif self.etat == 0:
                    self.etat = 1
                    self.cacher_dialogue()
                    ETATS_PNJ[self.nom] = self.etat
                elif joueur.possede("poisson") and joueur.possede("Clé"):
                    self.etat = 2
                    ETATS_PNJ[self.nom] = self.etat

                
            elif self.nom == "MERLIN":
                if self.etat == 0:
                    self.etat = 3
                    ETATS_PNJ[self.nom] = self.etat
                elif joueur.possede("champignon1") and joueur.possede("champignon2") and joueur.possede("champignon3"):
                    self.etat = 1
                    joueur.objets.append("bible")
                    self.cacher_dialogue()
                    joueur.objets.remove("champignon1")
                    joueur.objets.remove("champignon2")
                    joueur.objets.remove("champignon3")
                    ETATS_PNJ[self.nom] = self.etat
                elif self.etat == 1 :
                    self.etat = 2
                    ETATS_PNJ[self.nom] = self.etat
                elif self.etat == 2 and not joueur.possede("champignon1") or not joueur.possede("champignon2") or not joueur.possede("champignon3"):
                    self.etat = 2
                    ETATS_PNJ[self.nom] = self.etat

            elif self.nom == "CAISSIER":
                if self.etat == 0:
                    self.etat = 3
                    ETATS_PNJ[self.nom] = self.etat
                elif joueur.possede("caisse") :
                    self.etat = 1
                    self.cacher_dialogue()
                    joueur.objets.remove("caisse")
                    ETATS_PNJ[self.nom] = self.etat
                elif self.etat == 1 :
                    self.etat = 2
                    ETATS_PNJ[self.nom] = self.etat
                elif self.etat == 2 and not joueur.possede("caisse") :
                    self.etat = 2
                    ETATS_PNJ[self.nom] = self.etat

            elif self.nom == "GARDIEN":
                if self.etat == 0:
                    self.etat = 2
                    ETATS_PNJ[self.nom] = self.etat
                elif joueur.possede("Clé") and self.etat in (0, 2):
                    self.etat = 1
                    self.cacher_dialogue()
                    ETATS_PNJ[self.nom] = self.etat
                elif self.etat == 1 :
                    self.etat = 3
                    ETATS_PNJ[self.nom] = self.etat
                elif self.etat == 3 :
                    self.etat = 3
                    ETATS_PNJ[self.nom] = self.etat

            elif self.nom == "LUC":
                if joueur.possede("poisson") :
                    self.etat = 4
                    ETATS_PNJ[self.nom] = self.etat
                elif joueur.possede("Clé") :
                    self.etat = 1
                    ETATS_PNJ[self.nom] = self.etat
                elif joueur.possede("bible"):
                    self.etat = 2
                    ETATS_PNJ[self.nom] = self.etat
                elif joueur.possede("caisse"):
                    self.etat = 3
                    ETATS_PNJ[self.nom] = self.etat
                else :
                    self.etat = 5
                    ETATS_PNJ[self.nom] = self.etat

            elif self.nom == "INDICATION":
                if not joueur.possede("Clé"):
                    self.etat = 0
                    ETATS_PNJ[self.nom] = self.etat
                else :
                    self.etat = 1
                    ETATS_PNJ[self.nom] = self.etat
                    joueur.objets.remove("Clé")

            elif self.nom == "FLORA":
                if not joueur.possede("Clé"):
                    self.etat = 0
                    ETATS_PNJ[self.nom] = self.etat
                elif self.etat == 0:
                    self.cacher_dialogue()
                    self.etat = 1
                    joueur.objets.append("poisson")
                    ETATS_PNJ[self.nom] = self.etat
                elif self.etat == 1 and joueur.possede("poisson"):
                    self.etat = 2
                    ETATS_PNJ[self.nom] = self.etat

            elif self.nom == "Oh ?":
                joueur.objets.append("champignon1")

            elif self.nom == "Tiens ?":
                joueur.objets.append("champignon2")

            elif self.nom == "Eh !":
                joueur.objets.append("champignon3")

            elif self.nom == "KEVIN":
                if self.etat == 0:
                    self.etat = 2
                    ETATS_PNJ[self.nom] = self.etat
                elif joueur.possede("bible") :
                    self.etat = 1
                    self.cacher_dialogue()
                    joueur.objets.remove("bible")
                    ETATS_PNJ[self.nom] = self.etat
                elif self.etat == 1:
                    if self.choix_selectionne == 0 :
                        pygame.quit()
                        raise SystemExit

        if not self.affiche_dialogue:
            self.affiche_dialogue = True
            self.dialogue_index = 0
            self.dialogue_texte_affiche = ""
            self.temps_derniere_lettre = pygame.time.get_ticks()
            self.affiche_choix = False
            # Dialogue dynamique selon l'état
            self.dialogue_lignes = self.dialogues_par_etat.get(self.etat, ["..."])
            self.reponses = self.reponses_par_etat.get(self.etat, [])
            self.repliques_reponse = self.repliques_par_etat.get(self.etat, [])
        else:
            if self.dialogue_index >= len(self.dialogue_lignes):
                if self.reponses:
                    self.affiche_choix = True
                else:
                    self.cacher_dialogue()
                return  # on sort immédiatement après avoir géré la fin

            ligne_complete = self.dialogue_lignes[self.dialogue_index]

            if self.dialogue_texte_affiche != ligne_complete:
                self.dialogue_texte_affiche = ligne_complete
            else:
                self.dialogue_index += 1
                if self.dialogue_index >= len(self.dialogue_lignes):
                    if self.reponses:
                        self.affiche_choix = True
                    else:
                        self.cacher_dialogue()
                else:
                    self.dialogue_texte_affiche = ""
                    self.temps_derniere_lettre = pygame.time.get_ticks()


    def cacher_dialogue(self):
        self.affiche_dialogue = False
        self.dialogue_index = 0  
    
    def afficher_boite_dialogue(self, screen):
        texte = self.dialogue_texte_affiche

        box_width = 615
        box_height = 200
        x = (screen.get_width() - box_width) // 2
        y = screen.get_height() - box_height - 30
        boite = pygame.Rect(x, y, box_width, box_height)

        font = pygame.font.Font(None, 24)
        font_nom = pygame.font.Font(None, 28)

        pygame.draw.rect(screen, (0, 0, 0), boite)
        pygame.draw.rect(screen, (255, 255, 255), boite, 2)

        if self.nom:
            nom_surface = font_nom.render(self.nom, True, (255, 0, 0))
            screen.blit(nom_surface, (boite.x + 10, boite.y + 5))

        text_margin = 30
        lines = wrap_text(texte, font, box_width - text_margin)
        lines = lines[:7]
        
        for i, line in enumerate(lines):
            line_surface = font.render(line, True, (255, 255, 255))
            screen.blit(line_surface, (boite.x + 10, boite.y + 35 + i * 25))  # 35 pour laisser la place au nom


    def afficher_choix(self, screen):
        if not self.affiche_choix:
            return

        font = pygame.font.Font(None, 24)

        box_width = 350
        box_height = 35
        espacement = 10

        dialogue_box_width = 610
        dialogue_box_height = 150
        dialogue_x = (screen.get_width() - dialogue_box_width) // 2
        dialogue_y = screen.get_height() - dialogue_box_height - 30

        start_x = dialogue_x + dialogue_box_width + 20  
        start_y = dialogue_y 

        for i, texte in enumerate(self.reponses):
            rect = pygame.Rect(start_x, start_y + i * (box_height + espacement), box_width, box_height)
            pygame.draw.rect(screen, (0, 0, 0), rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)
            txt = font.render(texte, True, (255, 255, 255))
            screen.blit(txt, (rect.x + 10, rect.y + 5))



def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        # On teste la ligne potentielle AVEC le mot suivant
        test_line = current_line + (word + " ")
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            if current_line:  # On évite les lignes vides
                lines.append(current_line.strip())
            current_line = word + " "  # le mot passe sur la ligne suivante

    if current_line:
        lines.append(current_line.strip())

    return lines