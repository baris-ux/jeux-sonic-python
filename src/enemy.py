import pygame

class Enemy:
    def __init__(self, start_pos, w=50, h=50):
        self.rect = pygame.Rect(start_pos[0], start_pos[1], w, h)

        # Charge les images
        self.image_right = pygame.image.load("sprites/motobug/droite/droite.png").convert_alpha()
        self.image_left  = pygame.image.load("sprites/motobug/gauche/gauche.png").convert_alpha()

        # Redimensionne si nécessaire (ici à la taille du rect)
        self.image_right = pygame.transform.scale(self.image_right, (w, h))
        self.image_left  = pygame.transform.scale(self.image_left, (w, h))

        # Direction initiale
        self.speed = 100
        self.direction = -1  # -1 = gauche, +1 = droite

    def update(self, dt):
        self.rect.x += int(self.speed * self.direction * dt)

        if self.rect.left < 0 or self.rect.right > 800:
            self.direction *= -1

    def draw(self, window):
        # Choisir l'image selon la direction
        if self.direction == 1:
            window.blit(self.image_right, self.rect)
        else:
            window.blit(self.image_left, self.rect)
