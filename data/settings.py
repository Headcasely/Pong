'''Default settings used in game state and functions to change and return values.
'''

DEFAULT_SETTINGS = {
    'FPS' : 60,
    'player_1_name' : 'Player 1',
    'player_2_name' : 'Player 2',
    'Player 1 colour' : (255, 255, 255),
    'Player 2 colour' : (255, 255, 255),
    'ball_speed' : 1000
}

def get_setting(kwarg):
    return user_settings.get(kwarg)
    
def set_setting(kwarg, value):
    user_settings[kwarg] = value
    
def load_settings():
    return user_settings

user_settings = DEFAULT_SETTINGS.copy()
