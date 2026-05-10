import pygame

class Mob:
    def __init__(self, x, y, w=48, h=48):
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = 100
        self.direction = 1  # 1 = droite, -1 = gauche
        self.color = (220, 50, 50)

    def update(self, dt, map_w):
        self.rect.x += self.speed * self.direction * dt

        # Fait demi-tour aux bords de la map
        if self.rect.right >= map_w:
            self.direction = -1
        elif self.rect.left <= 0:
            self.direction = 1

    def draw(self, window, cam_x=0, cam_y=0):
        draw_rect = self.rect.move(-cam_x, -cam_y)
        pygame.draw.rect(window, self.color, draw_rect, border_radius=6)