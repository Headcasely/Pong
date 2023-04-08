import os
import pygame as pg
from . import tools, settings

pg.mixer.pre_init(44100, -16, 1, 512)
pg.init()

def resizable_window():
        DW = 0
        DH = 0
        DS = pg.display.set_mode((DW, DH), pg.FULLSCREEN | pg.RESIZABLE)
        DW, DH = DS.get_size()
        return DS
        
def get_screen_orientation():
    if SCREEN_W < SCREEN_H:
        return 'portrait'
    else:
        return 'landscape'

SCREEN = resizable_window()
SCREEN_RECT = SCREEN.get_rect()
SCREEN_W, SCREEN_H = SCREEN.get_size()
ORIENTATION = get_screen_orientation()

FPS = 60 

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Entity Constants
BALLSIZE = 25
PLAYER_SIZE = (100, 200)

# SFX
SFX = tools.load_all_sfx(os.path.join('data', 'resources', 'sfx'))
SFX['pongG5'].set_volume(0.1)
SFX['pongD5'].set_volume(0.1)
SFX['pongB4'].set_volume(0.1)
SFX['pongG4'].set_volume(0.1)
SFX['goal'].set_volume(0.1)

# Fonts
SPLASH_FONT = tools.Font.load('upheavtt.ttf', 250)
TITLE_FONT = tools.Font.load('upheavtt.ttf', 175)
MENU_FONT_D = tools.Font.load('upheavtt.ttf', 100)
MENU_FONT_S = tools.Font.load('upheavtt.ttf', 125)
SCORE_FONT = tools.Font.load('upheavtt.ttf', 150)