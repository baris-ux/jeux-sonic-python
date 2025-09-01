import pygame
from pathlib import Path
from player import Player
from items import RingManager
from enemy import Enemy

#BASE = Path(__file__).resolve().parent
BASE = Path(__file__).resolve().parent.parent
def asset(*p): return str(BASE.joinpath(*p))

def load_image(*parts):
    try:
        return pygame.image.load(asset(*parts)).convert_alpha()
    except Exception:
        return None

W, H = 800, 800
FLOOR_Y = 700
FPS = 60

class Jeu:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((W, H))
        pygame.display.set_caption("Sonic simple")

        # Icône (facultatif)
        icon = load_image("icone_sonic.png")
        if icon:
            pygame.display.set_icon(icon)

        sonic_img = load_image("sprites", "sonic_repos", "sonic_0.png")
        if sonic_img:
            sonic_img = pygame.transform.scale(sonic_img, (32, 48))
        self.player = Player(sonic_img, (100, FLOOR_Y - 48))
        self.enemy = Enemy((400, FLOOR_Y - 30), w=30, h=30) 
        

        # Anneaux
        ring_img = load_image("anneau.png")
        self.rings = RingManager(ring_img, FLOOR_Y)

        self.font = pygame.font.Font(None, 32)
        self.clock = pygame.time.Clock()

    def _draw(self):
        self.window.fill((0, 0, 0))
        pygame.draw.rect(self.window, (50, 50, 50), (0, FLOOR_Y, W, H - FLOOR_Y))
        self.rings.draw(self.window)
        self.enemy.draw(self.window)
        self.player.draw(self.window)
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
            self.rings.collect(self.player.rect)
            self.enemy.update(dt)

            if self.player.rect.colliderect(self.enemy.rect) and self.player.invincible_timer <= 0:
                print("touché par ennemy !")
                self.player.invincible_timer += 3.0
                if self.player.rect.centerx < self.enemy.rect.centerx:
                    self.player.rect.x -= 60 
                else:
                    self.player.rect.x += 60

            if self.player.invincible_timer > 0:
                self.player.invincible_timer -= dt 
                    

            self._draw()
        pygame.quit()

if __name__ == "__main__":
    Jeu().running()
