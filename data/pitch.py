import pygame as pg
from . import prep

class Pitch():
    def __init__(self):
        self.surface = pg.Surface((prep.SCREEN_W, prep.SCREEN_H))
        self.rect = self.surface.get_rect(topleft = (0, 0))
        pg.draw.line(self.surface,  prep.WHITE, (prep.SCREEN_W / 2, 0), (prep.SCREEN_W / 2, prep.SCREEN_H), 10)
        pg.draw.line(self.surface, prep.WHITE, (0, 150), (prep.SCREEN_W, 150), 10)
        
    def draw(self, screen):
        screen.blit(self.surface, self.rect)