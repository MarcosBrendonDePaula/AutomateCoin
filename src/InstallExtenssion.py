import pyautogui

def get_relative_position(x_percent, y_percent):
    screen_width, screen_height = pyautogui.size()
    x_pos = int(screen_width * x_percent / 100)
    y_pos = int(screen_height * y_percent / 100)
    return x_pos, y_pos

def installExtension(link):
    
    pass