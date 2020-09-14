import pygame
from const import *

SPD = 20

class Hostage(pygame.sprite.Sprite):
    
    def __init__(self,x,y):
        super().__init__()
        
        self.img = pygame.image.load("hostage.png").convert()
        self.img2 = pygame.transform.rotate(self.img,90)
        
        self.image = self.img
        self.image.set_colorkey(BLACK)
        
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y
        
        self.x_speed = 0
        self.y_speed = 0
        
        self.prevx = x
        self.prevy = y
    
    def left(self):
        self.x_speed = -SPD
        self.image = self.img2
        self.image.set_colorkey(BLACK)
        
    def right(self):
        self.x_speed = SPD
        self.image = pygame.transform.rotate(self.img2,180)
        self.image.set_colorkey(BLACK)

    def up(self):
        self.y_speed = -SPD
        self.image = self.img
        self.image.set_colorkey(BLACK)

    def down(self):
        self.y_speed = SPD
        self.image = pygame.transform.rotate(self.img,180)
        self.image.set_colorkey(BLACK)

    def stopX(self):
        self.x_speed = 0
    
    def stopY(self):
        self.y_speed = 0
    
    def locate(self,player):
        
        loc_x = self.rect.centerx - player.rect.centerx
        loc_y = self.rect.centery - player.rect.centery
        
        if loc_x < 12 and loc_x > -12:
            
            
            if loc_y > 12:
                self.stopX()
                self.up()
            elif loc_y < -12:
                self.stopX()
                self.down()
                
        elif loc_x > 12:
            self.stopY()
            self.left()
            
        elif loc_x < -12:
            self.stopY()
            self.right()
            
    def update_hostage(self,wall_list,player,player_list,enemy_list):
        
        self.locate(player)
        
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed
        
        
        # Wall collision logic for enemy
        collide = pygame.sprite.spritecollideany(self,wall_list)
        
        if collide != None:
            if self.rect.x - self.prevx > 0 or self.rect.x - self.prevx < 0 :
                self.rect.x = self.prevx
                
            if self.rect.y - self.prevy > 0 or self.rect.y - self.prevy < 0:
                self.rect.y = self.prevy
                
                
        # Player collision detection
        player_collide = pygame.sprite.spritecollide(self,player_list,False)
        
        for player in player_collide:
            if self.rect.x - self.prevx > 0 or self.rect.x - self.prevx < 0 :
                self.rect.x = self.prevx
                
            if self.rect.y - self.prevy > 0 or self.rect.y - self.prevy < 0:
                self.rect.y = self.prevy
                
        
        enemy_collide = pygame.sprite.spritecollide(self,enemy_list,False)
        
        for enemy in enemy_collide:
                
            if self.rect.x - self.prevx > 0 or self.rect.x - self.prevx < 0 :
                self.rect.x = self.prevx
            
            if self.rect.y - self.prevy > 0 or self.rect.y - self.prevy < 0:
                self.rect.y = self.prevy
            
        
        self.prevx = self.rect.x
        self.prevy = self.rect.y
        
    def update(self,flagX,flagY):
        # Move sprites to simulate camera scrolling
        if flagX == 1:          # if player sprite goes to right side of screen   
            self.rect.x -= 350
            self.prevx -= 350
        elif flagX == -1:       # same for left side
            self.rect.x += 350
            self.prevx += 350
        
        if flagY == 1:          # if player sprite goes to botton side of screen   
            self.rect.y -= 350
            self.prevy -= 350
        elif flagY == -1:       # same for top side
            self.rect.y += 350
            self.prevy += 350