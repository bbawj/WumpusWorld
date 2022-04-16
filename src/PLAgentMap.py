import Cell


class PLAgentMap:

    def __init__(self):
        self.columns = 3
        self.rows = 3
        self.map_loc = (1, 1)
        self.direction = 0
        self.initMap()

    def initMap(self):
        self.map = [[Cell.Cell() for _ in range(self.columns)] for _ in range(self.rows)]
        self.map[1][1].agent = True

    def printMap(self):
        self.updateCells()
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

    def updateCells(self):
        for row in self.map:
            for cell in row:
                if cell.agent:
                    cell.direction = self.direction

    def expandMap(self):
        y, x = self.map_loc
        if y == 0 or y == self.rows-1:
            self.expandMapVertically()
        elif x == 0 or x == self.columns-1:
            self.expandMapHorizontally()

    def updateAgentMovement(self, y1, x1):
        y0, x0 = self.map_loc
        self.updateAgentLocation(y0, x0, y1, x1)
        self.expandMap()

    def updateAgentLocation(self, cur_y, cur_x, next_y, next_x):
        # Update new cell
        self.map[next_y][next_x].agent = True
        self.map_loc = next_y, next_x

        # Remove from previous cell
        self.map[cur_y][cur_x].agent = False
        self.map[cur_y][cur_x].empty = True
        self.map[cur_y][cur_x].direction = None

    ########################################## MAP EXPANSION FUNCTIONS ##################################################################

    def expandMapVertically(self):
        self.expandMapUp()
        self.expandMapDown()

    def expandMapUp(self):
        self.map.insert(0, [Cell.Cell() for _ in range(self.columns)])
        self.rows += 1
        y0, x0 = self.map_loc
        self.map_loc = y0+1, x0

    def expandMapDown(self):
        self.map.append([Cell.Cell() for _ in range(self.columns)])
        self.rows += 1

    def expandMapHorizontally(self):
        self.expandMapRight()
        self.expandMapLeft()

    def expandMapRight(self):
        for row in self.map:
            row.append(Cell.Cell())
        self.columns += 1

    def expandMapLeft(self):
        for row in self.map:
            row.insert(0, Cell.Cell())
        self.columns += 1
        y0, x0 = self.map_loc
        self.map_loc = y0, x0+1

    def getPercepts(self,cell):
        y,x = self.map_loc
        self.map[y][x].copyCell(cell)

    def getPLPercepts(self):
        y, x = self.map_loc
        return self.map[y][x].getPLPercept()

    def moveForward(self):
        y0, x0 = self.map_loc
        y1, x1 = self.getNextCell(y0, x0)
        self.updateAgentLocation(y0, x0, y1, x1)
        self.expandMap()

    def getNextCell(self, y, x):
        current_dir = self.direction
        if current_dir == 0:
            return y - 1, x
        elif current_dir == 1:
            return y, x + 1
        elif current_dir == 2:
            return y + 1, x
        elif current_dir == 3:
            return y, x - 1

    def turnLeft(self):
        current_dir = self.direction
        self.direction = (current_dir - 1) % 4

    def turnRight(self):
        current_dir = self.direction
        self.direction = (current_dir + 1) % 4

    def getRelativeCellLoc(self, y, x):
        y0 = int(self.rows/2)-y
        x0 = -(int(self.columns/2)-x)
        return x0, y0

    def resetMap(self):
        self.columns = 3
        self.rows = 3
        self.map_loc = (1, 1)
        self.direction = 0
        self.initMap()

    def pickup(self):
        y, x = self.map_loc
        self.map[y][x].coin = False





