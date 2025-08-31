import pygame
from sonic import Jeu

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
        

    def lancement_menu(self):
        
        self.run = True

        while self.run:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False

            self.menu.fill((76, 65, 75))
            self.menu.blit(self.image_commencer, (200, 400))
            pygame.display.flip()

        
if __name__ == '__main__':
    pygame.init()
    menu().lancement_menu()
    
