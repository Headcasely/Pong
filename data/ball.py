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
        self.start_pos = (x, y)
        self.rect = self.image.get_rect(center = self.start_pos)
        self.old_rect = self.rect.copy()
        # Movement
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.dir = pg.math.Vector2(random.choice([-1, 1]), 0)
        self.speed = speed
        # Collision Objects
        self.players = players
        self.p1 = p1
        self.p2 = p2
        pg.draw.circle(self.image, prep.WHITE, (radius, radius), radius)
        
    def collisions(self, players, direction):
        hits = pg.sprite.spritecollide(self, players, False)
        if hits:
            self.play_random_sound()
            for player in hits:
                if direction == 'horizontal':
                    # right
                    if self.rect.right >= player.rect.left and self.old_rect.right <= player.old_rect.left:
                        self.rect.right = player.rect.left
                        self.pos.x = self.rect.x
                        self.bounce_to('left')
                    #left
                    elif self.rect.left <= player.rect.right and self.old_rect.left >= player.old_rect.right:
                        self.rect.left = player.rect.right
                        self.pos.x = self.rect.x
                        self.bounce_to('right')
                elif direction == 'vertical':
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
        if self.rect.y <= 150:
            self.rect.top = 150
            self.play_random_sound()
            self.dir.y *= -1
        elif self.rect.y + self.rect.height >= prep.SCREEN_H:
            self.rect.bottom = prep.SCREEN_H
            self.play_random_sound()
            self.dir.y *= -1
            
    def goal(self):
        #Player 1 scores
        if self.rect.x >= prep.SCREEN_W + prep.BALLSIZE * 2:
            self.p1.add_score()
            self.dir.x *= -1
            self.dir.y = random.randint(-1, 1)
            self.rect.midright = (self.p2.rect.midleft[0] -15, self.p2.rect.midleft[1])
            self.pos = pg.math.Vector2(self.rect.topleft)
            prep.SFX['goal'].play()
            
        # Player 2 scores
        if self.rect.x <= -self.rect.width - prep.BALLSIZE * 2:
            self.p2.add_score()
            self.dir.x *= -1
            self.dir.y = random.randint(-1, 1)
            self.rect.midleft = (self.p1.rect.midright[0] + 15, self.p1.rect.midright[1])
            self.pos = pg.math.Vector2(self.rect.topleft)
            prep.SFX['goal'].play()
            
    def reset_ball(self):
        self.rect.center = self.start_pos
        self.pos = pg.math.Vector2(self.rect.topleft)
        self.dir = pg.math.Vector2(random.choice([-1, 1]), 0)
                    
    def bounce_to(self, direction):
        if direction == 'left':
            self.dir.x = -1
        elif direction == 'right':
            self.dir.x = 1
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
        self.collisions(self.players, 'horizontal')
        self.pos.y += self.dir.y * self.speed * dt
        self.rect.y = round(self.pos.y)
        self.collisions(self.players, 'vertical')
        self.screen_collisions()
        self.goal()
        