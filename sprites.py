import pygame as pg
import sys
import random
import pytweening as tween
from os import path
from settings import *
from brs_agent import *
from ghost_behavior import *

vec = pg.math.Vector2
random.seed()

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
        self.picked_power = 0
        self.picked_power_pos = (0 ,0)
        self.picked_power_time = 0


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
            self.picked_power_time = self.game.session_time
            self.picked_power = 200 *(self.game.level % len(FRUITS)) # 1 - fruit
            self.picked_power_pos = (self.rect.centerx // self.game.tilesize , self.rect.centery // self.game.tilesize)
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
            self.picked_power_time = self.game.session_time
            self.game.score += 50 # 2 - pellet 
            self.game.picked_pellets_number += 1 
            self.picked_power = 50  # 1 - fruit
            self.picked_power_pos = (self.rect.centerx // self.game.tilesize , self.rect.centery // self.game.tilesize)
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
        elif now - self.last_update >  120 and self.keys == -1 and self.game.session_time > 0:
            if self.index == 11:
                self.index = 0
                self.game.player_img = pg.image.load(path.join(self.game.img_folder, 
                                            PACMAN_IMAGE[2])).convert_alpha()
                self.game.playing = False
                pg.event.get()
                return 0
            self.last_update = now
            # self.game.swap(3,0)
            self.rot = 0
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
        self.escape_corner = 0
        self.emergency = False
        self.map_len = len(self.game.map_data[0])
        self.ghost_now = vec(self.rect.center) // self.game.tilesize - vec(int((self.game.GRIDWIDTH-self.map_len)/2) , 5)
        self.ghost_now = (int(self.ghost_now[1]),int(self.ghost_now[0]))
        self.current_frame = 0

    def bug_prevent(self, maze, ghost_now, ghost_house):
        wall_arr=['F',1]
        try:
            if maze[ghost_now[0]][ghost_now[1]] in wall_arr:
                if self.key == 0:
                    self.path = breadth_search(maze, ghost_now,(ghost_now[0],ghost_now[1] + 1),emergency=True)
                elif self.key == 1:
                    self.path = breadth_search(maze, ghost_now,(ghost_now[0],ghost_now[1] - 1 ),emergency=True)
                elif self.key == 2:
                    self.path = breadth_search(maze, ghost_now,(ghost_now[0] + 1 ,ghost_now[1]),emergency=True)
                elif self.key == 3:
                    self.path = breadth_search(maze, ghost_now,(ghost_now[0] - 1,ghost_now[1]),emergency=True)
                self.emergency = True
        except IndexError:
        # if ghost_now[0]<0 or ghost_now[1] < 0 or ghost_now[0] > len(maze) or ghost_now[1] > len(maze):
            self.path = breadth_search(maze, ghost_now,ghost_house,emergency=True)
            print(self.path)
        
    def following(self):
        #define following function to catch the player
        #chanching scatter state
        if self.game.scatter_mode == True and (self.path == 0 or len(self.path) <= 2):
            self.game.scatter_mode = False
            self.path = breadth_search(self.game.maze,self.ghost_now,self.player_now)

        elif (self.path == 0 or len(self.path) <= 2) and self.game.scatter_mode != True:
            self.path = breadth_search(self.game.maze,self.ghost_now,self.player_now)  

        if self.path == 0 or len(self.path) <= 1 and self.game.is_pellet == False and self.game.session_time < 20:
            return 0

        elif self.path == 0 or len(self.path) <= 1 and self.game.is_pellet == False:
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

    def animate(self, img_array):
        now = pg.time.get_ticks()
        # if self.game.hell_mode:
        if now - self.last_update > ANIMATION_SPEED * 4 and self.game.player.keys != -1:
                self.last_update = now
                self.current_frame = (self.current_frame + 1 ) % len(img_array)
                self.image = pg.image.load(path.join(self.game.img_folder, img_array[self.current_frame])).convert_alpha()
                self.image = pg.transform.scale(self.image, (self.game.tilesize, self.game.tilesize))
                if self.game.picked_pellets_number == self.game.unlucky_pellet and img_array == BLINKY :
                    self.image = pg.image.load(path.join(self.game.img_folder, 'empty_ghost.png')).convert_alpha()
                    self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize , self.game.tilesize ))


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
        # map_len = len(self.game.map_data[0])
        if self.key == 0:
            self.ghost_now = vec(self.rect.right,self.rect.centery) // self.game.tilesize - vec(int((self.game.GRIDWIDTH-self.map_len)/2) , 5)
        elif self.key == 1:
            self.ghost_now = vec(self.rect.left,self.rect.centery) // self.game.tilesize - vec(int((self.game.GRIDWIDTH-self.map_len)/2) , 5)
            
        elif self.key == 2:
            self.ghost_now = vec(self.rect.centerx,self.rect.top) // self.game.tilesize - vec(int((self.game.GRIDWIDTH-self.map_len)/2) , 5)
            
        elif self.key == 3:
            self.ghost_now = vec(self.rect.centerx,self.rect.bottom) // self.game.tilesize - vec(int((self.game.GRIDWIDTH-self.map_len)/2) , 5)
            
    def game_over(self):
        self.game.player.keys = self.game.player.previous_key = -1
        self.game.current_sound.stop()
        self.game.current_sound = self.game.death_sound
        # self.game.ghost_img = pg.image.load(path.join(self.game.img_folder, 'empty_ghost.png')).convert_alpha()
        # self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize, self.game.tilesize))
        # pg.sprite.Sprite.kill(self)
        self.game.game_over = True
        self.game.death_sound.play()
        self.game.life_counter -= 1 


    def update(self):
        if self.game.player.keys != -1:
            self.bug_prevent(self.game.maze,self.ghost_now,self.game.ghost_house)
            self.behaviour()
            if self.ghost_now in self.game.ghost_house_area:
                self.eated = False
            if pg.sprite.spritecollide(self,self.game.player_group,False) and self.game.is_pellet == True and self.eated == False:
                # print("Eated: ",self.game.is_pellet)
                self.game.current_sound.stop()
                self.game.current_sound = self.game.eat_ghost
                self.eated = True 
                self.game.player.picked_power_time = self.game.session_time
                self.game.score += 200 * (self.game.ghost_counter % 4 + 1)
                self.game.ghost_counter += 1
                self.game.player.picked_power = 200 * (self.game.ghost_counter % 4 + 1)  # 1 - fruit
                self.game.player.picked_power_pos = (self.rect.centerx // self.game.tilesize , self.rect.centery // self.game.tilesize)
                self.game.eat_ghost.play()

            elif pg.sprite.spritecollide(self,self.game.player_group,False) and self.game.is_pellet == False and self.eated == False:
                self.game_over()    
        elif self.game.player.keys == -1 and self.game.session_time > 0:
            pg.sprite.Sprite.kill(self)
        
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
        self.img_array = BLINKY
        Ghost.__init__(self,game, x, y, path)
    
    def behaviour(self):
        # map_len = len(self.game.map_data[0])
        #convert nodes with
        
        self.player_now = vec(self.game.player.rect.center) // self.game.tilesize - vec(int((self.game.GRIDWIDTH-self.map_len)/2) , 5)
        self.ghost_now = vec(self.rect.center) // self.game.tilesize - vec(int((self.game.GRIDWIDTH-self.map_len)/2) , 5)
        self.adjustment()
        self.game.data_for_inky = dist(self.ghost_now,self.player_now)

        if vec(self.player_now) != vec(-5,-int((self.game.GRIDWIDTH-self.map_len)/2)):
            self.ghost_now = (int(self.ghost_now[1]),int(self.ghost_now[0]))
            self.player_now = (int(self.player_now[1]),int(self.player_now[0]))
            
            if (self.game.scatter_mode == True or self.game.is_pellet == True ) and self.game.p_ch_index < 2 and self.path != 0 and self.path[-1] != self.escape_corner :
                # self.path.pop(0)
                try:
                    self.escape_corner = random.choice(self.game.corner_set)
                except:
                    self.escape_corner = (1, 2)
                self.path = breadth_search(self.game.maze,self.ghost_now,self.escape_corner)
                self.game.p_ch_index += 1

            # if self.game.scatter_mode == True:
            #     self.path.pop()
            if self.path == 0 or len(self.path) <= 2 and self.game.scatter_mode == False and self.game.is_pellet == False:
                self.path = breadth_search(self.game.maze,self.ghost_now,self.player_now , runnig = True)
                # print("This function too ")
                
            if self.eated == True  and self.path[:-1] != self.game.ghost_house :
                # print("Called here")
                
                self.path = breadth_search(self.game.maze,self.ghost_now,self.game.ghost_house)
                 
            if self.path != 0 and vec(self.ghost_now) == vec(self.path[1]):
                self.path.pop(0)



            if self.game.is_pellet == False :
                self.game.p_ch_index = 0
                self.eated = False
                # self.path.pop(0)
                # self.game.ghost_img = pg.image.load(path.join(self.game.img_folder, BLINKY)).convert_alpha()
                # self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize, self.game.tilesize))
                self.animate(self.img_array)

            elif self.eated == True:
                self.speed *= 3  
                self.game.ghost_img = pg.image.load(path.join(self.game.img_folder, 'dead_gh.png')).convert_alpha()
                self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize, self.game.tilesize))
                # self.path = breadth_search(self.game.maze,self.ghost_now,self.game.ghost_house)

            elif self.game.is_pellet == True and self.eated == False :
                self.speed *= 0.5 
                self.game.ghost_img = pg.image.load(path.join(self.game.img_folder, 'blue_ghost.png')).convert_alpha()
                self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize, self.game.tilesize))
               
                # self.path = breadth_search(self.game.maze,self.ghost_now,self.game.ghost_house)
            
            if self.game.picked_pellets_number == self.game.unlucky_pellet :
                # self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize * 5, self.game.tilesize * 5))
                self.game.ghost_img = pg.image.load(path.join(self.game.img_folder, 'empty_ghost.png')).convert_alpha()
                self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize , self.game.tilesize ))
                
                self.speed *= 1.05
                self.game.is_pellet = False
            
            
            
            self.following()


        
class Pinky(Ghost):
    def __init__(self, game, x, y,path=None):
        self.image = pg.transform.scale(game.pinky_img, (game.tilesize, game.tilesize))
        self.rect = self.image.get_rect()
        self.img_array = PINKY
        Ghost.__init__(self,game, x, y, path)
    
    def behaviour(self):
        # map_len = len(self.game.map_data[0])
        #convert nodes with
        self.player_now = vec(self.game.player.rect.center) // self.game.tilesize - vec(int((self.game.GRIDWIDTH-self.map_len)/2) , 5)
        self.ghost_now = vec(self.rect.center) // self.game.tilesize - vec(int((self.game.GRIDWIDTH-self.map_len)/2) , 5)
        self.adjustment()
        self.ghost_now = (int(self.ghost_now[1]),int(self.ghost_now[0]))
        self.player_now = (int(self.player_now[1]),int(self.player_now[0]))
        
        if vec(self.player_now) != vec(-int((self.game.GRIDWIDTH-self.map_len)/2), -5) and self.game.session_time > 1:
            if  self.path == 0:
                 self.path = breadth_search(self.game.maze,self.ghost_now,self.game.ghost_house) 


            if (self.game.scatter_mode == True or self.game.is_pellet == True ) and self.game.p_ch_index < 2 and self.path != 0 and self.path[-1] != self.escape_corner :
                # self.path.pop(0)
                try:
                    self.escape_corner = random.choice(self.game.corner_set)
                except:
                    self.escape_corner = (1, 2)
                self.path = breadth_search(self.game.maze,self.ghost_now,self.escape_corner)
                self.game.p_ch_index += 1

            if self.path != 0 and self.eated == True and self.path[:-1] != self.game.ghost_house:
                self.path = breadth_search(self.game.maze,self.ghost_now,self.game.ghost_house) 

            if (self.path == 0 or len(self.path) <= 2):
                self.dir = dir_definer(self.game.player.speed)
                self.dest = pinky_beh(self.game.maze,self.player_now,self.dir)
                self.path = breadth_search(self.game.maze,self.ghost_now,self.dest) 
            try:
                if vec(self.ghost_now) == vec(self.path[1]):
                    self.path.pop(0)
            except:
                pass
            if self.game.is_pellet == False :
                self.speed = self.game.ghost_speed 
                self.eated = False
                # self.path.pop(0)
                # self.game.ghost_img = pg.image.load(path.join(self.game.img_folder, PINKY)).convert_alpha()
                # self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize, self.game.tilesize))
                # self.dir = dir_definer(self.game.player.speed)
                # self.dest = pinky_beh(self.game.maze,self.player_now,self.dir)
                self.animate(self.img_array)
            
            elif self.eated == True:
                self.speed *= 3  
                self.game.ghost_img = pg.image.load(path.join(self.game.img_folder, 'dead_gh.png')).convert_alpha()
                self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize, self.game.tilesize))
                # self.path = breadth_search(self.game.maze,self.ghost_now,self.game.ghost_house)

            elif self.game.is_pellet == True and self.eated == False :
                self.speed *= 0.5 
                self.game.ghost_img = pg.image.load(path.join(self.game.img_folder, 'blue_ghost.png')).convert_alpha()
                self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize, self.game.tilesize))
                # self.path = breadth_search(self.game.maze,self.ghost_now,self.game.ghost_house)
            self.following()
        else:
            self.animate(self.img_array)


class Inky(Ghost):
    def __init__(self, game, x, y, path=None):
        self.image = pg.transform.scale(game.inky_img, (game.tilesize, game.tilesize))
        self.dir = 0
        self.rect = self.image.get_rect()
        self.img_array = INKY
        Ghost.__init__(self,game, x, y, path)
    def behaviour(self):
        # map_len = len(self.game.map_data[0])
        #convert nodes with
        self.player_now = vec(self.game.player.rect.center) // self.game.tilesize - vec(int((self.game.GRIDWIDTH-self.map_len)/2) , 5)
        self.ghost_now = vec(self.rect.center) // self.game.tilesize - vec(int((self.game.GRIDWIDTH-self.map_len)/2) , 5)
        self.adjustment()
        self.ghost_now = (int(self.ghost_now[1]),int(self.ghost_now[0]))
        self.player_now = (int(self.player_now[1]),int(self.player_now[0]))
        
        if vec(self.player_now) != vec(-int((self.game.GRIDWIDTH-self.map_len)/2), -5) and self.game.session_time > 1:

            if self.eated == True and self.path[:-1] != self.game.ghost_house:
                self.path = breadth_search(self.game.maze,self.ghost_now,self.game.ghost_house) 


            if (self.game.scatter_mode == True or self.game.is_pellet == True and self.eated == False ) and self.path != 0 and self.game.p_ch_index < 2 and self.path[-1] != self.escape_corner :
                # self.path.pop(0)
                try:
                    self.escape_corner = random.choice(self.game.corner_set)
                except:
                    self.escape_corner = (1, 2)
                self.path = breadth_search(self.game.maze,self.ghost_now,self.escape_corner)
                self.game.p_ch_index += 1
            
            
            
            
            try:
                if (self.path == 0 or len(self.path) <= 2):
                    self.dir = dir_definer(self.game.player.speed)
                    self.dest = inky_beh(self.game.maze,self.player_now,self.dir,self.game.data_for_inky)
                    self.path = breadth_search(self.game.maze,self.ghost_now,self.dest) 
            except:
                pass
            try:
                if vec(self.ghost_now) == vec(self.path[1]):
                    self.path.pop(0)
            except:
                pass
            if self.game.is_pellet == False:
                self.speed = self.game.ghost_speed 
                self.eated = False
                # self.path.pop(0)
                # self.game.ghost_img = pg.image.load(path.join(self.game.img_folder, INKY)).convert_alpha()
                # self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize, self.game.tilesize))
                # self.dir = dir_definer(self.game.player.speed)
                # self.dest= pinky_beh(self.game.maze,self.player_now,self.dir)
                self.animate(self.img_array)
            
            elif self.eated == True:
                self.speed *= 3  
                self.game.ghost_img = pg.image.load(path.join(self.game.img_folder, 'dead_gh.png')).convert_alpha()
                self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize, self.game.tilesize))
                # self.path = breadth_search(self.game.maze,self.ghost_now,self.game.ghost_house)

            elif self.game.is_pellet == True and self.eated == False :
                self.speed *= 0.5 
                self.game.ghost_img = pg.image.load(path.join(self.game.img_folder, 'blue_ghost.png')).convert_alpha()
                self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize, self.game.tilesize))
                # self.path = breadth_search(self.game.maze,self.ghost_now,self.game.ghost_house)
            self.following()
        else:
            self.animate(self.img_array)

class Clyde(Ghost):
    def __init__(self, game, x, y,path=None):
        self.image = pg.transform.scale(game.clyde_img, (game.tilesize, game.tilesize))
        self.rect = self.image.get_rect()
        self.img_array = CLYDE
        Ghost.__init__(self,game, x, y, path)
    
    def behaviour(self):
        # map_len = len(self.game.map_data[0])
        #convert nodes with
        self.player_now = vec(self.game.player.rect.center) // self.game.tilesize - vec(int((self.game.GRIDWIDTH-self.map_len)/2) , 5)
        self.ghost_now = vec(self.rect.center) // self.game.tilesize - vec(int((self.game.GRIDWIDTH-self.map_len)/2) , 5)
        self.adjustment()
        self.ghost_now = (int(self.ghost_now[1]),int(self.ghost_now[0]))
        self.player_now = (int(self.player_now[1]),int(self.player_now[0]))
        
        if vec(self.player_now) != vec(-int((self.game.GRIDWIDTH-self.map_len)/2), -5) and self.game.session_time > 1:
            if (self.game.scatter_mode == True or self.game.is_pellet == True ) and self.game.p_ch_index < 2 and self.path != 0 and self.path[-1] != self.escape_corner :
                # self.path.pop(0)
                try:
                    self.escape_corner = random.choice(self.game.corner_set)
                except:
                    self.escape_corner = (1, 2)
                self.path = breadth_search(self.game.maze,self.ghost_now,self.escape_corner)
                self.game.p_ch_index += 1

            if (self.path == 0 or len(self.path) <= 2) :
                self.dir = dir_definer(self.game.player.speed)
                self.dest = pinky_beh(self.game.maze,self.player_now,self.dir)
                if clyde_beh(self.ghost_now,self.player_now):
                    self.path = breadth_search(self.game.maze,self.ghost_now,self.dest) 
                else:
                    try:
                        self.escape_corner = random.choice(self.game.corner_set)
                    except:
                        self.escape_corner = (1, 2)
                    self.path = breadth_search(self.game.maze,self.ghost_now,self.escape_corner)
            
            if self.eated == True and self.path[:-1] != self.game.ghost_house:
                self.path = breadth_search(self.game.maze,self.ghost_now,self.game.ghost_house) 

            try:
                if vec(self.ghost_now) == vec(self.path[1]):
                    self.path.pop(0)
            except:
                pass
            
            
            
            # if clyde_beh(self.ghost_now,self.player_now) and self.game.session_time % 4 == 0:
            #         self.path = breadth_search(self.game.maze,self.ghost_now,self.player_now)
            # elif not clyde_beh(self.ghost_now,self.player_now) and self.game.session_time % 4 == 0:
            #         self.path = breadth_search(self.game.maze,self.ghost_now,(1,1))
            
            if self.game.scatter_mode == True and self.game.p_ch_index < 2:
               self.path = breadth_search(self.game.maze,self.ghost_now,(1, 1))
         
            
            if self.game.is_pellet == False:
                self.speed = self.game.ghost_speed 
                self.eated = False
                # self.path.pop(0)
                # self.game.ghost_img = pg.image.load(path.join(self.game.img_folder, CLYDE)).convert_alpha()
                # self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize, self.game.tilesize))
                # self.dir = dir_definer(self.game.player.speed)
                # self.dest = pinky_beh(self.game.maze,self.player_now,self.dir)
                self.animate(self.img_array)
            
            elif self.eated == True:
                self.speed *= 3  
                self.game.ghost_img = pg.image.load(path.join(self.game.img_folder, 'dead_gh.png')).convert_alpha()
                self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize, self.game.tilesize))
                # self.path = breadth_search(self.game.maze,self.ghost_now,self.game.ghost_house)

            elif self.game.is_pellet == True and self.eated == False :
                self.speed *= 0.5 
                self.game.ghost_img = pg.image.load(path.join(self.game.img_folder, 'blue_ghost.png')).convert_alpha()
                self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize, self.game.tilesize))
                # self.path = breadth_search(self.game.maze,self.ghost_now,self.game.ghost_house)
                
            if (self.path == 0 or len(self.path) <= 2):
                self.dir = dir_definer(self.game.player.speed)
                self.dest = pinky_beh(self.game.maze,self.player_now,self.dir)
                self.path = breadth_search(self.game.maze,self.ghost_now,self.dest) 
            
            self.following()
        else:
            self.animate(self.img_array)

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
        self.pos = vec(x * game.tilesize,  y * game.tilesize)
    
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
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1
        Map_Object.__init__(self, self.groups ,game, x, y)
    
    def update(self):
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.y = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1

class Stats(Map_Object):
    def __init__(self,game, x, y,image,folder = 'img_folder'):
        self.groups = game.all_sprites
       
        if folder != 'img_folder':
            folder = game.fruit_folder
        else:
            folder = game.img_folder
        self.image = pg.transform.scale(pg.image.load(path.join(folder, image)),
                                        (game.tilesize, game.tilesize))
        Map_Object.__init__(self, self.groups ,game, x, y)

class Fruit(Map_Object):
    def __init__(self,game, x, y , fruit):
        self.groups = game.all_sprites, game.fruits
        self.image = pg.transform.scale(pg.image.load(path.join(game.fruit_folder, FRUITS[fruit])),
                                        (game.tilesize, game.tilesize))
        Map_Object.__init__(self, self.groups ,game, x, y)





