from cell import *
from world import World
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
                        world.push_cell(row + dr, col + dc, cell)


class Level1(World):
    def create(self):
        self.width = 100
        self.height = 50
        #Default is grass, that's fine

        # Create our house template
        house = Template("""
.................~~~~....................~~~.........................................................
...................~~~~...................~~~........................................................
...xxxxxxxxxxxxxxx..~~~..xxxxxxxxxxxxxxx..~~~........................................................
...x   x     x   x..~~~..x     x       x..~~~~.......................................................
...x             x..~~~..x  d  x   r   x...~~~~......................................................
...x   x     x   x..~~~..x     x       x...~~~~......................................................
...xxxxxx   xxxxxx..~~~..xx    xxxxDxxxx...~~~.......................................................
........xxRxx.......~~~....xx       xx....~~~........................................................
....................~~~~.....xxx xxx.....~~~.........................................................
....................~~~~................~~~..........................................................
.....................~~~~.............~~~~...........................................................
.......................~~~~~.........~~~~............................................................
........................~~~~~~~~=~~~~~~..............................................................
...........................~~~~~=~~~~................................................................
..............................B......................................................................
.....................................................................................................
.....................................................................................................
.....................................................................................................
.....................................................................................................
.....................................................................................................
.....................................................................................................
.....................................................................................................
.....................................................................................................
.....................................................................................................
.....................................................................................................
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
    })
        house.place(self, 0, 0)


