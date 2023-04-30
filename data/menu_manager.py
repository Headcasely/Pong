import pygame as pg
from . import prep
from . import control


class MenuManager:
    def __init__(self):
        self.selected_index = None
        self.last_option = None
        self.colour = prep.WHITE
        self.from_bottom = 100
        self.spacer = 150
        
        
    def draw_menu(self, screen):
        #screen.blit(self.title, self.title_rect)
        for i,opt in enumerate(self.rendered["des"]):
            opt[1].center = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery - self.from_bottom + i * self.spacer)
            if i == self.selected_index:
                rend_img, rend_rect = self.rendered['sel'][i]
                rend_rect.center = opt[1].center
                screen.blit(rend_img, rend_rect)
            else:
                screen.blit(opt[0], opt[1])
        
    def get_event_menu(self, event):
        self.mouse_click_menu(event)
        
    def update_menu(self):
        self.update_object_pos()
        
    def pre_render_options(self):
        deselected_font = prep.MENU_FONT_D
        selected_font = prep.MENU_FONT_S
        rendered_txt = {'des' : [], 'sel' : []}
        for option in self.options:
            d_font = deselected_font.render(option, 1, prep.WHITE).convert_alpha()
            d_rect = d_font.get_rect()
            s_font = selected_font.render(option, 1, prep.WHITE).convert_alpha()
            s_rect = s_font.get_rect()
            rendered_txt['des'].append((d_font, d_rect))
            rendered_txt['sel'].append((s_font, s_rect))
        self.rendered = rendered_txt
        
    def mouse_click_menu(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            for i, opt in enumerate(self.rendered['des']):
                if opt[1].collidepoint(pg.mouse.get_pos()):
                    self.selected_index = i
        if event.type == pg.MOUSEBUTTONUP and self.selected_index != None:
            for i, opt in enumerate(self.rendered['des']):
                if opt[1].collidepoint(pg.mouse.get_pos()):
                    self.select_option(self.selected_index)
                    prep.SFX['pongG5'].play()
                    
    def select_option(self, i):
        if self.selected_index == len(self.next_list):
            self.quit = True
        elif self.next_list[i] in control.app.state_dict:
            self.next = self.next_list[i]
            self.done = True
            self.selected_index = 0
        else:
            self.selected_index = i
    
    def update_object_pos(self):
        if self.orientation == 'landscape':
            self.title_rect.center = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.3)
        else:
            self.title_rect.center = (prep.SCREEN_RECT.centerx, prep.SCREEN_RECT.centery * 0.5)
           