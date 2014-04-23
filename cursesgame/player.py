from collections import defaultdict

class Player:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.inventory = defaultdict(lambda: 0)

    def pickup(self, item):
        """Adds an item to player's inventory."""
        self.inventory[item] += 1

    def drop(self, item):
        if self.inventory[item] <= 0:
            raise ItemNotInInventory
        else:
            self.inventory[item] -= 1

