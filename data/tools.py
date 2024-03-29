import os
import pygame as pg
from . import prep

class State:
    def __init__(self):
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None
        self.orientation = prep.ORIENTATION
        
        
    def cleanup(self):
        pass
        
    def startup(self):
        pass
        
    def get_event(self, event):
        pass
        
    def update(self, screen, dt):
        pass
        
    def draw(self, screen):
        pass
        
    def make_title(self, text, pos):
        title_text = prep.TITLE_FONT.render(text, 1, prep.WHITE)
        title_text_rect = title_text.get_rect(center = pos)
        return (title_text, title_text_rect)
        
#gfx

#sfx
def load_all_sfx(directory):
    sound_effects = {}
    for file in os.listdir(directory):
        name, ext = os.path.splitext(file)
        if ext.lower() in ('.wav'):
            sound_effects[name] = pg.mixer.Sound(os.path.join(directory, file))
    return sound_effects
    
#fonts
class Font:
    path = 'data/resources/fonts'
    @staticmethod
    def load(filename, size=150):
        p = os.path.join(Font.path, filename)
        return pg.font.Font(os.path.abspath(p), size)
        
#other functions
def print_to_file(string):
    with open('debug.txt', 'w', newline='\n') as f:
        f.write(str(string))
        
