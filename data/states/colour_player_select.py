from .. import prep, tools, menu_manager


class ColourPlayerSelect(tools.State, menu_manager.MenuManager):
    def __init__(self):
        tools.State.__init__(self)
        menu_manager.MenuManager.__init__(self)
        self.title_text, self.title_rect = self.make_title('Player', (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.5))
        self.title_text2, self.title_rect2 = self.make_title('Colours', (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.5 + 150))
        self.title_text_ls, self.title_rect_ls = self.make_title(f'Player Colours', (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.3))
        self.next = 'gameplay'
        self.options = ['Player 1', 'Player 2', 'Back']
        self.next_list = ['player_1_colour', 'player_2_colour', 'gameplay']
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
        if self.orientation == 'portrait':
            screen.blit(self.title_text, self.title_rect)
            screen.blit(self.title_text2, self.title_rect2)
        else:
            screen.blit(self.title_text_ls, self.title_rect_ls)
        self.draw_menu(screen)
        
    def update_object_pos(self):
        if self.orientation == 'landscape':
            # Update title
            self.title_rect_ls.center = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.3)
        else:
            self.title_rect.center = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.5)
            self.title_rect2.center = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.5 + 150)
        