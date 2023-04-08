import pygame as pg

from . import prep, tools

        
class Countdown:
    def __init__(self):
        self.surface = pg.Surface((300,200))
        self.surf_rect = self.surface.get_rect(center = prep.SCREEN_RECT.center)
        self.is_done = False
        self.start_countdown = True
        self.count = 3
        self.start_msg = 'go!' 
        self.delay = 1 #seconds
        self.font = prep.TITLE_FONT
        self.text = self.font.render(str(self.count), 1, 'white')
        self.text_rect = self.text.get_rect(center = (self.surf_rect.centerx, self.surf_rect.centery - 10))
        
    def draw(self, screen):
        pg.draw.rect(self.surface, 'black', (0, 0, 300, 200), 0)
        pg.draw.rect(self.surface, 'white', (0, 0, 300, 200), 20)
        screen.blit(self.surface, self.surf_rect)
        screen.blit(self.text, self.text_rect)
        
    def update(self, screen, dt):
        if self.start_countdown:
            self.text = self.font.render(str(self.count), 1, 'white')
            self.draw(screen)
            self.delay -= dt
            if self.delay <= 0:
                if self.count == self.start_msg:
                    self.is_done = True
                    self.start_countdown = False
                else:
                    self.count -= 1
                self.delay = 1
                
                if self.count == 1:
                    self.text_rect.centerx += 37
                else:
                    self.text_rect.center = (self.surf_rect.centerx, self.surf_rect.centery - 10)
                
                if self.count == 0:
                    self.count = self.start_msg
                    self.text_rect.centerx = self.surf_rect.centerx - 70
                