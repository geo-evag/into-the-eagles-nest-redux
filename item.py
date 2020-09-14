import pygame
from const import *

class Item(pygame.sprite.Sprite):
    
    def __init__(self,name,x,y):
        
        super().__init__()
        
        
        self.image = pygame.image.load(name+".png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name
        
    def update(self,flagX,flagY):
        # Move sprites to simulate camera scrolling
        if flagX == 1:          # if player sprite goes to right side of screen   
            self.rect.x -= 350
        elif flagX == -1:       # same for left side
            self.rect.x += 350
        
        if flagY == 1:          # if player sprite goes to botton side of screen   
            self.rect.y -= 350
        elif flagY == -1:       # same for top side
            self.rect.y += 350