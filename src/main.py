import pygame
import pytmx
from pathlib import Path
from player import Player
from items import RingManager

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

        # Chargement de la map TMX
        self.tmx_data = pytmx.load_pygame(asset("maps", "map_sonic"), pixelalpha=True)
        print(self.tmx_data.tilewidth, self.tmx_data.tileheight)  # ← ici
        print(self.tmx_data.width, self.tmx_data.height)  
        self.collision_rects = self._load_collisions()

        sonic_img = load_image("sprites", "sonic_repos", "sonic_0.png")
        self.player = Player(sonic_img, (100, FLOOR_Y - 48))

        ring_img = load_image("anneau.png")
        self.rings = RingManager(ring_img, FLOOR_Y)

        self.font = pygame.font.Font(None, 32)
        self.clock = pygame.time.Clock()

    def _load_collisions(self):
        """Récupère les rectangles de collision depuis le calque objet Tiled."""
        rects = []
        for layer in self.tmx_data.objectgroups:
            for obj in layer:
                rects.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        return rects

    def _draw_map(self):
        offset_y = -75  # ajuste cette valeur jusqu'à ce que ce soit bon
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, surf in layer.tiles():
                    self.window.blit(surf, (x * self.tmx_data.tilewidth,
                                        y * self.tmx_data.tileheight + offset_y))

    def _draw(self):
        self.window.fill((0, 0, 0))
        self._draw_map()
        self.rings.draw(self.window)
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
            self.player.physics(dt, FLOOR_Y, self.collision_rects)
            self.rings.collect(self.player.rect)
            self._draw()
        pygame.quit()

if __name__ == "__main__":
    Jeu().running()