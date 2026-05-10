import pygame
import pytmx
from pathlib import Path
from player import Player
from items import RingManager
from mob import Mob

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

        icon = load_image("icone_sonic.png")
        if icon:
            pygame.display.set_icon(icon)

        self.tmx_data = pytmx.load_pygame(asset("maps", "map_sonic.tmx"), pixelalpha=True)
        self.collision_rects = self._load_collisions()

        sonic_img = load_image("sprites", "sonic_repos", "sonic_0.png")
        self.player = Player(sonic_img, (100, FLOOR_Y - 48))

        ring_img = load_image("anneau.png")
        self.rings = RingManager(ring_img, FLOOR_Y)

        self.font = pygame.font.Font(None, 32)
        self.clock = pygame.time.Clock()

        self.map_pixel_w = self.tmx_data.width * self.tmx_data.tilewidth
        self.map_pixel_h = self.tmx_data.height * self.tmx_data.tileheight

        self.cam_x = 0
        self.cam_y = 0

        self.mobs = [
            Mob(400, FLOOR_Y - 48),
            Mob(700, FLOOR_Y - 48),
        ]
        self.game_over = False

    def _reset(self):
        sonic_img = load_image("sprites", "sonic_repos", "sonic_0.png")
        self.player = Player(sonic_img, (100, FLOOR_Y - 48))
        ring_img = load_image("anneau.png")
        self.rings = RingManager(ring_img, FLOOR_Y)
        self.mobs = [
            Mob(400, FLOOR_Y - 48),
            Mob(700, FLOOR_Y - 48),
        ]
        self.cam_x = 0
        self.cam_y = 0
        self.game_over = False

    def _update_camera(self):
        self.cam_x = self.player.rect.centerx - W // 2 + 50
        self.cam_y = self.player.rect.centery - H // 2
        self.cam_x = max(0, min(self.cam_x, self.map_pixel_w - W))
        self.cam_y = max(0, min(self.cam_y, self.map_pixel_h - H))

    def _load_collisions(self):
        rects = []
        for layer in self.tmx_data.objectgroups:
            for obj in layer:
                rects.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        return rects

    def _draw_map(self):
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, surf in layer.tiles():
                    self.window.blit(surf, (
                        x * self.tmx_data.tilewidth - self.cam_x,
                        y * self.tmx_data.tileheight - self.cam_y - 75
                    ))

    def _draw_game_over(self):
        self.window.fill((0, 0, 0))
        self._draw_map()

        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.window.blit(overlay, (0, 0))

        font_big = pygame.font.Font(None, 80)
        font_small = pygame.font.Font(None, 36)

        txt = font_big.render("GAME OVER", True, (220, 50, 50))
        self.window.blit(txt, (W // 2 - txt.get_width() // 2, H // 2 - 80))

        txt2 = font_small.render("Appuie sur R pour rejouer", True, (255, 255, 255))
        self.window.blit(txt2, (W // 2 - txt2.get_width() // 2, H // 2 + 20))

        pygame.display.flip()

    def _draw(self):
        self.window.fill((0, 0, 0))
        self._draw_map()
        self.rings.draw(self.window, self.cam_x, self.cam_y)
        for mob in self.mobs:
            mob.draw(self.window, self.cam_x, self.cam_y)
        self.player.draw(self.window, self.cam_x, self.cam_y)
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
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_r and self.game_over:
                        self._reset()

            if not self.game_over:
                self.player.handle_input(dt)
                self.player.physics(dt, FLOOR_Y, self.collision_rects)
                self.player.rect.x = max(0, min(self.player.rect.x, self.map_pixel_w - self.player.rect.width))
                self.player.rect.y = max(0, min(self.player.rect.y, self.map_pixel_h - self.player.rect.height))
                self._update_camera()
                self.rings.collect(self.player.rect)

                for mob in self.mobs:
                    mob.update(dt, self.map_pixel_w)
                    if mob.rect.colliderect(self.player.rect):
                        # Dash ou saut par le haut → éliminer le mob
                        if self.player.dashing or (self.player.vel_y > 0 and self.player.rect.bottom < mob.rect.centery):
                            self.mobs.remove(mob)
                            if not self.player.dashing:
                                self.player.vel_y = -400
                            break
                        else:
                            if self.rings.score == 0:
                                self.game_over = True
                                if self.player.run_sound:
                                    self.player.run_sound.stop()
                                self.player.vel_y = 0
                                break
                            else:
                                self.rings.score -= 1
                                self.player.rect.x += 100 if self.player.rect.x < mob.rect.x else -100

                self._draw()
            else:
                self._draw_game_over()

        pygame.quit()

if __name__ == "__main__":
    Jeu().running()