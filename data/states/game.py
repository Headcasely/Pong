import pygame as pg
from .. import prep, tools, settings
from .. import player, ball, scoreboard, pitch, countdown, label
from ..tools import print_to_file as ptf

class Game(tools.State):
    def __init__(self):
        super().__init__()
        self.game_over = False
        self.next = 'menu'
        self.winner = None
        self.score_limit = 3
        self.game_settings = settings.load_settings()
        self.top_boundary = 75
        
        # Sprite groups
        self.players = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        
        # Player sprites
        self.p1 = player.Player(0 + 200, prep.SCREEN_H//2 + self.top_boundary, self.game_settings['player_1_name'], self.game_settings['Player 1 colour'])
        self.p2 = player.Player(prep.SCREEN_W - 200, prep.SCREEN_H//2 + self.top_boundary, self.game_settings['player_2_name'], self.game_settings['Player 2 colour'])
        self.players.add(self.p1, self.p2)
        
            # Ball sprite
        self.ball = ball.Ball(prep.SCREEN_W // 2, prep.SCREEN_H // 2 + self.top_boundary, prep.BALLSIZE, self.game_settings['ball_speed'], self.p1, self.p2, self.players)
        
        # Other objects
        self.scoreboard = scoreboard.Scoreboard(self.p1, self.p2)
        self.pitch = pitch.Pitch()
        self.game_over_label = label.Label(None, (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery + self.top_boundary), font=prep.MENU_FONT_S, fill_colour=prep.BLACK, border_colour=prep.WHITE)
        self.countdown = countdown.Countdown(prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery + self.top_boundary)
        
        self.all_sprites.add(self.p1, self.p2, self.ball)
        
        
    def get_event(self, event):
        if not self.game_over:
            for player in self.players:
                player.get_event_player(event)
                
        else:
            if event.type == pg.MOUSEBUTTONDOWN:
                self.done = True
        
    def update(self, screen, dt):
        if not self.game_over:
            self.draw(screen)
            self.countdown.update(screen, dt)
            if self.countdown.is_done:
                self.scoreboard.update(screen)
                self.all_sprites.update(screen, dt)
                self.check_end_game(self.players)
        else:
            screen.fill(prep.BLACK)
            self.pitch.draw(screen)
            self.scoreboard.update(screen)
            self.players.draw(screen)
            self.game_over_label.update(f'{self.winner} wins!')
            self.game_over_label.draw(screen)
        
    def draw(self, screen):
        screen.fill(prep.BLACK)
        self.pitch.draw(screen)
        self.scoreboard.draw(screen)
        self.all_sprites.draw(screen)
        
    def check_end_game(self, players):
        for player in players:
            if player.score >= self.score_limit:
                self.winner = player.name
                self.game_over = True
                
    def reset_players(self, players):
        for player in players:
            player.reset_pos()
            ptf(f'PLAYER POS RESET: {player.rect.center}, {player.pos} ')
            player.reset_score()
            
    def startup(self):
        self.ball.reset_ball()
        self.countdown.delay = 1
        self.countdown.is_done = False
        self.countdown.start_countdown = True
        self.game_settings = settings.load_settings()
        self.p1.name = self.game_settings['player_1_name']
        self.p2.name = self.game_settings['player_2_name']
        self.p1.colour = self.game_settings['Player 1 colour']
        self.p2.colour = self.game_settings['Player 2 colour']
        for player in self.players:
            player.update_colour()
            player.rect.center = player.start_pos
        self.ball.speed = self.game_settings['ball_speed']
        
    def cleanup(self):
        self.countdown.count = 3
        self.reset_players(self.players)
        self.scoreboard.update(prep.SCREEN)
        self.game_over = False
        
    def update_object_pos(self):
        if self.orientation == 'landscape':
            # Update score positions
            self.scoreboard.score_1_rect.center = (prep.SCREEN_W * 0.25, 60)
            self.scoreboard.score_2_rect.center = (prep.SCREEN_W * 0.75, 60)
            # Reinitialise pitch
            del self.pitch
            self.pitch = pitch.Pitch()
            old_screen_h = 2033
            old_screen_w = 1080
            new_screen_h = 1080
            new_screen_w = 2033
            tb = round(self.top_boundary *(new_screen_h / old_screen_h))
            # Update p1 pos 
            x = 200
            y = self.p1.rect.centery
            relative_y = y / old_screen_h
            new_y = relative_y * new_screen_h
            self.p1.rect.center = (x, round(new_y))
            self.p1.pos = pg.math.Vector2(self.p1.rect.center)
            self.p1.start_pos = (200, prep.SCREEN_H // 2 + tb)
            
            # Update p2 pos
            x = prep.SCREEN_W - 200
            y = self.p2.rect.centery
            relative_y = y / old_screen_h
            new_y = relative_y * new_screen_h
            self.p2.rect.center = (x, round(new_y))
            self.p2.pos = pg.math.Vector2(self.p2.rect.center)
            self.p2.start_pos = (prep.SCREEN_W - 200, prep.SCREEN_H // 2 + tb)
            # Update ball pos
            x = self.ball.rect.centerx
            y = self.ball.rect.centery
            relative_x = x / old_screen_w
            relative_y = y / old_screen_h
            new_x = relative_x * new_screen_w
            new_y = relative_y * new_screen_h 
            self.ball.rect.center = (round(new_x), round(new_y))
            self.ball.pos = pg.math.Vector2(self.ball.rect.center)
            self.ball.start_pos = (prep.SCREEN_W // 2, prep.SCREEN_H // 2 + tb)
            # Update game over label
            self.game_over_label.pos = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery + tb)
            # Update countdown pos
            self.countdown.rect.center = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery + tb)
            #self.countdown.text_rect.center = (self.countdown.rect.centerx, self.countdown.rect.centery - 10)
            if self.countdown.count == 1:
                self.countdown.text_rect.centerx += 37
            else:
                self.countdown.text_rect.center = (self.countdown.rect.centerx, self.countdown.rect.centery - 10)
                
            if self.countdown.count == 0:
                self.countdown.count = self.countdown.start_msg
                self.countdown.text_rect.centerx = self.countdown.rect.centerx - 70
            tools.prints_to_file(f'{self.p1.name} start pos: {self.p1.start_pos}', f'{self.p1.name} center: {self.p1.rect.center}')
            tools.prints_to_file(f'{self.p2.name} start pos: {self.p2.start_pos}', f'{self.p2.name} center: {self.p2.rect.center}')
            tools.print_to_file(f'countdown rect center: {self.countdown.rect.center}')
            
        else:
            # Update score positions
            self.scoreboard.score_1_rect.center = (prep.SCREEN_W * 0.25, 60)
            self.scoreboard.score_2_rect.center = (prep.SCREEN_W * 0.75, 60)
            # Reinitialise pitch
            # pitch h p = 2033 - 160 = 2033
            #pitch h ls = 1080 - 160 = 1080
            del self.pitch
            self.pitch = pitch.Pitch()
            old_screen_h = 1080
            old_screen_w = 2033
            new_screen_h = 2033
            new_screen_w = 1080
            # Update p1 pos 
            x = 200
            y = self.p1.rect.centery
            relative_y = y / old_screen_h
            new_y = relative_y * new_screen_h
            self.p1.rect.center = (x, round(new_y))
            self.p1.pos = pg.math.Vector2(self.p1.rect.center)
            self.p1.start_pos = (200, prep.SCREEN_H // 2 + self.top_boundary)
            # Update p2 pos
            x = prep.SCREEN_W - 200
            y = self.p2.rect.centery
            relative_y = y / old_screen_h
            new_y = relative_y * new_screen_h
            self.p2.rect.center = (x, round(new_y))
            self.p2.pos = pg.math.Vector2(self.p2.rect.center)
            self.p2.start_pos = (prep.SCREEN_W - 200, prep.SCREEN_H // 2 + self.top_boundary)
            # Update ball pos
            x = self.ball.rect.centerx
            y = self.ball.rect.centery
            relative_x = x / old_screen_w
            relative_y = y / old_screen_h
            new_x = relative_x * new_screen_w
            new_y = relative_y * new_screen_h 
            self.ball.rect.center = (round(new_x), round(new_y))
            self.ball.pos = pg.math.Vector2(self.ball.rect.center)
            self.ball.start_pos = (prep.SCREEN_W // 2, prep.SCREEN_H // 2 + self.top_boundary)
            # Update game over label
            self.game_over_label.pos = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery + self.top_boundary)
            # Update countdown pos
            self.countdown.rect.center = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery + self.top_boundary)
            #self.countdown.text_rect.center = (self.countdown.rect.centerx, self.countdown.rect.centery - 10)
            if self.countdown.count == 1:
                self.countdown.text_rect.centerx += 37
            else:
                self.countdown.text_rect.center = (self.countdown.rect.centerx, self.countdown.rect.centery - 10)
                
            if self.countdown.count == 0:
                self.countdown.count = self.countdown.start_msg
                self.countdown.text_rect.centerx = self.countdown.rect.centerx - 70
            tools.prints_to_file(f'{self.p1.name} start pos: {self.p1.start_pos}', f'{self.p1.name} center: {self.p1.rect.center}')
            tools.prints_to_file(f'{self.p2.name} start pos: {self.p2.start_pos}', f'{self.p2.name} center: {self.p2.rect.center}')
            tools.print_to_file(f'countdown rect center: {self.countdown.rect.center}')
            