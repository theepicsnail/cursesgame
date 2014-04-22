import math
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
        self.row = 15
        self.col = 15

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

class Water(Item):
    character = '~'
    color = color(curses.COLOR_BLUE)
    passable = False

class Bridge(Item):
    character = '='
    color = color(curses.COLOR_YELLOW)

def run():
    window = curses.newwin(0,0,0,0)
    window.keypad(1)
    window.addstr(0,0,"Press escape to quit")
    window.addstr(1,0,"Use arrow keys to move")
    window.addstr(3,0,"Press any key to start")
    ch = window.getch()
    world_height = 100
    world_width = 100
    left = 10
    top = 10
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
    world[(20,15)] = Floor() # Poke a hole for a door

    for row in xrange(0,world_height):
        for col in xrange(int(math.sin(row/5.0)*3+50), int(math.sin(row/7.0)*4 + 60)):
            world[(row,col)] = Water()

    for col in xrange(50,58):
        world[(36, col)] = Bridge()
        world[(37, col)] = Bridge()
        world[(72, col)] = Bridge()
        world[(73, col)] = Bridge()

    while ch != 27:
        window.erase()
        top = max(0, player.row - min(world_height, height)/2)
        left = max(0, player.col - min(world_width, width)/2)
        #draw the screen
        for row in xrange(top, top+height):
            if row >= world_height:
                break
            for col in xrange(left, left+width):
                if col >= world_width:
                    break
                try:
                    if (row,col) in world:
                        char = world[(row,col)].character
                        attr = world[(row,col)].color
                    else:
                        char = 'w'
                        attr = color(curses.COLOR_GREEN)

                    window.addch(row-top, col-left, char, attr)
                except:pass
        window.addch(player.row-top, player.col-left, '@', color(curses.COLOR_YELLOW) | curses.A_BOLD)
        window.addstr(0,0, " ".join(map(str, [ch, player.row, player.col])))

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
            next_loc[0] >= world_height or\
            next_loc[1] >= world_width:
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
