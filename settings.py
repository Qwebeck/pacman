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
FONT_NAME = "arial"
# COLORS=[WHITE, BLACK, DARKGREY, LIGHTGREY, GREEN, RED, YELLOW]

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 100
TITLE = "Tilemap Demo"
BGCOLOR = DARKGREY

#player settings
PLAYER_SPEED = 100
ANIMATION_SPEED = 100
PACMAN_IMAGE = ['pacman_top.png', 'animation_pacman_top.png', 'circle.png']

#mob settings
GHOSTS = 5
GHOST_IMAGE = 'red_ghost.png'
BLINKY = 'red_ghost.png'
PINKY='pinky.png'
INKY='inky.png'
CLYDE='clyde.png'
GHOST_SPEED = 100


# GRID_SCALE = (int((self.GRIDWIDTH-map_len)/2),5) #0 -col 1 - row
TILESIZE = 16
WALLS=['hor.png','vert.png','l_end.png','r_end.png','lb_corner.png','rb_corner.png','l_corner.png','r_corner.png']