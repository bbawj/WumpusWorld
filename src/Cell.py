class Cell:
    def __init__(self):
        self.confounded = False
        self.stench = False
        self.tingle = False
        self.agent = False
        self.direction = None
        self.wumpus = False
        self.portal = False
        self.visited = False
        self.safe = False
        self.coin = False
        self.bump = False
        self.scream = False
        self.empty = True
        self.wall = False

    def printRow1(self):
        self.printCell1()
        self.printCell2()
        self.printCell3()

    def printRow2(self):
        self.printCell4_6()
        self.printCell5()
        self.printCell4_6()

    def printRow3(self):
        self.printCell7()
        self.printCell8()
        self.printCell9()

    # Confounded Indicator
    def printCell1(self):
        if self.wall:
            print("w", end=" ")
        elif self.confounded:
            print("%", end=" ")
        else:
            print(".", end=" ")

    # Stench Indicator
    def printCell2(self):
        if self.wall:
            print("w", end=" ")
        elif self.stench:
            print("=", end=" ")
        else:
            print(".", end=" ")

    # Tingle Indicator
    def printCell3(self):
        if self.wall:
            print("w", end=" ")
        elif self.tingle:
            print("T", end=" ")
        else:
            print(".", end=" ")

    # Agent Indicator
    def printCell4_6(self):
        if self.wall:
            print("w", end=" ")
        elif self.agent:
            print("-", end=" ")
        else:
            print(".", end=" ")

    # Wumpus/Portal/Direction/Safety Indicator
    def printCell5(self):
        if self.wall:
            print("w", end=" ")
        elif self.wumpus:
            print("W", end=" ")
        elif self.portal:
            print("O", end=" ")
        elif self.agent:
            self.printDirection()
        elif self.safe:
            if self.visited:
                print("S", end=" ")
            else:
                print("s", end=" ")
        else:
            print("?", end=" ")

    # Glitter Indicator
    def printCell7(self):
        if self.wall:
            print("w", end=" ")
        elif self.coin:
            print("*", end=" ")
        else:
            print(".", end=" ")

    # Bump Indicator
    def printCell8(self):
        if self.wall:
            print("w", end=" ")
        elif self.bump:
            print("B", end=" ")
        else:
            print(".", end=" ")

    # Bump Indicator
    def printCell9(self):
        if self.wall:
            print("w", end=" ")
        elif self.scream:
            print("@", end=" ")
        else:
            print(".", end=" ")

    def printDirection(self):
        direction_mapping = {0: "∧", 1: ">", 2: "∨", 3: "<"}
        print(direction_mapping[self.direction], end=" ")

    def copyCell(self, cell):
        self.stench = cell.stench
        self.tingle = cell.tingle
        self.visited = cell.visited
        self.safe = cell.safe
        self.coin = cell.coin
        self.bump = cell.bump
        self.scream = cell.scream
        self.empty = cell.empty
