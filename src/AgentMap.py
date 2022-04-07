import Cell


class AgentMap:

    def __init__(self):
        self.columns = 3
        self.rows = 3
        self.map = [[Cell.Cell() for _ in range(3)] for _ in range(3)]
        self.map_loc = (1, 1)
        self.initMap()

    def initMap(self):
        self.map[1][1].agent = True

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
        for row in self.map:
            for cell in row:
                if cell.agent:
                    cell.direction = direction

    def expandMap(self):
        y, x = self.map_loc
        if y == 0:
            self.expandMapUp()
        elif y == self.rows-1:
            self.expandMapDown()
        elif x == self.columns-1:
            self.expandMapRight()
        elif x == 0:
            self.expandMapLeft()

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

    def expandMapUp(self):
        self.map.insert(0, [Cell.Cell() for _ in range(self.columns)])
        self.rows += 1
        y0, x0 = self.map_loc
        self.map_loc = y0+1, x0

    def expandMapDown(self):
        self.map.append([Cell.Cell() for _ in range(self.columns)])
        self.rows += 1

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
