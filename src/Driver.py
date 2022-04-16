import WorldMap
import Agent


class Driver:

    def __init__(self, world=WorldMap.WorldMap(), agent=Agent.Agent()):
        self.world = world
        self.agent = agent
        self.assignAgent()

    def assignAgent(self):
        y, x = self.world.assignAgent(direction=self.agent.direction)
        self.world.agent_loc = (y, x)
        self.updateCellSafety(y, x)
        # self.passPercepts(self.world.map[y][x])

    ########################################## MOVING FUNCTIONS ###############################################################

    def moveAgentForward(self):
        self.clearTransitions()
        current_dir = self.agent.direction
        y0, x0 = self.world.agent_loc
        y1, x1 = self.getNextCell(current_dir)

        # If agent steps into portal
        if self.world.map[y1][x1].portal:
            y2, x2 = self.executePortal()
            self.updateAgentLocation(y0, x0, y2, x2)
            self.agent.resetPortal()
            # self.passPercepts(self.world.map[y2][x2])
            self.updateCellSafety(y2, x2)
            return "portal"

        # If agent steps into Wumpus cell
        elif self.world.map[y1][x1].wumpus:
            print("You got eaten by ze Wumpus!")
            self.restartGame()
            return "wumpus"

        elif self.world.map[y1][x1].wall:
            print("You bumped into a wall!")
            self.world.map[y0][x0].bump = True
            # self.passPercepts(self.world.map[y0][x0])
            return "wall"

        # If agent steps into empty cell
        elif self.world.map[y1][x1].empty:
            self.updateAgentLocation(y0, x0, y1, x1)
            self.updateCellSafety(y1, x1)
            # self.passPercepts(self.world.map[y1][x1])
            return "empty"

    def turnRight(self):
        self.clearTransitions()
        self.agent.turnRight()

    def turnLeft(self):
        self.clearTransitions()
        self.agent.turnLeft()

    ########################################## SHOOT FUNCTIONS ###############################################################

    def agentShoot(self):
        self.clearTransitions()
        if self.agent.shoot():
            print("Pew pew shoot arrow pew pew")
            current_dir = self.agent.direction
            if current_dir == 0:
                self.shootNorth()
            elif current_dir == 1:
                self.shootEast()
            elif current_dir == 2:
                self.shootSouth()
            elif current_dir == 3:
                self.shootWest()
        else:
            print("You're out of arrows!")

    def shootNorth(self):
        y, x = self.world.agent_loc
        is_clear_path = True
        y -= 1
        while y >= 0 and is_clear_path:
            is_clear_path = self.arrowFlying(y, x)
            y -= 1

    def shootEast(self):
        y, x = self.world.agent_loc
        is_clear_path = True
        x += 1
        while x < self.world.columns and is_clear_path:
            is_clear_path = self.arrowFlying(y, x)
            x += 1

    def shootSouth(self):
        y, x = self.world.agent_loc
        is_clear_path = True
        y += 1
        while y < self.world.rows and is_clear_path:
            is_clear_path = self.arrowFlying(y, x)
            y += 1

    def shootWest(self):
        y, x = self.world.agent_loc
        is_clear_path = True
        x -= 1
        while x >= 0 and is_clear_path:
            is_clear_path = self.arrowFlying(y, x)
            x -= 1

    def arrowFlying(self, y, x):
        cell = self.world.map[y][x]
        if cell.wumpus:
            cell.wumpus = False
            cell.empty = True
            self.world.assignStench(y, x, False)
            print("You killed the Wumpus! Stonks")
            y_a, x_a = self.world.agent_loc
            self.world.map[y_a][x_a].scream = True
            return False
        elif not cell.empty:
            return False
        else:
            return True

    ########################################## UTIL FUNCTIONS ###############################################################

    def printWorld(self):
        self.world.printMap(direction=self.agent.direction)

    # When agent steps into portal
    def executePortal(self):
        y2, x2 = self.world.getSafePos()
        print("Hocus Pocus you kena confundus")
        print("New location: ({0},{1})".format(x2, y2))
        return y2, x2

    # When agent steps into wumpus cell
    def restartGame(self):
        print("Starting new game...")
        self.world = WorldMap.WorldMap()
        self.agent = Agent.Agent()
        self.assignAgent()

    # To update next and previous cell when agent is being moved
    def updateAgentLocation(self, cur_y, cur_x, next_y, next_x):
        # Update new cell
        self.world.map[next_y][next_x].agent = True
        self.world.agent_loc = next_y, next_x

        # Remove from previous cell
        self.world.map[cur_y][cur_x].agent = False
        self.world.map[cur_y][cur_x].empty = True
        self.world.map[cur_y][cur_x].direction = None

    # To get the next cell location of agent given its current direction
    def getNextCell(self, current_dir):
        y, x = self.world.agent_loc
        if current_dir == 0:
            return y - 1, x
        elif current_dir == 1:
            return y, x + 1
        elif current_dir == 2:
            return y + 1, x
        elif current_dir == 3:
            return y, x - 1

    def updateCellSafety(self, y, x):
        self.world.map[y][x].safe = True
        self.world.map[y][x].visited = True

    def getPercepts(self):
        return self.world.getPercepts()

    def clearTransitions(self):
        for row in self.world.map:
            for cell in row:
                cell.bump = False
                cell.scream = False

    def pickup(self):
        y, x = self.world.agent_loc
        self.world.map[y][x].coin = False

    def checkCoin(self):
        y, x = self.world.agent_loc
        return self.world.map[y][x].coin


    ########################################## TESTING FUNCTIONS ###############################################################

    def buildTestEnv(self, columns=7, rows=6, num_coins=1, num_wumpus=1, num_portals=3, num_walls=3,
                     wall_loc=[(1, 1), (1, 2), (1, 3)],
                     wumpus_loc=(2, 3),
                     portal_loc=[(4, 1), (4, 3), (4, 5)],
                     coin_loc=[(1, 5)],
                     agent_loc=(3, 4),
                     direction=0):

        self.world.buildTestWorld(columns=columns, rows=rows, num_coins=num_coins, num_wumpus=num_wumpus,
                                  num_portals=num_portals, num_walls=num_walls, wall_loc=wall_loc,
                                  wumpus_loc=wumpus_loc,
                                  portal_loc=portal_loc, coin_loc=coin_loc)
        self.agent.direction = direction
        y, x = self.world.assignTestAgent(agent_loc=agent_loc, direction=direction)
        self.world.agent_loc = (y, x)
        self.updateCellSafety(y, x)
