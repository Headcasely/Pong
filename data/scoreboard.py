import pygame as pg
from . import prep


class Scoreboard:
    def __init__(self, p1, p2):
        self.font = prep.SCORE_FONT
        self.p1 = p1
        self.p2 = p2
        self.render_scores(p1, p2)
        
    def render_scores(self, p1, p2):
        self.score_1_text = self.font.render(str(p1.score), 1, prep.WHITE)
        self.score_1_rect = self.score_1_text.get_rect(center =(prep.SCREEN_W * 0.25, 60))
        self.score_2_text = self.font.render(str(p2.score), 1, prep.WHITE)
        self.score_2_rect = self.score_2_text.get_rect(center = (prep.SCREEN_W * 0.75, 60))
    
    def draw(self, screen):
        screen.blit(self.score_1_text, self.score_1_rect)
        screen.blit(self.score_2_text, self.score_2_rect)
        
    def update(self, screen):
        self.score_1_text = self.font.render(str(self.p1.score), 1, prep.WHITE)
        self.score_2_text = self.font.render(str(self.p2.score), 1, prep.WHITE)
        self.draw(screen)
        