import pygame
import pytmx # lit les fichiers pytmx 
from pytmx.util_pygame import load_pygame

class Map:
    def __init__(self, tmx_path, debug_colliders=False):
        self.debug_colliders = debug_colliders

        self.tmx = load_pygame(tmx_path, pixelalpha=True)
        tw, th = self.tmx.tilewidth, self.tmx.tileheight # On récupère la largeur et la hauteur d'une tuile
        self.width  = self.tmx.width  * tw # la largeur de la map en pixel = largeur du fichier tmx * largeur d'une tuile 
        self.height = self.tmx.height * th # la hauteur de la map en pixel = hauteur du fichier tmx * la hautueur d'une tuile

        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self._render_layers()

        self.colliders = []
        try:
            obj_layer = self.tmx.get_layer_by_name("Collisions")
            for obj in obj_layer:
                if getattr(obj, "width", 0) and getattr(obj, "height", 0):
                    rect = pygame.Rect(int(obj.x), int(obj.y - obj.height), int(obj.width), int(obj.height))
                    self.colliders.append(rect)
                elif getattr(obj, "points", None):
                    xs = [p[0] for p in obj.points]
                    ys = [p[1] for p in obj.points]
                    x, y = int(obj.x + min(xs)), int(obj.y + min(ys))
                    w, h = int(max(xs) - min(xs)), int(max(ys) - min(ys))
                    self.colliders.append(pygame.Rect(x, y, w, h))
        except KeyError:
            self.colliders = []

    def _render_layers(self):
        tw, th = self.tmx.tilewidth, self.tmx.tileheight
        for layer in self.tmx.visible_layers:
            if hasattr(layer, "tiles"):
                for x, y, data in layer.tiles():
                    # Avec load_pygame, 'data' est déjà une Surface
                    if isinstance(data, pygame.Surface):
                        img = data
                    else:
                        img = self.tmx.get_tile_image_by_gid(data)

                    if img:
                        self.surface.blit(img, (x * tw, y * th))

    def draw(self, screen):
        screen.blit(self.surface, (0, 0))
        if self.debug_colliders:
            for r in self.colliders:
                s = pygame.Surface((r.width, r.height), pygame.SRCALPHA)
                s.fill((255, 0, 0, 80))  # rouge semi-transparent
                screen.blit(s, (r.x, r.y))

    def get_colliders(self):
        return self.colliders
