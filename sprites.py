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
        self.shadow = pg.sprite.Group()
        self.image =  pg.transform.scale(self.game.player_img, (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.keys = -1
        self.previous_key = -1
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.index =0
        self.rot = 0

    def animation(self):
        if self.index == 2:
            self.index = 0
        # self.image = pg.transform.scale(pg.image.load(path.join(self.game.img_folder, PACMAN_IMAGE[self.index])),
        #                                 (TILESIZE, TILESIZE))
        self.index += 1

    def get_keys(self, key): #check for two keys
        self.vel = vec(0, 0)
        if key == 0: #left
            self.vel.x = -PLAYER_SPEED
        elif key == 1: #right
            self.vel.x = PLAYER_SPEED
        elif key == 2:#down
            self.vel.y = PLAYER_SPEED
        elif key == 3:#up
            self.vel.y = -PLAYER_SPEED

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
        # if self.previous_key != -1:
        #     self.keys = self.previous_key
        # self.get_keys()
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        coll = self.collide_with_walls('x')
        self.rect.y = self.pos.y
        if not coll:
            coll = self.collide_with_walls('y')
        return coll

    def update(self):
        # self.image = pg.transform.scale(pg.transform.rotate(self.game.player_img, self.rot),(TILESIZE,TILESIZE))
        # pg.transform.scale(self.game.player_img, (TILESIZE, TILESIZE))
        self.animation()
        self.get_keys(self.keys)
        collision = self.move()
        if collision:
            self.get_keys(self.previous_key)
            sec = self.move()
        else:
            self.image = pg.transform.scale(pg.transform.rotate(self.game.player_img, self.rot), (TILESIZE, TILESIZE))
            self.previous_key = self.keys



class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Coins(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        self.image = pg.transform.scale(pg.image.load(path.join(img_folder, 'coin.png')),
                                        (TILESIZE, TILESIZE))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y =y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

