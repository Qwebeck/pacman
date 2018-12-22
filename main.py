import pygame as pg
import sys
from os import path
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()


    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images')
        self.player_img = pg.image.load(path.join(self.img_folder, PACMAN_IMAGE[1])).convert_alpha()


        self.map_data = []
        with open(path.join(self.game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)


    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()

        map_len = len(self.map_data[0])
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                col += int((GRIDWIDTH-map_len)/2)
                # row += int(GRIDHEIGHT/2)
                row += 5
                if tile == '1':
                    Wall(self, col, row)
                if tile == '.':
                    Coins(self,col,row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'T':
                    Wall(self, col, row)
                col -= int((GRIDWIDTH-map_len)/2)
                row -= 5
    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

                self.image = pg.transform.scale(pg.transform.rotate(self.player_img, self.player.rot),
                                                (TILESIZE, TILESIZE))
                self.all_sprites.update()
                if event.key == pg.K_LEFT:
                    # self.player_image = pg.transform.rotate(self.player.image, 90)
                    self.swap(0)
                    self.player.rot = 90
                if event.key == pg.K_RIGHT:
                    # self.player.keys = 1
                    self.swap(1)
                    self.player.rot = -90
                if event.key == pg.K_UP:
                    # self.player.keys = 3
                    self.swap(3)
                    self.player.rot = 0

                if event.key == pg.K_DOWN:
                    # self.player.keys = 2
                    self.swap(2)
                    self.player.rot = 180


    def swap(self, dir):
        if self.player.previous_key == -1 :
            self.player.keys = dir
            self.player.previous_key = dir
        else:
            self.player.keys,self.player.previous_key = dir,self.player.keys

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
g.show_go_screen()