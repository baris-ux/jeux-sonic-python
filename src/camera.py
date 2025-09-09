import pygame

class Camera:
    def __init__(self, screen_w, screen_h):
        # la taille de l'écran
        self.screen_w = screen_w
        self.screen_h = screen_h 

        # position de la caméra
        self.offset_x = 0
        self.offset_y = 0

        # la taille du monde (le fichier.tmx)
        self.world_w = screen_w
        self.world_h = screen_h

    def world_size(self, world_w, world_h):
        self.world_w = world_w
        self.world_h = world_h

    def update(self, player):

        # centrer la caméra sur le joueur
        cx = player.rect.centerx - self.screen_w // 2
        cy = player.rect.centery - self.screen_h // 2

        # 
        max_x = max(0, self.world_w - self.screen_w)
        max_y = max(0, self.world_h - self.screen_h)

        self.offset_x = max(0, min(cx, max_x))
        self.offset_y = max(0, min(cy, max_y))

    def apply(self, rect):
        # renvoyer un rect décalé par la caméra
        return rect.move(-self.offset_x, -self.offset_y)
