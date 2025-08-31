import pygame
import pytmx
import pyscroll

class Jeu:
    def __init__(self):

        ############################################

        self.window_x = 800
        self.window_y = 800

        self.window = pygame.display.set_mode((self.window_x, self.window_y)) 
        
        pygame.display.set_caption("jeu sonic") 
        pygame_icon = pygame.image.load('icone_sonic.png') 
        pygame.display.set_icon(pygame_icon) 

        ####################################

        self.sprites_sonic = []

        self.sprites_sonic.append(pygame.image.load('./sprites/sonic_direction_haut.png'))

        #########################################
        self.liste_des_map = []

        self.liste_des_map.append(pytmx.load_pygame('map_1.tmx'))
        self.liste_des_map.append(pytmx.load_pygame('map_2.tmx'))
        self.liste_des_map.append(pytmx.load_pygame('map_3.tmx'))
        self.liste_des_map.append(pytmx.load_pygame('map_4.tmx'))
        self.liste_des_map.append(pytmx.load_pygame('map_5.tmx'))

        

        self.map_actuel = 0

        self.tmx_data = self.liste_des_map[self.map_actuel]
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.window.get_size())

        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer = 1)

        #####################################################
        

        self.sonic_position_x = 260 
        self.sonic_position_y = 100 
        self.rect_sonic = pygame.Rect(self.sonic_position_x, self.sonic_position_y, 45, 50) 

        self.vitesse_deplacement = 6

        self.points_joueur = 0

        ############################

        self.font = pygame.font.Font(None, 26)
        self.text = self.font.render('points récolté : ' + str(self.points_joueur), True,  (255, 255, 255), (0, 0, 0))

        ####################################
        
        self.anneau = pygame.image.load('anneau.png')
        self.liste_rect_anneau_1 = [pygame.Rect(150, 440, 25, 25), pygame.Rect(600, 440, 25, 25), pygame.Rect(700, 440, 25, 25)]
        self.liste_rect_anneau_2 = [pygame.Rect(150, 440, 25, 25), pygame.Rect(600, 440, 25, 25), pygame.Rect(700, 440, 25, 25)]
        self.liste_rect_anneau_3 = [pygame.Rect(150, 440, 25, 25), pygame.Rect(600, 440, 25, 25), pygame.Rect(700, 440, 25, 25)]
        self.liste_rect_anneau_4 = [pygame.Rect(150, 440, 25, 25), pygame.Rect(600, 440, 25, 25), pygame.Rect(700, 440, 25, 25)]
        self.liste_rect_anneau_5 = [pygame.Rect(150, 440, 25, 25), pygame.Rect(600, 440, 25, 25), pygame.Rect(700, 440, 25, 25)]
        
        #############################################

        self.gravite = (0, 6)
        self.resistance = (0,0)

        ############################################

        self.saut = 0 
        self.monter = 0
        self.descente = 0 
        self.nombre_saut = 0 
        self.sonic_saut = False 
        self.collision_sol = False

        ###################################### je charge les image de mon sprite qu'on va ensuite mettre dans une liste ##############################


        self.sonic_animation_bas = []
        self.sonic_animation_bas.append(pygame.image.load('./sprites/deplacement_en_bas/sonic_direction_bas.png'))
        self.sonic_animation_bas.append(pygame.image.load('./sprites/deplacement_en_bas/sonic_direction_bas_1.png')),
        self.sonic_animation_bas.append(pygame.image.load('./sprites/deplacement_en_bas/sonic_direction_bas_2.png')),
        self.sonic_animation_bas.append(pygame.image.load('./sprites/deplacement_en_bas/sonic_direction_bas_3.png')),
        self.sonic_animation_bas.append(pygame.image.load('./sprites/deplacement_en_bas/sonic_direction_bas_4.png')),

        self.sonic_animation_droite = []
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_1.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_2.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_3.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_4.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_5.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_6.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_7.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_8.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_9.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_10.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_11.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_12.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_13.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_14.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_15.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_16.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_17.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_18.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_19.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_20.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_21.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_22.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_23.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_24.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_25.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_26.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_27.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_28.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_29.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_30.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_31.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_32.png'))
        self.sonic_animation_droite.append(pygame.image.load('./sprites/deplacement_a_droite/sonic_direction_droite_33.png'))
        
        self.sonic_animation_gauche = []
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche.png'))
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_1.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_2.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_3.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_4.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_5.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_6.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_7.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_8.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_9.png'))
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_10.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_11.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_12.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_13.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_14.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_15.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_16.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_17.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_18.png'))
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_19.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_20.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_21.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_22.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_23.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_24.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_25.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_26.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_27.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_28.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_29.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_30.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_31.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_32.png')),
        self.sonic_animation_gauche.append(pygame.image.load('./sprites/deplacement_a_gauche/sonic_direction_gauche_33.png')),

        self.sprite_actuel = 0
        self.sonic = self.sonic_animation_droite[self.sprite_actuel] 
       
        self.sonic = self.sonic_animation_gauche[self.sprite_actuel] 

        self.sonic = self.sonic_animation_bas[self.sprite_actuel]
        self.sonic.set_colorkey([0, 0, 0])

        ########################################################

        self.son_anneau = pygame.mixer.Sound('./mp3/ring_sound_effect.wav')
        self.son_course = pygame.mixer.Sound('./mp3/course.wav')


        #########################################################
        self.clock = pygame.time.Clock()

    def points(self):

        if self.map_actuel == 0:
            self.points_map_1()

        elif self.map_actuel == 1:
            self.points_map_2()

        elif self.map_actuel == 2:
            self.points_map_3()

        elif self.map_actuel == 3:
            self.points_map_4()

        elif self.map_actuel == 4:
            self.points_map_5()

    #####################################################################################################################################################################################


    def points_map_1(self):
        
        for c in self.liste_rect_anneau_1:
                if self.rect_sonic.colliderect(c):
                    self.points_joueur += 1
                    self.text = self.font.render('points récolté : ' + str(self.points_joueur), True,  (255, 255, 255), (0, 0, 0))
                    self.liste_rect_anneau_1.remove(c)
                    self.son_anneau.play()
                    
        if len(self.liste_rect_anneau_1) == 0:
            self.group.draw(self.window)
            self.window.blit(self.text, (0, 0))
            self.window.blit(self.sonic, (self.sonic_position_x, self.sonic_position_y))
            pygame.display.flip()

        else:
            self.group.draw(self.window)
            self.window.blit(self.text, (0, 0))
            self.window.blit(self.sonic, (self.sonic_position_x, self.sonic_position_y))

            for an in self.liste_rect_anneau_1:
                self.window.blit(self.anneau, (an[0], an[1]))
                
            pygame.display.flip()

    def points_map_2(self):
        
        for c in self.liste_rect_anneau_2:
                if self.rect_sonic.colliderect(c):
                    self.points_joueur += 1
                    self.text = self.font.render('points récolté : ' + str(self.points_joueur), True,  (255, 255, 255), (0, 0, 0))
                    self.liste_rect_anneau_2.remove(c)
                    self.son_anneau.play()
                    
        if len(self.liste_rect_anneau_2) == 0:
            self.group.draw(self.window)
            self.window.blit(self.text, (0, 0))
            self.window.blit(self.sonic, (self.sonic_position_x, self.sonic_position_y))
            pygame.display.flip()

        else:
            self.group.draw(self.window)
            self.window.blit(self.text, (0, 0))
            self.window.blit(self.sonic, (self.sonic_position_x, self.sonic_position_y))

            for an in self.liste_rect_anneau_2:
                self.window.blit(self.anneau, (an[0], an[1]))
                
            pygame.display.flip()

    def points_map_3(self):
        
        
        for c in self.liste_rect_anneau_3:
                if self.rect_sonic.colliderect(c):
                    self.points_joueur += 1
                    self.text = self.font.render('points récolté : ' + str(self.points_joueur), True,  (255, 255, 255), (0, 0, 0))
                    self.liste_rect_anneau_3.remove(c)
                    self.son_anneau.play()
                        
        if len(self.liste_rect_anneau_3) == 0:
            self.group.draw(self.window)
            self.window.blit(self.text, (0, 0))
            self.window.blit(self.sonic, (self.sonic_position_x, self.sonic_position_y))
            pygame.display.flip()

        else:
            self.group.draw(self.window)
            self.window.blit(self.text, (0, 0))
            self.window.blit(self.sonic, (self.sonic_position_x, self.sonic_position_y))
            
            for an in self.liste_rect_anneau_3:
                self.window.blit(self.anneau, (an[0], an[1]))    
                pygame.display.flip()
                

    def points_map_4(self):
        
        for c in self.liste_rect_anneau_4:
                if self.rect_sonic.colliderect(c):
                    self.points_joueur += 1
                    self.text = self.font.render('points récolté : ' + str(self.points_joueur), True,  (255, 255, 255), (0, 0, 0))
                    self.liste_rect_anneau_4.remove(c)
                    self.son_anneau.play()
                        
        if len(self.liste_rect_anneau_4) == 0:
            self.group.draw(self.window)
            self.window.blit(self.text, (0, 0))
            self.window.blit(self.sonic, (self.sonic_position_x, self.sonic_position_y))
            pygame.display.flip()

        else:
            self.group.draw(self.window)
            self.window.blit(self.text, (0, 0))
            self.window.blit(self.sonic, (self.sonic_position_x, self.sonic_position_y))
            
            for an in self.liste_rect_anneau_4:
                self.window.blit(self.anneau, (an[0], an[1]))    
                pygame.display.flip()

    def points_map_5(self):
        
        for c in self.liste_rect_anneau_5:
                if self.rect_sonic.colliderect(c):
                    self.points_joueur += 1
                    self.text = self.font.render('points récolté : ' + str(self.points_joueur), True,  (255, 255, 255), (0, 0, 0))
                    self.liste_rect_anneau_5.remove(c)
                    self.son_anneau.play()
                        
        if len(self.liste_rect_anneau_5) == 0:
            self.group.draw(self.window)
            self.window.blit(self.text, (0, 0))
            self.window.blit(self.sonic, (self.sonic_position_x, self.sonic_position_y))
            pygame.display.flip()

        else:
            self.group.draw(self.window)
            self.window.blit(self.text, (0, 0))
            self.window.blit(self.sonic, (self.sonic_position_x, self.sonic_position_y))
            
            for an in self.liste_rect_anneau_5:
                self.window.blit(self.anneau, (an[0], an[1]))    
                pygame.display.flip()

    ##################################################################################################################################################################################

    def deplacement(self):
        self.bouton_presser = pygame.key.get_pressed()
        dx,dy=0,0

        if self.bouton_presser[pygame.K_SPACE]:
            self.sonic_saut = True
            
            self.nombre_saut += 1 
            self.sonic = self.sprites_sonic[0]  

        elif self.bouton_presser[pygame.K_RIGHT]:
            dx = self.vitesse_deplacement
        
            self.sprite_actuel += 1 

            if self.sprite_actuel >= len(self.sonic_animation_droite): 
                self.sprite_actuel = 28

            self.sonic = self.sonic_animation_droite[self.sprite_actuel]

        elif self.bouton_presser[pygame.K_LEFT]:
            dx = -self.vitesse_deplacement
            
            self.sprite_actuel += 1 
            if self.sprite_actuel >= len(self.sonic_animation_gauche): 
                self.sprite_actuel = 28

            self.sonic = self.sonic_animation_gauche[self.sprite_actuel]

            
        self.sonic_position_x += dx 
        self.sonic_position_y += dy 
        self.rect_sonic = pygame.Rect(self.sonic_position_x,self.sonic_position_y,29,39)

        self.liste_obstacle= []   

        for obj in self.tmx_data.objects: 
            if obj.type == 'collision': 
                self.liste_obstacle.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height)) 

        for obj in self.liste_obstacle: 
            if self.rect_sonic.colliderect(obj): 
                self.resistance = (0, -6) 
                self.collision_sol = True
                self.nombre_saut = 0

            else: 
                self.resistance = (0,0) 

            if self.sonic_saut and self.collision_sol: 
                if self.nombre_saut < 2: 
                    self.sauter() 

    def sauter(self):

        if self.sonic_saut == True: 

            if self.monter >= 10: 
                self.descente -= 1 
                self.saut = self.descente

            elif self.monter <10: 
                self.monter += 1  
                self.saut = self.monter

            if self.descente <0:
                self.monter = 0
                self.descente = 0
                self.sonic_saut = False 

        self.sonic_position_y -= self.saut * 4 

    def carte(self):

        if self.sonic_position_x >= 800:
            self.sonic_position_x = 0
            self.sonic_position_y = 440

            if self.map_actuel == 4:
                self.tmx_data = self.liste_des_map[self.map_actuel]
                self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
                self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.window.get_size())
                self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer = 1)

            else:
                self.map_actuel += 1
                self.tmx_data = self.liste_des_map[self.map_actuel]
                self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
                self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.window.get_size())
                self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer = 1)

        if self.sonic_position_x < 0:
            self.sonic_position_x = 800
            self.sonic_position_y = 440
            
            if self.map_actuel == 0:
                self.tmx_data = self.liste_des_map[self.map_actuel]
                self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
                self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.window.get_size())
                self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer = 1)

            else:
                self.map_actuel -= 1
                self.tmx_data = self.liste_des_map[self.map_actuel]
                self.map_data = pyscroll.data.TiledMapData(self.tmx_data)
                self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.window.get_size())
                self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer = 1)

    def gravite_jeu(self):

        self.sonic_position_y += self.gravite[1] + self.resistance[1]

    def running(self):

        self.run = True

        while self.run:
            
            self.gravite_jeu()
            self.carte()
            self.deplacement()
            self.points()

            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False


            self.clock.tick(60) # corresspond au nombre de frame par seconde 

if __name__ == '__main__':
    pygame.init()
    Jeu().running()
