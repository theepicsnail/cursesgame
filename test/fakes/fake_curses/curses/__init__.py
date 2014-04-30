COLOR_WHITE = "white"
COLOR_BLACK = "black"
COLOR_RED = "red"
COLOR_BLUE = "blue"
COLOR_YELLOW = "yellow"
COLOR_CYAN = "cyan"
COLOR_GREEN = "green"

class __Attribute:
    def __init__(self, val):
        self.val = val
    def __ror__(self,other):
        return other + (self.val,)

A_BOLD = __Attribute('B')
A_REVERSE = __Attribute('R')

def initscr():
    pass
def start_color():
    pass
def curs_set(cursor):
    pass


__color_pairs = {0:(COLOR_WHITE, COLOR_BLACK)}
def color_pair(n):
    return __color_pairs[n]
def init_pair(n, fg, bg):
    __color_pairs[n] = (fg,bg)

def wrapper(func):
    pass
