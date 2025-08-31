import pygame
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
def asset(*parts):
    return str(BASE.joinpath(*parts))

def load_image(*parts):
    try:
        return pygame.image.load(asset(*parts)).convert_alpha()
    except Exception:
        return None

class Player:
    def __init__(self, img, start_pos, w=32, h=48):
        if img:
            img = pygame.transform.scale(img, (w, h))
        self.default_img = img
        self.image = img

        self.rect = pygame.Rect(start_pos[0], start_pos[1], w, h)

        # physique / états
        self.vel_y = 0
        self.on_ground = False
        self.speed = 220
        self.jump_velocity = -420
        self.gravity = 1200

        # --- Animation "flèche bas" (one-shot) ---
        # Charge sonic_0.png .. sonic_5.png depuis sprites/deplacement_en_bas/
        self.down_frames = []
        for i in range(4):
            frame = load_image("sprites", "deplacement_en_bas", f"sonic_{i}.png")
            if frame:
                self.down_frames.append(pygame.transform.scale(frame, (w, h)))

        # État de l’anim
        self.down_playing = False       # en lecture ?
        self.down_can_restart = True    # autorisé à redémarrer sur prochain appui ?
        self.down_index = 0             # frame courante
        self.down_timer = 0.0           # chrono pour avancer
        self.down_frame_time = 0.06     # durée d'une frame (secondes)

        self._space_was_down = False
        self._combo_was_active = False

    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        down_now  = keys[pygame.K_DOWN]
        space_now = keys[pygame.K_SPACE]
        space_pressed = space_now and not self._space_was_down  # appui instantané
        combo_now = down_now and space_now and self.on_ground and len(self.down_frames) >= 4

        # Déplacements horizontaux
        dx = 0
        if keys[pygame.K_LEFT]:
            dx -= self.speed * dt
        if keys[pygame.K_RIGHT]:
            dx += self.speed * dt
        self.rect.x += int(dx)

        # --- Cas spécial ↓ + Espace : montrer sonic_3.png (sans saut, sans anim) ---
        if combo_now:
            self.image = self.down_frames[3]  # sonic_3.png
        else:
            # Saut : seulement à l'appui, et seulement si ↓ n'est pas tenue
            if space_pressed and self.on_ground and not down_now:
                self.vel_y = self.jump_velocity
                self.on_ground = False

            # Animation ↓ normale : 0 -> 2, puis fige
            if down_now and self.on_ground and self.down_frames:
                max_index = min(2, len(self.down_frames) - 1)

                if self.down_can_restart and not self.down_playing:
                    self.down_playing = True
                    self.down_can_restart = False
                    self.down_index = 0
                    self.down_timer = 0.0

                if self.down_playing:
                    self.down_timer += dt
                    while self.down_timer >= self.down_frame_time and self.down_index < max_index:
                        self.down_timer -= self.down_frame_time
                        self.down_index += 1

                    self.image = self.down_frames[self.down_index]
                    if self.down_index == max_index:
                        self.down_playing = False
                else:
                    self.image = self.down_frames[self.down_index]
            else:
                # reset + image par défaut
                self.down_playing = False
                self.down_can_restart = True
                self.down_index = 0
                self.down_timer = 0.0
                self.image = self.default_img

        # --- DÉCLENCHEMENT DU DASH À LA RELÂCHE DE LA COMBO ↓+Espace ---
        if self._combo_was_active and not combo_now:
            self.rect.x += 100  # avance de 50px vers la droite (ajuste si tu veux gauche/droite)

        # Mémos d'état (toujours à la fin)
        self._space_was_down = space_now
        self._down_was_down = down_now
        self._combo_was_active = combo_now



    def physics(self, dt, floor_y=700):
        # Gravité + collision sol
        self.vel_y += self.gravity * dt
        self.rect.y += int(self.vel_y * dt)

        if self.rect.bottom >= floor_y:
            self.rect.bottom = floor_y
            self.vel_y = 0
            self.on_ground = True

    def draw(self, window):
        if self.image:
            window.blit(self.image, self.rect)
        else:
            pygame.draw.rect(window, (0, 120, 255), self.rect, border_radius=6)
