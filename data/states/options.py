from .. import prep
from .. import tools
from .. import menu_manager


class Options(tools.State, menu_manager.MenuManager):
    def __init__(self):
        tools.State.__init__(self)
        menu_manager.MenuManager.__init__(self)
        self.title_text, self.title_rect = self.make_title('Options', (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.5))
        self.next = 'game'
        self.options = ['Gameplay', 'Audio', 'Back']
        self.next_list = ['gameplay', 'audio', 'menu']
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
        