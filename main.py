import pygame
import player, enemy, hostage, item, door
from const import *

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 850

SPD = 20        #player speed

class Wall(pygame.sprite.Sprite):
    
    
    
    def __init__(self,name,x,y):
        super().__init__()
        
        self.img = pygame.image.load(name).convert()
        self.img2 = pygame.transform.rotate(self.img,90)
        
        self.image = self.img
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect() 
        self.rect.x = x
        self.rect.y = y
        
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
   

pygame.init()

font = pygame.font.SysFont('Unispace', 72, True, False)
pygame.mixer.music.load("theme.ogg")
shot = pygame.mixer.Sound("shot.ogg")
enemy_down = pygame.mixer.Sound("enemy_down.ogg")
ammo_pickup = pygame.mixer.Sound("ammo.ogg")
key_pickup = pygame.mixer.Sound("key.ogg")
health_pickup = pygame.mixer.Sound("health.ogg")
ammo_pickup.set_volume(0.5)
health_pickup.set_volume(0.2)


walk_sound = [0,1]

walk_sound = pygame.mixer.Sound("walk.ogg")

lvl_loaded = False
lvl_gen = False

def load_level(level_name):
    level = open(level_name+".txt","r")
    st = []
    lvl = []
    for row in level:
        for i in row:
            if i != "\n":
                st.append(i)
        lvl.append(st)
        st = []
    return lvl

#print(lvl,'\n\ninfo:\n\trows:',len(lvl),'\ncols:',len(lvl[0]))


# Set the width and height of the screen [width, height]
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Into the Eagle's Nest")

splash = pygame.image.load("splash1.jpg").convert()
    
panel = pygame.image.load("side_panel.jpg").convert()

game_win = pygame.image.load("game_win.png").convert()
lose_splash = pygame.image.load("failed.png").convert()
# Loop until the user clicks the close button.
tilesize = 86
start = False
done = False
lost = False
score = 0
level = 1
win = False

flagX = 0 # Camera scroll for X axis, if 1, scroll to right, if -1 scroll to left
flagY = 0 # Camera scroll for Y axis, if 1, scroll upwards, if -1 scroll downwards


floor_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()
item_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
door_list = pygame.sprite.Group()
bullet_list = pygame.sprite.Group()
exit_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()



def generate_level(lvl):
    enemy_id = 0
    global init_x,init_y
    print("\n\n\t\t----- Info -----\n\nlevel:",level)
    for i in range(len(lvl[0])):
        for j in range(len(lvl)):
    
            if lvl[j][i] == "X":
                wall = Wall('wall3.jpg',i*tilesize,j*tilesize)
                wall_list.add(wall)
                all_sprites_list.add(wall)
                
            elif lvl[j][i] == "T":
                floor = Wall('floor2.jpg',i*tilesize,j*tilesize)
                floor_list.add(floor)
                all_sprites_list.add(floor)
                
            elif lvl[j][i] == "D":
                floor = Wall('floor2.jpg',i*tilesize,j*tilesize)
                floor_list.add(floor)
                all_sprites_list.add(floor)
                door1 = door.Door(i*tilesize,j*tilesize+20)
                door_list.add(door1)
                all_sprites_list.add(door1)
                
                
            elif lvl[j][i] == "A":
                floor = Wall('floor2.jpg',i*tilesize,j*tilesize)
                floor_list.add(floor)
                all_sprites_list.add(floor)
                for x in range(2):
                    for y in range(2):
                        ammobox = item.Item("ammobox",i*tilesize+x*42,j*tilesize+y*42)
                        item_list.add(ammobox)
                        all_sprites_list.add(ammobox)
                        
            elif lvl[j][i] == "E":
                floor = Wall('floor2.jpg',i*tilesize,j*tilesize)
                floor_list.add(floor)
                all_sprites_list.add(floor)
                enemy1 = enemy.Enemy(i*tilesize+5,j*tilesize+5,enemy_id)
                enemy_list.add(enemy1)
                all_sprites_list.add(enemy1)
                enemy_id += 1
                
            elif lvl[j][i] == "k":
                floor = Wall('floor2.jpg',i*tilesize,j*tilesize)
                floor_list.add(floor)
                all_sprites_list.add(floor)
                key = item.Item("key",i*tilesize+10,j*tilesize+10)
                item_list.add(key)
                all_sprites_list.add(key)
                
            elif lvl[j][i] == "h":
                floor = Wall('floor2.jpg',i*tilesize,j*tilesize)
                floor_list.add(floor)
                all_sprites_list.add(floor)
                healthkit = item.Item("healthkit",i*tilesize+10,j*tilesize+10)
                item_list.add(healthkit)
                all_sprites_list.add(healthkit)
                
            elif lvl[j][i] == "i":
                floor = Wall('floor2.jpg',i*tilesize,j*tilesize)
                floor_list.add(floor)
                all_sprites_list.add(floor)
                item1 = item.Item("painting",i*tilesize+10,j*tilesize+10)
                item_list.add(item1)
                all_sprites_list.add(item1)
                
            elif lvl[j][i] == "f":
                floor = Wall('floor2.jpg',i*tilesize,j*tilesize)
                floor_list.add(floor)
                all_sprites_list.add(floor)
                food = item.Item("food",i*tilesize+10,j*tilesize+10)
                item_list.add(food)
                all_sprites_list.add(food)
                
            elif lvl[j][i] == "Q":
                floor = Wall('floor2.jpg',i*tilesize,j*tilesize)
                floor_list.add(floor)
                all_sprites_list.add(floor)
                game_exit = item.Item("exit",i*tilesize,j*tilesize)
                item_list.add(game_exit)
                all_sprites_list.add(game_exit)
                
def menu(screen):
    global lvl_loaded,lvl_gen
    text = font.render("Press any key to start game", True, WHITE)
    screen.blit(splash,[0,0])
    screen.blit(text,[115,700])
    
    if lvl_loaded == False:
        lvl = load_level("level1")
        level_loaded = True
    if lvl_gen == False:
        generate_level(lvl)
        lvl_gen = True


player = player.Player("soldier.png",150,150)
player_list = pygame.sprite.Group()
player_list.add(player)
all_sprites_list.add(player)

hostage = hostage.Hostage(200,800)
hostage_list = pygame.sprite.Group()
hostage_list.add(hostage)
all_sprites_list.add(hostage)



# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# camera scrolling
def scroll(flagX,flagY):
    if player.rect.x >= 620:
        flagX = 1
    elif player.rect.x <= 32:
        flagX = -1
    if player.rect.y >= 620:
        flagY = 1
    elif player.rect.y <= 32:
        flagY = -1
    all_sprites_list.update(flagX,flagY)

def pickup_text(item):
    text = font.render("Picked up"+str(item),True,WHITE)
    screen.blit(text,[250,850])

def main_draw(screen,lost,flagX,flagY,panel):
    global score,win
    if lost == False:
        
        player.update_pl(wall_list,enemy_list,item_list,door_list)
        hostage.update_hostage(wall_list,player,player_list,enemy_list)
        
        item_collide = pygame.sprite.spritecollide(player,item_list,True)
        for i in item_collide:  
            if i.name == "ammobox":
                player.ammo += 5
                ammo_pickup.play()
                pickup_text(i.name)

            if i.name == "key":
                player.keys += 1
                key_pickup.play()
                pickup_text(i.name)
                
            elif i.name == "healthkit":
                player.hits += 10
                health_pickup.play()
                pickup_text(i.name)
                
            elif i.name == "food":
                player.hits += 5
                pickup_text(i.name)
                
            elif i.name == "painting":
                score += 50
                pickup_text(i.name)
            elif i.name == "exit":
                win = True
                
            if player.hits > 99:
                    player.hits = 99
                    
        for enemy in enemy_list:
            enemy.update_enemy(wall_list,player,player_list,enemy_list,door_list)
            
        scroll(flagX,flagY)
        flagX = flagY = 0
        
        # --- Drawing code should go here
            
        all_sprites_list.draw(screen)
        enemy_list.draw(screen)
        player_list.draw(screen)
        hostage_list.draw(screen)
        
        for bullet in bullet_list:
            
            enemy_hit_list = pygame.sprite.spritecollide(bullet,enemy_list,True)
            for e in enemy_hit_list:
                enemy_down.play()
                e.kill()
                print("enemy",e,"killed")
                bullet_list.remove(bullet)
                bullet.kill()
                score += 100
            
            wall_hit = pygame.sprite.spritecollideany(bullet,wall_list)
            if wall_hit != None:
                bullet.kill()
                bullet_list.remove(bullet)
            

        screen.blit(panel,[700,0])
        pygame.draw.rect(screen,BLACK,[0,700,1000,150])
        txt_keys = font.render(str(player.keys), True, YELLOW)
        txt_ammo = font.render(str(player.ammo), True, YELLOW)
        txt_hits = font.render(str(player.hits), True, YELLOW)
        txt_score = font.render(str(score),True, YELLOW)
        screen.blit(txt_keys,[890,85])
        screen.blit(txt_ammo,[890,185])
        screen.blit(txt_hits,[890,285])
        screen.blit(txt_score,[750,395])
         



# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            
        # User pressed down on a key
        elif event.type == pygame.KEYDOWN:
            start = True
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.stopY()
                walk_sound.play(-1)
                player.left()
                
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.stopY()
                walk_sound.play(-1)
                player.right()
                
                
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                player.stopX()
                walk_sound.play(-1)
                player.up()
                
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.stopX()
                walk_sound.play(-1)
                player.down()
                
            elif event.key == pygame.K_SPACE:
               
                if player.ammo > 0:
                   shot.play()
                   x = player.shoot()
                   bullet_list.add(x)
                   all_sprites_list.add(x)
                else:
                    print("No ammo!")
               
            elif event.key == pygame.K_ESCAPE:
                pass
 
        # Reset speed when key goes up
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.stopX()
                walk_sound.stop()
                
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.stopX()
                walk_sound.stop()
                
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                player.stopY()
                walk_sound.stop()
                
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.stopY()
                walk_sound.stop()
                
            elif event.key == pygame.K_SPACE:
                player.set_image()
                

                
    # --- Game logic should go here
    
    
    # --- Screen-clearing code goes here

    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.

    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(BLACK)
    if start == False:
        menu(screen)
        
    elif start == True and player.hits > 0:
        main_draw(screen,lost,flagX,flagY,panel)
        
    elif player.hits <= 0:
        screen.fill(BLACK)
        screen.blit(lose_splash,[0,0])
        player.kill()
        player_list.empty()
        enemy_list.empty()
        all_sprites_list.empty()
        pygame.display.flip()
        #done = True
    
    if win == True:
        screen.fill(BLACK)
        screen.blit(game_win,[0,0])
        player.kill()
        player_list.empty()
        enemy_list.empty()
        all_sprites_list.empty()
        pygame.display.flip()
    
    # --- Go ahead and update the screen with what we've drawn.
    if player.hits > 0:
        pygame.display.flip()
    
    

    # --- Limit to 10 frames per second
    clock.tick(10)

# Close the window and quit.
pygame.quit()