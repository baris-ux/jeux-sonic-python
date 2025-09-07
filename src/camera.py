import pygame

class Camera:
    def __init__(self, screen_w, screen_h):
        self.offset_x = 0
        self.offset_y = 0
        self.screen_w = screen_w
        self.screen_h = screen_h

    def update(self, player):
        # centrer la caméra sur le joueur
        self.offset_x = player.rect.centerx - self.screen_w // 2
        self.offset_y = player.rect.centery - self.screen_h // 2

    def apply(self, rect):
        # renvoyer un rect décalé par la caméra
        return rect.move(-self.offset_x, -self.offset_y)
