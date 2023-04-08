import random, time
import pygame as pg
from . import prep, tools

class Ball(pg.sprite.Sprite):
    def __init__(self, x, y, radius, speed, p1, p2, players):
        super().__init__()
        # Image
        self.image = pg.Surface((radius * 2, radius * 2))
        self.image.fill(prep.BLACK)
        self.image.set_colorkey(prep.BLACK)
        self.radius = radius
        # Position
        self.rect = self.image.get_rect(center = (x, y))
        self.old_rect = self.rect.copy()
        # Movement
        self.pos = pg.math.Vector2(self.rect.center)
        self.dir = pg.math.Vector2(random.choice([-1, 1]), random.randrange(-1,1))
        self.speed = speed
        # Collision Objects
        self.players = players
        self.p1 = p1
        self.p2 = p2
        pg.draw.circle(self.image, prep.WHITE, (radius, radius), radius)
        
    def collisions(self, players):
        hits = pg.sprite.spritecollide(self, players, False)
        if hits:
            self.play_random_sound()
            for player in hits:
                # right
                if self.rect.right >= player.rect.left and self.old_rect.right <= player.old_rect.left:
                    self.rect.right = player.rect.left
                    self.pos.x = self.rect.x
                    self.bounce()     
                #left
                elif self.rect.left <= player.rect.right and self.old_rect.left >= player.old_rect.right:
                    self.rect.left = player.rect.right
                    self.pos.x = self.rect.x
                    self.bounce()
                #up
                if self.rect.top <= player.rect.bottom and self.old_rect.top >= player.old_rect.bottom:
                    self.rect.top = player.rect.bottom
                    self.pos.y = self.rect.y
                    self.dir.y *= -1
                #down
                elif self.rect.bottom >= player.rect.top and self.old_rect.bottom <= player.old_rect.top:
                    self.rect.bottom = player.rect.top
                    self.pos.y = self.rect.y
                    self.dir.y *= -1
                    
    def screen_collisions(self):
        if self.rect.y <= 170 or self.rect.y + self.rect.height >= prep.SCREEN_H:
            #prep.SFX['pongG5'].play()
            self.play_random_sound()
            self.dir.y *= -1
            
    def goal(self, p1, p2):
        #Player 1 scores
        if self.rect.x >= prep.SCREEN_W + 50:
            p1.add_score()
            self.rect = self.image.get_rect(midright = (self.p2.rect.midleft[0] -10, self.p2.rect.midleft[1]))
            self.pos = pg.math.Vector2(self.rect.midright)
            self.dir.x *= -1
            prep.SFX['goal'].play()
            
        # Player 2 scores
        if self.rect.x <= -self.rect.width - 50:
            p2.add_score()
            self.rect = self.image.get_rect(midleft = (self.p1.rect.midright[0] + 10, self.p1.rect.midright[1]))
            self.pos = pg.math.Vector2(self.rect.midleft)
            self.dir.x *= -1
            prep.SFX['goal'].play()
            
    def reset_ball(self):
        self.rect = self.image.get_rect(center = (prep.SCREEN_W / 2, prep.SCREEN_H / 2))
        self.pos = pg.math.Vector2(self.rect.center)
        self.dir = pg.math.Vector2(random.choice([-1, 1]), random.randrange(-1,1))
                    
    def bounce(self):
        self.dir.x *= -1
        self.dir.y = random.randint(-1, 1)
        
    def play_random_sound(self):
        sfx = list(prep.SFX.keys())
        choices = sfx[:3]
        sound = random.choice(choices)
        prep.SFX[sound].play()
        
    def update(self, screen, dt):
        self.old_rect = self.rect.copy()
        
        if self.dir.magnitude() != 0:
            self.dir = self.dir.normalize()
            
        self.pos.x += self.dir.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.collisions(self.players)
        self.pos.y += self.dir.y * self.speed * dt
        self.rect.y = round(self.pos.y)
        self.collisions(self.players)
        self.screen_collisions()
        self.goal(self.p1, self.p2)