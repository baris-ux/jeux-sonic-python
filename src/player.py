import pygame 

class Player:
    def __init__(self, img, start_pos):
        self.image = img
        self.rect = pygame.Rect(start_pos[0], start_pos[1], 32, 48)
        self.vel_y = 0
        self.on_ground = 0

    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= int(220 * dt)
        if keys[pygame.K_RIGHT]:
            self.rect.x += int(220 * dt)
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = -420
            self.on_ground = False

    def physics(self, dt, floor_y=700):
        self.vel_y += 1200 * dt
        self.rect.y += int(self.vel_y * dt)
        if self.rect.bottom >= floor_y:
            self.rect.bottom = floor_y
            self.vel_y = 0
            self.on_ground = True

    def draw(self, window):
        if self.image:
            window.blit(self.image, self.rect)
        else:
            pygame.draw.rect(window, (0, 120, 255), self.rect)