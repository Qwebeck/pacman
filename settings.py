WHITE = (255, 255, 255)
WHITE_OP_Q = (255, 255, 255, 0.2)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
DARKGREY_OP_Q = (40, 40, 40, 0.2)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (26, 94, 204)
FONT_NAME = "crackman.ttf"
PACMAN_LIFES = "PacFont.ttf"
FONTSIZE = 20
# COLORS=[WHITE, BLACK, DARKGREY, LIGHTGREY, GREEN, RED, YELLOW]

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 70
TITLE = "Pacman game"
# BGCOLOR = DARKGREY
BGCOLOR = BLACK
#should grow with growth of pixels per second 
IGNORE_SPACE = 4


#player settings
PLAYER_SPEED = 80
#animation settings
ANIMATION_SPEED = 40
PACMAN_IMAGE = ['pacman_top.png', 'animation_pacman_top.png', 'circle.png']
DEATH = ['dying_1.png','dying_2.png','dying_3.png','dying_4.png','dying_5.png','dying_6.png','dying_7.png','dying_8.png','dying_9.png','dying_10.png','dying_11.png',]
FRUITS = ['cherry.png','red_apple.png','strawberry.png','orange_apple.png','green_apple.png']
BOB_RANGE = 5
BOB_SPEED = 0.3
#mob settings
GHOSTS = 5
GHOST_IMAGE = 'red_ghost.png'
BLINKY = 'red_ghost.png'
PINKY='pinky.png'
INKY='inky.png'
CLYDE='clyde.png'
GHOST_SPEED = 60





# GRID_SCALE = (int((self.GRIDWIDTH-map_len)/2),5) #0 -col 1 - row
TILESIZE = 16
WALLS=['hor.png','vert.png','l_end.png','r_end.png','lb_corner.png','rb_corner.png','l_corner.png','r_corner.png','door.png','v_wall.png','v_wall_t_end.png']