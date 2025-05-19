import pygame


class Screen:
    def __init__(self):
        WIDTH, HEIGHT = (1920, 1080)
        self.display: pygame.display = pygame.display.set_mode((WIDTH, HEIGHT),pygame.FULLSCREEN)
        pygame.display.set_caption("Enigma")
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.framerate: int = 144
        self.deltatime: float = 0.0
        self.icone = pygame.image.load("enigma/assets/images/icone_jeu.png")
        pygame.display.set_icon(self.icone)

    def update(self) -> None:
        pygame.display.update()
        self.clock.tick(self.framerate)
        self.display.fill((0, 0, 0))
        self.deltatime = self.clock.get_time()

    def get_delta_time(self) -> float:
        return self.deltatime

    def get_size(self) -> tuple[int, int]:
        return self.display.get_size()

    def get_display(self) -> pygame.display:
        return self.display
