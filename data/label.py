import pygame as pg
#from . import prep


class Label:
    def __init__(self, text, pos, **kwargs):
        self.text = text
        self.pos = pos
        self.process_kwargs(kwargs)
        self.render_text(self.text, self.text_colour)
        self.render_box()
     
    def process_kwargs(self, kwargs):
       settings = {
           'font' : pg.font.Font(None, 50),
           'text_colour' : 'white',
           'fill_colour' : None,
           'padding' : 30,
           'border_colour' : None,
           'weight' : 10
       }
       for kwarg in kwargs:
           if kwarg in settings:
               settings[kwarg] = kwargs[kwarg]
           else:
               raise AttributeError(f'{self.__class__.__name__} has no keyword: {kwarg}')
       self.__dict__.update(settings)
       
    def render_text(self, text, colour):
        self.text = self.font.render(text, 1, colour)
        self.text_rect = self.text.get_rect(center = self.pos)
        
    def update(self, text):
        self.text = self.font.render(text, 1, self.text_colour)
        self.text_rect = self.text.get_rect(center = self.pos)
        self.render_box()
    
    def render_box(self):
        if self.text:
            self.box = pg.Surface((self.text.get_width() + self.padding, self.text.get_height() + self.padding)).convert()
            self.box_rect = self.box.get_rect(center = self.text_rect.center)
            
    def draw(self, screen):
        if self.fill_colour:
            pg.draw.rect(self.box, self.fill_colour, (0, 0, self.box_rect.w, self.box_rect.h), 0)
        if self.border_colour and self.weight:
            pg.draw.rect(self.box, self.border_colour, (0, 0, self.box_rect.w, self.box_rect.h), self.weight)
            screen.blit(self.box, self.box_rect)
        if self.text:
            screen.blit(self.text, self.text_rect)

