import pygame as pg

from .. import prep, tools, menu_manager, settings, button


class ScoreMenu(tools.State, menu_manager.MenuManager):
    def __init__(self):
        tools.State.__init__(self)
        menu_manager.MenuManager.__init__(self)
        
        self.title_text, self.title_rect = self.make_title('Score', (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.5))
        self.title_text2, self.title_rect2 = self.make_title('Limit', (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.5 + 150))
        self.title_text_ls, self.title_rect_ls = self.make_title('Score Limit', (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.3))
        self.options = ['back']
        self.score_options = ['3', '5', '7', '9']
        self.score_limit = [3, 5, 7, 9]
        self.next = 'gameplay'
        self.next_list =['gameplay']
        self.from_bottom = 100
        self.spacer = 150
        
        self.btn_settings = {
            'func' : None,
            'font' : prep.SCORE_FONT,
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
        self.buttons = button.create_text_button_grid(prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery - self.from_bottom, 1, 4, self.score_options, spacer=150, **self.btn_settings)
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
                settings.set_setting('score_limit', self.score_limit[btn.id])
        
    def update(self, screen, dt):
        self.update_menu()
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
        if self.orientation == 'landscape':
            screen.blit(self.title_text_ls, self.title_rect_ls)
        else:
            screen.blit(self.title_text, self.title_rect)
            screen.blit(self.title_text2, self.title_rect2)
        self.draw_menu(screen)
        for btn in self.buttons:
            btn.draw(screen)
        
    def draw_menu(self, screen):
        for i,opt in enumerate(self.rendered["des"]):
            opt[1].center = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery - self.from_bottom + len(self.score_options) * self.spacer)
            if i == self.selected_index:
                rend_img, rend_rect = self.rendered['sel'][i]
                rend_rect.center = opt[1].center
                screen.blit(rend_img, rend_rect)
            else:
                screen.blit(opt[0], opt[1])
                
    def update_object_pos(self):
        if self.orientation == 'landscape':
            # Update title
            self.title_rect_ls.center = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.3)
            # Update btns
            spacer = 50
            from_bottom = 150
            self.from_bottom = 200
            total_w = len(self.buttons) * (self.buttons[0].rect.w + spacer)
            for i, btn in enumerate(self.buttons):
                btn_x = prep.SCREEN_RECT.centerx - (total_w//2)+ i * (btn.rect.w + spacer)
                # For vertical btn list
                #btn_y = prep.SCREEN_RECT.centery + i * (btn.rect.h + spacer) - from_bottom
                # For horizontal btn list
                btn_y = prep.SCREEN_RECT.centery + (btn.rect.h + spacer) - self.from_bottom
                btn.rect.left, btn.rect.centery = btn_x, btn_y
                btn.text_rect.center = btn.rect.center
            # Update back btn
            for i,opt in enumerate(self.rendered["des"]):
                opt[1].center = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery - self.from_bottom + len(self.score_options) * self.spacer)
        # If portrait
        else:
            # Update title
            self.title_rect.center = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.5)
            self.title_rect2.center = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.5 + 150)
            spacer = 50
            self.from_bottom = 100
            #update btns
            for i, btn in enumerate(self.buttons):
                btn_x = prep.SCREEN_RECT.centerx // (len(self.buttons)/2) + i * (btn.rect.w + spacer)
                #btn_y = prep.SCREEN_RECT.centery + i * (btn.rect.h + spacer) - self.from_bottom
                btn_y = prep.SCREEN_RECT.centery + (btn.rect.h + spacer) - self.from_bottom
                btn.rect.center = (btn_x, btn_y)
                