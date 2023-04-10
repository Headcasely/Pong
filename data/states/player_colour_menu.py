import pygame as pg
from .. import prep, tools, menu_manager, button, settings


class PlayerColourMenu(tools.State, menu_manager.MenuManager):
    def __init__(self, player):
        tools.State.__init__(self)
        menu_manager.MenuManager.__init__(self)
        self.player = player
        self.from_bottom = 140
        self.spacer = 75
        self.title_text, self.title_rect = self.make_title(f'{self.player}', (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.5))
        self.title_text2, self.title_rect2 = self.make_title('Colour', (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.5 + self.spacer))
        self.next = 'gameplay'
        self.options = ['back']
        self.next_list = ['gameplay']
        self.pre_render_options()
        
        
        self.btn_size = [100, 100]
        self.btn_settings = {
            'weight' : 10,
            'border_colour' : 'white'
        }
        
        self.colour_list = [
            (255, 255, 255), # white
            (255, 0, 0), # red
            (0, 255, 0), # green
            (0, 0, 255), # blue
            (255, 255, 0), # yellow
            (255, 0, 255), # magenta
            (0, 255, 255), # cyan
            (255, 165, 0), # orange
            (125, 0, 125) # purple
        ]
        
        self.buttons = button.create_colour_button_grid(prep.SCREEN_W // 3 - self.btn_size[0]//2 - 25, prep.SCREEN_H // 2 - self.btn_size[1] , self.btn_size[0], self.btn_size[1], 3, 3, 25, self.colour_list, **self.btn_settings)
        self.selected_btn = 0
    
    def cleanup(self):
        self.selected_index = None
    
    def get_event(self, event):
        self.get_event_menu(event)
        for btn in self.buttons:
            btn.get_event_button(event)
            if btn.clicked:
                self.selected_btn = btn.id
                settings.set_setting(f'{self.player} colour', btn.fill_colour)
        
    def update(self, screen, dt):
        self.update_menu()
        for btn in self.buttons:
            btn.update()
            if btn.id == self.selected_btn:
                btn.border_colour = 'gold'
            else:
                btn.border_colour = None
        self.draw(screen)
        
    def draw(self, screen):
        screen.fill(prep.BLACK)
        screen.blit(self.title_text, self.title_rect)
        screen.blit(self.title_text2, self.title_rect2)
        self.draw_menu(screen)
        for btn in self.buttons:
            btn.draw(screen)
    
    def draw_menu(self, screen):
        #screen.blit(self.title, self.title_rect)
        for i,opt in enumerate(self.rendered["des"]):
            opt[1].center = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.h - self.from_bottom + i * self.spacer)
            if i == self.selected_index:
                rend_img, rend_rect = self.rendered['sel'][i]
                rend_rect.center = opt[1].center
                screen.blit(rend_img, rend_rect)
            else:
                screen.blit(opt[0], opt[1])
         
    def return_button_colour(self,btn):
        return btn.fill_colour
        
    def select_colour(self):
        pass