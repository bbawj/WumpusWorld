import random
import AgentMap

class Agent:
    def __init__(self):
        directions = [0, 1, 2, 3]
        self.direction = random.choice(directions)
        self.relative_loc = (0, 0)
        self.arrow = True
        self.coin = 0
        self.map = AgentMap.AgentMap()

    ########################################## MOVING FUNCTIONS ###############################################################

    def turnLeft(self):
        current_dir = self.direction
        self.direction = (current_dir - 1) % 4

    def turnRight(self):
        current_dir = self.direction
        self.direction = (current_dir + 1) % 4

    ########################################## LOCATION FUNCTIONS ###############################################################

    def updateRelativeLocation(self):
        y0, x0 = self.relative_loc
        y_m, x_m = self.map.agent_loc
        current_dir = self.direction
        if current_dir == 0:
            self.relative_loc = (y0 - 1, x0)
            self.map.updateAgentMovement(y_m - 1, x_m)
        elif current_dir == 1:
            self.relative_loc = (y0, x0 + 1)
            self.map.updateAgentMovement(y_m, x_m + 1)
        elif current_dir == 2:
            self.relative_loc = (y0 + 1, x0)
            self.map.updateAgentMovement(y_m + 1, x_m)
        elif current_dir == 3:
            self.relative_loc = (y0, x0 - 1)
            self.map.updateAgentMovement(y_m, x_m- 1)

    def resetGame(self):
        self.resetPortal()
        self.arrow = True
        self.coin = 0

    def resetPortal(self):
        self.resetLocation()
        self.resetDirection()

    def resetLocation(self):
        self.relative_loc = (0, 0)

    def resetDirection(self):
        directions = [0, 1, 2, 3]
        self.direction = random.choice(directions)

    ########################################## SHOOT FUNCTIONS ###############################################################

    def shoot(self):
        if self.arrow:
            self.arrow = False
            return True
        return False

    ########################################## UTIL FUNCTIONS ###############################################################

    def pickup(self):
        self.coin += 1

    def printMap(self):
        self.map.printMap(direction=self.direction)
