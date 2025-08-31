import pygame
from pathlib import Path

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

        try:
            pygame.display.set_icon(pygame.image.load(asset("icone_sonic.png")))
        except:
            pass

        # Sonic : rectangle ou sprite
        try:
            self.sonic_img = pygame.image.load(asset("sprites", "sonic_direction_haut.png")).convert_alpha()
        except:
            self.sonic_img = None

        self.sonic_rect = pygame.Rect(100, FLOOR_Y-48, 32, 48)
        self.vel_y = 0
        self.on_ground = True

        # Anneaux
        try:
            self.ring_img = pygame.image.load(asset("anneau.png")).convert_alpha()
        except:
            self.ring_img = None
        self.rings = [pygame.Rect(300, FLOOR_Y-32, 24, 24),
                      pygame.Rect(500, FLOOR_Y-32, 24, 24),
                      pygame.Rect(650, FLOOR_Y-32, 24, 24)]
        self.score = 0
        self.font = pygame.font.Font(None, 32)

        self.clock = pygame.time.Clock()

    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.sonic_rect.x -= int(220 * dt)
        if keys[pygame.K_RIGHT]:
            self.sonic_rect.x += int(220 * dt)
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -420
            self.on_ground = False

    def physics(self, dt):
        self.vel_y += 1200 * dt
        self.sonic_rect.y += int(self.vel_y * dt)
        if self.sonic_rect.bottom >= FLOOR_Y:
            self.sonic_rect.bottom = FLOOR_Y
            self.vel_y = 0
            self.on_ground = True

    def collect_rings(self):
        for r in self.rings[:]:
            if self.sonic_rect.colliderect(r):
                self.rings.remove(r)
                self.score += 1

    def draw(self):
        self.window.fill((0, 0, 0))
        pygame.draw.rect(self.window, (50, 50, 50), (0, FLOOR_Y, W, H-FLOOR_Y))
        for r in self.rings:
            if self.ring_img:
                self.window.blit(self.ring_img, r)
            else:
                pygame.draw.ellipse(self.window, (255, 215, 0), r, 3)
        if self.sonic_img:
            self.window.blit(self.sonic_img, self.sonic_rect)
        else:
            pygame.draw.rect(self.window, (0, 120, 255), self.sonic_rect)
        txt = self.font.render(f"Points : {self.score}", True, (255,255,255))
        self.window.blit(txt, (10, 10))
        pygame.display.flip()

    def running(self):
        run = True
        while run:
            dt = self.clock.tick(FPS) / 1000
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    run = False
            self.handle_input(dt)
            self.physics(dt)
            self.collect_rings()
            self.draw()
        pygame.quit()

if __name__ == "__main__":
    Jeu().running()
