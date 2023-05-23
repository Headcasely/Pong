import pygame as pg
from . import prep, tools


class Player(pg.sprite.Sprite):
    def __init__(self, x, y, name, colour):
        super().__init__()
        self.name = name
        self.colour = colour
        self.score = 0
        # Image
        self.image = pg.Surface(prep.PLAYER_SIZE)
        self.image.fill(self.colour)
        # Position
        self.start_pos = (x, y)
        self.rect = self.image.get_rect(center = self.start_pos)
        self.old_rect = self.rect.copy()
        # Movement
        self.drag = False
        self.finger = None
        self.pos = pg.math.Vector2(self.rect.center)
        
    def get_event_player(self, event):
        self.old_rect = self.rect.copy()
        if event.type == pg.FINGERDOWN:
            x = int(event.x * prep.SCREEN.get_width())
            y = int(event.y * prep.SCREEN.get_height())
            if self.rect.collidepoint(x, y):
                self.finger = event.finger_id
                self.drag = True
                self.fx, self.fy = x, y
                self.offx = self.rect.x - self.fx
                self.offy = self.rect.y - self.fy
                    
        if event.type == pg.FINGERMOTION:
            x = int(event.x * prep.SCREEN.get_width())
            y = int(event.y * prep.SCREEN.get_height())
            if self.drag and self.finger == event.finger_id:
                self.fx, self.fy = x, y
                self.rect.y = self.fy + self.offy
                if self.rect.y <= 160:
                    self.rect.y = 160
                elif self.rect.y + self.rect.height >= prep.SCREEN_H:
                    self.rect.y = prep.SCREEN_H - self.rect.height
                
        if event.type == pg.FINGERUP:
            if self.finger == event.finger_id:
                self.drag = False
                    
    def update(self, screen, dt):
        if self.rect.y <= 160:
            self.rect.y = 160
        elif self.rect.y + self.rect.height >= prep.SCREEN_H:
            self.rect.y = prep.SCREEN_H - self.rect.height
        self.draw(screen)
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    def add_score(self):
        self.score += 1
        
    def reset_score(self):
        self.score = 0
        
    def reset_pos(self):
        self.rect.center = self.start_pos
        self.pos = pg.math.Vector2(self.rect.center)
        self.old_rect = self.rect.copy()
        
    def update_colour(self):
        self.image.fill(self.colour)
        