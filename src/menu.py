import pygame
from main import Jeu

class menu:
    def __init__(self):
        pygame.init()

        self.menu = pygame.display.set_mode((800, 800))
        pygame.display.set_caption('menu')
        self.bouton = pygame.Rect(200, 400, 400, 300)
        self.image_commencer = pygame.image.load('bouton_commencer.png')

    def commencement(self):

        if event.type == get_pressed:

            if self.bouton.collidepoint(event.pos):
                print('ok')
        

    # ✅ Corrigé — intègre ça dans lancement_menu()
    def lancement_menu(self):
        self.run = True
        while self.run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.bouton.collidepoint(event.pos):
                        Jeu().running()  # lance le jeu !

            
if __name__ == '__main__':
    pygame.init()
    menu().lancement_menu()
    
