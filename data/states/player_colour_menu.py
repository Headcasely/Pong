import pygame as pg
from .. import prep, tools, menu_manager, button, settings


class PlayerColourMenu(tools.State, menu_manager.MenuManager):
    def __init__(self, player):
        tools.State.__init__(self)
        menu_manager.MenuManager.__init__(self)
        self.player = player
        
        self.title_text, self.title_rect = self.make_title(f'{self.player}', (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.5))
        self.title_text2, self.title_rect2 = self.make_title('Colour', (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.5 + 150))
        self.title_text_ls, self.title_rect_ls = self.make_title(f'{self.player} Colour', (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.3))
        
        self.next = 'colour_player_select'
        self.options = ['back']
        self.next_list = ['colour_player_select']
        self.pre_render_options()
        self.from_bottom = 367
        
        self.btn_settings = {
            'weight' : 25,
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
        
        self.buttons = button.create_colour_button_grid(prep.SCREEN_W // 3 - 150, prep.SCREEN_H // 2 - 200 , 200, 200, 3, 3, 25, self.colour_list, **self.btn_settings) #grid w, h = 675, 675
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
        if self.orientation == 'portrait':
            screen.blit(self.title_text, self.title_rect)
            screen.blit(self.title_text2, self.title_rect2)
        else:
            screen.blit(self.title_text_ls, self.title_rect_ls)
        self.draw_menu(screen)
        for btn in self.buttons:
            btn.draw(screen)
    
    def draw_menu(self, screen):
        for i,opt in enumerate(self.rendered["des"]):
            opt[1].center = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.h - self.from_bottom + i * self.spacer)
            if i == self.selected_index:
                rend_img, rend_rect = self.rendered['sel'][i]
                rend_rect.center = opt[1].center
                screen.blit(rend_img, rend_rect)
            else:
                screen.blit(opt[0], opt[1])
         
    def return_button_colour(self, btn_id):
        return btn.fill_colour
        
    def update_object_pos(self):
        if self.orientation == 'landscape':
            self.title_rect_ls.center = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.3)
            # Update colour buttons
            btn_size = self.buttons[0].rect.w
            spacer = 20
            x = prep.SCREEN_W // 3 
            y = prep.SCREEN_H // 2 - 250
            id = 0
            for row in range(3):
                for col in range(3):
                    btn_x = x + col * (btn_size + spacer)
                    btn_y = y + row * (btn_size + spacer)
                    self.buttons[id].rect.topleft = (btn_x, btn_y)
                    id +=1
            # Update back button
            self.from_bottom = 90
            for i,opt in enumerate(self.rendered["des"]):
                opt[1].center = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery - self.from_bottom + i * self.spacer)
            
        else:
            self.title_rect.center = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.5)
            self.title_rect2.center = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.5 + 150)
            # Update colour buttons
            btn_size = self.buttons[0].rect.w
            spacer = 20
            x = prep.SCREEN_W // 3 - 150
            y = prep.SCREEN_H // 2 - 200
            id = 0
            for row in range(3):
                for col in range(3):
                    btn_x = x + col * (btn_size + spacer)
                    btn_y = y + row * (btn_size + spacer)
                    self.buttons[id].rect.topleft = (btn_x, btn_y)
                    id +=1
            # Update back button
            self.from_bottom = 367
            for i,opt in enumerate(self.rendered["des"]):
                opt[1].center = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery - self.from_bottom + i * self.spacer)
