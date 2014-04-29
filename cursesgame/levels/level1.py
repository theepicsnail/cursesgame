from cell import *
from world import World
from player import Player
class Template:
    def __init__(self, data, mapping):
        rows = data.strip().split("\n")
        template = []
        for row in rows:
            types = map(mapping.get, row)
            template.append(map(lambda cls: cls() if cls else None, types))
        self.data = template

    def place(self, world, row, col):
        for dr, t_row in enumerate(self.data):
            for dc, t_dat in enumerate(t_row):
                if t_dat is not None:
                    if type(t_dat) is not list:
                        cells = [t_dat]
                    else:
                        cells = t_dat

                    for cell in cells:
                        world.push_cell((row + dr, col + dc), cell)


class Level1(World):
    def create(self):
        self.width =  200
        self.height = 100
        for r in xrange(self.height):
            for c in xrange(self.width):
                dr = (r-self.height/2)
                dc = (c-self.width/2)
                if dr*dr + dc*dc/4 >= 45*45:
                    self.push_cell((r,c), Water())

        Template("""
..........................~~~~~~~................
........................~~~~...~~~~~~............
.....................~~~~..........~~~~~~.......
...................~~~~...............~~~........
..................~~~~..................~~~......
.................~~~~....................~~~.....
...................~~~~...................~~~....
...xxxxxxxxxxxxxxx..~~~..xxxxxxxxxxxxxxx..~~~....
...x   x     x   x..~~~..x     x       x..~~~~...
...x             x..~~~..x  d  x   r   x...~~~~..
...x   x     x   x..~~~..x     x       x...~~~~..
...xxxxxx   xxxxxx..~~~..xx    xxxxDxxxx...~~~...
........xxRxx.......~~~....xx       xx....~~~....
....................~~~~.....xxx xxx.....~~~.....
....................~~~~................~~~......
.....................~~~~.............~~~~.......
.......................~~~~~.........~~~~........
........................~~~~~~~~=~~~~~~..........
...........................~~~~~=~~~~............
..............................B..................
.................................................
""", {
    "x": Brick,
    " ": Floor,
    "d": lambda:[Floor(), Diamond()],
    "D": lambda:[Floor(), DiamondDoor()],
    "r": lambda:[Floor(), RedDiamond()],
    "R": lambda:[Floor(), RedDiamondDoor()],
    "=": Bridge,
    "~": Water,
    "B": PushableBlock
    }).place(self, 20, 50)
        self.push_cell((self.height/2, self.width/2), self.player)



