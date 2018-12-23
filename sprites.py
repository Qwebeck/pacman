import pygame as pg
import sys
from os import path
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
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

    def collide_with_walls(self, dir):
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        if dir == 'x':
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                elif self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
                return True
        if dir == 'y':
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.width
                elif self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
                return True

    def move(self):
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        coll = self.collide_with_walls('x')
        if pg.sprite.spritecollide(self, self.game.coins, True):
            self.game.score += 100
        self.rect.y = self.pos.y
        # self.teleport()
        # try self.teleport() exeptt
        if not coll:
            coll = self.collide_with_walls('y')
        return coll

    def update(self):
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


        else:
            self.image = pg.transform.scale(pg.transform.rotate(self.game.player_img, self.rot), (self.game.tilesize, self.game.tilesize))
            self.previous_key = self.keys
            self.previous_rot = self.rot




    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > ANIMATION_SPEED and self.keys != -1:
            self.last_update = now
            self.current_frame = (self.current_frame + 1 ) % 3
            self.game.player_img = pg.image.load(path.join(self.game.img_folder, PACMAN_IMAGE[self.current_frame])).convert_alpha()

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((self.game.tilesize, self.game.tilesize))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * self.game.tilesize
        self.rect.y = y * self.game.tilesize

class Coins(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        self.image = pg.transform.scale(pg.image.load(path.join(img_folder, 'coin.png')),
                                        (game.tilesize, game.tilesize))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y =y
        self.rect.x = x * game.tilesize
        self.rect.y = y * game.tilesize

