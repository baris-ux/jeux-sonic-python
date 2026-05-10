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

pygame.mixer.pre_init(44100, -16, 2, 256)
pygame.init()
pygame.mixer.init()

class Player:
    def __init__(self, img, start_pos, w=96, h=96):
        if img:
            img = pygame.transform.scale(img, (w, h))
        self.default_img = img
        self.image = img

        self.rect = pygame.Rect(start_pos[0], start_pos[1], w, h)

        self.vel_y = 0
        self.on_ground = False
        self.speed = 220
        self.jump_velocity = -550
        self.gravity = 1200

        self._is_running_sound = False

        try:
            self.jump_sound = pygame.mixer.Sound(asset("sounds", "jump.wav"))
            self.jump_sound.set_volume(0.8)
        except Exception as e:
            self.jump_sound = None
            print("Impossible de charger le son de saut:", e)

        try:
            self.run_sound = pygame.mixer.Sound(asset("sounds", "run.wav"))
            self.run_sound.set_volume(0.8)
        except Exception as e:
            self.run_sound = None
            print("Impossible de charger le son de course:", e)

        self.down_frames = []
        for i in range(4):
            frame = load_image("sprites", "deplacement_en_bas", f"sonic_{i}.png")
            if frame:
                self.down_frames.append(pygame.transform.scale(frame, (w, h)))

        self.right_frames = []
        for i in range(13):
            frame = load_image("sprites", "deplacement_a_droite", f'sonic_{i}.png')
            if frame:
                self.right_frames.append(pygame.transform.scale(frame, (w, h)))

        self.left_frames = []
        for i in range(13):
            frame = load_image("sprites", "deplacement_a_gauche", f'sonic_{i}.png')
            if frame:
                self.left_frames.append(pygame.transform.scale(frame, (w, h)))

        self.down_playing = False
        self.down_can_restart = True
        self.down_index = 0
        self.down_timer = 0.0
        self.down_frame_time = 0.06

        self.right_index = 0
        self.right_timer = 0.0
        self.right_frame_time = 0.08

        self.left_index = 0
        self.left_timer = 0.0
        self.left_frame_time = 0.08

        self._space_was_down = False
        self._combo_was_active = False
        self.facing_right = True

        # Dash
        self.dashing = False
        self.dash_timer = 0.0
        self.dash_duration = 0.3
        self.dash_speed = 500

    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        down_now  = keys[pygame.K_DOWN]
        right_now = keys[pygame.K_RIGHT]
        left_now  = keys[pygame.K_LEFT]
        space_now = keys[pygame.K_SPACE]
        space_pressed = space_now and not self._space_was_down
        combo_now = down_now and space_now and self.on_ground and len(self.down_frames) >= 4

        # Dash en cours → ignore les autres inputs
        if self.dashing:
            self.dash_timer -= dt
            dash_dx = self.dash_speed * dt if self.facing_right else -self.dash_speed * dt
            self.rect.x += int(dash_dx)
            self.image = self.down_frames[3]  # ← garde la frame du dash
            if self.dash_timer <= 0:
                self.dashing = False
            self._space_was_down = space_now
            self._combo_was_active = combo_now
            return

        # Déplacements horizontaux
        dx = 0
        if left_now:
            dx -= self.speed * dt
        if right_now:
            dx += self.speed * dt
        self.rect.x += int(dx)

        if dx > 0:
            self.facing_right = True
        elif dx < 0:
            self.facing_right = False

        if combo_now:
            self.image = self.down_frames[3]
        else:
            if space_pressed and self.on_ground and not down_now:
                self.vel_y = self.jump_velocity
                self.on_ground = False
                if self.jump_sound:
                    self.jump_sound.play()

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
                self.down_playing = False
                self.down_can_restart = True
                self.down_index = 0
                self.down_timer = 0.0
                self.image = self.default_img

                if self.on_ground and self.right_frames and dx > 0:
                    self.right_timer += dt
                    while self.right_timer >= self.right_frame_time:
                        self.right_timer -= self.right_frame_time
                        self.right_index += 1
                        if self.right_index >= len(self.right_frames):
                            self.right_index = 8
                    self.image = self.right_frames[self.right_index]

                elif self.on_ground and self.left_frames and dx < 0:
                    self.left_timer += dt
                    while self.left_timer >= self.left_frame_time:
                        self.left_timer -= self.left_frame_time
                        self.left_index += 1
                        if self.left_index >= len(self.left_frames):
                            self.left_index = 8
                    self.image = self.left_frames[self.left_index]

                else:
                    self.right_index = 0
                    self.left_index = 0
                    self.right_timer = 0.0
                    self.left_timer = 0.0
                    if self.facing_right:
                        self.image = self.default_img
                    else:
                        self.image = pygame.transform.flip(self.default_img, True, False)

                is_running_now = (self.on_ground and abs(dx) > 0 and not down_now and not combo_now)

                if self.run_sound:
                    if is_running_now:
                        if not self._is_running_sound:
                            self.run_sound.play(-1)
                            self._is_running_sound = True
                    else:
                        if self._is_running_sound:
                            self.run_sound.stop()
                            self._is_running_sound = False

        # Déclenchement du dash à la relâche de la combo ↓+Espace
        if self._combo_was_active and not combo_now:
            self.dashing = True
            self.dash_timer = self.dash_duration

        self._space_was_down = space_now
        self._down_was_down = down_now
        self._combo_was_active = combo_now

    def physics(self, dt, floor_y=700, collision_rects=None):
        self.vel_y += self.gravity * dt
        self.rect.y += int(self.vel_y * dt)

        self.on_ground = False

        if self.rect.bottom >= floor_y:
            self.rect.bottom = floor_y
            self.vel_y = 0
            self.on_ground = True

        if collision_rects:
            for rect in collision_rects:
                if self.rect.colliderect(rect):
                    if self.vel_y > 0 and self.rect.bottom - int(self.vel_y * dt) <= rect.top + 10:
                        self.rect.bottom = rect.top
                        self.vel_y = 0
                        self.on_ground = True
                    elif self.vel_y < 0:
                        self.rect.top = rect.bottom
                        self.vel_y = 0

    def draw(self, window, cam_x=0, cam_y=0):
        draw_rect = self.rect.move(-cam_x, -cam_y)
        if self.image:
            window.blit(self.image, draw_rect)
        else:
            pygame.draw.rect(window, (0, 120, 255), draw_rect, border_radius=6)