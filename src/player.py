# src/player.py
import pygame
from pathlib import Path

# Chemins d'assets : main.py est dans src/, on remonte d'un cran vers la racine du projet
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
        # sprite par défaut (repos)
        if img:
            img = pygame.transform.scale(img, (w, h))
        self.default_img = img
        self.image = img

        # boite du joueur
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
        for i in range(6):
            frame = load_image("sprites", "deplacement_en_bas", f"sonic_{i}.png")
            if frame:
                self.down_frames.append(pygame.transform.scale(frame, (w, h)))

        # État de l’anim
        self.down_playing = False       # en lecture ?
        self.down_can_restart = True    # autorisé à redémarrer sur prochain appui ?
        self.down_index = 0             # frame courante
        self.down_timer = 0.0           # chrono pour avancer
        self.down_frame_time = 0.06     # durée d'une frame (secondes)

    def handle_input(self, dt):
        keys = pygame.key.get_pressed()

        # Déplacements horizontaux
        dx = 0
        if keys[pygame.K_LEFT]:
            dx -= self.speed * dt
        if keys[pygame.K_RIGHT]:
            dx += self.speed * dt
        self.rect.x += int(dx)

        # Saut
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_velocity
            self.on_ground = False

        # Gestion animation flèche bas (one-shot, seulement au sol)
        if keys[pygame.K_DOWN] and self.on_ground and self.down_frames:
            # Démarrage si autorisé et pas déjà en cours
            if self.down_can_restart and not self.down_playing:
                self.down_playing = True
                self.down_can_restart = False
                self.down_index = 0
                self.down_timer = 0.0

            # Avancer l'anim sans boucler
            if self.down_playing:
                self.down_timer += dt
                while self.down_timer >= self.down_frame_time and self.down_index < len(self.down_frames) - 1:
                    self.down_timer -= self.down_frame_time
                    self.down_index += 1

                # Afficher la frame courante
                self.image = self.down_frames[self.down_index]

                # Arrivé à la dernière -> figer (stopper playing, pas de loop)
                if self.down_index == len(self.down_frames) - 1:
                    self.down_playing = False
            else:
                # déjà figé sur la dernière frame ou pas de progression
                self.image = self.down_frames[self.down_index]
        else:
            self.down_playing = False
            self.down_can_restart = True
            self.down_index = 0
            self.down_timer = 0.0
            self.image = self.default_img

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
