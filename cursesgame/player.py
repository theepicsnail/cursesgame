from collections import defaultdict

class Player:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.inventory = defaultdict(int)

    def pickup(self, item):
        """Adds an item to player's inventory."""
        self.inventory[item] += 1

    def drop(self, item):
        if self.inventory[item] <= 0:
            raise Exception("Item not in inventory")
        else:
            self.inventory[item] -= 1
            if self.inventory[item] == 0:
                del self.inventory[item]

    def has_a(self, item):
        return item in self.inventory
