import pygame
from pathlib import Path
from player import Player
from items import RingManager

BASE = Path(__file__).resolve().parent
def asset(*p): return str(BASE.joinpath(*p))

W, H = 800, 800
FLOOR_Y = 700
FPS = 60

class Jeu:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((W, H))
        pygame.display.set_caption("Sonic simple")

        # Icône (facultatif)
        try:
            pygame.display.set_icon(pygame.image.load(asset("icone_sonic.png")))
        except:
            pass

        # Sprite Sonic (facultatif)
        try:
            sonic_img = pygame.image.load(asset("sprites", "sonic_direction_haut.png")).convert_alpha()
        except:
            sonic_img = None
        self.player = Player(sonic_img, (100, FLOOR_Y - 48))

        try:
            ring_img = pygame.image.load(asset("anneau.png")).convert_alpha()
        except:
            ring_img = None
        self.rings = RingManager(ring_img, FLOOR_Y)

        self.font = pygame.font.Font(None, 32)
        self.clock = pygame.time.Clock()

    def _draw(self):
        # Fond + sol
        self.window.fill((0, 0, 0))
        pygame.draw.rect(self.window, (50, 50, 50), (0, FLOOR_Y, W, H - FLOOR_Y))

        # Anneaux + joueur
        self.rings.draw(self.window)
        self.player.draw(self.window)

        # Score (depuis RingManager)
        txt = self.font.render(f"Points : {self.rings.score}", True, (255, 255, 255))
        self.window.blit(txt, (10, 10))

        pygame.display.flip()

    def running(self):
        run = True
        while run:
            dt = self.clock.tick(FPS) / 1000
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    run = False

            self.player.handle_input(dt)
            self.player.physics(dt, FLOOR_Y)
            self.rings.collect(self.player.rect)  # <- collecte via RingManager
            self._draw()

        pygame.quit()

if __name__ == "__main__":
    Jeu().running()
