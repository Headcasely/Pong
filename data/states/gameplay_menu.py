import pygame as pg
from .. import prep, tools, menu_manager

# Implement player name inputs

class GameplayMenu(tools.State, menu_manager.MenuManager):
    def __init__(self):
        tools.State.__init__(self)
        menu_manager.MenuManager.__init__(self)
        self.title_text, self.title_rect = self.make_title('Gameplay', (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.5))
        self.next = 'options'
        self.options = ['Player 1 Name', 'Player 2 Name', 'Player 1 Colour', 'Player 2 Colour', 'Ball Speed', 'Back']
        self.next_list = ['options', 'options', 'player_1_colour', 'player_2_colour', 'ball_speed', 'options']
        
        self.from_bottom = 100
        self.pre_render_options()
        #self.pre_render_titles()
        
    def cleanup(self):
        self.selected_index = None
        
    def startup(self):
        pass
        
    def get_event(self, event):
        self.get_event_menu(event)
        
        
    def update(self, screen, dt):
        self.update_menu()
        self.draw(screen)
        
    def draw(self, screen):
        screen.fill(prep.BLACK)
        screen.blit(self.title_text, self.title_rect)
        self.draw_menu(screen)
        
    def update_object_pos(self):
        if self.orientation == 'landscape':
            self.title_rect.center = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.3)
            self.from_bottom = 200
            self.spacer = 130
            for i,opt in enumerate(self.rendered["des"]):
                opt[1].center = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery - self.from_bottom + i * self.spacer)
        else:
            self.title_rect.center = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.5)
            self.from_bottom = 100
            self.spacer = 150
            
        