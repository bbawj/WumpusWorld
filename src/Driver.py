import WorldMap
import Agent


class Driver:

    def __init__(self, world=WorldMap.WorldMap(), agent=Agent.Agent()):
        self.world = world
        self.agent = agent
        self.assignAgent()

    def assignAgent(self):
        y, x = self.world.getSafePos()
        self.world.map[y][x].agent = True
        self.world.map[y][x].direction = self.agent.direction
        self.world.map[y][x].empty = False
        self.world.agent_loc = (y, x)

    ########################################## MOVING FUNCTIONS ###############################################################

    def moveAgentForward(self):
        current_dir = self.agent.direction
        y0, x0 = self.world.agent_loc
        y1, x1 = self.getNextCell(current_dir)

        # If agent steps into portal
        if self.world.map[y1][x1].portal:
            y2, x2 = self.executePortal()
            self.updateAgentLocation(y0, x0, y2, x2)
            self.agent.resetPortal()

        # If agent steps into Wumpus cell
        elif self.world.map[y1][x1].wumpus:
            print("You got eaten by ze Wumpus!")
            self.restartGame()

        # If agent steps into empty cell
        elif self.world.map[y1][x1].empty:
            self.updateAgentLocation(y0, x0, y1, x1)
            self.agent.updateRelativeLocation()

    def faceAgentNorth(self):
        while self.agent.direction != 0:
            self.agent.turnRight()

    def moveAgentNorth(self):
        self.faceAgentNorth()
        self.moveAgentForward()

    def faceAgentEast(self):
        while self.agent.direction != 1:
            self.agent.turnRight()

    def moveAgentEast(self):
        self.faceAgentEast()
        self.moveAgentForward()

    def faceAgentSouth(self):
        while self.agent.direction != 2:
            self.agent.turnRight()

    def moveAgentSouth(self):
        self.faceAgentSouth()
        self.moveAgentForward()

    def faceAgentWest(self):
        while self.agent.direction != 3:
            self.agent.turnRight()

    def moveAgentWest(self):
        self.faceAgentWest()
        self.moveAgentForward()

    ########################################## SHOOT FUNCTIONS ###############################################################

    def agentShoot(self):
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
