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
        self.enemies = [
            Enemy((400, FLOOR_Y - 30), w=30, h=30)
        ]
        

        # Anneaux
        ring_img = load_image("anneau.png")
        self.rings = RingManager(ring_img, FLOOR_Y)

        self.font = pygame.font.Font(None, 32)
        self.clock = pygame.time.Clock()

    def _draw(self):
        self.window.fill((0, 0, 0))
        pygame.draw.rect(self.window, (50, 50, 50), (0, FLOOR_Y, W, H - FLOOR_Y))
        self.rings.draw(self.window)
        for enemy in self.enemies:
            enemy.draw(self.window)
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

            if self.player.invincible_timer > 0:
                self.player.invincible_timer = max(0.0, self.player.invincible_timer - dt)

            for enemy in self.enemies[:]:   # [:] = copie pour pouvoir remove
                enemy.update(dt)

                if self.player.rect.colliderect(enemy.rect):
                    overlap = self.player.rect.clip(enemy.rect)

                    if overlap.width > overlap.height:
                        # collision verticale
                        if self.player.rect.centery < enemy.rect.centery:
                            print("Sonic a touché l'ennemi PAR LE HAUT")
                            self.enemies.remove(enemy)   # supprimer cet ennemi
                            self.player.vel_y = -400     # rebond
                        else:
                            print("Sonic a touché l'ennemi PAR LE BAS")
                    else:
                        # collision horizontale
                        if self.player.invincible_timer <= 0: 
                            if self.player.rect.centerx < enemy.rect.centerx:
                                print("Sonic a touché l'ennemi PAR LA GAUCHE")
                                self.player.rect.x -= 150

                            else:
                                print("Sonic a touché l'ennemi PAR LA DROITE")
                                self.player.rect.x += 150

                            self.player.invincible_timer = 4.0
                            if self.player.drop_rings_sound and self.rings.score > 0: 
                                self.player.drop_rings_sound.play()

                            self.rings.score = 0 # importent :  On joue d'abord le son et pui on met a 0 le score sinon le son ne sera jamais joué si il perd ses anneau avant !

            self._draw()
        pygame.quit()

if __name__ == "__main__":
    Jeu().running()
