import pygame as pg
from .. import prep, tools, menu_manager

# implement colour selector for players
# Implement player name inputs

class GameplayMenu(tools.State, menu_manager.MenuManager):
    def __init__(self):
        tools.State.__init__(self)
        menu_manager.MenuManager.__init__(self)
        self.title_text, self.title_rect = self.make_title('Gameplay', (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.5))
        self.next = 'options'
        self.options = ['Player 1 Name', 'Player 2 Name', 'Player 1 Colour', 'Player 2 Colour', 'Ball Speed', 'Back']
        self.next_list = ['options', 'options', 'player_1_colour', 'player_2_colour', 'ball_speed', 'options']
        
        self.from_bottom = 200
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
        #self.draw_titles(screen)
        
    
#                
#    def pre_render_titles(self):
#        deselected_font = prep.MENU_FONT_D
#        rendered_titles = []
#        for title in self.titles:
#            d_font = deselected_font.render(title, 1, prep.WHITE)
#            d_rect = d_font.get_rect()
#            rendered_titles.append((d_font, d_rect))
#        self.rendered_titles = rendered_titles
#                
#    def draw_titles(self, screen):
#        if self.orientation == 'portrait':
#            for i, title in enumerate(self.rendered_titles):
#                title[1].center = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery - self.from_bottom + i * self.spacer)
#                screen.blit(title[0], title[1])
#        else:
#            pass