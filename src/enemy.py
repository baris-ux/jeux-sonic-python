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


        # ------- Physique ---------- #

        self.vel_y = 0
        self.gravity = 2000
        self.on_ground = False
        self.pos_y = float(self.rect.y)


    def update(self, dt, colliders):
        self.rect.x += int(self.speed * self.direction * dt)

        if self.rect.left < 0 or self.rect.right > 800:
            self.direction *= -1

        self.vel_y += self.gravity * dt
        dy = self.vel_y * dt

        STEP = 6.0
        steps = max(1, int(abs(dy) // STEP))
        step = dy / steps if steps > 0 else 0.0

        self.on_ground = False
        for _ in range(steps):
            prev_bottom = self.rect.bottom
            self.pos_y += step
            self.rect.y = int(self.pos_y)

            collided = False
            for r in colliders:
                if self.rect.colliderect(r):
                    if self.vel_y > 0 and prev_bottom <= r.top:
                        # on tombe et on atterrit
                        self.rect.bottom = r.top
                        self.pos_y = float(self.rect.y)
                        self.vel_y = 0.0
                        self.on_ground = True
                        collided = True
                        break
                    elif self.vel_y < 0:
                        # on montait et on tape un plafond
                        self.rect.top = r.bottom
                        self.pos_y = float(self.rect.y)
                        self.vel_y = 0.0
                        collided = True
                        break
            if collided and self.on_ground:
                break

    def draw(self, window, camera=None):
        img = self.image_right if self.direction == 1 else self.image_left
        draw_rect = self.rect if camera is None else camera.apply(self.rect)
        window.blit(img, draw_rect)