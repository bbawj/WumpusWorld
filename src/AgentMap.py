import Cell


class AgentMap:

    def __init__(self):
        self.columns = 3
        self.rows = 3
        self.map = [[Cell.Cell() for _ in range(3)] for _ in range(3)]
        self.agent_loc = (1, 1)
        self.initMap()
        self.y_min = 0
        self.y_max = 0
        self.x_min = 0
        self.x_max = 0

    def initMap(self):
        blanks = [(0, 0), (0, 2), (2, 0), (2, 2)]
        for y, x in blanks:
            self.map[y][x].blank = True
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

    def updateMapMax(self, y_cur, x_cur):
        if y_cur > self.y_max:
            self.y_max = y_cur
        if y_cur < self.y_min:
            self.y_min = y_cur
        if x_cur > self.x_max:
            self.x_max = x_cur
        if x_cur < self.x_min:
            self.x_min = x_cur

    def expandMap(self, direction):
        if self.y_max - self.y_min + 3 > length(self.map):
            if direction == 0:
                self.map.insert([Cell.Cell(blank=True) for _ in range(self.columns)])

    def updateAgentMovement(self, y1, x1):
        y0, x0 = self.agent_loc
        self.updateAgentLocation(y0, x0, y1, x1)

        self.updateMapMax(y1, x1)

    def updateAgentCells(self, y, x):
        y0, x0 = self.agent_loc

    def updateAgentLocation(self, cur_y, cur_x, next_y, next_x):
        # Update new cell
        self.map[next_y][next_x].agent = True
        self.agent_loc = next_y, next_x

        # Remove from previous cell
        self.map[cur_y][cur_x].agent = False
        self.map[cur_y][cur_x].empty = True
        self.map[cur_y][cur_x].direction = None