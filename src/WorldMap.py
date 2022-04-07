import random
import Cell

class WorldMap:
    def __init__(self, columns=7, rows=6, num_coins=1, num_wumpus=1, num_portals=3, num_walls=3):
        if columns < 3:
            self.columns = 3
            print("Map must have at least 3 columns! Set to 3 Columns")
        else:
            self.columns = columns

        if rows < 3:
            self.rows = 3
            print("Map must have at least 3 rows! Set to 3 Rows")
        else:
            self.rows = rows

        if num_coins < 1:
            self.num_coins = 1
            print("Map must have at least 1 Coin!")
        else:
            self.num_coins = num_coins

        if num_wumpus < 1:
            self.num_wumpus = 1
            print("Map must have at least 1 Wumpus!")
        else:
            self.num_wumpus = num_wumpus

        if num_portals < 3:
            self.num_portals = 3
            print("Map must have at least 3 Portals!")
        else:
            self.num_portals = num_portals

        if num_walls < 0:
            self.num_walls = 0
            print("Number of walls cannot be negative")
        else:
            self.num_walls = num_walls

        # Check if map is large enough to fit
        self.checkSize()
        self.map = [[Cell.Cell() for i in range(self.columns)] for j in range(self.rows)]

        # Init objects
        self.buildSurroundingWalls()
        self.assignWumpus()
        self.assignPortal()
        self.assignWalls()
        self.assignCoin()

    ########################################## INIT FUNCTIONS ##################################################################

    def checkSize(self):
        flag = True
        while self.num_coins + self.num_wumpus + self.num_portals + 1 > self.columns * self.rows:
            if flag:
                print("Too many objects! Expanding world...")
                flag = False
            self.columns += 1
            self.rows += 1
        print("Map size: ", self.columns, "x", self.rows)

    def buildSurroundingWalls(self):
        for y in range(self.rows):
            self.map[y][0].wall = True
            self.map[y][0].empty = False
            self.map[y][self.columns - 1].wall = True
            self.map[y][self.columns - 1].empty = False

        for x in range(self.columns):
            self.map[0][x].wall = True
            self.map[0][x].empty = False
            self.map[self.rows - 1][x].wall = True
            self.map[self.rows - 1][x].empty = False

    def assignPortal(self):
        for i in range(self.num_portals):
            y, x = self.getEmptyPos()
            self.map[y][x].portal = True
            self.map[y][x].empty = False
            self.assignTingle(y, x)

    def assignTingle(self, y, x):
        if y != 0:
            self.map[y - 1][x].tingle = True
        if y != self.rows - 1:
            self.map[y + 1][x].tingle = True
        if x != 0:
            self.map[y][x - 1].tingle = True
        if x != self.columns - 1:
            self.map[y][x + 1].tingle = True

    def assignWumpus(self):
        for i in range(self.num_wumpus):
            y, x = self.getEmptyPos()
            self.map[y][x].wumpus = True
            self.map[y][x].empty = False
            self.assignStench(y, x, True)

    # Used to assign stench when Wumpus is spawned and deassign stench when Wumpus is killed
    def assignStench(self, y, x, exists):
        if y != 0:
            self.map[y - 1][x].stench = exists
        if y != self.rows - 1:
            self.map[y + 1][x].stench = exists
        if x != 0:
            self.map[y][x - 1].stench = exists
        if x != self.columns - 1:
            self.map[y][x + 1].stench = exists

    def assignCoin(self):
        for i in range(self.num_coins):
            y, x = self.getEmptyPos()
            self.map[y][x].coin = True
            self.map[y][x].glitter = True

    def assignWalls(self):
        for i in range(self.num_walls):
            y, x = self.getEmptyPos()
            self.map[y][x].wall = True
            self.map[y][x].empty = False

    ########################################## UTIL FUNCTIONS ##################################################################

    def getEmptyPos(self):
        x = random.randrange(0, self.columns)
        y = random.randrange(0, self.rows)
        isEmpty = self.map[y][x].empty
        while isEmpty == False:
            x = random.randrange(0, self.columns)
            y = random.randrange(0, self.rows)
            isEmpty = self.map[y][x].empty
        return y, x

    def getAnyPos(self):
        x = random.randrange(0, self.columns)
        y = random.randrange(0, self.rows)
        return y, x

    def getSafePos(self):
        x = random.randrange(0, self.columns)
        y = random.randrange(0, self.rows)
        is_empty = self.map[y][x].empty
        is_tingle = self.map[y][x].tingle
        is_stench = self.map[y][x].stench
        while not (is_empty and (not is_tingle) and (not is_stench)):
            x = random.randrange(0, self.columns)
            y = random.randrange(0, self.rows)
            is_empty = self.map[y][x].empty
            is_tingle = self.map[y][x].tingle
            is_stench = self.map[y][x].stench
        return y, x

    def printMap(self, direction):
        self.updateCells(direction)
        print("_ " * self.columns * 4)
        for row in self.map:

            print("|", end=" ")
            for cell in row:
                cell.printRow1()
                print("|", end=" ")
            print()

            print("|", end=" ")
            for cell in row:
                cell.printRow2()
                print("|", end=" ")
            print()

            print("|", end=" ")
            for cell in row:
                cell.printRow3()
                print("|", end=" ")
            print()
            print("_ " * self.columns * 4)

    def updateCells(self, direction):
        y, x = self.agent_loc
        self.map[y][x].direction = direction
