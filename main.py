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
        self.session_time = 0
        self.font_name = pg.font.match_font(FONT_NAME)
        self.running = True
        #timer variable
        self.last_update = 0
        self.last_scatter_update = 0
        self.ghost_speed = GHOST_SPEED
        self.life_counter = 3
        self.is_pellet = False
        self.pellet_activation = 0
        self.p_ch_index = 0
        self.scatter_mode = True   

    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images')
        self.dead_anim = path.join(self.img_folder, 'dead_an')
        # print("Image folder in main:",self.img_folder)
        self.player_img = pg.image.load(path.join(self.img_folder, PACMAN_IMAGE[2])).convert_alpha()
        self.blinky_img = pg.image.load(path.join(self.img_folder, BLINKY)).convert_alpha()
        self.pinky_img = pg.image.load(path.join(self.img_folder, PINKY)).convert_alpha()
        self.inky_img = pg.image.load(path.join(self.img_folder, INKY)).convert_alpha()
        self.clyde_img = pg.image.load(path.join(self.img_folder, CLYDE)).convert_alpha()
        self.running = False
        self.FPS = FPS
        self.map_data = []
        with open(path.join(self.game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
        maze = []
        self.player_cords = maze_transform(maze,self.map_data)
        self.maze = maze
       
      
    # initialize all variables and do all the setup for a new game
    def new(self):
        self.session_time = 0
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.ghosts = pg.sprite.Group()
        self.player_group = pg.sprite.Group()
        self.pellets = pg.sprite.Group()
        self.fruits= pg.sprite.Group()
        self.data_for_inky = 0
        self.score = 0
        self.scatter_mode = True
        for life in range(self.life_counter):
                x = ((self.GRIDWIDTH - len(self.map_data[0])) // 2 + 5 + life + 0.10*life)  
                y = ((self.GRIDHEIGHT - len(self.map_data) + 4)) 
                Lifes(self,x,y)
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
                    Wall(self, col, row,WALLS[0])
                elif self.maze[y][x] == 0:
                    Coins(self,col,row)
                elif self.maze[y][x] == 3:
                    Pellets(self,col,row)
                elif self.maze[y][x] == 'H':
                    self.ghost_house = (row - 5,col - int((self.GRIDWIDTH-map_len)/2))
                elif self.maze[y][x] == 'P':
                    self.player = Player(self, col, row)
                elif self.maze[y][x] == 'C':
                    Wall(self, col, row,WALLS[7])
                elif self.maze[y][x] == 'V':
                    Wall(self, col, row,WALLS[6])
                elif self.maze[y][x] == 'N':
                    Wall(self, col, row,WALLS[4])
                elif self.maze[y][x] == 'F':
                    Wall(self, col, row,WALLS[1])
                elif self.maze[y][x] == 'J':
                    Wall(self, col, row,WALLS[2])
                elif self.maze[y][x] == 'M':
                    Wall(self, col, row,WALLS[3])
                elif self.maze[y][x] == 'B':
                    Wall(self, col, row,WALLS[5])
                elif self.maze[y][x] == 'G':
                    # print(self.maze)
                    ghost_cord = (row - 5,col - int((self.GRIDWIDTH-map_len)/2))
                    # print("Player :",self.player_cords)
                    # print("Ghost :",ghost_cord)
                    path = breadth_search(self.maze,ghost_cord,self.player_cords)
                    self.ghost = Blinky(self,col,row,path)
                elif self.maze[y][x] == 'p':
                    # print(self.maze)
                    ghost_cord = (row - 5,col - int((self.GRIDWIDTH-map_len)/2))
                    path = breadth_search(self.maze,ghost_cord,(1,1))
                    Pinky(self,col,row,path)
                elif self.maze[y][x] == 'i':
                    # print(self.maze)
                    ghost_cord = (row - 5,col - int((self.GRIDWIDTH-map_len)/2))
                    path = breadth_search(self.maze,ghost_cord ,(len(self.maze) - 2, 1))
                    Inky(self,col,row,path)
                elif self.maze[y][x] == 'c':
                    # print(self.maze)
                    ghost_cord = (row - 5,col - int((self.GRIDWIDTH-map_len)/2))
                    path = breadth_search(self.maze,ghost_cord, (ghost_cord[0],ghost_cord[1]-1))
                    Clyde(self,col,row,path)
                
    def path_draw(self,path):
        map_len = len(self.map_data[0])
        for node in path:
            pg.draw.circle(self.screen,RED,((node[1] + int((self.GRIDWIDTH-map_len)/2)) * self.tilesize + 8,(node[0] + 5) * self.tilesize + 8 ),1)
    
    def run(self):
        #print
        # game loop - set self.playing = False to end the game
        # print(self.life_counter)
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(self.FPS) / 1000
            now = pg.time.get_ticks()
            if now - self.last_update > 1000:
                self.last_update = now
                self.seconds += 1
                if self.player.keys != -1:
                    self.session_time += 1
                if self.seconds >= 60:
                    self.seconds = 0
                    self.minutes += 1
            
            if  now - self.last_scatter_update > 10000 :
                print("Scatter mode state before update:", self.scatter_mode)
                self.last_scatter_update = now
                self.scatter_mode = not self.scatter_mode
                print("Scatter mode activation")
                print("Scatter mode state:", self.scatter_mode)
            
                
            if now - self.pellet_activation > 4000 and  self.is_pellet == True:
                self.is_pellet = False
                self.p_ch_index = 0
            
           
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        # self.all_sprites.update()
       
        self.coins.update()
        self.pellets.update()
        self.walls.update()
        self.ghosts.update()
        self.player_group.update()
        
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
        self.draw_text("Timer :", self.tilesize, WHITE, self.GRIDWIDTH // 2 * self.tilesize, 3 * self.tilesize)
        self.draw_text(minutes +":" + seconds, self.tilesize, WHITE, (self.GRIDWIDTH // 2 + 3) * self.tilesize, 3 * self.tilesize)
        self.draw_text("Score :", self.tilesize, WHITE, (self.GRIDWIDTH - len(self.map_data[0])) // 2 * self.tilesize, 3 * self.tilesize)
        self.draw_text(str(self.score), self.tilesize, WHITE, ((self.GRIDWIDTH - len(self.map_data[0])) // 2 + 5) * self.tilesize, 3 * self.tilesize)
        self.draw_text("Lifes :", self.tilesize, WHITE, ((self.GRIDWIDTH - len(self.map_data[0])) // 2 ) * self.tilesize, ((self.GRIDHEIGHT - len(self.map_data) + 4)) * self.tilesize)
        
    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # pg.display.set_caption("{:.2f}".format(self.session_time))
        self.screen.fill(BGCOLOR)
        # self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.drawing_of_changable()

        # self.path_draw(self.ghost.path)
        
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

    # def wait_for_key(self):
    #     waiting = True
    #     while waiting:
    #         self.clock.tick(self.FPS)
    #         # for event in pg.event.get():
    #             # self.menu.react(event)
    #             # print(self.slider.get_value())
    #             # self.tilesize = int(self.slider.get_value())
    #         for event in pg.event.get():
    #             if event.type == pg.QUIT:
    #                 waiting = False
    #                 self.running = False
    #             if event.type == pg.KEYUP:
    #                 waiting = False

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
        if self.speed != PLAYER_SPEED:
            self.FPS = 100

        # pg.display.flip()
        # self.wait_for_key()

    def show_go_screen(self):
        pass



# create the game object
g = Game()
# g.show_start_screen()
while True:
    if g.life_counter == -1:
        break
    
    g.new()
    g.run()
g.show_go_screen()


