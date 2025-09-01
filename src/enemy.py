import pygame

class Enemy:
    def __init__(self, start_pos, w=50, h=50, color=(200, 50, 50)):
        self.rect = pygame.Rect(start_pos[0], start_pos[1], w, h)
        self.color = color

        self.speed = 100
        self.direction = -1

    def update(self, dt):
        self.rect.x += int(self.speed * self.direction * dt)

        if self.rect.left < 0 or self.rect.right > 800:
            self.direction *= -1


    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect, border_radius=6)
