import pygame as pg


class Button:
    def __init__(self, rect, id=None, msg=None, **kwargs):
        self.id = id
        self.msg = msg
        self.rect = pg.Rect(rect)
        self.surface = pg.Surface(self.rect.size)
        
        self.process_kwargs(kwargs)
        self.render_text(self.msg)
        self.render_surface()
        self.clicked = False
        self.hovered = False
        
    def process_kwargs(self, kwargs):
        settings = {
            'func' : None,
            'font' : pg.font.Font(None, 50),
            'text_colour' : 'white',
            'fill' : True,
            'fill_colour' : None,
            'border' : True,
            'border_colour' : 'white',
            'weight' : 10,
            'padding' : 30,
            'clickable': True,
            'call_on_release' : False
        }
        
        for kwarg in kwargs:
            if kwarg in settings:
                settings[kwarg] = kwargs[kwarg]
            else:
                raise AttributeError(f'{self.__class__.__name__} has no keyword: {kwarg}')
        self.__dict__.update(settings)
        
    def render_text(self, msg):
        if self.msg and self.text_colour:
            self.text = self.font.render(msg, 1, self.text_colour)
            self.text_rect = self.text.get_rect(center = self.rect.center)
            
    def render_surface(self):
        if self.msg:
            self.surface = pg.Surface((self.text.get_width() + self.padding, self.text.get_height() + self.padding)).convert()
            self.rect = self.surface.get_rect(center = self.text_rect.center)
    
    def get_event_button(self, event):
        if self.clickable:
            if event.type == pg.MOUSEBUTTONDOWN:
                self.on_click(event)
            if event.type == pg.MOUSEBUTTONUP:
                self.on_release(event)
            
    def draw(self, screen):
        # Fill
        if self.fill and self.fill_colour:
            pg.draw.rect(self.surface, self.fill_colour, (0,0,self.rect.w, self.rect.h), 0)
        # Border
        if self.border and self.border_colour and self.weight:
            pg.draw.rect(self.surface, self.border_colour, (0,0, self.rect.w, self.rect.h), self.weight)
        # Draw rect and/or border
        screen.blit(self.surface, self.rect)
        # Text
        if self.msg:
            screen.blit(self.text, self.text_rect)
            
    def check_hover(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            if not self.hovered:
                self.hovered = True
        else:
            self.hovered = False
            
    def update(self):
        self.check_hover()
        self.render_text(self.msg)
        self.render_surface()

    def on_click(self, event):
        if self.rect.collidepoint(event.pos):
            self.clicked = True
            if self.func != None:
                self.func()
                
    def on_release(self, event):
        if self.clicked and self.call_on_release:
            if self.rect.collidepoint(event.pos):
                if self.func != None:
                    self.func()
        self.clicked = False


def create_colour_button_grid(x, y, w, h, rows=1, cols=2, spacer=10, colour_list=None, **btn_settings):
    btns = []
    if colour_list is None:
        colour_list = [(0, 0, 0) for row in range(rows) for col in range(cols)]
    for row in range(rows):
        for col in range(cols):
            btn_x = x + col * (w + spacer)
            btn_y = y + row * (h + spacer)
            btn_id = row * cols + col
            colour = colour_list[btn_id]
            btns.append(Button((btn_x, btn_y, w, h), btn_id, fill_colour=colour, **btn_settings))
    return btns
 
   
def create_text_button_grid(x, y, rows,cols, text_list, w=0, h=0, spacer=10, **btn_settings):
    btns = []
    for row in range(rows):
        for col in range(cols):
            btn_x = x + col * (w + spacer)
            btn_y = y + row * (h + spacer)
            btn_id = row * cols + col
            text = text_list[btn_id]
            btns.append(Button((btn_x, btn_y, 0, 0), btn_id, **btn_settings, msg=text))
    return btns
        