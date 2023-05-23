import pygame as pg
from .. import prep, tools, menu_manager


class MainMenu(tools.State, menu_manager.MenuManager):
    def __init__(self):
        tools.State.__init__(self)
        menu_manager.MenuManager.__init__(self)
        self.title_text, self.title_rect = self.make_title('Main Menu', (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.5))
        self.next = 'game'
        self.options = ['Play', 'Options', 'Quit']
        self.next_list = ['game', 'options']
        self.pre_render_options()
        
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
        