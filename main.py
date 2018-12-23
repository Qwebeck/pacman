import pygame as pg
import sys
from os import path
from settings import *
import settings
from sprites import *
import thorpy


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.score = 0
        self.minutes = 0
        self.seconds = 0
        self.font_name = pg.font.match_font(FONT_NAME)
        self.running = True
        #timer variable
        self.last_update = 0


    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images')
        self.player_img = pg.image.load(path.join(self.img_folder, PACMAN_IMAGE[2])).convert_alpha()
        self.running = False

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
                #coordinates i want map to appear
                col += int((GRIDWIDTH-map_len)/2)
                row += 5

                if tile == '1':
                    Wall(self, col, row)
                if tile == '.':
                    Coins(self,col,row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                # if tile == 'T':
                #     if tile in self.teleports:
                #         #gridheight guarants me that there will be no repeated keys in dictionary
                #         self.teleports[col + GRIDHEIGHT] = row
                #     else:
                #         self.teleports[col]=row
                col -= int((GRIDWIDTH-map_len)/2)
                row -= 5
    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            now = pg.time.get_ticks()
            if now - self.last_update > 1000:
                self.last_update = now
                self.seconds += 1
                if self.seconds >= 60:
                    self.seconds = 0
                    self.minutes += 1
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

    def drawing_of_changable(self):
        if self.minutes < 10:
            minutes = "0" + str(self.minutes)
        else:
            minutes = str(self.minutes)
        if self.seconds < 10:
            seconds = "0" + str(self.seconds)
        else:
            seconds = str(self.seconds)
        self.draw_text("Timer ", TILESIZE, WHITE, GRIDWIDTH // 2 * TILESIZE, 3 * TILESIZE)
        self.draw_text(minutes +":"+ seconds, TILESIZE, WHITE, (GRIDWIDTH // 2 + 3)* TILESIZE, 3 * TILESIZE)
        self.draw_text("Score ", TILESIZE, WHITE, (GRIDWIDTH - len(self.map_data[0]))//2 * TILESIZE, 3 * TILESIZE)
        self.draw_text(str(self.score), TILESIZE, WHITE, ((GRIDWIDTH - len(self.map_data[0]))// 2 + 5) * TILESIZE, 3 * TILESIZE)



    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.drawing_of_changable()
        pg.display.flip()


    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                self.all_sprites.update()
                if event.key == pg.K_LEFT:
                    self.swap(0,90)
                    # self.player.rot = 90
                if event.key == pg.K_RIGHT:
                    self.swap(1,-90)
                    self.player.rot = -90
                if event.key == pg.K_UP:
                    self.swap(3,0)
                    # self.player.rot = 0

                if event.key == pg.K_DOWN:
                    self.swap(2,180)
                    # self.player.rot = 180


    def swap(self, dir ,rot):
        if self.player.previous_key == -1 :
            self.player.keys = dir
            self.player.previous_key = dir
            self.player.rot = rot
            self.player.previous_rot = rot
        else:
            self.player.rot, self.player.previous_rot = rot, self.player.rot
            self.player.keys, self.player.previous_key = dir, self.player.keys

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def show_start_screen(self):
        pass
        # self.wait_for_key()

    def show_go_screen(self):
        pass



# create the game object
g = Game()

while True:

    g.new()
    g.run()
g.show_go_screen()


#  self.screen.fill(BGCOLOR)
#             application = th.Application(size=(WIDTH, HEIGHT), caption="Hello world")
#
#             e_title = th.make_text("Pacman", font_size=20, font_color=(0, 0, 150))
#             e_title.center()
#             e_title.set_topleft((None, 10))
#             play_button = th.make_button("Play", func=th.functions.quit_menu_func)
#
#             varset = th.VarSet()
#             varset.add("tilesize", value=TILESIZE, text="Size of objects:", limits=(8, 32))
#             varset.add("speed", value=PLAYER_SPEED, text="Speed:", limits=(10, 500))
#             varset.add("player_name", value=PLAYER_NAME, text="Player name:")
#             e_options = th.ParamSetterLauncher.make([varset], "Options", "Options")
#             e_background = th.Background.make(color=DARKGREY,
#                                               elements=[e_title, play_button, e_options])
#             th.store(e_background, [play_button, e_options])
#             th.store(e_background)
#
#             menu = th.Menu(e_background)  # create a menu on top of the background
#             menu.play()  # launch the menu
#             pg.display.flip()
#             MOD_TILE = varset.get_value("tilesize")
#             MOD_NAME = varset.get_value("player_name")
#             MOD_SPEED = varset.get_value("speed")
#             return  MOD_TILE,MOD_SPEED,MOD_NAME