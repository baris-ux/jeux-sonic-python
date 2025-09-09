import pygame

class Enemy:
    def __init__(self, start_pos, w=50, h=50, world_w=None):
        self.rect = pygame.Rect(start_pos[0], start_pos[1], w, h)

        self.image_right = pygame.image.load("sprites/motobug/droite/droite.png").convert_alpha()
        self.image_left  = pygame.image.load("sprites/motobug/gauche/gauche.png").convert_alpha()

        self.image_right = pygame.transform.scale(self.image_right, (w, h))
        self.image_left  = pygame.transform.scale(self.image_left, (w, h))

        self.speed = 100
        self.direction = -1  # -1 = gauche, +1 = droite

        self.world_w = world_w


        # ------- Physique ---------- #

        self.vel_y = 0
        self.gravity = 2000
        self.on_ground = False
        self.pos_x = float(self.rect.x)
        self.pos_y = float(self.rect.y)


    def update(self, dt, colliders):
        # --------- HORIZONTAL ---------
        dx = self.speed * self.direction * dt

        # sous-pixel: avancer en float puis caster en int
        self.pos_x += dx
        self.rect.x = int(self.pos_x)

        # 1) Demi-tour si on tape un mur (collision horizontale)
        hit_wall = False
        for r in colliders:
            if self.rect.colliderect(r):
                if dx > 0:
                    self.rect.right = r.left
                elif dx < 0:
                    self.rect.left = r.right
                self.pos_x = float(self.rect.x)   # resync float
                self.direction *= -1
                hit_wall = True
                break

        # 2) Bornes du MONDE (pas l’écran)
        if self.world_w is not None:
            if self.rect.left <= 0:
                self.rect.left = 0
                self.pos_x = float(self.rect.x)
                self.direction = 1
            elif self.rect.right >= self.world_w:
                self.rect.right = self.world_w
                self.pos_x = float(self.rect.x)
                self.direction = -1

        # --------- VERTICAL (gravité) ---------
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
                        # on tombait -> on atterrit
                        self.rect.bottom = r.top
                        self.pos_y = float(self.rect.y)
                        self.vel_y = 0.0
                        self.on_ground = True
                        collided = True
                        break
                    elif self.vel_y < 0:
                        # on montait -> plafond
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