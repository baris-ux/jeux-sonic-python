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
    def __init__(self, idle_right, idle_left, start_pos, w=96, h=96):
        self.idle_right = pygame.transform.scale(idle_right, (w, h)) if idle_right else None
        self.idle_left  = pygame.transform.scale(idle_left,  (w, h)) if idle_left  else None

        self.image = self.idle_right or self.idle_left

        self.rect = pygame.Rect(start_pos[0], start_pos[1], w, h)
        self.pos_y = float(self.rect.y)
        self.pos_x = float(self.rect.x)
        self.dx = 0.0

        self.vel_y = 0
        self.on_ground = False
        self.speed = 400
        self.jump_velocity = -850
        self.gravity = 2000

        self.invincible_timer = 0.0 #si le joueur est touché on le rend invincible le temps de quelques seconde mais initalement il n'est pas invinscible

        self.facing = 1 # si 1 alors le joueur regarde à droite si -1 joueur regarde à gauche

        self.dash_remaining = 0.0 # temps de dash restant

        #################################################################################################################""

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

        try:
            self.drop_rings_sound = pygame.mixer.Sound(asset("sounds","drop_rings.wav"))
            self.drop_rings_sound.set_volume(0.8)
        except Exception as e:
            self.drop_rings_sound = None
            print("Impossible de charger le son de drop rings:", e)

        try:
            self.gain_ring_sound = pygame.mixer.Sound(asset("sounds","gain_ring.wav"))
            self.gain_ring_sound.set_volume(0.8)
        except Exception as e:
            self.gain_ring_sound = None
            print("Impossible de charger le son de drop rings:", e)

        ################################################################################################################

        self.down_frames = []
        for i in range(4): # 0 à 2
            frame = load_image("sprites", "deplacement_en_bas", f"sonic_{i}.png")
            if frame:
                self.down_frames.append(pygame.transform.scale(frame, (w, h)))

        self.right_frames = []
        for i in range(13): # 0 à 12
            frame = load_image("sprites", "deplacement_a_droite", f'sonic_{i}.png')
            if frame:
                self.right_frames.append(pygame.transform.scale(frame, (w, h)))

        
        self.left_frames = []
        for i in range(13): # 0 à 12
            frame = load_image("sprites", "deplacement_a_gauche", f'sonic_{i}.png')
            if frame:
                self.left_frames.append(pygame.transform.scale(frame, (w, h)))


        self.jump_frames = []
        for i in range(13): # 0 à 10
            frame = load_image("sprites", "saut", f'sonic_{i}.png')
            if frame:
                self.jump_frames.append(pygame.transform.scale(frame, (w, h)))


        self.idle_right = load_image("sprites", "sonic_repos_droite", "sonic_0.png")
        if self.idle_right:
            self.idle_right = pygame.transform.scale(self.idle_right, (w, h))

        self.idle_left = load_image("sprites", "sonic_repos_gauche", "sonic_0.png")
        if self.idle_left:
            self.idle_left = pygame.transform.scale(self.idle_left, (w, h))

    ############################################################################################################################################

        # État de l’anim
        self.down_playing = False       # en lecture ?
        self.down_can_restart = True    # autorisé à redémarrer sur prochain appui ?
        self.down_index = 0             # frame courante
        self.down_timer = 0.0           # chrono pour avancer
        self.down_frame_time = 0.06     # durée d'une frame (secondes)

        self.right_index = 0
        self.right_timer = 0.0
        self.right_frame_time = 0.08

        self.left_index = 0
        self.left_timer = 0.0
        self.left_frame_time = 0.08

        self.jump_index = 0
        self.jump_timer = 0.0
        self.jump_frame_time = 0.06

        self._space_was_down = False
        self._combo_was_active = False

    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        down_now  = keys[pygame.K_DOWN]
        right_now = keys[pygame.K_RIGHT]
        left_now = keys[pygame.K_LEFT]
        space_now = keys[pygame.K_SPACE]
        space_pressed = space_now and not self._space_was_down  # appui instantané
        combo_now = down_now and space_now and self.on_ground and len(self.down_frames) >= 4

        # Déplacements horizontaux
        dx = 0
        if left_now: # si on va à gacuhe 
            dx -= self.speed * dt 
            self.facing = -1
        if right_now: # si on va à droite 
            dx += self.speed * dt 
            self.facing = 1

        if self.dash_remaining != 0.0:
            speed = 400.0  
            dir_ = 1 if self.dash_remaining > 0 else -1
            step = min(speed * dt, abs(self.dash_remaining))
            dx += dir_ * step
            self.dash_remaining -= dir_ * step
        
        self.dx = dx

        if self.dash_remaining != 0.0 and self.on_ground and self.down_frames:
            self.image = self.down_frames[3]
        else:
            # ------- si on appuie sur espace, qu'on n'est pas au sol et qu'on appuie pas sur la flèche du bas on peut sauter -----------
            if space_pressed and self.on_ground and not down_now:
                self.vel_y = self.jump_velocity
                self.on_ground = False
                self.jump_index = 0
                self.jump_timer = 0.0

                # --------- Sécurité: ne joue le son que si l’audio est chargé ------ #
                if self.jump_sound:
                    self.jump_sound.play()

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
                
                if self.on_ground:
                    if self.facing == 1 and self.idle_right:
                        self.image = self.idle_right
                    elif self.facing == -1 and self.idle_left:
                        self.image = self.idle_left
                    else:
                        idle = self.default_img
                        if self.facing == -1 and idle is not None:
                            idle = pygame.transform.flip(idle, True, False)
                        self.image = idle

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
                    # si on ne marche pas à droite → image par défaut
                    self.right_index = 0
                    self.left_index = 0
                    self.right_timer = 0.0
                    self.left_timer = 0.0

        # --- déclenchement du dash quand on relache flèche du bas + Espace ---
        if self._combo_was_active and not combo_now:
            self.dash_remaining += 1100 * self.facing

        if not self.on_ground and self.jump_frames:
            self.jump_timer += dt
            while self.jump_timer >= self.jump_frame_time and self.jump_index < len(self.jump_frames) - 1:
                self.jump_timer -= self.jump_frame_time
                self.jump_index += 1
            self.image = self.jump_frames[self.jump_index]
        else:
            self.jump_index = 0
            self.jump_timer = 0.0

        self._space_was_down = space_now
        self._down_was_down = down_now
        self._combo_was_active = combo_now



    def physics(self, dt, Colliders):
        dx = self.dx
        self.dx = 0.0
        self.pos_x += dx
        self.rect.x = int(self.pos_x)

        for r in Colliders:
            if self.rect.colliderect(r):
                if dx > 0:  
                    self.rect.right = r.left
                    self.facing = -1
                elif dx < 0: 
                    self.rect.left = r.right
                    self.facing = 1
                    
                    
                self.pos_x = float(self.rect.x)
                self.dash_remaining = 0.0

        # 1) Gravité + limite de vitesse de chute
        self.vel_y += self.gravity * dt
        MAX_FALL_SPEED = 1200.0
        if self.vel_y > MAX_FALL_SPEED:
            self.vel_y = MAX_FALL_SPEED

        # 2) Déplacement vertical découpé (anti-tunneling)
        dy = self.vel_y * dt
        STEP = 6.0  # taille d'un sous-pas (entre 4 et 8 px, c'est bien)
        steps = max(1, int(abs(dy) // STEP))
        step = dy / steps if steps > 0 else 0.0

        self.on_ground = False

        for _ in range(steps):
            prev_bottom = self.rect.bottom

            self.pos_y += step
            self.rect.y = int(self.pos_y)

            collided = False
            for r in Colliders:
                if self.rect.colliderect(r):
                    if self.vel_y > 0 and prev_bottom <= r.top:
                        # on tombait et on touche le dessus -> se poser
                        self.rect.bottom = r.top
                        self.pos_y = float(self.rect.y)
                        self.vel_y = 0.0
                        self.on_ground = True
                        collided = True
                        break
                    elif self.vel_y < 0:
                        # plafond
                        self.rect.top = r.bottom
                        self.pos_y = float(self.rect.y)
                        self.vel_y = 0.0
                        collided = True
                        break

            if collided and self.on_ground:
                # déjà posé, inutile de continuer les sous-pas
                break

        # 3) Capteur de pieds (sécurise l'état "au sol")
        feet = self.rect.copy()
        feet.height = 2
        feet.top = self.rect.bottom
        if any(feet.colliderect(r) for r in Colliders):
            self.on_ground = True



    def draw(self, window, camera=None):
        if self.image:
            self.image.set_alpha(120 if self.invincible_timer > 0 else 255)
            draw_rect = self.rect if camera is None else camera.apply(self.rect)
            window.blit(self.image, draw_rect)  # <-- utiliser draw_rect
        else:
            draw_rect = self.rect if camera is None else camera.apply(self.rect)
            pygame.draw.rect(window, (0, 120, 255), draw_rect, border_radius=6)
