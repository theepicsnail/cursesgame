import curses, curses.wrapper
curses.initscr()
curses.start_color()
pairs = []
def color(fg=curses.COLOR_WHITE, bg=curses.COLOR_BLACK):
    key = (fg, bg)
    pid = len(pairs)+1

    if key in pairs:
        return curses.color_pair(pairs.index(key)+1)

    curses.init_pair(pid, fg, bg)
    pairs.append(key)
    return curses.color_pair(pid)

class Player:
    def __init__(self):
        self.row = 5
        self.col = 5

class Item(object):
    character = ' '
    color = color()
    passable = True

class Brick(Item):
    character = '#'
    color = color(curses.COLOR_RED)
    passable = False

class Floor(Item):
    character = ' '
    color = color()

def run():
    window = curses.newwin(0,0,0,0)
    window.keypad(1)
    window.addstr(0,0,"Press escape to quit")
    window.addstr(1,0,"Use arrow keys to move")
    window.addstr(3,0,"Press any key to start")
    ch = window.getch()

    left = 0
    top = 0
    height, width = window.getmaxyx()
    player = Player()
    world = {} # Map of (row, col) to item

    #build a 'house'
    for i in xrange(10,20):
        for j in xrange(11,20):
            world[(i,j)] = Floor()
        world[(i,10)] = Brick()
        world[(i,20)] = Brick()
        world[(10,i)] = Brick()
        world[(20,i)] = Brick()
    world[(10,15)] = Floor() # Poke a hole for a door

    while ch != 27:
        #draw the screen
        for col in xrange(left, left+width):
            for row in xrange(top, top+height):
                try:
                    if (row,col) in world:
                        char = world[(row,col)].character
                        attr = world[(row,col)].color
                    else:
                        char = 'w'
                        attr = color(curses.COLOR_GREEN)

                    window.addch(row, col, char, attr)
                except:pass
        window.addch(player.row, player.col, '@', color(curses.COLOR_YELLOW) | curses.A_BOLD)
        window.addstr(0,0, str(ch)+" ")

        #handle input
        ch = window.getch()
        next_loc = [player.row, player.col]
        if ch == 258: # Down
            next_loc[0] += 1
        elif ch == 259: # Up
            next_loc[0] -= 1
        elif ch == 260: # left
            next_loc[1] -= 1
        elif ch ==261: # right
            next_loc[1] += 1
        next_loc = tuple(next_loc)

        # collision detection
        # out of bounds
        if next_loc[0] < 0 or\
            next_loc[1] < 0 or\
            next_loc[0] >= height or\
            next_loc[1] >= width:
            continue
        if next_loc in world:
            if not world[next_loc].passable:
                continue
        player.row = next_loc[0]
        player.col = next_loc[1]

def main(screen):
    try:
        run()
    finally:
        curses.nocbreak()
        curses.echo()
        curses.endwin()

curses.wrapper(main)
