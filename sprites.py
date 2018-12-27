import pygame as pg
import sys
import random
from os import path
from settings import *
from brs_agent import *
vec = pg.math.Vector2
random.seed()



#TODO
#teleportation bug
#change AI logic 
#add graphic
#add bonuses 
#add new ghost classes
#4 other ghosts 

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
                sprite.pos.y = hits[0].rect.top - sprite.rect.width
            elif sprite.vel.y < 0:
                sprite.pos.y = hits[0].rect.bottom
            sprite.vel.y = 0
            sprite.rect.y = sprite.pos.y
            return True


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

    def get_keys(self, key): #check for two keys
        self.vel = vec(0, 0)
        if key == 0: #left
            self.vel.x = -self.game.speed
        elif key == 1: #right
            self.vel.x = self.game.speed
        elif key == 2:#down
            self.vel.y = self.game.speed
        elif key == 3:#up
            self.vel.y = -self.game.speed

    def teleport(self):
        maplen = len(self.game.map_data[0])
        if self.pos.x > ((self.game.GRIDWIDTH - maplen -4 )//2 + maplen) * self.game.tilesize:
            #uppos that  4 because of  5 i add in my init
            self.pos.x = (self.game.GRIDWIDTH - maplen) // 2 * self.game.tilesize
        if self.pos.x < (self.game.GRIDWIDTH - maplen)//2 * self.game.tilesize:
            self.pos.x = ((self.game.GRIDWIDTH - maplen - 4) // 2 + maplen ) * self.game.tilesize
        # if self.vel.x > 0 and self.pos.x > self.game.teleports[self.pos.y//32 + GRIDHEIGHT] + 32 :
            # +32 because i want be on right end of the tile and just then teleport
        #     print("called")
        #     self.pos.x = self.game.teleports[self.pos.y//32]
        # elif self.vel.x < 0 and self.pos.x < self.game.teleports[self.pos.y]:
        #     self.pos.x = self.game.teleports[self.pos.y//32 + GRIDHEIGHT]

    # def collide_with_walls(self, dir):
    #     hits = pg.sprite.spritecollide(self, self.game.walls, False)
    #     if dir == 'x':
    #         if hits:
    #             if self.vel.x > 0:
    #                 self.pos.x = hits[0].rect.left - self.rect.width
    #             elif self.vel.x < 0:
    #                 self.pos.x = hits[0].rect.right
    #             self.vel.x = 0
    #             self.rect.x = self.pos.x
    #             return True
    #     if dir == 'y':
    #         if hits:
    #             if self.vel.y > 0:
    #                 self.pos.y = hits[0].rect.top - self.rect.width
    #             elif self.vel.y < 0:
    #                 self.pos.y = hits[0].rect.bottom
    #             self.vel.y = 0
    #             self.rect.y = self.pos.y
    #             return True
    # player_cords
    #same 

    #declare movement and interaction with objects
    def move(self):
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        coll = collide_with_walls(self,'x',self.game.walls)
        if pg.sprite.spritecollide(self, self.game.coins, True):
            self.game.score += 100
        # power up that turns all ghosts in blue  
        if pg.sprite.spritecollide(self,self.game.pellets,True):
            self.game.pellet_activation = self.last_update
            self.game.is_pellet = True
        self.rect.y = self.pos.y
        # self.teleport()
        # try self.teleport() exeptt
        if not coll:
            coll = collide_with_walls(self,'y',self.game.walls)
        return coll


    def update(self):
        #change in future
        map_len = len(self.game.map_data[0])

        self.game.player_coords = (self.rect.centerx // self.game.tilesize -int((self.game.GRIDWIDTH-map_len)/2),self.rect.centery // self.game.tilesize - 5)
        # print("Player coordinates :",self.game.player_coords)
        self.get_keys(self.keys)
        self.teleport()
        collision = self.move()
        self.animate()
        # print(self.rot)
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


class Ghost(pg.sprite.Sprite):
    def __init__(self, game, x, y,path=None):
        self.groups = game.all_sprites, game.ghosts
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize, self.game.tilesize))
        self.rect = self.image.get_rect()
        self.pos = vec(x, y) * self.game.tilesize
        self.vel = vec(0, 0)
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.last_update = 0
        self.previous_rect = vec(self.rect.center)#ghost previous position
        
        # self.offset = random.choice([-1, 1])  # -1 - x-axes
        # self.dir = random.choice([-1,1])
        self.speed = self.game.ghost_speed
        self.path = path
        self.index = 0
        # self.previous_ghost_pos = (self.rect.centerx// self.game.tilesize,self.rect.centery//self.game.tilesize)
        # self.turn_point = vec(0 ,0)
        self.key = -1
        self.previous_key = -1
        # self.following()
        
        
        

    def following(self):
        #define following function to catch the player
        # print(self.path)
        if self.previous_key != self.key:
            print("I change it")
            self.previous_key = self.key
        if len(self.path) <= 1 :
            self.game_over()
            return 0 

        map_len = len(self.game.map_data[0])
        move_y = self.path[self.index + 1][0] - self.path[self.index][0] #array path to player return indexes in reverse order - [0] - y coordinates , [1] - x self.game.tilesize
        move_x =self.path[self.index + 1][1] - self.path[self.index][1]
        if move_y == 0:
            if move_x > 0:#move right by x 
                self.key = 1
                # self.turn_point = (vec(self.path[self.index + 1][1],self.path[self.index + 1][0])  + vec(int((self.game.GRIDWIDTH-map_len)/2) , 5) )  * self.game.tilesize + vec(self.game.tilesize , 0)
            else:
                self.key = 0
                # self.turn_point = (vec(self.path[self.index + 1][1],self.path[self.index + 1][0])  + vec(int((self.game.GRIDWIDTH-map_len)/2) , 5) )  * self.game.tilesize 
        elif move_x == 0:
            if move_y > 0:
                self.key = 2
                # self.turn_point = (vec(self.path[self.index + 1][1],self.path[self.index + 1][0])  + vec(int((self.game.GRIDWIDTH-map_len)/2) , 5) )  * self.game.tilesize           
            else:
                self.key = 3
                # self.turn_point = (vec(self.path[self.index + 1][1],self.path[self.index + 1][0])  + vec(int((self.game.GRIDWIDTH-map_len)/2) , 5) )  * self.game.tilesize - vec(0 ,self.game.tilesize) 
        #last vector is vector of changes 
        # print("Node: ",(self.path[self.index + 1][1],self.path[self.index + 1][0]))
        # print("Node on map: ",(vec(self.path[self.index + 1][1],self.path[self.index + 1][0])  + vec(int((self.game.GRIDWIDTH-map_len)/2) , 5) ) )
        # print("Turn point center : " ,self.turn_point)
        # self.index += 1

        # print("Remove: ",self.path[self.index])
        # self.path.pop(self.index )
        # print("Path in following:",self.path)
        print("Place to go:", vec(self.path[self.index + 1][0],self.path[self.index + 1][1]))

        
        
        # self.path[index + 1][0] - self.path[index][0]
        # self.path[index + 1][0] - self.path[index][0]



    def get_keys(self, key): #check for two keys
        self.vel = vec(0, 0)
        if key == 0: #left
            self.vel.x = -self.game.speed
        elif key == 1: #right
            self.vel.x = self.game.speed
        elif key == 2:#down
            self.vel.y = self.game.speed
        elif key == 3:#up
            self.vel.y = -self.game.speed

    def movement(self):
        # changing velocity
        # self.get_keys(self.key)
        # now = pg.time.get_ticks()
        # if now - self.last_update > 5000:
        
        #     self.turn()
        #     self.last_update = now
        if self.game.player.keys != -1:
            # self.following()
            self.speed = self.game.ghost_speed
            self.pos += self.vel * self.game.dt
            self.rect.x = self.pos.x
            coll = collide_with_walls(self,'x',self.game.walls)
            self.rect.y = self.pos.y
            # self.teleport() print
            # try self.teleport() exeptt
            if not coll:
                coll = collide_with_walls(self,'y',self.game.walls)
            return coll
        
    def game_over(self):
        self.game.playing = False
        self.game.life_counter -= 1 



    def update(self):
        map_len = len(self.game.map_data[0])
        #convert nodes with
        self.player_now = vec(self.game.player.rect.center) // self.game.tilesize - vec(int((self.game.GRIDWIDTH-map_len)/2) , 5)
        ghost_now = vec(self.rect.center) // self.game.tilesize - vec(int((self.game.GRIDWIDTH-map_len)/2) , 5)
  
        if vec(self.player_now) != vec(-17, -5) and self.game.player.current_tile != self.player_now :
            self.game.player.current_tile = self.player_now
            ghost_now = (int(ghost_now[1]),int(ghost_now[0]))
            self.player_now = (int(self.player_now[1]),int(self.player_now[0]))

            if self.game.is_pellet == False:
                self.game.ghost_img = pg.image.load(path.join(self.game.img_folder, GHOST_IMAGE)).convert_alpha()
                self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize, self.game.tilesize))
                self.path = breadth_search(self.game.maze,ghost_now,self.player_now)
            elif self.game.is_pellet == True:
                print("power-up")
                self.game.ghost_img = pg.image.load(path.join(self.game.img_folder, 'blue_ghost.png')).convert_alpha()
                self.image = pg.transform.scale(self.game.ghost_img, (self.game.tilesize, self.game.tilesize))
                self.path = breadth_search(self.game.maze,ghost_now,self.game.ghost_house)
            # self.path.pop(0)
            self.following()

        

        #GHOST_SPEED
        # if vec(self.rect.center) // self.game.tilesize - vec(int((self.game.GRIDWIDTH-map_len)/2) , 5) != self.previous_rect:
        #     self.previous_rect = vec(self.rect.center) // self.game.tilesize - vec(int((self.game.GRIDWIDTH-map_len)/2) , 5)
        #     print(self.previous_rect)
            # self.following()

            # print(self.path)


        
        # print("Current player tile :",self.game.player.current_tile)
        # if (self.player_now[1],self.player_now[0]) not in self.path:
        # #     # print("Player position: ", self.player_now )
        # #     # print(self.path)
        #     self.path.append((self.player_now[1],self.player_now[0]))
        
        if pg.sprite.spritecollide(self,self.game.player_group,True):
            self.game_over()
        
        self.get_keys(self.key)
        # print("Current key:",self.key)
        #if self.movement returns True that mens collision , so we save our key get from following and using our previous key
        if self.movement():
            # print("Previous key:",self.previous_key)
            self.get_keys(self.previous_key)

            self.movement()
        else:
            if self.previous_key != self.key:
                self.previous_key = self.key
        


        # if self.key == 1 and self.rect.x + self.game.tilesize == self.turn_point[0] and self.rect.y == self.turn_point[1]:
        #     # print(vec(self.rect.center))
        #     self.following()
        # elif self.key == 0 and self.rect.x == self.turn_point[0] and self.rect.y == self.turn_point[1]:
        #     self.following()
        # elif self.key == 2 and self.rect.x == self.turn_point[0] and self.rect.y == self.turn_point[1]:
        #     self.following()
        # elif self.key == 3 and self.rect.x == self.turn_point[0] and self.rect.y - self.game.tilesize == self.turn_point[1]:
        #     self.following()
        #    self.key = random.choice([0,1,2,3])
           
            


class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((self.game.tilesize, self.game.tilesize))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * self.game.tilesize
        self.rect.y = y * self.game.tilesize

class Map_Object(pg.sprite.Sprite):
    def __init__(self, groups ,game, x, y):
        # self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, groups)
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y =y
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

