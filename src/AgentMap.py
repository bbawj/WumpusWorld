import Cell

class AgentMap:

    def __init__(self):
        self.columns = 3
        self.rows = 3
        self.map = [[Cell.Cell() for _ in range(3)] for _ in range(3)]
        self.initMap()

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
