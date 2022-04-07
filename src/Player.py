import Driver


class Player:
    def __init__(self, driver=Driver.Driver()):
        self.driver = driver

    def parseCmd(self, cmd):
        cmd = cmd.split(' ')
        if cmd[0] == "move":
            self.executeMoveCmd(cmd[1])
        elif cmd[0] == "face":
            self.executeFaceCmd(cmd[1])
        elif cmd[0] == "shoot":
            self.executeShootCmd()
        else:
            print("Command not recognised")

    def executeFaceCmd(self, cmd):
        if cmd == "up":
            self.driver.faceAgentNorth()
        elif cmd == "down":
            self.driver.faceAgentSouth()
        elif cmd == "left":
            self.driver.faceAgentWest()
        elif cmd == "right":
            self.driver.faceAgentEast()

    def executeMoveCmd(self, cmd):
        if cmd == "up":
            self.driver.moveAgentNorth()
        elif cmd == "down":
            self.driver.moveAgentSouth()
        elif cmd == "left":
            self.driver.moveAgentWest()
        elif cmd == "right":
            self.driver.moveAgentEast()

    def executeShootCmd(self):
        self.driver.agentShoot()

    def play(self):
        self.driver.printWorld()
        self.driver.agent.printMap()
        cmd = input()
        while cmd != "end":
            self.driver.clearTransitions()
            self.parseCmd(cmd)
            self.driver.printWorld()
            self.driver.agent.printMap()
            print(self.driver.agent.relative_loc)
            print("Coins: ", self.driver.agent.coin)
            cmd = input()
