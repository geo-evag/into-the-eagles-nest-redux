# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 19:26:03 2020

@author: Replay
"""

import pygame
from const import *

BULLET_SPD = 80

class Bullet(pygame.sprite.Sprite):
        
    def __init__(self,x,y,direction):
        super().__init__()
        blt = pygame.Surface((20,20))
        self.image = blt
        self.image.set_colorkey(BLACK)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.direction = direction
        self.speed_x = 0
        self.speed_y = 0
        
        
        if self.direction == "UP":
            self.speed_x = 0
            self.speed_y = -BULLET_SPD
        elif self.direction == "DOWN":
            self.speed_x = 0
            self.speed_y = BULLET_SPD
        elif self.direction == "LEFT":
            self.speed_x = -BULLET_SPD
            self.speed_y = 0
        else:
            self.speed_x = BULLET_SPD
            self.speed_y = 0
    
    def update(self,flagX,flagY):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y