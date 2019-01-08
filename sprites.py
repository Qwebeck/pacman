import pygame as pg
import sys
import random
from os import path
from settings import *
from brs_agent import *
from ghost_behavior import *

vec = pg.math.Vector2
random.seed()



#TODO

#add graphic
#add bonuses 

#add dependenciec between ghost_speed , following update time , tilesize and player speed 


#self.game.ghost_speed




def collide_with_walls(sprite, dir, group):
    hits = pg.sprite.spritecollide(sprite, group, False)
    if dir == 'x':
        if hits:
            if sprite.vel.x > 0:
                sprite.pos.x = hits[0].rect.left - sprite.rect.width
            elif sprite.vel.x < 0:
                sprite.pos.x = hits[0].rect.right
            sprite.vel.x = 0
            sprite.rect.x = sprite.pos.x
            return True
    if dir == 'y':
        if hits:
            if sprite.vel.y > 0:
                sprite.pos.y = hits[0].rect.top - sprite.rect.height
            elif sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom
            sprite.vel.y = 0
            sprite.rect.y = sprite.pos.y
            return True

def dir_definer(vel):
    if vel > 0:
        return 1
    else:
        return -1

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites,game.player_group
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.scale(self.game.player_img, (self.game.tilesize, self.game.tilesize))
        self.rect = self.image.get_rect()
        self.keys = -1
        self.previous_key = -1
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * self.game.tilesize
        self.index =0
        self.rot = 0
        self.previous_rot = 0
        self.last_update = 0
        self.current_frame = 0
        self.current_tile = self.pos//self.game.tilesize
        self.stay = True
        self.speed = self.game.speed


    def get_keys(self, key): #check for two keys
        self.vel = vec(0, 0)
        if key == 0: #left
            #self.speed
            self.vel.x = -self.speed
        elif key == 1: #right
            self.vel.x = self.speed
        elif key == 2:#down
            self.vel.y = self.speed
        elif key == 3:#up
            self.vel.y = -self.speed

    def teleport(self):
        maplen = len(self.game.map_data[0])
        if self.pos.x > ((self.game.GRIDWIDTH - maplen -4 )//2 + maplen) * self.game.tilesize:
            #uppos that  4 because of  5 i add in my init
            self.pos.x = (self.game.GRIDWIDTH - maplen) // 2 * self.game.tilesize
        if self.pos.x < (self.game.GRIDWIDTH - maplen)//2 * self.game.tilesize:
            self.pos.x = ((self.game.GRIDWIDTH - maplen - 4) // 2 + maplen ) * self.game.tilesize
        
    #declare movement and interaction with objects
    def move(self):
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        coll = collide_with_walls(self,'x',self.game.walls)
        hits = pg.sprite.spritecollide(self, self.game.coins, True)
        fruit_hit = pg.sprite.spritecollide(self, self.game.fruits,True)
        if fruit_hit:
            self.game.current_sound.stop()
            self.game.current_sound = self.game.eat_fruit_sound
            self.game.score += 200 *(self.game.level % len(FRUITS))
            self.game.picked = 1
            self.game.eat_fruit_sound.play()
        if hits:
            self.game.current_sound.stop()
            self.game.current_sound = self.game.eat_coin
            self.game.score += 10
            self.game.free_nodes.append((hits[0].rect.x // self.game.tilesize , hits[0].rect.y // self.game.tilesize))
            self.game.eat_coin.play()
        # power up that turns all ghosts in blue  
        if pg.sprite.spritecollide(self,self.game.pellets,True):
            self.game.current_sound.stop()
            self.game.current_sound = self.game.eat_coin
            self.game.pellet_activation = self.last_update
            self.game.is_pellet = True
            self.game.score += 50
            self.game.eat_coin.play()
            
        self.rect.y = self.pos.y
        if not coll:
            coll = collide_with_walls(self,'y',self.game.walls)
        return coll


    def update(self):
        #change in future
        map_len = len(self.game.map_data[0])

        self.game.player_coords = (self.rect.centerx // self.game.tilesize -int((self.game.GRIDWIDTH-map_len)/2),self.rect.centery // self.game.tilesize - 5)

        self.get_keys(self.keys)
        self.teleport()
        collision = self.move()
        self.animate()
        if collision:
            self.image = pg.transform.scale(pg.transform.rotate(self.game.player_img, self.previous_rot), (self.game.tilesize, self.game.tilesize))
            self.get_keys(self.previous_key)
            self.teleport()
            if self.move():#move returns true when collision
                self.image = pg.image.load(path.join(self.game.img_folder, PACMAN_IMAGE[2])).convert_alpha()
                self.image = pg.transform.scale(self.image, (self.game.tilesize, self.game.tilesize))
                self.stay = True


        else:
            self.stay = False
            self.image = pg.transform.scale(pg.transform.rotate(self.game.player_img, self.rot), (self.game.tilesize, self.game.tilesize))
            self.previous_key = self.keys
            self.previous_rot = self.rot

    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > ANIMATION_SPEED and self.keys != -1:
            self.last_update = now
            self.current_frame = (self.current_frame + 1 ) % 3
            self.game.player_img = pg.image.load(path.join(self.game.img_folder, PACMAN_IMAGE[self.current_frame])).convert_alpha()
        elif now - self.last_update > (ANIMATION_SPEED  * 1.2 )and self.keys == -1 and self.game.session_time > 0:
            if self.index == 11:
                self.index = 0
                self.game.player_img = pg.image.load(path.join(self.game.img_folder, 
                                            PACMAN_IMAGE[2])).convert_alpha()
                self.game.playing = False
                return 0
            self.last_update = now
            self.game.swap(3,0)
            self.game.player_img = pg.image.load(path.join(self.game.dead_anim, 
                                            DEATH[self.index])).convert_alpha()
            self.index += 1

class Ghost(pg.sprite.Sprite):
    def __init__(self, game, x, y,path=None):
        self.groups = game.all_sprites, game.ghosts
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.pos = vec(x, y) * self.game.tilesize
        self.vel = vec(0, 0)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.last_update = 0
        self.previous_rect = vec(self.rect.center)#ghost previous position
        self.eated = False
        self.speed = self.game.ghost_speed
        self.path = path
        self.index = 0
        self.key = -1
        self.previous_key = -1
        
        
    def following(self):
        #define following function to catch the player
        #chanching scatter state
        if self.game.scatter_mode == True and len(self.path) <= 2:
            self.game.scatter_mode = False
            self.path = breadth_search(self.game.maze,self.ghost_now,self.player_now)

        elif len(self.path) <= 2 and self.game.scatter_mode != True:
            self.path = breadth_search(self.game.maze,self.ghost_now,self.player_now)  

        if len(self.path) <= 1 and self.game.is_pellet == False and self.game.session_time < 20:
            return 0

        elif len(self.path) <= 1 and self.game.is_pellet == False:
            self.game_over()
            return 0

        elif self.game.is_pellet == True and len(self.path) <= 1:
            return 0 
        
        elif self.eated == True and len(self.path) <= 1:
             self.eated == False
             return 0
        move_y = self.path[self.index + 1][0] - self.path[self.index][0] #array path to player return indexes in reverse order - [0] - y coordinates , [1] - x self.game.tilesize
        move_x =self.path[self.index + 1][1] - self.path[self.index][1]
        
        if move_y == 0:
            if move_x > 0:#move right by x 
                self.key = 1
            else:
                self.key = 0
        elif move_x == 0:
            if move_y > 0:
                self.key = 2
            else:
                self.key = 3


    def get_keys(self, key): #check for two keys
        self.vel = vec(0, 0)
        if key == 0: #left
            self.vel.x = -self.speed
        elif key == 1: #right
            self.vel.x = self.speed
        elif key == 2:#down
            self.vel.y = self.speed
        elif key == 3:#up
            self.vel.y = -self.speed

    def movement(self):
        if self.game.player.keys != -1:
            self.speed = self.game.ghost_speed
            self.pos += self.vel  * self.game.dt
            self.rect.x = self.pos.x
            self.rect.y = self.pos.y
            if self.previous_key != self.key:
                self.previous_key = self.key
      
        
    def adjustment(self):
        map_len = len(self.game.map_data[0])
        if self.key == 0:
            self.ghost_now = vec(self.rect.right,self.rect.centery) // self.game.tilesize - vec(int((self.game.GRIDWIDTH-map_len)/2) , 5)
        elif self.key == 1:
            self.ghost_now = vec(self.rect.left,self.rect.centery) // self.game.tilesize - vec(int((self.game.GRIDWIDTH-map_len)/2) , 5)
            
        elif self.key == 2:
            self.ghost_now = vec(self.rect.centerx,self.rect.top) // self.game.tilesize - vec(int((self.game.GRIDWIDTH-map_len)/2) , 5)
            
        elif self.key == 3:
            self.ghost_now = vec(self.rect.centerx,self.rect.bottom) // self.game.tilesize - vec(int((self.game.GRIDWIDTH-map_len)/2) , 5)
            
        
    def game_over(self):
        self.game.player.keys = self.game.player.previous_key = -1
        self.game.current_sound.stop()
        self.game.current_sound = self.game.death_sound
        # self.game.playing = False
        self.game.death_sound.play()
        self.game.life_counter -= 1 

    def update(self):
        if self.game.player.keys != -1:
            self.behaviour()
            if pg.sprite.spritecollide(self,self.game.player_group,False) and self.game.is_pellet == True:
                print("Eated: ",self.game.is_pellet)
                self.game.current_sound.stop()
                self.game.current_sound = self.game.eat_ghost
                self.eated = True 
                self.game.score += 200
                self.game.eat_ghost.play()

            elif pg.sprite.spritecollide(self,self.game.player_group,False) and self.game.is_pellet == False and self.eated == False:
                self.game_over()
       

        
        self.get_keys(self.key)
        if self.movement():
            self.get_keys(self.previous_key)
            self.movement()
        else:
            if self.previous_key != self.key:
                self.previous_key = self.key
              
class Blinky(Ghost):

    def __init__(self, game, x, y,path=None):
        self.image = pg.transform.scale(game.blinky_img, (game.tilesize, game.tilesize))
        self.rect = self.image.get_rect()
        Ghost.__init__(self,game, x, y, path)
    
    def behaviour(self):
        map_len = len(self.game.map_data[0])
        #convert nodes with
        
        self.player_now = vec(self.game.player.rect.center) // self.game.tilesize - vec(int((self.game.GRIDWIDTH-map_len)/2) , 5)
        self.ghost_now = vec(self.rect.center) // self.game.tilesize - vec(int((self.game.GRIDWIDTH-map_len)/2) , 5)
        self.adjustment()
        self.game.data_for_inky = dist(self.ghost_now,self.player_now)

        if vec(self.player_now) != vec(-5,-int((self.game.GRIDWIDTH-map_len)/2)):
            self.ghost_now = (int(self.ghost_now[1]),int(self.ghost_now[0]))
            self.player_now = (int(self.player_now[1]),int(self.player_now[0]))
            
            if self.game.scatter_mode == True and self.game.p_ch_index < 2:
                # self.path.pop(0)
                self.path = breadth_search(self.game.maze,self.ghost_now,(1, 2))
                self.game.p_ch_index += 1

            if self.game.scatter_mode == True:
                self.path.pop()


            if self.game.is_pellet == False and vec(self.ghost_now) == vec(self.path[1]):
                self.game.p_ch_index = 0
                self.eated = False
                self.path.pop(0)
                self.game.ghost_img = pg.image.load(path.join(self.game.img_folder, BLINKY)).convert_alpha()
                self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize, self.game.tilesize))
            elif self.eated == True:
                self.speed = 150 
                self.game.ghost_img = pg.image.load(path.join(self.game.img_folder, 'dead_gh.png')).convert_alpha()
                self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize, self.game.tilesize))
                self.path = breadth_search(self.game.maze,self.ghost_now,self.game.ghost_house)

            elif self.game.is_pellet == True and self.eated == False:
                self.speed = 50
                self.game.ghost_img = pg.image.load(path.join(self.game.img_folder, 'blue_ghost.png')).convert_alpha()
                self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize, self.game.tilesize))
                self.path = breadth_search(self.game.maze,self.ghost_now,self.game.ghost_house)
            
            self.following()
        
class Pinky(Ghost):
    def __init__(self, game, x, y,path=None):
        self.image = pg.transform.scale(game.pinky_img, (game.tilesize, game.tilesize))
        self.rect = self.image.get_rect()
        Ghost.__init__(self,game, x, y, path)
    
    def behaviour(self):
        map_len = len(self.game.map_data[0])
        #convert nodes with
        self.player_now = vec(self.game.player.rect.center) // self.game.tilesize - vec(int((self.game.GRIDWIDTH-map_len)/2) , 5)
        self.ghost_now = vec(self.rect.center) // self.game.tilesize - vec(int((self.game.GRIDWIDTH-map_len)/2) , 5)
        self.adjustment()
        self.ghost_now = (int(self.ghost_now[1]),int(self.ghost_now[0]))
        self.player_now = (int(self.player_now[1]),int(self.player_now[0]))
        
        if vec(self.player_now) != vec(-int((self.game.GRIDWIDTH-map_len)/2), -5) and self.game.session_time > 1:
            
            if self.game.scatter_mode == True and self.game.p_ch_index < 2:
               self.path = breadth_search(self.game.maze,self.ghost_now,(1, 1))
            
            elif self.game.is_pellet == False and vec(self.ghost_now) == vec(self.path[1]):
                self.speed = self.game.ghost_speed 
                self.eated = False
                self.path.pop(0)
                self.game.ghost_img = pg.image.load(path.join(self.game.img_folder, PINKY)).convert_alpha()
                self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize, self.game.tilesize))
                self.dir = dir_definer(self.game.player.speed)
                self.dest = pinky_beh(self.game.maze,self.player_now,self.dir)
            
            elif self.eated == True:
                self.speed = 150 
                self.game.ghost_img = pg.image.load(path.join(self.game.img_folder, 'dead_gh.png')).convert_alpha()
                self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize, self.game.tilesize))
                self.path = breadth_search(self.game.maze,self.ghost_now,self.game.ghost_house)

            elif self.game.is_pellet == True and self.eated == False:
                self.speed = 50
                self.game.ghost_img = pg.image.load(path.join(self.game.img_folder, 'blue_ghost.png')).convert_alpha()
                self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize, self.game.tilesize))
                self.path = breadth_search(self.game.maze,self.ghost_now,self.game.ghost_house)
                
            if len(self.path) <= 2:
                self.dir = dir_definer(self.game.player.speed)
                self.dest = pinky_beh(self.game.maze,self.player_now,self.dir)
                self.path = breadth_search(self.game.maze,self.ghost_now,self.dest) 
            
            self.following()

class Inky(Ghost):
    def __init__(self, game, x, y, path=None):
        self.image = pg.transform.scale(game.inky_img, (game.tilesize, game.tilesize))
        self.dir = 0
        self.rect = self.image.get_rect()
        Ghost.__init__(self,game, x, y, path)
    def behaviour(self):
        map_len = len(self.game.map_data[0])
        #convert nodes with
        self.player_now = vec(self.game.player.rect.center) // self.game.tilesize - vec(int((self.game.GRIDWIDTH-map_len)/2) , 5)
        self.ghost_now = vec(self.rect.center) // self.game.tilesize - vec(int((self.game.GRIDWIDTH-map_len)/2) , 5)
        self.adjustment()
        self.ghost_now = (int(self.ghost_now[1]),int(self.ghost_now[0]))
        self.player_now = (int(self.player_now[1]),int(self.player_now[0]))
        
        if vec(self.player_now) != vec(-int((self.game.GRIDWIDTH-map_len)/2), -5) and self.game.session_time > 2:
            
            if self.game.scatter_mode == True and self.game.p_ch_index < 2:
               self.path = breadth_search(self.game.maze,self.ghost_now,(1, len(self.game.maze[0])-2))
            
            elif self.game.is_pellet == False and vec(self.ghost_now) == vec(self.path[1]):
                self.speed = self.game.ghost_speed 
                self.eated = False
                self.path.pop(0)
                self.game.ghost_img = pg.image.load(path.join(self.game.img_folder, INKY)).convert_alpha()
                self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize, self.game.tilesize))
                self.dir = dir_definer(self.game.player.speed)
                self.dest = pinky_beh(self.game.maze,self.player_now,self.dir)
            
            elif self.eated == True:
                self.speed = 150 
                self.game.ghost_img = pg.image.load(path.join(self.game.img_folder, 'dead_gh.png')).convert_alpha()
                self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize, self.game.tilesize))
                self.path = breadth_search(self.game.maze,self.ghost_now,self.game.ghost_house)

            elif self.game.is_pellet == True and self.eated == False:
                self.speed = 50
                self.game.ghost_img = pg.image.load(path.join(self.game.img_folder, 'blue_ghost.png')).convert_alpha()
                self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize, self.game.tilesize))
                self.path = breadth_search(self.game.maze,self.ghost_now,self.game.ghost_house)
                
            if len(self.path) <= 2:
                self.dir = dir_definer(self.game.player.speed)
                self.dest = inky_beh(self.game.maze,self.player_now,self.dir,self.game.data_for_inky)
                self.path = breadth_search(self.game.maze,self.ghost_now,self.dest) 
         
            self.following()
            self.following()

class Clyde(Ghost):
    def __init__(self, game, x, y,path=None):
        self.image = pg.transform.scale(game.clyde_img, (game.tilesize, game.tilesize))
        self.rect = self.image.get_rect()
        Ghost.__init__(self,game, x, y, path)
    
    def behaviour(self):
        map_len = len(self.game.map_data[0])
        #convert nodes with
        self.player_now = vec(self.game.player.rect.center) // self.game.tilesize - vec(int((self.game.GRIDWIDTH-map_len)/2) , 5)
        self.ghost_now = vec(self.rect.center) // self.game.tilesize - vec(int((self.game.GRIDWIDTH-map_len)/2) , 5)
        self.adjustment()
        self.ghost_now = (int(self.ghost_now[1]),int(self.ghost_now[0]))
        self.player_now = (int(self.player_now[1]),int(self.player_now[0]))
        
        if vec(self.player_now) != vec(-int((self.game.GRIDWIDTH-map_len)/2), -5) and self.game.session_time > 1:
            if clyde_beh(self.ghost_now,self.player_now) and self.game.session_time % 4 == 0:
                    self.path = breadth_search(self.game.maze,self.ghost_now,self.player_now)
            elif not clyde_beh(self.ghost_now,self.player_now) and self.game.session_time % 4 == 0:
                    self.path = breadth_search(self.game.maze,self.ghost_now,(1,1))
            
            if self.game.scatter_mode == True and self.game.p_ch_index < 2:
               self.path = breadth_search(self.game.maze,self.ghost_now,(1, 1))
            
            elif self.game.is_pellet == False and vec(self.ghost_now) == vec(self.path[1]):
                self.speed = self.game.ghost_speed 
                self.eated = False
                self.path.pop(0)
                self.game.ghost_img = pg.image.load(path.join(self.game.img_folder, CLYDE)).convert_alpha()
                self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize, self.game.tilesize))
                self.dir = dir_definer(self.game.player.speed)
                self.dest = pinky_beh(self.game.maze,self.player_now,self.dir)
            
            elif self.eated == True:
                self.speed = 150 
                self.game.ghost_img = pg.image.load(path.join(self.game.img_folder, 'dead_gh.png')).convert_alpha()
                self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize, self.game.tilesize))
                self.path = breadth_search(self.game.maze,self.ghost_now,self.game.ghost_house)

            elif self.game.is_pellet == True and self.eated == False:
                self.speed = 50
                self.game.ghost_img = pg.image.load(path.join(self.game.img_folder, 'blue_ghost.png')).convert_alpha()
                self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize, self.game.tilesize))
                self.path = breadth_search(self.game.maze,self.ghost_now,self.game.ghost_house)
                
            if len(self.path) <= 2:
                self.dir = dir_definer(self.game.player.speed)
                self.dest = pinky_beh(self.game.maze,self.player_now,self.dir)
                self.path = breadth_search(self.game.maze,self.ghost_now,self.dest) 
            
            self.following()

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y, image):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        img_folder = path.join(self.game.game_folder, 'images')
        self.image = pg.transform.scale(pg.image.load(path.join(game.img_folder, image)),
                                        (game.tilesize, game.tilesize))
        self.rect = self.image.get_rect()
        # self.x = x
        # self.y =y
        self.rect.x = x * game.tilesize
        self.rect.y = y * game.tilesize

class Map_Object(pg.sprite.Sprite):
    def __init__(self, groups ,game, x, y):
        pg.sprite.Sprite.__init__(self, groups)
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        self.rect = self.image.get_rect()
        self.rect.x = x * game.tilesize
        self.rect.y = y * game.tilesize
    
class Coins(Map_Object):
    def __init__(self,game, x, y):
        self.groups = game.all_sprites, game.coins
        self.image = pg.transform.scale(pg.image.load(path.join(game.img_folder, 'coin.png')),
                                        (game.tilesize, game.tilesize))
        Map_Object.__init__(self, self.groups ,game, x, y)

class Pellets(Map_Object):
    def __init__(self,game, x, y):
        self.groups = game.all_sprites,game.pellets
        self.image = pg.transform.scale(pg.image.load(path.join(game.img_folder, 'pellet.png')),
                                        (game.tilesize, game.tilesize))
        Map_Object.__init__(self, self.groups ,game, x, y)

class Stats(Map_Object):
    def __init__(self,game, x, y,image):
        self.groups = game.all_sprites
        self.image = pg.transform.scale(pg.image.load(path.join(game.img_folder, image)),
                                        (game.tilesize, game.tilesize))
        Map_Object.__init__(self, self.groups ,game, x, y)

class Fruit(Map_Object):
    def __init__(self,game, x, y , fruit):
        self.groups = game.all_sprites, game.fruits
        self.image = pg.transform.scale(pg.image.load(path.join(game.fruit_folder, FRUITS[fruit])),
                                        (game.tilesize, game.tilesize))
        Map_Object.__init__(self, self.groups ,game, x, y)

        


           
