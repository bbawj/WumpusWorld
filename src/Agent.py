import random

class Agent:
    def __init__(self):
        directions = [0, 1, 2, 3]
        self.direction = random.choice(directions)
        self.relative_loc = (0, 0)
        self.arrow = True
        self.coin = 0

    ########################################## MOVING FUNCTIONS ###############################################################

    def turnLeft(self):
        current_dir = self.direction
        self.direction = (current_dir - 1) % 4

    def turnRight(self):
        current_dir = self.direction
        self.direction = (current_dir + 1) % 4

    ########################################## LOCATION FUNCTIONS ###############################################################

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



