# items.py
import pygame

class RingManager:
    def __init__(self, ring_img, floor_y):
        self.ring_img = ring_img
        self.rings = [
            pygame.Rect(300, floor_y - 32, 24, 24),
            pygame.Rect(500, floor_y - 32, 24, 24),
            pygame.Rect(650, floor_y - 32, 24, 24),
        ]
        self.score = 0

    def collect(self, player_rect):
        collected = 0
        for r in self.rings[:]:
            if player_rect.colliderect(r):
                self.rings.remove(r)
                self.score += 1
                collected += 1
        return collected

    def draw(self, window):
        for r in self.rings:
            if self.ring_img:
                window.blit(self.ring_img, r)
            else:
                pygame.draw.ellipse(window, (255, 215, 0), r, 3)
