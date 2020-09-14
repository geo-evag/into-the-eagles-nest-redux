import pygame, bullet
from const import *


SPD = 20        #player speed

class Player(pygame.sprite.Sprite):
    
    
    
    def __init__(self,name,x,y):
        super().__init__()
        
        self.img = pygame.image.load(name).convert()
        self.img.set_colorkey(BLACK)
        self.img2 = pygame.transform.rotate(self.img,90)
        self.img2.set_colorkey(BLACK)
        
        self.img_fire = pygame.image.load("soldier_fire.png").convert()
        self.img_fire.set_colorkey(BLACK)
        
        self.image = self.img
        self.image.set_colorkey(BLACK)
        
        self.dir = "UP"

        self.rect = self.image.get_rect() 
        self.rect.x = x
        self.rect.y = y
        
        self.help_x = 0
        self.help_y = 0
        
        self.x_speed = 0
        self.y_speed = 0
        
        self.prevx = 0
        self.prevy = 0
        
        self.hits = 99
        self.ammo = 10
        self.keys = 00
    
    def update_pl(self,wall_list,enemy_list,item_list,door_list):  
        self.rect.x += self.x_speed   
        self.rect.y += self.y_speed   
        
        
        # Wall collision logic for player
        collide = pygame.sprite.spritecollideany(self,wall_list)
    
        if collide != None:
            if self.rect.x - self.prevx > 0 or self.rect.x - self.prevx < 0:
                self.rect.x = self.prevx
                
            if self.rect.y - self.prevy > 0 or self.rect.y - self.prevy < 0:
                self.rect.y = self.prevy
                
        door_collide = pygame.sprite.spritecollide(self,door_list,False)
        
        for door in door_collide:
            if self.keys > 0:
                door.kill()
                door_list.remove(door)
                self.keys -= 1
                
            if self.rect.x - self.prevx > 0 or self.rect.x - self.prevx < 0:
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
            
            
    def left(self):
        self.x_speed = -SPD
        self.dir = "LEFT"
        self.set_image()
        
        
    def right(self):
        self.x_speed = SPD
        self.dir = "RIGHT"
        self.set_image()
        

    def up(self):
        self.y_speed = -SPD
        self.dir = "UP"
        self.set_image()
        

    def down(self):
        self.y_speed = SPD
        self.dir = "DOWN"
        self.set_image()
        

    def stopX(self):
        self.x_speed = 0
    
    def stopY(self):
        self.y_speed = 0
        
    def shoot(self):
        self.ammo -= 1
        prev_img = self.image
        if self.dir == "UP":
            self.image = self.img_fire
            
        elif self.dir == "DOWN":
            i = pygame.transform.rotate(self.img_fire,180)
            self.image = i
            
        elif self.dir == "LEFT":
            i = pygame.transform.rotate(self.img_fire,90)
            self.image = i
            
        elif self.dir == "RIGHT":
            i = pygame.transform.rotate(self.img_fire,270)
            self.image = i
        return bullet.Bullet(self.rect.centerx-10,self.rect.centery-10,self.dir)

    def set_image(self):
        if self.dir == "UP":        
            self.image = self.img
        elif self.dir == "DOWN":
            self.image = pygame.transform.rotate(self.img,180)
        elif self.dir == "RIGHT":
            self.image = pygame.transform.rotate(self.img2,180)
        elif self.dir == "LEFT":
            self.image = self.img2
            
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