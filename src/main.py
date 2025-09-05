import pygame
from pathlib import Path
from player import Player
from items import RingManager
from enemy import Enemy
from map import Map

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

        ########################

        sonic_img = load_image("sprites", "sonic_repos", "sonic_0.png")
        if sonic_img:
            sonic_img = pygame.transform.scale(sonic_img, (32, 48))

        self.player = Player(sonic_img, (100, 200))

        #####################

        self.enemies = [
            Enemy((400, 0), w=50, h=50)
        ]

        ####################""
        

        # Anneaux
        ring_img = load_image("anneau.png")
        self.rings = RingManager(ring_img)

        self.font = pygame.font.Font(None, 32)
        self.clock = pygame.time.Clock()
        
        ########################################

        try:
            self.gain_ring_sound = pygame.mixer.Sound(asset("sounds","gain_ring.wav"))
            self.gain_ring_sound.set_volume(0.8)
        except Exception as e:
            self.gain_ring_sound = None
            print("Impossible de charger le son de drop rings:", e)

        try:
            self.enemy_defeated = pygame.mixer.Sound(asset("sounds","enemy_defeated.wav"))
            self.enemy_defeated.set_volume(0.8)
        except Exception as e:
            self.enemy_defeated = None
            print("Impossible de charger le enemy defeated:", e)

        ############### chargement de la map tiled ##############

        self.map = Map(asset("maps", "map_1.tmx"), debug_colliders=True)

        ##########################################

    def _draw(self):
        self.map.draw(self.window)
        
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

            # Player d'abord
            self.player.handle_input(dt)

            # Un seul get_colliders par frame
            colliders = self.map.get_colliders()

            # Physique du joueur avec collisions
            self.player.physics(dt, colliders)

            # Timer d'invincibilité
            if self.player.invincible_timer > 0:
                self.player.invincible_timer = max(0.0, self.player.invincible_timer - dt)

            # ✅ ENNEMIS : update + collisions avec le joueur (DANS la boucle)
            for enemy in self.enemies[:]:   # [:] = copie pour pouvoir remove
                enemy.update(dt, colliders)

                # collisions player <-> ennemi
                if self.player.rect.colliderect(enemy.rect):
                    overlap = self.player.rect.clip(enemy.rect)

                    if overlap.width > overlap.height:
                        # collision verticale
                        if self.player.rect.centery < enemy.rect.centery:
                            print("Sonic a touché l'ennemi PAR LE HAUT")
                            self.enemies.remove(enemy)   # supprimer cet ennemi
                            self.player.vel_y = -400     # rebond
                            if self.enemy_defeated:
                                self.enemy_defeated.play()
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

                            self.rings.score = 0

            # ✅ ANNEAUX : gravité + collisions AVANT la collecte
            self.rings.update(dt, colliders)

            # ✅ Collecte APRÈS la mise à jour
            collected = self.rings.collect(self.player.rect) or 0
            if collected > 0 and self.gain_ring_sound:
                self.gain_ring_sound.play()

            # Dessin
            self._draw()
        pygame.quit()


if __name__ == "__main__":
    Jeu().running()
