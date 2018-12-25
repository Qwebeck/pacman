import pygame

from thorpy.miscgui import constants

# default pygame black arrow
arrow = (
    (16,
     16),
    (0,
     0),
    (0x00,
     0x00,
     0x40,
     0x00,
     0x60,
     0x00,
     0x70,
     0x00,
     0x78,
     0x00,
     0x7C,
     0x00,
     0x7E,
     0x00,
     0x7F,
     0x00,
     0x7F,
     0x80,
     0x7C,
     0x00,
     0x6C,
     0x00,
     0x46,
     0x00,
     0x06,
     0x00,
     0x03,
     0x00,
     0x03,
     0x00,
     0x00,
     0x00),
    (0x40,
     0x00,
     0xE0,
     0x00,
     0xF0,
     0x00,
     0xF8,
     0x00,
     0xFC,
     0x00,
     0xFE,
     0x00,
     0xFF,
     0x00,
     0xFF,
     0x80,
     0xFF,
     0xC0,
     0xFF,
     0x80,
     0xFE,
     0x00,
     0xEF,
     0x00,
     0x4F,
     0x00,
     0x07,
     0x80,
     0x07,
     0x80,
     0x03,
     0x00))

diamond = ((16, 16), (7, 7),
           (0, 0, 1, 0, 3, 128, 7, 192, 14, 224, 28, 112, 56, 56, 112, 28, 56,
            56, 28, 112, 14, 224, 7, 192, 3, 128, 1, 0, 0, 0, 0, 0),
           (1, 0, 3, 128, 7, 192, 15, 224, 31, 240, 62, 248, 124, 124, 248, 62,
            124, 124, 62, 248, 31, 240, 15, 224, 7, 192, 3, 128, 1, 0, 0, 0))

ball = ((16, 16), (7, 7),
        (0, 0, 3, 192, 15, 240, 24, 248, 51, 252, 55, 252, 127, 254, 127, 254,
         127, 254, 127, 254, 63, 252, 63, 252, 31, 248, 15, 240, 3, 192, 0, 0),
        (3, 192, 15, 240, 31, 248, 63, 252, 127, 254, 127, 254, 255, 255, 255,
         255, 255, 255, 255, 255, 127, 254, 127, 254, 63, 252, 31, 248, 15, 240,
         3, 192))

broken_x = ((16, 16), (7, 7),
            (0, 0, 96, 6, 112, 14, 56, 28, 28, 56, 12, 48, 0, 0, 0, 0, 0, 0, 0, 0,
             12, 48, 28, 56, 56, 28, 112, 14, 96, 6, 0, 0),
            (224, 7, 240, 15, 248, 31, 124, 62, 62, 124, 30, 120, 14, 112, 0, 0, 0,
             0, 14, 112, 30, 120, 62, 124, 124, 62, 248, 31, 240, 15, 224, 7))


tri_left = (
    (16,
     16),
    (1,
     1),
    (0,
     0,
     96,
     0,
     120,
     0,
     62,
     0,
     63,
     128,
     31,
     224,
     31,
     248,
     15,
     254,
     15,
     254,
     7,
     128,
     7,
     128,
     3,
     128,
     3,
     128,
     1,
     128,
     1,
     128,
     0,
     0),
    (224,
     0,
     248,
     0,
     254,
     0,
     127,
     128,
     127,
     224,
     63,
     248,
     63,
     254,
     31,
     255,
     31,
     255,
     15,
     254,
     15,
     192,
     7,
     192,
     7,
     192,
     3,
     192,
     3,
     192,
     1,
     128))

tri_right = (
    (16,
     16),
    (14,
     1),
    (0,
     0,
     0,
     6,
     0,
     30,
     0,
     124,
     1,
     252,
     7,
     248,
     31,
     248,
     127,
     240,
     127,
     240,
     1,
     224,
     1,
     224,
     1,
     192,
     1,
     192,
     1,
     128,
     1,
     128,
     0,
     0),
    (0,
     7,
     0,
     31,
     0,
     127,
     1,
     254,
     7,
     254,
     31,
     252,
     127,
     252,
     255,
     248,
     255,
     248,
     127,
     240,
     3,
     240,
     3,
     224,
     3,
     224,
     3,
     192,
     3,
     192,
     1,
     128))

tower = (  # sized 24x24
    "XXXXXXXXXXXXXXXXXXXXXXXX",
    "X                      X",
    "X                      X",
    "X                      X",
    "X                      X",
    "X                      X",
    "X                      X",
    "X                      X",
    "X                      X",
    "X                      X",
    "X                      X",
    "X                      X",
    "X                      X",
    "X                      X",
    "X                      X",
    "X                      X",
    "X                      X",
    "X                      X",
    "X                      X",
    "X                      X",
    "X                      X",
    "X                      X",
    "X                      X",
    "XXXXXXXXXXXXXXXXXXXXXXXX",
)


strings_chablon = (  # sized 24x24
    "XX                      ",
    "XXX                     ",
    "XXXX                    ",
    "XX.XX                   ",
    "XX..XX                  ",
    "XX...XX                 ",
    "XX....XX                ",
    "XX.....XX               ",
    "XX......XX              ",
    "XX.......XX             ",
    "XX........XX            ",
    "XX........XXX           ",
    "XX......XXXXX           ",
    "XX.XXX..XX              ",
    "XXXX XX..XX             ",
    "XX   XX..XX             ",
    "     XX..XX             ",
    "      XX..XX            ",
    "      XX..XX            ",
    "       XXXX             ",
    "       XX               ",
    "                        ",
    "                        ",
    "                        ",
)

strings_sizerX = (  # sized 24x16
    "     X      X           ",
    "    XX      XX          ",
    "   X.X      X.X         ",
    "  X..X      X..X        ",
    " X...XXXXXXXX...X       ",
    "X................X      ",
    " X...XXXXXXXX...X       ",
    "  X..X      X..X        ",
    "   X.X      X.X         ",
    "    XX      XX          ",
    "     X      X           ",
    "                        ",
    "                        ",
    "                        ",
    "                        ",
    "                        ",
)
strings_sizerY = (  # sized 16x24
    "     X          ",
    "    X.X         ",
    "   X...X        ",
    "  X.....X       ",
    " X.......X      ",
    "XXXXX.XXXXX     ",
    "    X.X         ",
    "    X.X         ",
    "    X.X         ",
    "    X.X         ",
    "    X.X         ",
    "    X.X         ",
    "    X.X         ",
    "XXXXX.XXXXX     ",
    " X.......X      ",
    "  X.....X       ",
    "   X...X        ",
    "    X.X         ",
    "     X          ",
    "                ",
    "                ",
    "                ",
    "                ",
    "                ",
)
strings_sizerXY = (  # sized 24x16
    "XXXXXXXX                ",
    "X.....X                 ",
    "X....X                  ",
    "X...X                   ",
    "X..X.X                  ",
    "X.X X.X                 ",
    "XX   X.X    X           ",
    "X     X.X  XX           ",
    "       X.XX.X           ",
    "        X...X           ",
    "        X...X           ",
    "       X....X           ",
    "      X.....X           ",
    "     XXXXXXXX           ",
    "                        ",
    "                        ",
)

strings_txt = (  # sized 8x16
    "ooo ooo ",
    "   o    ",
    "   o    ",
    "   o    ",
    "   o    ",
    "   o    ",
    "   o    ",
    "   o    ",
    "   o    ",
    "   o    ",
    "   o    ",
    "   o    ",
    "   o    ",
    "ooo ooo ",
    "        ",
    "        ",
)


class MouseCursor:
    """Object defining a cursor that can be used in place of the standard mouse
    cursor, through the function mousecursor.change_cursor(cursor).
    """
    def __init__(self, strings, size, hotspot):
        self.strings = strings
        self.size = size
        self.hotspot = hotspot

    def get_cursor(self):
        curs, mask = pygame.cursors.compile(self.strings, 'X', '.', 'o')
        return (self.size, self.hotspot, curs, mask)


text_cursor = MouseCursor(strings_txt, (8, 16), (0, 0)).get_cursor()
tower_cursor = MouseCursor(tower, (24,24), (0,0)).get_cursor()

cursors = {constants.CURSOR_NORMAL: arrow,
           constants.CURSOR_TEXT: text_cursor,
           constants.CURSOR_BROKEN: broken_x,
           constants.CURSOR_BALL: ball}


def change_cursor(cursor):
    if isinstance(cursor, int):
        cursor = cursors[cursor]
    pygame.mouse.set_cursor(*cursor)
