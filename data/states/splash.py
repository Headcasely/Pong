import pygame as pg
from .. import prep
from .. import tools


class Splash(tools.State):
    def __init__(self):
        super().__init__()
        self.next = 'menu'
        self.time_active = 0
        self.delay = 5
        self.text = prep.SPLASH_FONT.render('PONG', 1, prep.WHITE)
        self.text_rect = self.text.get_rect(center = prep.SCREEN_RECT.center)
        
    def timer(self, dt):
        self.time_active += dt
        if self.time_active >= self.delay:
            self.done = True
        
    def update(self, screen, dt):
        self.draw(screen)
        self.timer(dt)
        
    def draw(self, screen):
        screen.blit(self.text, self.text_rect)
        
    def update_object_pos(self):
        self.text_rect.center = prep.SCREEN_RECT.center
        