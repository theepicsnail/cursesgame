import curses
import math
from player import Player
from cell import *
from util import color

def run():
    screen = curses.newwin(0, 0, 0, 0)
    status = screen.subwin(4, 0, 0, 0)  # rows:4, cols:auto, top:0, left:0
    status.border(0, 0, 0, 0, 0, 0, 0, 0)
    window = screen.subwin(0, 0, 4, 0) # rows:auto, cols: auto, top:4, left:0
    window.keypad(1)
    window.addstr(0, 0, "Press escape to quit")
    window.addstr(1, 0, "Use arrow keys to move")
    window.addstr(3, 0, "Press any key to start")
    char = window.getch()
    world_height = 100
    world_width = 100
    left = 10
    top = 10
    height, width = window.getmaxyx()
    player = Player(15, 15)
    world = {} # Map of (row, col) to item

    #build a 'house'
    for i in xrange(10, 20):
        for j in xrange(11, 20):
            world[(i, j)] = Floor()
        world[(i, 10)] = Brick()
        world[(i, 20)] = Brick()
        world[(10, i)] = Brick()
        world[(20, i)] = Brick()
    world[(20, 15)] = Floor() # Poke a hole for a door

    world[(90, 90)] = Diamond()
    world[(25, 25)] = Diamond()
    world[(25, 26)] = Diamond()
    world[(25, 27)] = Diamond()
    world[(25, 28)] = Diamond()
    world[(25, 29)] = RedDiamond()

    for row in xrange(0, world_height):
        for col in xrange(int(math.sin(row/5.0)*3+50), int(math.sin(row/7.0)*4 + 60)):
            world[(row, col)] = Water()

    for col in xrange(50, 58):
        world[(36, col)] = Bridge()
        world[(37, col)] = Bridge()
        world[(72, col)] = Bridge()
        world[(73, col)] = Bridge()

    while char != 27:
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
                    if (row, col) in world:
                        char = world[(row, col)].character
                        attr = world[(row, col)].color
                    else:
                        char = 'w'
                        attr = color(curses.COLOR_GREEN)

                    window.addstr(row-top, col-left, char.encode('utf-8'), attr)
                except:pass
        window.addch(player.row-top, player.col-left, '@', color(curses.COLOR_YELLOW) | curses.A_BOLD)
        status.addstr(1, 1, "Pos: {}, {}".format(player.row, player.col))

        for idx, (item, count) in enumerate(player.inventory.items()):
            status.addstr(2, 1+4*idx, item.character.encode('utf-8'), item.color)
            status.addstr("{:<3}".format(count))
        status.refresh()

        #handle input
        char = window.getch()
        next_loc = [player.row, player.col]
        if char == 258: # Down
            next_loc[0] += 1
        elif char == 259: # Up
            next_loc[0] -= 1
        elif char == 260: # left
            next_loc[1] -= 1
        elif char == 261: # right
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
            old_loc = (player.row, player.col)
            player.row, player.col = next_loc
            if not world[next_loc].on_collision(player, world):
                player.row, player.col = old_loc
                continue

        player.row, player.col = next_loc


