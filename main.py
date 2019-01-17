import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
import thorpy as th
from brs_agent import *
import pytmx
import random

random.seed()

#self.player.keys

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.speed=PLAYER_SPEED
        self.tilesize = TILESIZE
        self.GRIDWIDTH = WIDTH / self.tilesize
        self.GRIDHEIGHT = HEIGHT / self.tilesize
        self.ghosts = GHOSTS # ghost number on map
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.high_scores = []
        
        self.score = 0
        self.minutes = 0
        self.seconds = 0
        self.session_time = 0
        self.font_name = pg.font.match_font(FONT_NAME)
        self.running = True
        self.login = LOGIN
        #timer variable
        self.last_update = 0
        self.last_scatter_update = 0
        self.ghost_speed = GHOST_SPEED
        self.life_counter = 3
        self.is_pellet = False
        self.pellet_activation = 0
        self.p_ch_index = 0
        self.scatter_mode = True   
        self.level = 1
        self.fruit = 0
        self.game_over = False
        self.free_nodes = []
        self.picked = 0 # check for fruits 
        self.scatter_frequency = 20000
        self.ghost_counter = 0
        self.unlucky_pellet = random.randint(1,3)
        self.picked_pellets_number = 0
        self.hell_mode = False
        self.load_data()
        

    def load_data(self):
        self.volume = 0.1
        self.game_folder = path.dirname(__file__)
        self.img_folder = path.join(self.game_folder, 'images')
        self.dead_anim = path.join(self.img_folder, 'dead_an')
        self.fruit_folder = path.join(self.img_folder, 'fruits')
        self.sound_folder = path.join(self.game_folder,'sounds')

        # print("Image folder in main:",self.img_folder)
        self.player_img = pg.image.load(path.join(self.img_folder, PACMAN_IMAGE[2])).convert_alpha()
        self.blinky_img = pg.image.load(path.join(self.img_folder, BLINKY[0])).convert_alpha()
        self.pinky_img = pg.image.load(path.join(self.img_folder, PINKY[0])).convert_alpha()
        self.inky_img = pg.image.load(path.join(self.img_folder, INKY[0])).convert_alpha()
        self.clyde_img = pg.image.load(path.join(self.img_folder, CLYDE[0])).convert_alpha()
        self.eat_coin = pg.mixer.Sound(path.join(self.sound_folder,'pacman_chomp.wav'))
        self.intro = pg.mixer.Sound(path.join(self.sound_folder,'pacman_beginning.wav'))
        self.death_sound = pg.mixer.Sound(path.join(self.sound_folder,'pacman_death.wav'))
        self.eat_fruit_sound = pg.mixer.Sound(path.join(self.sound_folder,'pacman_eatfruit.wav'))
        self.eat_ghost = pg.mixer.Sound(path.join(self.sound_folder,'pacman_eatghost.wav'))  
        pg.mixer.music.load(path.join(self.sound_folder,'Airport-lounge-music-for-airports.mp3'))  
        pg.mixer.music.set_volume(0.05)
        self.intro.set_volume(self.volume) 
        self.eat_coin.set_volume(self.volume)
        self.intro.set_volume(self.volume)
        self.death_sound.set_volume(self.volume)
        self.eat_fruit_sound.set_volume(self.volume)
        self.eat_ghost.set_volume(self.volume)
        self.current_sound = self.intro     
        self.running = False
        self.FPS = FPS
        self.map_data = []
        self.high_scores = []
        # print(self.high_scores)
        with open(path.join(self.game_folder, 'main_map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
        with open(path.join(self.game_folder, 'high_scores.txt'), 'r') as file:
            for line in file:
                # print(line)
                try: 
                    self.high_scores.append(int(line[:-1]))
                except:
                    pass
        # print("high_Scores ",self.high_scores)
        self.high_scores.sort(reverse = True)
        maze = []
        self.player_cords = maze_transform(maze,self.map_data)
        self.maze = maze
       
      
    # initialize all variables and do all the setup for a new game
    def new(self):
        self.load_data()
        self.session_time = 0
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.ghosts = pg.sprite.Group()
        self.player_group = pg.sprite.Group()
        self.pellets = pg.sprite.Group()
        self.fruits= pg.sprite.Group()
        self.data_for_inky = 0
        self.scatter_mode = False
        self.game_over = False
        self.fruit = 0
        self.pellet_index = 0
        if self.life_counter == 3:
            self.intro.play()
        
        
        # for life in range(self.life_counter):
        #         x = ((self.GRIDWIDTH - len(self.map_data[0])) // 2 + 5 + life + 0.10*life)  
        #         y = ((len(self.map_data)) + 6) 
        #         Stats(self,x,y,'pacman_right.png')
        x = ((self.GRIDWIDTH - len(self.map_data[0]) //2 - 5))  
        y = ((len(self.map_data)) + 6) 
        Stats(self,x,y,FRUITS[(self.level - 1) % len(FRUITS)],self.fruit_folder)
            
        # for row in self.maze:
        #     print(row)
        # self.walls_on_map = []
        map_len = len(self.map_data[0])
        for y in range(len(self.maze)):
            for x in range (len(self.maze[0])):
                col = x + int((self.GRIDWIDTH-map_len)/2)
                row = y + 5
                if self.maze[y][x] == 1:
                    #without params can be a beatiful space mode 
                    # self.walls_on_map.append((col * self.tilesize,row * self.tilesize,self.tilesize,self.tilesize))
                    Wall(self, col, row,WALLS[0])
                elif self.maze[y][x] == 0:
                    if (col,row) not in self.free_nodes:
                        Coins(self,col,row)
                elif self.maze[y][x] == 3:
                    Pellets(self,col,row)
                elif self.maze[y][x] == 'H':
                    self.ghost_house = (row - 5,col - int((self.GRIDWIDTH-map_len)/2))
                    self.ghost_house_area = ghost_house_area(self.maze,self.ghost_house)
             
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
                elif self.maze[y][x] == 'D':
                    Wall(self, col, row,WALLS[8])
                elif self.maze[y][x] == 'M':
                    Wall(self, col, row,WALLS[3])
                elif self.maze[y][x] == 'U':
                    Wall(self, col, row,WALLS[9])
                elif self.maze[y][x] == 'R':
                    Wall(self, col, row,WALLS[10])
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
            self.corner_set = [(1,1),(len(self.maze[0]) - 1, 1), (1,len(self.maze) - 1),(len(self.maze[0]) - 1, len(self.maze) - 1)]
                
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
            if bool(self.coins) == False and self.session_time > 0:
                self.free_nodes = []
                self.playing  = False
                self.level += 1
                self.score += 100
                self.ghost_speed += 1
                self.scatter_frequency += 100
            
            if  now - self.last_scatter_update > self.scatter_frequency :
                # print("Scatter mode state before update:", self.scatter_mode)
                self.last_scatter_update = now
                self.scatter_frequency += 1000 
                self.scatter_mode = not self.scatter_mode
                # print("Scatter mode activation")
                # print("Scatter mode state:", self.scatter_mode)
            # print(self.free_nodes)
            if self.score % 1000 > 900 and self.fruit == 0:
                # print("Fruit appear")
                try:
                    fruit_position = random.choice(self.free_nodes)
                    Fruit(self,fruit_position[0],fruit_position[1],(self.level - 1) % len(FRUITS))
                    self.fruit = 1
                except:
                    pass
            if now - self.pellet_activation > 6000 and  self.is_pellet == True:
                self.is_pellet = False
                self.ghost_counter = 0
                self.p_ch_index = 0
                # if self.hell_mode == True:
                #     self.hell_mode = False
            
            # if self.is_pellet == True and self.picked_pellets_number == self.unlucky_pellet:
            #     self.hell_mode == True
            
            if not self.game_over:
                self.events()
            try :
                self.update()
            except (KeyError,TypeError):
                pass
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop   
       
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
        print("Hell mode pellet",self.unlucky_pellet)
        print("Hell mode state",self.hell_mode)
        print("Picked pellets ", self.picked_pellets_number)
        if self.minutes < 10:
            minutes = "0" + str(self.minutes)
        else:
            minutes = str(self.minutes)
        if self.seconds < 10:
            seconds = "0" + str(self.seconds)
        else:
            seconds = str(self.seconds)
        self.draw_text("Timer :", FONTSIZE, YELLOW,( self.GRIDWIDTH // 2   + 5 )* self.tilesize , 3 * self.tilesize, FONT_NAME)
        self.draw_text(minutes +":" + seconds, FONTSIZE, YELLOW, (self.GRIDWIDTH // 2 + 10) * self.tilesize, 3 * self.tilesize, FONT_NAME)
        self.draw_text("Level :", FONTSIZE, YELLOW, (self.GRIDWIDTH - len(self.map_data[0]) + 17) // 2 * self.tilesize , 3 * self.tilesize, FONT_NAME)
        self.draw_text(str(self.level), FONTSIZE, YELLOW, (self.GRIDWIDTH - len(self.map_data[0]) + 28) // 2 * self.tilesize, 3 * self.tilesize, FONT_NAME)
        self.draw_text("Score :", FONTSIZE, YELLOW, (self.GRIDWIDTH - len(self.map_data[0])) // 2 * self.tilesize, 3 * self.tilesize, FONT_NAME)
        self.draw_text(str(self.score), FONTSIZE, YELLOW, ((self.GRIDWIDTH - len(self.map_data[0])) // 2 + 5) * self.tilesize, 3 * self.tilesize, FONT_NAME)
        self.draw_text("Lifes :", FONTSIZE, YELLOW, ((self.GRIDWIDTH - len(self.map_data[0])) // 2 ) * self.tilesize, ((len(self.map_data)) + 6)  * self.tilesize, FONT_NAME)
        self.draw_text("1" * self.life_counter, FONTSIZE, YELLOW, ((self.GRIDWIDTH - len(self.map_data[0])) // 2  + 5) * self.tilesize, ((len(self.map_data)) + 6)  * self.tilesize, PACMAN_LIFES)
        self.draw_text("High score:", 32 , YELLOW, WIDTH - 15 * self.tilesize , 5 * self.tilesize, FONT_NAME)
        if self.score < self.high_scores[0]:
             self.draw_text(str(self.high_scores[0]), 32 , YELLOW, WIDTH - 15 * self.tilesize , 7 * self.tilesize, FONT_NAME)
        else:
             self.draw_text(str(self.score), 32 , YELLOW, WIDTH - 15 * self.tilesize , 7 * self.tilesize, FONT_NAME)

        if self.picked_pellets_number == self.unlucky_pellet:
            self.draw_text("Sorry ,you picked a wrong pellet ", FONTSIZE , YELLOW, ((self.GRIDWIDTH - len(self.map_data[0])) // 2 ) * self.tilesize, ((len(self.map_data)) + 10)  * self.tilesize, FONT_NAME)
            self.draw_text("Now Bilnky is faster and invisiable", FONTSIZE , YELLOW, ((self.GRIDWIDTH - len(self.map_data[0])) // 2 ) * self.tilesize, ((len(self.map_data)) + 15)  * self.tilesize, FONT_NAME)
            self.draw_text("Pick up next pellet to stop it ", FONTSIZE , YELLOW, ((self.GRIDWIDTH - len(self.map_data[0])) // 2 ) * self.tilesize, ((len(self.map_data)) + 20)  * self.tilesize, FONT_NAME)
        # for i in range (5):
        #     # sprint(self.high_scores)
        #     try :
        #         if i >= len(self.high_scores):
        #             break
        #         self.draw_text(str(i + 1) + '.' +  str(self.high_scores[i]), 32 , YELLOW, WIDTH - 15 * self.tilesize , ((i + 1) * 2 + 5) * self.tilesize, FONT_NAME)
        #     except TypeError:
        #         pass

        if self.player.picked_power != 0 and self.session_time - self.player.picked_power_time < 3:
            # print("Called picked item function ")
            self.draw_text("+" + str(self.player.picked_power),int(self.tilesize * 1.5) ,YELLOW,self.player.picked_power_pos[0] * self.tilesize + self.tilesize / 4 ,self.player.picked_power_pos[1] * self.tilesize + self.tilesize/4,FONT_NAME)
        elif self.session_time - self.player.picked_power_time > 3:
            self.player.picked_power = 0
    
    def draw(self):
        # pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # pg.display.set_caption("{:.2f}".format(self.session_time))
        self.screen.fill(BGCOLOR)
        # self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.drawing_of_changable()
        if self.picked == 1:
                x = ((self.GRIDWIDTH - len(self.map_data[0]) //2 - 5))  
                y = ((len(self.map_data)) + 6) 
                pg.draw.rect(self.screen,BLACK,(x,y,self.tilesize,self.tilesize))

        # self.path_draw(self.ghost_house_area)
        
        pg.display.flip()

    def events(self):
        # catch all events here
      
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN and self.game_over == False:
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
            
    def draw_text(self, text, size, color, x, y, font):
        # if not number:
        font = pg.font.Font(font, size)
        # else :
        #     font = pg.font.Font(self.font_name, size * 2)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        self.screen.blit(text_surface, text_rect)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(self.FPS)
            # for event in pg.event.get():
                # self.menu.react(event)
                # print(self.slider.get_value())
                # self.tilesize = int(self.slider.get_value())
            for event in pg.event.get():
                if event.type == pg.QUIT :
                    waiting = False
                    self.quit()
                    
                if event.type == pg.KEYUP:
                    waiting = False

    def show_start_screen(self):
        application = th.Application(size=(WIDTH, HEIGHT), caption="Hello pacman")
        pg.mixer.music.play(loops = - 1)
        e_title = th.make_text("Pacman", font_size=40, font_color=YELLOW )
        e_title.set_font(path.join(self.game_folder,FONT_NAME))
        # inserter = th.Inserter.make(name="Inserter: ", value=" ")
        # e_title.center()
        e_title.set_topleft((10, 10))
        play_button = th.make_button("Play", func=th.functions.quit_menu_func)
    
        varset = th.VarSet()
        # varset.add("tilesize", value=TILESIZE, text="Size of objects:", limits=(10, 16))
        # varset.add("speed", value=PLAYER_SPEED, text="Speed:", limits=(10, 100))
        varset.add("ghost_speed", value=GHOST_SPEED, text="Ghosts speed:", limits=(10, 100))
        varset.add("scatter_freq", value=self.scatter_frequency // 1000, text="Scatter mode frequency:", limits=(0, 30))
        # varset.add("volume", value=self.volume * 100, text="Volume:", limits=(0, 100))
        # varset.add("login",value = LOGIN, text ="Login :")
        e_options = th.ParamSetterLauncher.make([varset], "Options", "Options")
        quit_button = th.make_button("Quit",func=th.functions.quit_func)
        elements = [ e_title , play_button, e_options, quit_button]
        e_background = th.Background.make(color=BLACK, elements=elements , image=path.join(self.img_folder,("bg.jpg")))
        th.store(e_background, elements)
        th.store(e_background)
        menu = th.Menu(e_background)  # create a menu on top of the background
        
       
        menu.play()  # launch the menu
        
        
        pg.display.flip()
        # self.tilesize = varset.get_value("tilesize")
        # self.speed = varset.get_value("speed")
        self.GRIDWIDTH = WIDTH / self.tilesize
        self.GRIDHEIGHT = HEIGHT / self.tilesize
        
        self.ghost_speed = varset.get_value("ghost_speed")
        
        # if self.volume != (varset.get_value("volume")/100):
        #     print(self.volume)
        #     print(varset.get_value("volume")/100)
        #     self.volume = (varset.get_value("volume")/100)
        #     print(self.volume)
        #     print(varset.get_value("volume")/100)
        # self.intro.set_volume(self.volume) 
        # self.eat_coin.set_volume(self.volume)
        # self.intro.set_volume(self.volume)
        # self.death_sound.set_volume(self.volume)
        # self.eat_fruit_sound.set_volume(self.volume)
        # self.eat_ghost.set_volume(self.volume)
        self.scatter_frequency = varset.get_value("scatter_freq") * 1000
        
        # if self.tilesize < TILESIZE:
        #     self.speed = 60 / self.tilesize * 10
        #     self.ghost_speed =  60 / self.tilesize * 10 - 10  
        
        # self.login = varset.get_value("login")
        # pg.display.flip()
        # self.wait_for_key()

    def show_go_screen(self):
        file = open("high_scores.txt","a")
        file.write(str(self.score))
        file.write('\n')
        file.close()

        self.screen.fill(BLACK)
        self.draw_text("Your score is :" + str(self.score),30,YELLOW, self.tilesize, 10 * self.tilesize,FONT_NAME)
        if len(self.high_scores) == 0:
           self.draw_text("You set new record :" + str(self.score),30,YELLOW, 5 * self.tilesize, 15 * self.tilesize,FONT_NAME)
        elif int(self.score) - int(self.high_scores[0]) > 0:
           self.draw_text("You set new record.",30,YELLOW, 5 * self.tilesize, 15 * self.tilesize,FONT_NAME)
           self.draw_text("Also it is better than previous on :" + str(int(self.score) - int(self.high_scores[0])) + " points",30,YELLOW, 10 * self.tilesize, 20 * self.tilesize,FONT_NAME)
        else:
            self.draw_text("You was close.To be the best you nedd only " + str(int(self.high_scores[0]) - int(self.score)) + " points.",30,YELLOW, 5 * self.tilesize, 15 * self.tilesize,FONT_NAME)
            self.draw_text("Keep trying",30,YELLOW, 5 * self.tilesize, 20 * self.tilesize,FONT_NAME)     
        self.draw_text("Press any button to return to the menu  ",30,YELLOW, 15 * self.tilesize, 25 * self.tilesize,FONT_NAME)
        pg.display.flip()
        self.free_nodes = []
        self.wait_for_key()
        self.show_start_screen()
        self.score = 0



# create the game object
g = Game()
g.show_start_screen()
while True:
    if g.life_counter == -1:
        g.load_data()
        g.new()
        g.show_go_screen()
        # break
    
    g.new()
    g.run()
g.show_go_screen()


