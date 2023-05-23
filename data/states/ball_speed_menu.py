import pygame as pg

from .. import prep, tools, menu_manager, settings, button


class BallSpeedMenu(tools.State, menu_manager.MenuManager):
    def __init__(self):
        tools.State.__init__(self)
        menu_manager.MenuManager.__init__(self)
        
        self.title_text, self.title_rect = self.make_title('Ball Speed', (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.5))
        self.options = ['back']
        self.speed_options = ['slow', 'normal', 'fast', 'insane']
        self.speeds = [750, 1000, 1250, 1500]
        self.next = 'gameplay'
        self.next_list =['gameplay']
        self.from_bottom = 100
        self.spacer = 150
        
        self.btn_settings = {
            'func' : None,
            'font' : prep.MENU_FONT_D,
            'text_colour' : 'white',
            'fill' : False,
            'fill_colour' : None,
            'border' : False,
            'border_colour' : None,
            'weight' : 10,
            'padding' : 30,
            'clickable': True,
            'call_on_release' : False
        }
        self.buttons = button.create_text_button_grid(prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery - self.from_bottom, 4, 1, self.speed_options, spacer=150, **self.btn_settings)
        self.selected_button = 1
        self.pre_render_options()
    
    def startup(self):
        pass
    
    def cleanup(self):
        self.selected_index = None
        
    def get_event(self, event):
        self.get_event_menu(event)
        for btn in self.buttons:
            btn.get_event_button(event)
            if btn.clicked:
                self.selected_button = btn.id
                settings.set_setting('ball_speed', self.speeds[btn.id])
        
    def update(self, screen, dt):
        self.update_menu()
        self.update_object_pos()
        for btn in self.buttons:
            btn.update()
            if btn.id == self.selected_button:
                btn.border = True 
                btn.border_colour = 'gold'
            else:
                btn.border = False
                btn.border_colour = None
        self.draw(screen)
        
    def draw(self, screen):
        screen.fill(prep.BLACK)
        screen.blit(self.title_text, self.title_rect)
        self.draw_menu(screen)
        for btn in self.buttons:
            btn.draw(screen)
        
    def draw_menu(self, screen):
        #screen.blit(self.title, self.title_rect)
        for i,opt in enumerate(self.rendered["des"]):
            opt[1].center = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery - self.from_bottom + len(self.speed_options) * self.spacer)
            if i == self.selected_index:
                rend_img, rend_rect = self.rendered['sel'][i]
                rend_rect.center = opt[1].center
                screen.blit(rend_img, rend_rect)
            else:
                screen.blit(opt[0], opt[1])
                
    def update_object_pos(self):
        if self.orientation == 'landscape':
            # Update title
            self.title_rect.center = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.3)
            # Update btns
            spacer = 20
            from_bottom = 150
            self.from_bottom = 200
            for i, btn in enumerate(self.buttons):
                btn_x = prep.SCREEN_RECT.centerx
                btn_y = prep.SCREEN_RECT.centery + i * (btn.rect.h + spacer) - from_bottom
                btn.rect.center = (btn_x, btn_y)
                btn.text_rect.center = btn.rect.center
            # Update back btn
            for i,opt in enumerate(self.rendered["des"]):
                opt[1].center = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery - self.from_bottom + len(self.speed_options) * self.spacer)
        # If portrait
        else:
            # Update title
            self.title_rect.center = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.5)
            spacer = 20
            self.from_bottom = 100
            #update btns
            for i, btn in enumerate(self.buttons):
                btn_x = prep.SCREEN_RECT.centerx
                btn_y = prep.SCREEN_RECT.centery + i * (btn.rect.h + spacer) - self.from_bottom
                btn.rect.center = (btn_x, btn_y)
                