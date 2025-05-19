import pygame
import pyscroll
import pytmx

from player import Player
from screen import Screen
from Collisions import Collisions
from PNJs import PNJ
from enigme import *
class Map:
    def __init__(self, screen: Screen):
        self.screen: Screen = screen
        self.tmx_data: pytmx.TiledMap | None = None
        self.map_layer: pyscroll.BufferedRenderer | None = None
        self.group: pyscroll.PyscrollGroup | None = None
        self.player: Player | None = None
        self.enigme_class: Enigme | None = None
        self.pnjs: list[PNJ] = []
        self.enigmes: list[Enigme] = []
        self.switchs: list[Collisions] | None = None
        self.objets: list[Collisions] | None = None
        self.plaques: list[Plaque] | None = None
        self.current_map: Collisions = Collisions("switch", "map0", pygame.Rect(0, 0, 0, 0), 0)
        self.musique = True
        self.switch_map(self.current_map)

    def switch_map(self, switch: Collisions) -> None:
        self.tmx_data = pytmx.load_pygame(f"enigma/assets/map/{switch.name}.tmx")
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.BufferedRenderer(map_data, self.screen.get_size())
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=11)

        if switch.name.split("_")[0] == "map":
            self.map_layer.zoom = 3
        else:
            self.map_layer.zoom = 3.75

        self.switchs = []
        self.objets = []
        self.pnjs = []
        self.plaques = []
        self.enigmes = []

        for obj in self.tmx_data.objects:
            if not obj.name:
                continue
            type = obj.name.split(" ")[0]
            if type == 'collisions':
                self.objets.append(Collisions(
                    type, obj.name.split(" ")[1], pygame.Rect(obj.x, obj.y, obj.width, obj.height), int(obj.name.split(" ")[-1])
                ))
            elif type == "sortie":
                self.switchs.append(Collisions(
                    type, obj.name.split(" ")[1], pygame.Rect(obj.x, obj.y, obj.width, obj.height), int(obj.name.split(" ")[-1])
                ))
            elif type == "pnj":
                if obj.name == "pnj MUSEE 0":
                    self.pnjs.append(PNJ(
                        nom="VITRINE",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "Rien de suspect ici.",
                        "Allons voir la prochaine vitrine."
                    ]

                elif obj.name == "pnj MUSEE1 0":
                    self.pnjs.append(PNJ(
                        nom="VITRINE ",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "Rien de suspect ici.",
                        "Quoique...",
                        "Qu'est-ce que c'est que ça ? On dirait...",
                        "Une clé ?",
                        "Intéressant",
                        "Allons voir s'il n'y a pas d'autres potentiels indices."
                    ]

                elif obj.name == "pnj GARDIEN 0":
                    self.pnjs.append(PNJ(
                        nom="GARDIEN",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "Oh, bonjour.",
                        "Désolé, je ne suis pas au top aujourd'hui, avec tout ce qui s'est passé...",
                        "Tu es surement au courant ? Nous avons été cambriolés. Des masques antiques mayas ont notamment été volés. Un butin d'une valeur de près de 15 millions d'§, mais surtout d'incroyables antiquités...",
                        "Sans ces masques au coeur de notre collection, le musée va potentiellement fermer... Et je me retrouverai sans emploi...",
                        "Il faut absolument retrouver ces masques ! Être gardien de musée, c'est ma passion !"
                    ]
                    self.pnjs[-1].reponses_par_etat[0] = [
                        "Quelle aubaine, je suis détective !",
                        "C'est surement dur pour vous...",
                        "DES MASQUES MAYAS ???"
                    ]
                    self.pnjs[-1].repliques_par_etat[0] = [
                        "Vraiment ? Alors tu vas pouvoir être utile ! Peux-tu inspecter les vitrines en détail ? La police l'a déjà fait, mais je doute qu'ils aient bien regardé partout... Reviens me voir s'il y a quelque chose de suspect !",
                        "Je ne te le fais pas dire. Mais je me considère chanceux : je pourrais être comme ce pauvre GUILLAUME... Tiens, finalement je te trouve sympathique ; n'hésite pas à regarder toutes les vitrines si tu veux t'amuser. Tu serais capable de faire mieux que les policiers, ces incompétents !",
                        "NIGERUNDAYOOOOOOOOOOOOOOOO !!! Oui, comme dans Jojo. Tu es amusant ! Allez, tu vas me servir à quelque chose : regarde toutes les vitrines du musée et essaie de voir si tu peux trouver quelque chose... Tu seras surement plus efficace que la police ! Si tu trouves, reviens me voir."
                    ]
                    self.pnjs[-1].dialogues_par_etat[1] = [
                        "Ah mais oui, des clés ! Tiens donc, je ne pensais pas que tu ferais vraiment mieux que les gendarmes du coin...",
                        "Les gens du coin au global, d'ailleurs. Ils n'ont aucune culture ! Aucun intérêt pour l'art, et aucune connaissance des animés ! Sauf Chloé, elle est super sympa",
                        "Revenons à nos clés. Elles me disent quelque chose, tiens.",
                        "Tu devrais aller voir ZIMA, c'est un ancien mineur. Il a plein de chose à dire, sur tout ! Mais il est un peu adepte des théories du complot...",
                        "Grand remplacement, si tu vois ce que je veux dire."
                    ]
                    self.pnjs[-1].dialogues_par_etat[2] = [
                        "Alors, tu as trouvé quelque chose ?",
                        "Non ? Pourtant, je suis sur qu'il y a quelque chose de caché dans ces vitrines, j'en ai l'étrange conviction depuis que tu es arrivé...",
                        "Continue à chercher ! Lis bien toutes les explications des vitrines !"
                    ]
                    self.pnjs[-1].dialogues_par_etat[3] = [
                        "Va parler à ZIMA, je t'ai dit ! Oh, et si tu la vois, passe le bonjour à CHLOE de ma part.",
                        "Ils habitent tous les deux dans les maisons à l'Est du village. Fais toutes les maisons, tu les trouveras."
                    ]

                elif obj.name == "pnj PLAQUE1 0":
                    self.pnjs.append(PNJ(
                        nom="PLAQUE",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "L'ENFER, C'EST LES AUTRES",
                        "Jean-Paul Sartre."
                    ]

                elif obj.name == "pnj PLAQUE2 0":
                    self.pnjs.append(PNJ(
                        nom="PLAQUE",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "L'ENNUI EST LE MALHEUR DES GENS HEUREUX",
                        "Horace Walpole."
                    ]

                elif obj.name == "pnj PLAQUE3 0":
                    self.pnjs.append(PNJ(
                        nom="PLAQUE",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "SI T'ES TOUT SEUL AVEC TES PROBLEMES C'EST PEUT-ÊTRE PARCE QUE LE PROBLEME C'EST TOI",
                        "Orelsan."
                    ]

                elif obj.name == "pnj PLAQUE4 0":
                    self.pnjs.append(PNJ(
                        nom="PLAQUE",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "NO I SWEAR, I DON'T HAVE A GUN",
                        "Kurt Cobain."
                    ]

                elif obj.name == "pnj PLAQUE5 0":
                    self.pnjs.append(PNJ(
                        nom="PLAQUE",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "NE DEBARASSEZ PAS LA TABLE, A MOINS QUE LES HOMMES NE SE LEVENT POUR LE FAIRE AUSSI.",
                        "Coco Chanel."
                    ]

                elif obj.name == "pnj PLAQUE6 0":
                    self.pnjs.append(PNJ(
                        nom="PLAQUE",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "LA PLUS GRANDE GLOIRE N'EST PAS DE NE JAMAIS TOMBER, MAIS DE SE RELEVER A CHAQUE CHUTE",
                        "Nelson Mandela."
                    ]

                elif obj.name == "pnj PLAQUE7 0":
                    self.pnjs.append(PNJ(
                        nom="PLAQUE",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "JE SUPPOSE QUE LA PLUS GRANDE MARQUE QUE NOUS AYONS OBTENUE, CE SONT LES AMIS QUE NOUS NOUS SOMMES FAITS EN COURS DE ROUTE",
                        "Kindred."
                    ]

                elif obj.name == "pnj CHAMPIGNON1 0" :
                    self.pnjs.append(PNJ(
                        nom="Oh ?",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "Vous avez trouvé un champignon !"
                    ]

                elif obj.name == "pnj CHAMPIGNON2 0" :
                    self.pnjs.append(PNJ(
                        nom="Tiens ?",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "Vous avez trouvé un champignon !"
                    ]

                elif obj.name == "pnj CHAMPIGNON3 0" :
                    self.pnjs.append(PNJ(
                        nom="Eh !",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "Vous avez trouvé un champignon !"
                    ]

                elif obj.name == "pnj MERLIN 0":
                    self.pnjs.append(PNJ(
                        nom="MERLIN",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "Salut, moi c'est MERLIN !",
                        "Mais...",
                        "D'où viens-tu ? Tu as l'air d'être apparu comme ça, au milieu de nulle part..."
                        "C'est impressionnant. Et puis, comment connais-tu cet endroit ?",
                        "Nous ne sommes que deux à le connaitre, par amour pour les champignons : moi et le prêtre.",
                        "D'ailleurs, je cueille des champignons, comme tu le vois.",
                        "Mais je n'en trouve pas pour l'instant, la cueuillette est mauvaise.",
                        "Par contre, j'ai trouvé un livre ! Sûrement au prêtre. Je te propose un deal.",
                        "Tu me ramasses trois champignons, et je te passe le livre.",
                        "Alors ?"
                    ]
                    self.pnjs[-1].reponses_par_etat[0] = [
                        "Ok, Deal !",
                        "N'importe lesquels ? C'est dangereux...",
                        "Le prêtre ?..."
                    ]
                    self.pnjs[-1].repliques_par_etat[0] = [
                        "Génial ! Reviens me voir quand tu as fini alors.",
                        "Non, ne t'inquiète pas. Il n'y en a pas de toxiques dans la région. Allez, deal !",
                        "Oui... ça m'étonne de lui qu'il égare quelque chose, ce n'est pas dans ses habitudes..."
                    ]
                    self.pnjs[-1].dialogues_par_etat[1] = [
                        "Ah, tu as tout ! Eh bien, un deal est un deal. Tiens !",
                        "Au plaisir !"
                    ]
                    self.pnjs[-1].dialogues_par_etat[2] = [
                        "Tu es toujours là ?",
                        "Je n'ai plus besoin de toi, et je n'ai plus rien à t'offrir, désolé.",
                        "N'oublie pas d'aller voir le prêtre pour lui rendre sa bible ! Il sera content."
                    ]
                    self.pnjs[-1].dialogues_par_etat[3] = [
                        "Et mes champignons ? Cherche-les dans l'herbe !"
                    ]
                
                elif obj.name == "pnj THIERRY 0":
                    self.pnjs.append(PNJ(
                        nom="THIERRY",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "Ne me dérange pas ! Je joue, là",
                        "A quoi ? Ben ! aux échecs évidemment. ça se voit pas ?",
                        "Hein ? Oui, il n'y a pas de jeu. On mémorise l'emplacement des pièces",
                        "Bon, tu me déconcentres, là ! Laisse moi tranquille !"
                    ]

                elif obj.name == "pnj PAUL 0":
                    self.pnjs.append(PNJ(
                        nom="PAUL",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "Oh, bonjour.",
                        "Ce que je fait ? Des échecs. On joue en mémorisant la position des pièces sur un faux échiquier.",
                        "Hein ? Oui, c'est dur !",
                        "La preuve en est, je passe mon temps à perdre. Mais je ne me plains pas, c'est assez amusant !",
                        "Salut !"
                    ]

                elif obj.name == "pnj ZIMA 0":
                    self.pnjs.append(PNJ(
                        nom="ZIMA",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "Salut.",
                        "Tu es nouveau au village ? Je ne t'avais jamais vu avant.",
                        "Je suis ici depuis longtemps moi, je connais bien le coin.",
                        "T'as des questions en particulier ?"
                    ]
                    self.pnjs[-1].reponses_par_etat[0] = ["Tu sais quelque chose sur ces clés ?","Pourquoi les gens ont-ils peur de la grotte ?"]
                    self.pnjs[-1].repliques_par_etat[0] = [
                        "Ces clés ? Mais oui ! Tiens, je te le dirais si tu vas me chercher ma pioche... dans la grotte, elle se trouve dans la grotte. Regarde ta carte si tu es perdu !",
                        "La grotte ? J'ai quelque chose à moi là-bas, une pioche ! Tu pourrais aller la chercher, ça serait super ! Mais attention ; en tant qu'ancien mineur, je peux te dire : on s'y perd facilement. C'est comme la gare : depuis qu'une entreprise étrangère s'est installée là-bas, des choses bizarre se passent. Rien contre le fait que ce soit des étrangers, bien sûr ! Et je te dirais d'où viennent ces clés que tu trimballes."
                    ]
                    self.pnjs[-1].dialogues_par_etat[1] = [
                        "Oh, tu es là.",
                        "Tu as suivi mes conseils ? Fait attention à la gare !",
                        "Et aussi, pense à ma pioche. Mais fait attention, la grotte est un labyrinthe...",
                        "Et je ne suis pas raciste. Je trouve ça juste étrange, cette histoire de gare.",
                        "Oh comme c'est bizarre...",
                        "Bref."
                    ]
                    self.pnjs[-1].dialogues_par_etat[2] = [
                        "Tu as ma pioche ? Oui ?",
                        "Merci ! Bon je t'ai promis des infos, je te les donne",
                        "Je ne sais pas à quoi servent ces clés, mais François sait ! Si tu fait ce qu'il te demande, il te donnera à son tour un indice... ",
                        "Mais je ne sais rien d'autre."
                    ]
                    self.pnjs[-1].dialogues_par_etat[3] = [
                        "Va voir FRANCOIS, je t'ai dit !",
                        "Et fait attention à toi : des gens louches trainent dans le coin...",
                        "Genre... bazané."
                    ]

                elif obj.name == "pnj JUSTIN 0":
                    self.pnjs.append(PNJ(
                        nom="JUSTIN",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "Yo.",
                        "J'te connais pas, tu sors d'où ?",
                        "Bah ! anyway. Ce n'est pas important.",
                        "Ce qui est important, c'est que je suis... en congé ! Eh oui !",
                        "Le village est tellement secoué par le vol du musée que le maire nous a renvoyé chez nous pour la journée !",
                        "Bon, en tant qu'employé de mairie, je foutais déjà pas grand-chose, mais ça a le mérite d'être sympa !",
                        "Ne plus avoir à sortir de chez soi, jouer à LoL toute la journée... Quel bonheur !",
                        "Tu travailles, toi ?"
                    ]
                    self.pnjs[-1].reponses_par_etat[0] = ["Oui, je suis détective !","Tu joues à LoL ? Sale puant","Le caissier travaille, lui"]
                    self.pnjs[-1].repliques_par_etat[0] = [
                        "Sérieux ! c'est trop cool ! ... Ah bah enft non, je suis bien en vacances moi... n'enquètes surtout pas ! De toute façon, je ne te dirai rien.",
                        "Pas du tout, c'est un jeu compliqué et très stratégique ; les gens qui y jouent sont généralement très intelligents ! Regarde les joueurs d'échecs au bar, par exemple : ce sont des génies ! Et c'est normal car ils y jouent. Et puis je suis lavé, là, c'est bien la preuve qu'on prend des douches.",
                        "Oui, mais lui, il ne pense qu'à l'argent... et ROSSIER, mdrrrrr. Va l'interroger, tu verras. Et n'hésite pas à passer le bonjour au BARMAN de ma part, si tu vas au bar !"
                    ]
                    self.pnjs[-1].dialogues_par_etat[1] = [
                        "Lache moi, tu vois pas que je suis en pleine game ???",
                        "Orh, tu es lourd."
                    ]
                
                elif obj.name == "pnj POT 0":
                    self.pnjs.append(PNJ(
                        nom="POT MYSTERE",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "Tiens, un pot ! Qu'il y a-t-il à l'intérieur ?",
                        "Une pioche ! C'est surement la pioche de ZIMA !",
                        "C'est super, on peut sortir maintenant ! La sortie se trouve juste à côté !"
                    ]
                    self.pnjs[-1].dialogues_par_etat[1] = [
                        "La pioche a déjà été récupérée, on peut sortir maintenant."
                    ]

                elif obj.name == "pnj ROSSIER 0":
                    self.pnjs.append(PNJ(
                        nom="ROSSIER",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "Bonjour !",
                        "C'est moi, votre prof de NSI préféré !",
                        "Je rigole. J'ai pas trop encore l'habitude d'être à la retraite, ça date d'il y a si peu de temps...",
                        "J'étais prof de NSI, pour tout te dire ! C'était assez fun comme métier, la programmation est un monde merveilleux.",
                        "'Hello World !' lol.",
                        "J'ai eu beaucoup d'élèves, j'ai enseigné pendant plus de 30 ans !",
                        "Mais mes préférés sont sans contestation la génération 2008.",
                        "Fin ce sont les meilleurs quoi, regarde ce jeu magnifique ! C'est eux qui l'ont fait.",
                        "Et c'est moi qui vais le noter ! D'ailleurs, tu penses que je vais mettre combien ?"
                    ]
                    self.pnjs[-1].reponses_par_etat[0] = ["0/20, c'est nul !","Boaf, ça mérite bien un 14/20","5 de plus que la moyenne de la classe", "Entre 19 et 22 sur 20"]
                    self.pnjs[-1].repliques_par_etat[0] = [
                        "Jamais ! Mon chouchou Thierry a participé à sa conception, ça vaut au moins 18 !",
                        "J'aurais dit un peu plus, quand même. Je trouve que celui qui a fait mes dialogues les a bien réussis, ça vaut bien quelques points de plus.",
                        "La moyenne de la classe sera surement de 15, donc ça fait 20. Je suis d'accord !",
                        "Bien vu ! J'hésite encore à mettre plus de 20, mais sinon c'est plus ou moins ça oui. C'est vraiment un super jeu !"
                    ]
                    self.pnjs[-1].dialogues_par_etat[1] = [
                        "Ce jeu est le meilleur jeu auquel j'ai jamais joué.",
                        "(Après LoL, HollowKnight, tous les Zelda, etc, etc)",
                        "Mais ça reste bien !",
                        "Ah, mais tu souhaites avoir des renseignement ? Je n'ai rien à te dire hélas.",
                        "Mais n'hésite pas à aller voir la TOMBE au-dessus du quartier résidentiel. ",
                        "C'est important de se recueillir devant, ça sert à honorer les morts. Surtout celui-ci, il manque beaucoup au concepteur du jeu."
                    ]

                elif obj.name == "pnj RIEN 0" :
                    self.pnjs.append(PNJ(
                        nom="DOMMAGE !",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "Il n'y a pas de champignons ici"
                    ]

                elif obj.name == "pnj MAIRE 0" :
                    self.pnjs.append(PNJ(
                        nom="MAIRE",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "Ce vol est une catastrophe pour notre ville !",
                        "Je ne vais pas être réélu !"
                    ]       

                elif obj.name == "pnj CHLOE 0":
                    self.pnjs.append(PNJ(
                        nom="CHLOE",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "Bonjour !",
                        "Je suis l'une des trois conceptrices de ce jeu, CHLOE !",
                        "Il est bien, hein ?",
                        "Ah, qui sont les deux autres concepteurs ? Des malades mentaux. A l'heure qu'il est, ils sont surement au bar. Tu devrais aller les voir, ils doivent jouer aux échecs.",
                        "Quoi, si je sais quelque chose à propos du vol ? Non, rien du tout. Mais je trouve certaines personnes suspectes, pour tout te dire..."
                    ]
                    self.pnjs[-1].reponses_par_etat[0] = ["FRANCOIS ?", "GUILLAUME ?", "KEVIN ?"]
                    self.pnjs[-1].repliques_par_etat[0] = [
                        "Avec ses problèmes ? Il n'arrive pas à se déplacer, le pauvre ! Non, ce n'est pas lui. Va plutôt voir du côté du prètre, il me parait bien étrange... Tu savais qu'il y avait un passage secret entre le musée et la forêt ? Il l'aurait utilisé pour réaliser le vol... Enfin, ce ne sont que des spéculations.",
                        "Lui ? Ha ! Il croit nous avoir en simulant la dyslexie, mais tout le village est au courant. C'est vraiment un bolosse, donc je ne pense pas qu'il ait pu monter un truc pareil. Par contre, le prètre... Tu devrais te renseigner, il paraît qu'il y a un passage secret entre le musée et la forêt, pas loin de l'église. C'est suspect.",
                        "Le prètre ? Oui, il est ultra suspect. Il y aurait un passage secret entre le musée et la forêt, et ça déboucherait pas loin de son église... Tu devrais te renseigner"
                    ]
                    self.pnjs[-1].dialogues_par_etat[1] = [
                        "Va voir du côté du prètre, il est suspect. Et va interroger les joueurs d'échecs !"
                    ]

                elif obj.name == "pnj CAISSIER 0":
                    self.pnjs.append(PNJ(
                        nom="CAISSIER",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "Bonjour, jeune homme !",
                        "Ou jeune fille ? Bah ! On s'en fout en vrai.",
                        "Tout ce qui compte, c'est mon amour pour ROSSIER.",
                        "Tu viens pour acheter quelque chose ? J'ai quelques objets sympas à vendre. Après tout je suis caissier. Par exemple, une lampe torche, ou des infos sur le vol...",
                        "Alors, que veux tu ?"
                    ]
                    self.pnjs[-1].reponses_par_etat[0] = ["La lampe torche a l'air utile. J'achète !", "Vous avez des infos sur le vol ???", "Et c'est une bonne condition, ça, caissier ?"]
                    self.pnjs[-1].repliques_par_etat[0] = [
                        "Et une lampe torche, une ! Ah... Ben enft non, je suis à cours de stock. Mais je  te donnerai des infos si tu vas chercher un truc pour moi ! C'est un colis, et c'est mon frère qui l'a. Il habite dans la maison d'à côté. Va me la chercher et je te donnerai des infos !",
                        "Oui... Mais il va falloir faire quelque chose pour moi si tu veux en avoir. Peux-tu aller voir mon frère dans une des maisons ? Il a un objet à moi. Ramène le moi et je te donne les infos que tu veux",
                        "Tu sais, je ne pense pas qu'il y ait de bonne ou de mauvaise situation... Moi, si je devais résumer ma vie aujourd'hui avec toi, je dirais que c'est d'abord des rencontres. Des gens qui m'ont tendu la main, peut-être à un moment où je ne pouvais pas, où j'étais seul chez moi. Et c'est assez curieux de se dire que les hasards, les rencontres, forgent une destinée... Et ta destinée, là maintenant, c'est que t'aille chercher un colis pour moi chez mon frère. Si tu me l'apportes, je te filerai des infos."
                    ]
                    self.pnjs[-1].dialogues_par_etat[1] = [
                        "Oh, tu m'as rapporté ma caisse ! Merci beaucoup. C'est une commande Amazon que mon frère m'avait volée, il regarde dans les boite aux lettres des autres car il n'a rien de mieux à faire",
                        "C'est une commande très importante pour moi. Mais c'est secret, tu ne l'as pas ouverte j'espère ?"
                    ]
                    self.pnjs[-1].reponses_par_etat[1] = ["Non", "Non mdr", "Peut-être hehehe"]
                    self.pnjs[-1].repliques_par_etat[1] = [
                        "Bien, très bien. Pour ton info, c'est vrai ! Je te conseille d'aller parler à FRANCOIS et au BARMAN, ils ont des trucs intéressant à raconter. Ce sont des puits à infos. Et pense bien à regarder toutes les plaques dans les maisons, elles ont des choses sympa à dire. J'aime bien celle d'ARNOLD, ça représente bien son état d'esprit.",
                        "Je n'aime pas ton attitude... Mais bon, si tu n'as rien regardé. Pour ce que je sais... va voir au bar, les poivrots ont toujours des trucs à raconter. Et n'hésite pas à parler à Charlotte ! Sa récompense en vaut la peine.",
                        "Oh non... surtout, ne le dis à personne, d'accord ! Tiens, je te donne des conseils en échange de ton silence : va parler à FRANCOIS, il a toujours des trucs à dire. Il habite à côté de chez GUILLAUME, qui habite à côté de chez ARNOLD."
                    ]
                    self.pnjs[-1].dialogues_par_etat[2] = ["Va parler aux gens que je t'ai indiqués, je t'ai dit ! Ha, et aussi, il ne faut surtout pas parler du contenu de la caisse ! A qui que ce soit !"]
                    self.pnjs[-1].dialogues_par_etat[3] = ["Ben alors, tu fais quoi ici ? Tu as ma caisse ?","Va la chercher, orh !"]

                elif obj.name == "pnj KEVIN 0":
                    self.pnjs.append(PNJ(
                        nom="KEVIN",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "... Mais où est donc passé ce livre...",
                        "Oh.",
                        "Bonjour, jeune homme.",
                        "Je ne t'ai jamais vu avant. Tu n'est pas du coin, si ? Je connais tout le monde dans le village grâce à mon travail à la paroisse. Je suis prêtre, au passage",
                        "...",
                        "Tu es sûrement venu pour t'ouvrir aux voies du seigneur ?",
                        "Je ne vais pas pouvoir t'aider pour l'instant, j'ai perdu ma bible.",
                        "Mais n'hésite pas à revenir quand tu veux, je me ferais un plaisir de t'initier aux enseignements de notre Seigneur Jésus-Christ.",
                        "(Et optionellement, si tu retrouves ma bible...)"
                    ]
                    self.pnjs[-1].reponses_par_etat[0] = ["Je suis athée, désolé.", "Je peux essayer de retrouver votre bible."]
                    self.pnjs[-1].repliques_par_etat[0] = [
                        "Tant pis. Au revoir, jeune enfant.",
                        "Merci, c'est très noble de ta part. Je l'ai probablement perdu autour de la forêt, si ça peut t'aider."
                    ]
                    self.pnjs[-1].dialogues_par_etat[1] = [
                        "Oh ! Tu as retrouvé ma bible ! Merci infiniment.",
                        "J'y tiens beaucoup, cet exemplaire-là est spécial à mes yeux.",
                        "Tu l'as trouvée où ? "
                    ]
                    self.pnjs[-1].reponses_par_etat[1] = ["Près de la sortie du dernier portail"]
                    self.pnjs[-1].repliques_par_etat[1] = ["Alors tu sais... Oui, c'est moi qui ait fait le vol. Mais à qui cela importe ? Ce jeu n'est qu'un code, et je ne peux pas en sortir. Mais je peux le modifier à ma faveur, grâce aux pouvoir des inventions de Nathan ! Je refuse d'être victime d'un choix du joueur. Moi, et moi seul, déciderai de ma fin."]
                    self.pnjs[-1].dialogues_par_etat[2] = [
                        "Eh bien, pourquoi es-tu revenu ? Tu recherches toujours le secret de la foi ?",
                        "Si tu pouvais tenter de trouver ma bible, plutôt..."
                    ]

                elif obj.name == "pnj TOMBE 0":
                    self.pnjs.append(PNJ(
                        nom = "TOMBE",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes = [
                            "Un poème est marqué sur cette tombe.",
                            "Il dit :",
                            "Lorsqu’un vivant nous quitte, ému, je le contemple ;",
                            "Car entrer dans la mort, c’est entrer dans le temple,",
                            "Et quand un homme meurt, je vois distinctement",
                            "Dans son ascension mon propre avènement.",
                            "C'est un beau poème",
                            "Il est signé : En souvenir de mon ego, Paul."
                        ] 
                    ))
                
                elif obj.name == "pnj CHARLOTTE 0":
                    self.pnjs.append(PNJ(
                        nom="CHARLOTTE",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "Bonjour, je suis CHARLOTTE !",
                        "Je suis la jardinière de la ville, et j'ai oublié combien de fleurs bleues j'ai planté dans la ville...",
                        "Pourrais-tu les compter pour moi ? Je te donnerai une récompense !"
                    ]
                    self.pnjs[-1].reponses_par_etat[0] = ["Oui, bien sûr !", "Bof, j'ai pas le temps."]
                    self.pnjs[-1].repliques_par_etat[0] = [
                        "Super, reviens me voir quand tu as fini !",
                        "Tant pis... Je demanderai à quelqu'un d'autre."
                    ]

                elif obj.name == "pnj BARMAN 0":
                    self.pnjs.append(PNJ(
                        nom="LUC",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "Bonjour, je suis LUC !",
                        "Je suis le BARMAN du seul bar du village !",
                        "Donc oui, je fais des affaires hehehehe.",
                        "Mais je ne vends pas que des boissons, mais disons aussi des ... informations ...",
                        "Y-a-t'il quelque chose que tu souhaites savoir en particulier ?",
                        "Je sais plein de choses !"
                    ]
                    self.pnjs[-1].reponses_par_etat[0] = ["Tu vas me faire payer ces informations ?","Qui sont les deux golmons autour de la table ?"]
                    self.pnjs[-1].repliques_par_etat[0] = [
                        "Evidemment ! Il faut pas déconner, j'ai une boutique à tenir quand même !",
                        "Eux, là ? Ne cherche pas à dialoguer avec eux, ils sont concentrés. Oublie les, ce sont des fous"
                    ]
                    self.pnjs[-1].dialogues_par_etat[1] = [
                        "Tu as une clé ? Tu devrais aller voir ZIMA !"
                    ]
                    self.pnjs[-1].dialogues_par_etat[2] = [
                        "Tu as une bible ? Tu devrais aller voir KEVIN !"
                    ]
                    self.pnjs[-1].dialogues_par_etat[3] = [
                        "Tu as une caisse ? Tu devrais aller voir le CAISSIER !"
                    ]
                    self.pnjs[-1].dialogues_par_etat[4] = [
                        "Tu as un poisson ? Tu devrais aller voir FRANCOIS !"
                    ]
                    self.pnjs[-1].dialogues_par_etat[5] = [
                        "Pense à aller voir le GARDIEN !"
                    ]
                    

                elif obj.name == "pnj POLICIER 0":
                    self.pnjs.append(PNJ(
                        nom="PABLO",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "Bonjour, jeune homme !",
                        "Que fais-tu ici ?",
                        "On a eu un délit récemment dans le coin, alors c'est un peu le stress en ce moment, vois-tu ?",
                        "Bref, fait attention à ce que tu fais, on est déjà en train de galérer pour trouver le responsable de ce vol. Le GARDIEN du musée en est encore tout retourné.",
                        "Il faut dire qu'il y en a pour plus de 15 millions d'§..."
                    ]
                    self.pnjs[-1].reponses_par_etat[0] = ["Je comprends, ça doit être stressant.", "Bonne chance dans l'enquète !"]
                    self.pnjs[-1].repliques_par_etat[0] = [
                        "En effet... le pire, c'est que le vol s'est fait au nez et à la barbe des collègues, alors que le musée se situe juste à côté ! C'est le batiment juste à gauche du commissariat. J'étais chez moi au moment du drame, pour tout te dire. Va voir le GARDIEN, tiens, ça lui fera plaisir de voir autre chose que des képis. Il est presqu'en dépression.",
                        "Merci ! On en a pour longtemps, on n'a pas l'ombre d'un suspect pour l'instant... Mais on trouvera, la justice triomphe toujours ! Le musée se trouve juste à gauche du commissariat, on trouvera forcément des indices. Tu devrais aller voir le GARDIEN, tiens, peut-être te dira-t-il quelque chose qu'il a oublié de nous partager. On pourrait avoir un début de piste comme ça !"
                    ]
                    self.pnjs[-1].dialogues_par_etat[1] = [
                        "Va voir le GARDIEN si tu veux obtenir des infos !",
                        "Et n'hésite pas à parler à tous les autres habitants. Ils ont peut-être des choses à dire."
                    ]

                elif obj.name == "pnj MARTIN 0":
                    self.pnjs.append(PNJ(
                        nom="MARTIN",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "Ha ?"
                        "Tiens, bonjour ! Tu viens de sortir de la grotte, ou je suis fou ?",
                        "Je me présente : MARTIN, fan ultime de Jojo !",
                        "Cet entrain a d'ailleurs fait de moi un des suspects principaux du vol, comme ce sont des masques mayas qui ont été volés...",
                        "Mais j'avais un alibi, donc ils m'ont relaché !",
                        "Et toi, es-tu fan de Jojo ?"
                    ]
                    self.pnjs[-1].reponses_par_etat[0] = ["NIGERUNDAYOOOOOOOO", "Oui ! le GARDIEN aussi d'ailleurs.","Non, je déteste cette série"]
                    self.pnjs[-1].repliques_par_etat[0] = [
                        "JOSEPH JOEYSTARRRR meilleure série du monde. Comme tu as de bons goûts, je vais t'aider : l'épreuve suivante est très dure, mais tu peux l'éviter en utilisant un trou dans la barrière en dessous de l'entrepôt. La jardinière n'arrive pas à faire pousser une haie à cet emplacement depuis bientôt deux ans, et refuse de mettre un poteau.",
                        "Ah bon ?? Je passerai le voir plus souvent, alors ! Je savais que CHLOE était fan d'animés, mais je croyais que c'était la seule du village à part moi... On apprend des choses tous les jours ! Tiens, pour m'avoir donné cette information, je vais t'aider ; il y a un trou entre les barrières au sud de l'entrepôt, tu peux passer par là pour éviter l'épreuve de l'entrepôt.",
                        "VADE RETRO, SATANAS ! Tu n'as aucun goût. Pour la peine, je ne te donnerai pas d'indice pour la prochaine épreuve, nah ! Ne pas aimer Jojo, vraiment aucun style !"
                    ]
                    self.pnjs[-1].dialogues_par_etat[1] = [
                        "Souviens-toi de l'indice que je t'ai donné ! Ou pas, d'ailleurs...",
                        "Est-ce que tu aimes Jojo ?",
                        "Enfin bref, ça n'a aucune importance"
                    ]

                elif obj.name == "pnj NATHAN 0":
                    self.pnjs.append(PNJ(
                        nom="NATHAN",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[1] = [
                        "Bravo, tu as réussi l'épreuve des caisses !",
                        "Ou alors tu as triché ? Après tout, tu n'étais pas obligé de la réussir pour passer, ou même de passer par l'entrepôt : il y a un trou dans le grillage en-dessous...",
                        "Mais bref, venons-en au fait : d'une manière ou d'une autre, tu as réussi à arriver à venir jusque là. Tu as donc survécu à mes énigmes du labo, minimum ! Félicitations à toi !",
                        "J'avais à l'origine créé ces épreuves pour m'amuser, et tu les as résolues haut la main ! Tu sembles être un génie !",
                        "J'ai donc une tache très importante à te confier, mais j'ai besoin de ton entière confiance.",
                        "Je crois savoir commment le coupable a fait son coup ; mais je n'ai pas de preuves...",
                        "Vois-tu, j'ai aussi repris les batiments de la bibliothèque et de la gare, autrefois, afin de m'amuser ; malheureusement, celui de la gare, une énigme à base de portails, a été détournée par quelqu'un du village afin d'en faire son bureau.",
                        "Depuis ce bureau, et à l'aide des portails, il a mis au point un système qui lui permet de se rendre n'importe où, n'importe comment, lui permettant ainsi de réaliser le vol des masques.",
                        "Je ne peux pas y aller moi-même, car le voleur me connait et je serais compromis. Mais toi, il ne t'a jamais vu !",
                        "Ainsi, si tu te rends à la gare, tu pourras tenter de résoudre l'énigme des portails et ainsi être téléporté à l'endroit d'où le voleur a fait son coup ! Cela te permettrait de trouver le coupable !",
                        "Acceptes-tu cette lourde tâche ?"
                    ]
                    self.pnjs[-1].reponses_par_etat[1] = ["Oui !", "Oui, je ferais tout pour trouve le coupable !","Et la bibliothèque ?"]
                    self.pnjs[-1].repliques_par_etat[1] = [
                        "Je suis heureux de voir ton engouement ! J'aimerai bien pouvoir t'aider quant à la résolution de l'énigme des portails, mais le voleur l'a probablement changée... Je ne peux que te souhaiter bonne chance ! ",
                        "Ton engouement fait plaisir à voir ! J'espère aussi que l'auteur de ce vol sera arrêté, et les masques rendus au musée. Ce cher GARDIEN sera si content, mdr.",
                        "La bibliothèque ? N'hésite pas à y passer une fois cette affaire finie, je suis très fier des petites énigmes que j'y ait installé ! Cependant, il faut d'abord commencer par résoudre l'énigme des portails et appréhender le voleur. Je compte sur toi !"
                    ]
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "Bonjour, je suis NATHAN !",
                        "Nous n'avons rien à nous dire, je crois",
                        "C'est ce qu'il me semble en tout cas. Peut-être plus tard dans l'aventure..."
                    ]


                elif obj.name == "pnj POISSONNIERE 0":
                    self.pnjs.append(PNJ(
                        nom="FLORA",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[1] = [
                        "Tu es ici pour récupérer quelque chose ?"
                    ]
                    self.pnjs[-1].reponses_par_etat[1] = ["Oui, une commande de FRANCOIS !"]
                    self.pnjs[-1].repliques_par_etat[1] = ["Ah ? Eh bien, voici sa commande ! Tu passeras le bonjour à FRANCOIS de ma part !"]
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "Bonjour !",
                        "Je suis FLORA la poissonniere !",
                        "Tu es ici pour récupérer quelque chose ?"
                    ]
                    self.pnjs[-1].reponses_par_etat[0] = ["Non, pas spécialement."]
                    self.pnjs[-1].repliques_par_etat[0] = ["Ah, très bien, pas spécialement ! Tu es venu juste pour visiter ? Tu es marrant, toi. Enfin je ne juge pas. A propos, t'as entendu de ce qui se passe au village ? Le vol, tout ça... Tu devrais aller voir le GARDIEN du musée, il doit être au bout de sa vie. Comme je ne peux pas... Eh oui, je vends des poissons, moi, j'ai pas le temps !"]
                    self.pnjs[-1].dialogues_par_etat[2] = [
                        "Ben alors, qu'est-ce que tu fais encore là, tu t'es perdu ?",
                        "Rapporte son poisson à FRANCOIS, voyons !",
                        "Et si c'est fait, et que tu es perdu, va voir le BARMAN : il t'aidera toujours !"
                    ]

                elif obj.name == "pnj ARNOLD 0":
                    self.pnjs.append(PNJ(
                        nom="ARNOLD",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "Yop, moi c'est Arnold !",
                        "Chuis le chômeur du village (le frère du caissier) en quelques sorte.",
                        "J'ai un truc à lui d'ailleurs mais ça me sert à rien. Un colis...",
                        "Tiens, autant m'amuser : je te le donne si tu résous mon énigme.",
                        "Trois loups et trois moutons sont coincés d'un côté de la rivière avec une barque pour traverser. Ils veulent tous passer de l'autre côté, mais problème : seul deux animaux peuvent utiliser la barque à la fois.",
                        "De plus, si les loups se retrouvent en majorité numérique d'un côté ou de l'autre de la rivière après un trajet en barque, ils décideront de manger les moutons car ce sont de SALES ANIMAUX SANGUINAIRES.",
                        "(Je suis végan)",
                        "Compte tenu de toutes ces informations, combien de trajets simples faut-il au minimum pour que tous les animaux puissent traverser sans que personne ne se fasse manger ?"
                    ]
                    self.pnjs[-1].reponses_par_etat[0] = ["Je dirais... 13 essais !", "C'est 11, je crois", "Woaw ! Euh... 17 trajets ?"]
                    self.pnjs[-1].repliques_par_etat[0] = [
                        "Eh bien bravo, tu y étais presque ! C'était 11 essais. Bon, comme je suis gentil, je te laisse réessayer.",
                        "Oui, bravo ! C'est exactement ça. T'as répondu au hasard ouuuu... Enfin bref, voilà ton objet.",
                        "Perdu ! Réfléchis mieux la prochaine fois... Tu es vraiment nul dis donc ! Incroyable d'être aussi mauvais en maths comme ça. T'as maths spécifiques, toi, non ? Oui ? Ben ça se voit lol."
                    ]
                    self.pnjs[-1].dialogues_par_etat[1] = [
                        "Je t'ai déjà filé la caisse, va la redonner à mon frère. Et surtout ne l'ouvre pas, c'est secret."
                    ]
                    self.pnjs[-1].dialogues_par_etat[2] = [
                        "Ah, je vois que tu as refilé la caisse à mon frère ! Il devait être content de le retrouver, son colis. Tu veux savoir ce qu'il y avait à l'intérieur ?"
                    ]
                    self.pnjs[-1].reponses_par_etat[2] = ["Oui, c'était quoi ?","Non, certainement pas","Je l'avais déjà ouverte"]
                    self.pnjs[-1].repliques_par_etat[2] = [
                        "... Quelque chose d'assez amusant... Mais je ne te dirais pas, finalement ! Il t'as surement dit que c'était un colis Amazon ? Ce menteur...",
                        "Tu as raison, ce n'est pas tes affaires. Il faut savoir faire la part des choses et ne pas mettre son nez partout, surtout quand on est détective : ça aide à ne pas tomber dans de fausses pistes.",
                        "Ha ! Coquin va. Alors, que penses-tu de sa collection de conversation épistolaires ? Il garde toutes les lettres que ROSSIER lui envoie, il est fou amoureux. C'est marrant quand même non ? Il les fait même restaurer par un expert à la capitale, pour que rien ne se perde ! Il les avait envoyées il n'y a pas longtemps, d'ailleurs, c'est pour ça qu'elles étaient dans un colis."
                    ]
                    self.pnjs[-1].dialogues_par_etat[3] = [
                        "Laisse moi tranquille maintenant. Je dois méditer."
                    ]
                    self.pnjs[-1].dialogues_par_etat[4] = [
                        "Allez, réessaie"
                    ]

                elif obj.name == "pnj GUILLAUME 0":
                    self.pnjs.append(PNJ(
                        nom="GUILLAUME",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "Bongeour, ze sui Guiyôme !",
                        "Ze sui Disseuhlaicsyk.",
                        "Hici cé mah mèson.",
                        "El é billeun hein ?",
                        "Ze pass bokou deux tant hà lihrre shé mont voasein Arnold, ze lème bokou.",
                        "Tue ème lihrre twa ?"
                    ]
                    self.pnjs[-1].reponses_par_etat[0] = ["Oui, beaucoup !", "Non, pas tellement...", "MDRRRRRR IL SAIT PAS PARLER"]
                    self.pnjs[-1].repliques_par_etat[0] = [
                        "Koul ! nézzitte pa hà pahcet hà la billbibohrtèkke halor !",
                        "Oh, dôme âge... Ci tue shenjes dahvie, la billbibohrtèkke é hein nandroa koul.",
                        "... Je parle bien si je veux trou du cul. Là, t'es surpris hein ? Eh oe je suis pas dyslexique enft c'est juste pour toucher des allocs prcq j'ai la flemme de travailler. Quoi, tu vas poucav ? Mais qui va te croire ? Je vais t'accuser de moqueries envers les handicapés et tout le monde va te prendre pour quelqu'un de détraqué, un sale type qui n'a aucune compassion pour les diminués mentaux."
                    ]

                elif obj.name == "pnj FRANSOA 0":
                    self.pnjs.append(PNJ(
                        nom="FRANCOIS",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "Salut, moi c'est François !",
                        "Et toi ?",
                        "...",
                        "Tu veux pas me dire ?",
                        "Comme tu veux..."
                    ]
                    self.pnjs[-1].dialogues_par_etat[1] = [
                        "Eh, mais je connais cette clé !",
                        "Comme ça, tu enquêtes sur le vol ?",
                        "...",
                        "OK, anyway, tu veux pas répondre. Par contre, pour cette clé, je sais quelques trucs.",
                        "Va chercher ma commande à la poissonnerie au Sud du village, et je te dirais tout !",
                        "Tu sais quoi, je partagerai même le poisson avec toi, tu as l'air sympathique",
                        "Deal ?"
                    ]
                    self.pnjs[-1].reponses_par_etat[1] = ["OK, je te ramène ton poisson !", "Mouais, demande à quelqu'un d'autre", "Que penses-tu de la crise du hareng ?"]
                    self.pnjs[-1].repliques_par_etat[1] = [
                        "Nice ! Je t'attendrai ici alors.",
                        "Ok, comme tu veux. Mais sache que ma proposition tient toujours.",
                        "Je trouve que notre gouvernement ne s'intéresse pas assez à ce problème sociétal majeur. Mais je ne m'étendrai pas plus sur le sujet, car ça risque de mal finir."
                    ]
                    self.pnjs[-1].dialogues_par_etat[2] = [
                        "Parfait, tu m'as apporté le poisson ! Merci ! Voici tout ce que je sais :",
                        "Cette clé te servira pour débloquer le premier indice du laboratoire. Tu y trouvera des indices permettant d'avancer dans l'enquète.",
                    ]

                elif obj.name == "pnj LIVRE1 0":
                    self.pnjs.append(PNJ(
                        nom="LIVRE",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = [
                        "Tiens, un livre. C'est sur...",
                        "Les chants d'oiseaux en période de reproduction ?",
                        "C'est vraiment un sujet de PNE de merde. Qu'est-ce que t'en penses ?",
                        "(Oui, je suis un livre et je parle ya quoi.)",
                        "Alors ?"
                    ]
                    self.pnjs[-1].reponses_par_etat[0] = ["Oui, c'est très nul.", "Nan en vrai ça va... "]
                    self.pnjs[-1].repliques_par_etat[0] = [
                        "C'était le sujet de PNE de Paul, un des concepteurs de ce jeu. Il est vraiment con mdr.",
                        "J'aurais aimé proposer une BD sympa mais au lieu de ça..."
                    ]
                
                elif obj.name == "pnj LAST 0":
                    self.pnjs.append(PNJ(
                        nom="LA FIN ?",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        dialogue_lignes=[]
                    ))
                    self.pnjs[-1].dialogues_par_etat[0] = ["Le dernier portail ?"]
            
            
                elif obj.name == "pnj BIBLIO 0":
                    self.pnjs.append(PNJ(
                        nom = "MARCEAU le Bibliothécaire",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width, 
                        height=obj.height,
                        dialogue_lignes = [
                            "Bienvenue dans la bibliothèque",
                            "Essayez de faire le moins de bruit possible",
                            "les gens travaillent ici",
                            "Certains espèrent avoir 20 à la prochaine éval.",
                        ] 
                    ))

                elif obj.name == "pnj INDICATION1 0":
                        self.pnjs.append(PNJ(
                        nom = "INDICATION",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width, 
                        height=obj.height,
                        dialogue_lignes = []
                        ))
                        self.pnjs[-1].dialogues_par_etat[1] = [
                            "b-i-i-i-p",
                            "Clé reconnue.",
                            "Voici les indices :",
                            "Plusieurs tests ont été effectués...",
                            "Lorsque l'on met 291, 1 chiffre est correct et bien placé",
                            "Lorsque l'on met 245, 1 chiffre est correct mais mal placé",
                            "Lorsque l'on met 461, 2 chiffres sont corrects mais tous les deux mal placés",
                            "Le code est maintenant résolvable."
                        ]
                        self.pnjs[-1].dialogues_par_etat[0] = [
                            "Vous n'avez pas la clé pour avancer",
                            "Allez chercher la clé."
                        ]

            elif type == "enigme":

                if obj.name == "enigme musique 0":
                    self.enigme_maitre = Enigme(
                        nom="musique aléatoire",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        event="sound"
                    )
                    self.enigmes.append(self.enigme_maitre)
                elif obj.name == "enigme musique explication":
                    self.pnjs.append(PNJ(
                        nom = "INDICATION",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width, 
                        height=obj.height,
                        dialogue_lignes = [
                            "A LA RECHERCHE D'UN MUSICIEN TALENTUEUX",
                            "La harpe est cassée..."
                            "Il faut rejouer la mélodie produite pour le réparer",
                            "Pour cela, les pierres magiques sur le sol permettent de jouer les même sons que la harpe produit",
                            "Mais étant cassée, la harpe ne rejoue pas les même mélodie à chaque fois..."
                        ] 
                    ))
                elif obj.name.startswith("enigme musique"):
                    numero = int(obj.name.split(" ")[-1])
                    self.enigmes.append(EnigmeMusique(
                        numero=numero,
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        enigme_cible=self.enigme_maitre,
                        event="sound"
                    ))

                elif obj.name.startswith("enigme tp explication"):
                    numero = int(obj.name.split(" ")[-1])
                    if numero == 0:
                        explication = [
                                "Les portails ont été créées par Aperture Science",
                            ]
                    elif numero == 1:
                        explication = [
                                "+4BD2A5",
                            ]
                    elif numero == 2:
                        explication = [
                                "-348945",
                            ]
                    elif numero == 3:
                        explication = [
                                "Ajouter et soustraire",
                            ]
                    elif numero == 4:
                        explication = [
                                "Commencer au 2 lanternes bleu",
                            ]
                    elif numero == 5:
                        explication = [
                                "+18357A",
                            ]
                    elif numero == 6:
                        explication = [
                                "-2D7DD8",
                            ]
                    else:
                        explication = [
                                "Codes Hex",
                            ]

                    self.pnjs.append(PNJ(
                        nom = "INDICATION",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width, 
                        height=obj.height,
                        dialogue_lignes = explication
                    ))

                elif obj.name.startswith("enigme on/off"):
                    if switch.name == "grotte0":
                        self.enigmes.append(Enigme(
                            nom="levier",
                            x=obj.x,
                            y=obj.y,
                            width=obj.width,
                            height=obj.height,
                            event="on/off",
                            map="grotte1"
                        ))
                    elif switch.name == "grotte1":
                        self.enigmes.append(Enigme(
                            nom="levier",
                            x=obj.x,
                            y=obj.y,
                            width=obj.width,
                            height=obj.height,
                            event="on/off",
                            map="grotte0"
                        ))

                elif obj.name.startswith("enigme caisse"):
                        self.caisses = Caisse(
                            self.screen,
                            obj.x, 
                            obj.y
                        )
                        self.objets.append(self.caisses)
                        self.group.add(self.caisses) 
                elif obj.name.startswith("enigme plaque"):
                        numero = int(obj.name.split(" ")[-1])
                        self.plaques.append(Plaque(
                        numero=numero,
                        x=obj.x,
                        y=obj.y,
                        width=obj.width,
                        height=obj.height,
                        enigme_cible=self.caisses,
                        event="caisse"
                        ))
                elif obj.name == "enigme entrepot explication":
                        self.pnjs.append(PNJ(
                        nom = "INDICATION",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width, 
                        height=obj.height,
                        dialogue_lignes = [
                            "Il faut placer les boites sur toutes les plaques de pression pour pouvoir sortir",
                            "(Si tu te retrouve bloqué, appuie sur E et le niveau sera remis à zéro automatiquement).",
                        ]))
                        
                elif obj.name == "enigme code 0":
                        self.enigmes.append(Enigme(
                            nom="code",
                            x=obj.x,
                            y=obj.y,
                            width=obj.width,
                            height=obj.height,
                            event="code_0"
                        ))
                elif obj.name == "enigme code 1":
                        self.enigmes.append(Enigme(
                            nom="code",
                            x=obj.x,
                            y=obj.y,
                            width=obj.width,
                            height=obj.height,
                            event="code_1"
                        ))
                        
                elif obj.name == "enigme code_explication 1":
                        self.pnjs.append(PNJ(
                        nom = "INDICATION",
                        x=obj.x,
                        y=obj.y,
                        width=obj.width, 
                        height=obj.height,
                        dialogue_lignes = [
                            "Le code est composé de 4 chiffres distincts : ABCD",
                            "On sait seulement que ABCD X 4 = DCBA"
                        ]))
                        
            elif type == "reset":
                self.enigmes.append(Enigme(
                            nom="reset",
                            x=obj.x,
                            y=obj.y,
                            width=obj.width,
                            height=obj.height,
                            event="reset"
                        ))
                
            elif type == "secret":
                if obj.name.startswith("secret biblio"):
                    numero = int(obj.name.split(" ")[-1])
                    if numero == 0:
                        self.pnjs.append(PNJ(
                            nom = "LIVRE",
                            x=obj.x,
                            y=obj.y,
                            width=obj.width, 
                            height=obj.height,
                            dialogue_lignes = [
                                "Vingt Mille Lieues sous les mers",
                                "Ecrit par Jules Verne",
                                "Paru en 1869"
                            ] 
                        ))
                    elif numero == 1:
                        self.pnjs.append(PNJ(
                            nom = "LIVRE",
                            x=obj.x,
                            y=obj.y,
                            width=obj.width, 
                            height=obj.height,
                            dialogue_lignes = [
                                "Les Trois Mousquetaires",
                                "Ecrit par Alexandre Dumas",
                                "Paru en 1844"
                            ] 
                        ))
                    elif numero == 2:
                        self.pnjs.append(PNJ(
                            nom = "LIVRE",
                            x=obj.x,
                            y=obj.y,
                            width=obj.width, 
                            height=obj.height,
                            dialogue_lignes = [
                                "Le Cid",
                                "Ecrit par Pierre Corneille",
                                "paru en 1637"
                            ] 
                        ))
                    elif numero == 3:
                        self.pnjs.append(PNJ(
                            nom = "LIVRE",
                            x=obj.x,
                            y=obj.y,
                            width=obj.width, 
                            height=obj.height,
                            dialogue_lignes = [
                                "L'île du temps perdu",
                                "Ecrit par Silvana Gandolfi",
                                "Paru en 1997"
                            ] 
                        ))
                    else:
                        self.pnjs.append(PNJ(
                            nom = "LIVRE",
                            x=obj.x,
                            y=obj.y,
                            width=obj.width, 
                            height=obj.height,
                            dialogue_lignes = [
                                "Shingeki no Kyojin",
                                "Ecrit et dessiné par Hajime Isayama",
                                "Paru en 2009"
                            ] 
                        ))
                if obj.name=="secret grotte":
                        self.pnjs.append(PNJ(
                            nom = "Panneau",
                            x=obj.x,
                            y=obj.y,
                            width=obj.width, 
                            height=obj.height,
                            dialogue_lignes = [
                                "Mine contenant du diamand, or, fer, redstone, charbon, lapis et peut-être même de l'emeraude",
                                "I AM STEVE",
                                "(me voler pas mes ressources s'il vous plait)"
                            ] 
                        ))

        self.check_musique(switch)

        if self.player :
            self.pose_player(switch,self.player.tp_pos)
            self.player.align_hitbox()
            self.player.step = 16
            self.player.add_switchs(self.switchs)
            self.player.add_collisions(self.objets)
            self.group.add(self.player)
        self.current_map = switch

    def check_musique(self,switch):
            if self.musique==False:
                pygame.mixer.music.stop()
                if self.enigme_class:
                        self.enigme_class.canal.stop()	
            else:
                if switch.name == "biblio0":
                    pygame.mixer.music.stop()
                elif switch.name == "labo0":
                    pygame.mixer.music.load("enigma/assets/sound/Undertale OST 080 - Finale.mp3")
                    pygame.mixer.music.play(-1)
                elif switch.name.startswith("labo"):
                    pass
                elif switch.name == "grotte0":
                    pygame.mixer.music.load("enigma/assets/sound/Celeste.mp3")
                    pygame.mixer.music.play(-1)
                elif switch.name.startswith("grotte"):
                    pass
                elif switch.name == "gare0":
                    pygame.mixer.music.load("enigma/assets/sound/Celeste2.mp3")
                    pygame.mixer.music.play(-1)
                elif switch.name.startswith("gare"):
                    pass
                else:
                    pygame.mixer.music.load("enigma/assets/sound/backtrack_1.wav")
                    pygame.mixer.music.play(-1)
                    if self.enigme_class:
                        self.enigme_class.canal.stop()	

    def add_player(self, player) -> None:
        self.group.add(player)
        self.player = player
        self.player.align_hitbox()
        self.player.add_switchs(self.switchs)
        self.player.add_collisions(self.objets)

    def update(self) -> None:
        if self.player:
            if self.player.change_map:
                self.switch_map(self.player.change_map)
                self.player.change_map = None

        self.group.update()
        for sprite in self.group.sprites():
            self.group.change_layer(sprite, sprite.rect.bottom)
            
        self.group.center(self.player.rect.center)
        self.group.draw(self.screen.get_display())

        for pnj in self.pnjs:
            pnj.update_dialogue()
            if pnj.affiche_dialogue:
                pnj.afficher_boite_dialogue(self.screen.get_display())
                pnj.afficher_choix(self.screen.get_display())  # ← ici
        
        if self.current_map.name == "entrepot0":
            for plaque in self.plaques:
                plaque.update(self.player,self.objets,len(self.plaques))

        for enigme in self.enigmes:
            if isinstance(enigme, Enigme):
                enigme.mise_a_jour_sequence_sonore()





    def pose_player(self, switch: Collisions,player_pos=None):
        if player_pos:
            position = player_pos
            self.player.tp_pos = None
        else:
            position = self.tmx_data.get_object_by_name("spawn " + self.current_map.name + " " + str(switch.port))
        self.player.position = pygame.math.Vector2(position.x, position.y)