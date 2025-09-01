# --- en haut du fichier ---
import pygame
import pytmx
from pathlib import Path

class Map:
    def __init__(self, tmx_path, debug_colliders=False):
        self.debug_colliders = debug_colliders

        self.tmx = pytmx.util_pygame.load_pygame(tmx_path, pixelalpha=True)

        tw, th = self.tmx.tilewidth, self.tmx.tileheight
        width, height = self.tmx.width * tw, self.tmx.height * th

        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self._render_layers()

        # --- RÉCUPÈRE LES COLLIDERS DEPUIS LE CALQUE D’OBJETS "collisions"
        self.colliders = []
        for layer in self.tmx.layers:
            if isinstance(layer, pytmx.TiledObjectGroup) and layer.name == "collisions":
                for obj in layer:
                    # on ne gère que les rectangles (width/height > 0)
                    if getattr(obj, "visible", True) and obj.width and obj.height:
                        rect = pygame.Rect(int(obj.x), int(obj.y), int(obj.width), int(obj.height))
                        self.colliders.append(rect)

        # --- SPAWN: accepte "spawn_player" où qu’il soit
        self.spawn = (100, 100)
        found_spawn = False
        for layer in self.tmx.layers:
            if isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if obj.name == "spawn_player":
                        self.spawn = (int(obj.x), int(obj.y))
                        found_spawn = True
                        break
            if found_spawn:
                break

    def _render_layers(self):
        tw, th = self.tmx.tilewidth, self.tmx.tileheight
        for layer in self.tmx.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx.get_tile_image_by_gid(gid)
                    if tile:
                        self.surface.blit(tile, (x * tw, y * th))

    def draw(self, screen):
        screen.blit(self.surface, (0, 0))
        if self.debug_colliders:
            for r in self.colliders:
                s = pygame.Surface((r.width, r.height), pygame.SRCALPHA)
                s.fill((255, 0, 0, 80))  # rouge semi-transparent
                screen.blit(s, (r.x, r.y))

    def get_colliders(self):
        return self.colliders

    def get_spawn(self):
        return self.spawn
