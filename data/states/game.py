import pygame as pg
from .. import prep, tools, settings
from .. import player, ball, scoreboard, pitch, countdown, label

class Game(tools.State):
    def __init__(self):
        super().__init__()
        self.game_over = False
        self.next = 'menu'
        self.winner = None
        self.game_settings = settings.load_settings()
        
        # Sprite groups
        self.players = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        
        # Player sprites
        self.p1 = player.Player(0 + prep.PLAYER_SIZE[0]*2, prep.SCREEN_H/2, self.game_settings['player_1_name'], self.game_settings['Player 1 colour'])
        self.p2 = player.Player(prep.SCREEN_W - prep.PLAYER_SIZE[0]*2, prep.SCREEN_H/2, self.game_settings['player_2_name'], self.game_settings['Player 2 colour'])
        self.players.add(self.p1, self.p2)
        
            # Ball sprite
        self.ball = ball.Ball(prep.SCREEN_W / 2, prep.SCREEN_H / 2, prep.BALLSIZE, self.game_settings['ball_speed'], self.p1, self.p2, self.players)
        
        # Other objects
        self.scoreboard = scoreboard.Scoreboard(self.p1, self.p2)
        self.pitch = pitch.Pitch()
        self.game_over_label = label.Label(None, prep.SCREEN_RECT.center, font=prep.MENU_FONT_S, fill_colour=prep.BLACK, border_colour=prep.WHITE)
        self.countdown = countdown.Countdown()
        
        self.all_sprites.add(self.ball, self.p1, self.p2)
        
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
            if player.score >= 5:
                self.winner = player.name
                self.game_over = True
                
    def reset_players(self, players):
        for player in players:
            player.reset_pos()
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
        self.ball.speed = self.game_settings['ball_speed']
        
    def cleanup(self):
        self.countdown.count = 3
        self.reset_players(self.players)
        self.scoreboard.update(prep.SCREEN)
        self.game_over = False
                
    