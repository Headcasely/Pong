import sys, os

import pygame  as pg

from . import prep, tools, settings
#from .states import *
from .states import splash, mainmenu, options, game, gameplay_menu, player_colour_menu, ball_speed_menu

class Control:
    def  __init__(self, **settings):
        self.__dict__.update(settings)
        self.done = False
        self.window = prep.SCREEN
        self.screen = prep.SCREEN.copy()
        self.clock = pg.time.Clock()
        tools.prints_to_file(f'window size: {self.window.get_size()}', f'screen size: {self.screen.get_size()}')
        
    def setup_states(self, state_dict, state_name):
        self.state_dict = state_dict
        self.state_name = state_name
        self.state = self.state_dict[self.state_name]
        
    def flip_state(self):
        self.state.done = False
        previous, self.state_name = self.state_name, self.state.next
        self.state.cleanup()
        try:
            self.state = self.state_dict[self.state_name]
        except KeyError:
            self.state_name = previous
        self.state.startup()
        self.state.previous = previous
        
    def update(self, screen, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(screen, dt)
        
    
    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
                
            if event.type == pg.VIDEORESIZE:
                tools.print_to_file('RESIZE EVENT')
                # Update screen
                prep.SCREEN_W, prep.SCREEN_H = event.w, event.h
                prep.SCREEN = pg.display.set_mode((0, 0), pg.FULLSCREEN)
                self.window = prep.SCREEN
                self.screen = self.window.copy()
                prep.SCREEN_RECT = prep.SCREEN.get_rect()
                # Update object positions
                for state in self.state_dict.values():
                    state.orientation = prep.get_screen_orientation()
                    state.update_object_pos()
                tools.print_to_file(f'NEW ORIENTATION: {self.state.orientation}')
                tools.print_to_file('OBJECTS UPDATED')
            self.state.get_event(event)
            
            
    def main_loop(self):
        while not self.done:
            delta_time = self.clock.tick(self.FPS) / 1000
            self.event_loop()
            self.update(self.screen, delta_time)
            self.window.blit(self.screen, (0,0))
            try:
                pg.display.update()
            except Exception as e:
                tools.print_to_file(f'{e}'.upper())


game_settings = settings.user_settings
state_dict = {
        'splash' : splash.Splash(),
        'menu' : mainmenu.MainMenu(),
        'options' : options.Options(),
        #'audio' : audi.Audio(),
        'gameplay' : gameplay_menu.GameplayMenu(),
        'game' : game.Game(),
        'player_1_colour' : player_colour_menu.PlayerColourMenu('Player 1'),
        'player_2_colour' : player_colour_menu.PlayerColourMenu('Player 2'),
        'ball_speed' : ball_speed_menu.BallSpeedMenu()
}
app = Control(**game_settings)
app.setup_states(state_dict, 'splash')
tools.print_to_file('STARTING GAME LOOP')
app.main_loop()
tools.print_to_file('EXITING GAME LOOP')
pg.quit()
sys.exit()
