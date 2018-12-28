import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
import thorpy as th
from brs_agent import *
import pytmx

class Game:
    def __init__(self):
        pg.init()
        self.speed=PLAYER_SPEED
        self.tilesize = TILESIZE
        self.GRIDWIDTH = WIDTH / self.tilesize
        self.GRIDHEIGHT = HEIGHT / self.tilesize
        self.ghosts = GHOSTS # ghost number on map
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
        self.ghost_speed = GHOST_SPEED
        self.life_counter = 3
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images')
        self.is_pellet = False
        self.pellet_activation = 0
        
    
    # def maze_transform(maze,map):
    # for row, tiles in enumerate(map):
    #     row = []
    #     for col, tile in enumerate(tiles):
    #         if tile == '\n':
    #             break    
    #         if tile=='.' or tile =='G' or tile == 'P':
    #             row.append(0)    
    #         else:
    #             row.append(1) 
    #     maze.append(row)
    # return maze  player_cords
 
    

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images')
        self.player_img = pg.image.load(path.join(self.img_folder, PACMAN_IMAGE[2])).convert_alpha()
        self.ghost_img = pg.image.load(path.join(self.img_folder, GHOST_IMAGE)).convert_alpha()
        self.running = False

        self.map_data = []
        with open(path.join(self.game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
        maze = []
        self.player_cords = maze_transform(maze,self.map_data)
        self.maze = maze
       
        # for row in self.maze:
            # print(row)
        

    # def _render_region(self,image, rect, color, rad):
    #     # """Helper function for round_rect."""
    #     corners = rect.inflate(-2*rad, -2*rad)
    #     for attribute in ("topleft", "topright", "bottomleft", "bottomright"):
    #         pg.draw.circle(image, color, getattr(corners,attribute), rad)
    #     image.fill(color, rect.inflate(-2*rad,0))
    #     image.fill(color, rect.inflate(0,-2*rad))

    # def round_rect(self, surface, rect, color, rad=20, border=0, inside=(0,0,0,0)):
    #     # """
    #     # Draw a rect with rounded corners to surface.  Argument rad can be specified
    #     # to adjust curvature of edges (given in pixels).  An optional border
    #     # width can also be supplied; if not provided the rect will be filled.
    #     # Both the color and optional interior color (the inside argument) support
    #     # alpha.
    #     # """
    #     rect = pg.Rect(rect)
    #     zeroed_rect = rect.copy()
    #     zeroed_rect.topleft = 0,0
    #     image = pg.Surface(rect.size).convert_alpha()
    #     image.fill((0,0,0,0))
    #     self._render_region(image, zeroed_rect, color, rad)
    #     if border:
    #         zeroed_rect.inflate_ip(-2*border, -2*border)
    #         self._render_region(image, zeroed_rect, inside, rad)
    #     surface.blit(image, rect)
       
    def draw_walls(self):
        for rect in self.walls_on_map:
            pg.draw.rect(self.screen,WHITE,rect,1)
            
        #    self.rect(self.screen, rect, WHITE, 2, 1, BLUE)
           

    # initialize all variables and do all the setup for a new game
    def new(self):
        
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.ghosts = pg.sprite.Group()
        self.player_group = pg.sprite.Group()
        self.pellets = pg.sprite.Group()
        for row in self.maze:
            print(row)
        self.walls_on_map = []
        map_len = len(self.map_data[0])
        for y in range(len(self.maze)):
            for x in range (len(self.maze[0])):
                col = x + int((self.GRIDWIDTH-map_len)/2)
                row = y + 5
                if self.maze[y][x] == 1:
                    #without params can be a beatiful space mode 
                    self.walls_on_map.append((col * self.tilesize,row * self.tilesize,self.tilesize,self.tilesize))
                    Wall(self, col, row)
                elif self.maze[y][x] == 0:
                    Coins(self,col,row)
                elif self.maze[y][x] == 3:
                    Pellets(self,col,row)
                elif self.maze[y][x] == 'H':
                    self.ghost_house = (row - 5,col - int((self.GRIDWIDTH-map_len)/2))
                elif self.maze[y][x] == 'P':
                    self.player = Player(self, col, row)
                elif self.maze[y][x] == 'G':
                    # print(self.maze)
                    ghost_cord = (row - 5,col - int((self.GRIDWIDTH-map_len)/2))
                    print("Player :",self.player_cords)
                    print("Ghost :",ghost_cord)
                    path = breadth_search(self.maze,ghost_cord,self.player_cords)
                    
                    for i in range (1,len(path) - 1):
                        if path[i][0] != path[i-1][0] and path[i][1] != path[i-1][1]:
                            print("Previous : ",path[i])
                            print("Current :",path[i-1])
                    print("Path :",path)
                    Ghost(self,col,row,path)




                # x -= int((self.GRIDWIDTH-map_len)/2)
                # y -= 5

        # for row, tiles in enumerate(self.map_data):
        #     for col, tile in enumerate(tiles):
        #         #coordinates i want map to appear
        #         col += int((self.GRIDWIDTH-map_len)/2)
        #         row += 5

        #         if tile == '1':
        #             Wall(self, col, row)
        #         if tile == '.':
        #             Coins(self,col,row)
        #         if tile == 'P':
        #             self.player = Player(self, col, row)
        #         if tile == 'G':
        #             # print(self.maze)
        #             ghost_cord = (row - 5,col - int((self.GRIDWIDTH-map_len)/2))
        #             print("Player :",self.player_cords)
        #             print("Ghost :",ghost_cord)
        #             path = breadth_search(self.maze,ghost_cord,self.player_cords)
                    
                    # for i in range (1,len(path) - 1):
                    #     if path[i][0] != path[i-1][0] and path[i][1] != path[i-1][1]:
                    #         print("Previous : ",path[i])
                    #         print("Current :",path[i-1])
                    # print("Path :",path)
                    # Ghost(self,col,row,path)

                # if tile == 'T':
                #GHOST_SPEED
                #     if tile in self.teleports:
                #         #gridheight guarants me that there will be no repeated keys in dictionary
                #         self.teleports[col + GRIDHEIGHT] = row
                #     else:
                #         self.teleports[col]=row
             
    def run(self):
        #print
        # game loop - set self.playing = False to end the game
        print(self.life_counter)
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
            if now - self.pellet_activation > 4000 and  self.is_pellet == True:
                self.is_pellet = False
            self.events()
            self.update()
            self.draw()


    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        # self.draw_walls()

    def draw_grid(self):
        for x in range(0, WIDTH, self.tilesize):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, self.tilesize):
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
        self.draw_text("Timer ", self.tilesize, WHITE, self.GRIDWIDTH // 2 * self.tilesize, 3 * self.tilesize)
        self.draw_text(minutes +":" + seconds, self.tilesize, WHITE, (self.GRIDWIDTH // 2 + 3) * self.tilesize, 3 * self.tilesize)
        self.draw_text("Score ", self.tilesize, WHITE, (self.GRIDWIDTH - len(self.map_data[0])) // 2 * self.tilesize, 3 * self.tilesize)
        self.draw_text(str(self.score), self.tilesize, WHITE, ((self.GRIDWIDTH - len(self.map_data[0])) // 2 + 5) * self.tilesize, 3 * self.tilesize)



    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.drawing_of_changable()
        self.draw_walls()
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
            # for event in pg.event.get():
                # self.menu.react(event)
                # print(self.slider.get_value())
                # self.tilesize = int(self.slider.get_value())
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False

    def show_start_screen(self):
        application = th.Application(size=(WIDTH, HEIGHT), caption="Hello world")
        e_title = th.make_text("Pacman", font_size=20, font_color=WHITE)
        # e_title.center()
        e_title.set_topleft((10, 10))
        play_button = th.make_button("Play", func=th.functions.quit_menu_func)
        varset = th.VarSet()
        varset.add("tilesize", value=TILESIZE, text="Size of objects:", limits=(8, 32))
        varset.add("speed", value=PLAYER_SPEED, text="Speed:", limits=(10, 500))
        varset.add("ghosts", value=GHOSTS, text="Ghosts:", limits=(0, 20))
        varset.add("ghost_speed", value=GHOST_SPEED, text="Ghosts speed:", limits=(10, 500))
        e_options = th.ParamSetterLauncher.make([varset], "Options", "Options")
        quit_button = th.make_button("Quit",func=th.functions.quit_func)
        elements = [e_title, play_button, e_options, quit_button]
        e_background = th.Background.make(color=DARKGREY, elements=elements)
        th.store(e_background, elements)
        th.store(e_background)
        menu = th.Menu(e_background)  # create a menu on top of the background
        menu.play()  # launch the menu
        pg.display.flip()
        self.tilesize = varset.get_value("tilesize")
        self.speed = varset.get_value("speed")
        self.GRIDWIDTH = WIDTH / self.tilesize
        self.GRIDHEIGHT = HEIGHT / self.tilesize
        self.ghosts = varset.get_value("ghosts")
        self.ghost_speed = varset.get_value("ghost_speed")

        # pg.display.flip()
        # self.wait_for_key()


    def show_go_screen(self):
        pass



# create the game object
g = Game()
g.show_start_screen()
while True:
    if g.life_counter == 0:
        break
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