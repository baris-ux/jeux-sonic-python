# items.py
import pygame

class RingManager:
    
    def __init__(self, ring_img):
        self.rings = [
            Ring(300, 0, 24, ring_img),  
            Ring(500, 0, 24, ring_img),
            Ring(650, 0, 24, ring_img),
        ]
        self.score = 0

    def update(self, dt, colliders):
        for ring in self.rings:
            ring.update(dt, colliders)

    def collect(self, player_rect):
        collected = 0
        for ring in self.rings[:]:
            if player_rect.colliderect(ring.rect):
                self.rings.remove(ring)
                self.score += 1
                collected += 1
        return collected

    def draw(self, window, camera=None):
        for ring in self.rings:
            ring.draw(window, camera)


class Ring:
    def __init__(self, x, y, size=24, img=None):
        self.rect = pygame.Rect(x, y, size, size)
        self.pos_y = float(y)
        self.vel_y = 0.0
        self.gravity = 2000.0
        self.on_ground = False
        self.img = pygame.transform.smoothscale(img, (self.rect.w, self.rect.h)) if img else None

    def draw(self, window, camera=None):
        draw_rect = self.rect if camera is None else camera.apply(self.rect)

        if self.img:
            window.blit(self.img, draw_rect)
        else:
            pygame.draw.ellipse(window, (255, 215, 0), draw_rect, 3)

    def update(self, dt, colliders):
        self.vel_y += self.gravity * dt
        dy = self.vel_y * dt

        STEP = 6.0
        steps = max(1, int(abs(dy) // STEP))
        step = dy / steps

        self.on_ground = False
        for _ in range(steps):
            prev_bottom = self.rect.bottom
            self.pos_y += step
            self.rect.y = int(self.pos_y)

            collided = False
            for r in colliders:
                if self.rect.colliderect(r):
                    if self.vel_y > 0 and prev_bottom <= r.top:
                        self.rect.bottom = r.top
                        self.pos_y = float(self.rect.y)
                        self.vel_y = 0.0
                        self.on_ground = True
                        collided = True
                        break
                    elif self.vel_y < 0:
                        self.rect.top = r.bottom
                        self.pos_y = float(self.rect.y)
                        self.vel_y = 0.0
                        collided = True
                        break
            if collided:
                break
