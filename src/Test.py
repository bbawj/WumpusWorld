import PLAgentMap
import Agent
import PLAgentMap
import Driver
import WorldMap
from pyswip import Prolog


class Test:
    def __init__(self, agent):
        self.agent = agent
        self.initRest()

    def initRest(self):
        self.prolog = Prolog()
        self.prolog.consult(self.agent)
        self.plam = PLAgentMap.PLAgentMap()
        self.a = Agent.Agent()
        self.w = WorldMap.WorldMap()
        self.d = Driver.Driver(world=self.w, agent=self.a)

    ########################################## TESTING FUNCTIONS ##################################################################

    def randomExplore(self):
        self.initRest()
        self.play()

    def env1_test1_localMapping(self, actions):
        self.d.buildTestEnv(direction=3)
        for action in actions:
            self.executeAction(action)
        self.printMap()
        print("\t\t\t\t Expected \t Actual")
        self.printAgentLoc(expected_loc="r(-1, 2)", expected_dir="reast")

    def env1_test2_SensoryInteference(self, actions):

        self.d.buildTestEnv(direction=3)
        for action in actions:
            self.executeAction(action)
        self.printMap()

        certainWumpus, wumpus, tingleSensed, portalInferred = self.env1_sensoryCheck()

        print("\t\t\t\t Expected \tActual")
        print("Certain Wumpus at (1,1): \t True \t\t" + certainWumpus)
        print("Wumpus at (-1,1): \t\t False \t\t" + wumpus)
        print("Tingle at (0,3): \t\t True \t\t" + tingleSensed)
        print("Portal at (1,1): \t\t True \t\t" + portalInferred)

    def env1_test3_PortalReset(self, actions, arrow):

        self.d.buildTestEnv(direction=3)
        for action in actions:
            self.executeAction(action)
        self.printMap()

        expected_arrow = "True"
        if arrow:
            self.shoot()
            expected_arrow = "False"

        has_arrow = self.arrowCheck()

        certainWumpus, wumpus, tingleSensed, portalInferred = self.env1_sensoryCheck()

        print("Before portal reset:")
        print("\t\t\t\t Expected \tActual")
        print("Certain Wumpus at (1,1): \t True \t\t" + certainWumpus)
        print("Wumpus at (-1,1): \t\t False \t\t" + wumpus)
        print("Tingle at (0,3): \t\t True \t\t" + tingleSensed)
        print("Portal at (1,1): \t\t True \t\t" + portalInferred)
        print("Agent has arrow: \t\t " + expected_arrow + "\t\t" + has_arrow)

        self.portalReset()
        self.printMap()
        has_arrow = self.arrowCheck()
        certainWumpus, wumpus, tingleSensed, portalInferred = self.env1_sensoryCheck()

        print("After game reset:")
        print("\t\t\t\t Expected \t Actual")
        print("Certain Wumpus at (1,1): \t False \t\t " + certainWumpus)
        print("Wumpus at (-1,1): \t\t False \t\t " + wumpus)
        print("Tingle at (0,3): \t\t False \t\t " + tingleSensed)
        print("Portal at (1,1): \t\t False \t\t " + portalInferred)
        print("Agent has arrow: \t\t " + expected_arrow + "\t\t " + has_arrow)

        self.printAgentLoc(expected_loc="r(0, 0)", expected_dir="rnorth")

    def env1_test4_explore(self):
        self.d.buildTestEnv(columns=7, rows=6, num_coins=1, num_wumpus=1, num_portals=3, num_walls=3,
                            wall_loc=[(1, 2), (1, 3), (2, 5)],
                            wumpus_loc=(4, 3),
                            portal_loc=[(2, 1), (3, 1), (3, 5)],
                            coin_loc=[(1, 1)],
                            agent_loc=(2, 3),
                            direction=0)
        self.play()

    def env1_test5_GameReset(self, actions, arrow):

        self.d.buildTestEnv(direction=3)
        for action in actions:
            self.executeAction(action)
        self.printMap()

        expected_arrow = "True"
        if arrow:
            self.shoot()
            expected_arrow = "False"

        has_arrow = self.arrowCheck()

        certainWumpus, wumpus, tingleSensed, portalInferred = self.env1_sensoryCheck()

        print("Before portal reset:")
        print("\t\t\t\t Expected \tActual")
        print("Certain Wumpus at (1,1): \t True \t\t" + certainWumpus)
        print("Wumpus at (-1,1): \t\t False \t\t" + wumpus)
        print("Tingle at (0,3): \t\t True \t\t" + tingleSensed)
        print("Portal at (1,1): \t\t True \t\t" + portalInferred)
        print("Agent has arrow: \t\t " + expected_arrow + "\t\t" + has_arrow)

        self.gameReset()

        self.printMap()
        has_arrow = self.arrowCheck()
        certainWumpus, wumpus, tingleSensed, portalInferred = self.env1_sensoryCheck()

        print("After game reset:")
        print("\t\t\t\t Expected \t Actual")
        print("Certain Wumpus at (1,1): \t False \t\t " + certainWumpus)
        print("Wumpus at (-1,1): \t\t False \t\t " + wumpus)
        print("Tingle at (0,3): \t\t False \t\t " + tingleSensed)
        print("Portal at (1,1): \t\t False \t\t " + portalInferred)
        print("Agent has arrow: \t\t True \t\t " + has_arrow)

        self.printAgentLoc(expected_loc="r(0, 0)", expected_dir="rnorth")

    def env1_sensoryCheck(self):

        certainWumpus = "True"
        wumpus = "True"
        tingleSensed = "True"
        portalInferred = "True"

        if len(list(self.prolog.query("certainWumpus(1,1)."))) == 0:
            certainWumpus = "False"
        if len(list(self.prolog.query("wumpus(-1,1)."))) == 0:
            wumpus = "False"
        if len(list(self.prolog.query("tingle(0,3)."))) == 0:
            tingleSensed = "False"
        if len(list(self.prolog.query("confundus(0,4)."))) == 0:
            portalInferred = "False"

        return certainWumpus, wumpus, tingleSensed, portalInferred

    ########################################## UTIL FUNCTIONS ##################################################################

    def executeAction(self, action):
        if action == "moveforward":
            self.moveForward()
        elif action == "turnright":
            self.turnRight()
        elif action == "turnleft":
            self.turnLeft()

    def arrowCheck(self):
        has_arrow = "True"
        if len(list(self.prolog.query("hasarrow."))) == 0:
            has_arrow = "False"
        return has_arrow

    def portalReset(self):
        print("Simulating portal reset...")
        list(self.prolog.query("reposition."))
        self.plam.resetMap()

    def gameReset(self):
        print("Simulating game reset...")
        self.d.restartGame()
        self.plam.resetMap()
        list(self.prolog.query("reborn."))

    def printAgentLoc(self, expected_loc, expected_dir):
        agent_rel_loc = list(self.prolog.query("current(X,Y)."))
        coords = agent_rel_loc[0]['X']
        rel_dir = agent_rel_loc[0]['Y']
        print("Agent relative location: \t " + expected_loc + " \t", coords)
        print("Agent relative direction: \t " + expected_dir + "\t\t", rel_dir)

    def executeMoves(self, moveList):
        for move in moveList:
            for action in move:
                if action == "turnright":
                    self.turnRight()
                elif action == "turnleft":
                    self.turnLeft()
                elif action == "moveforward":
                    self.moveForward()
                elif action == "pickup":
                    self.pickUp()
                elif action == "shoot":
                    self.shoot()

    def getNextMoves(self):
        soln = list(self.prolog.query("explore(L)."))
        if len(soln) == 0:
            return None
        else:
            moveList = soln[0]['L']
            return moveList

    def play(self):
        self.printMap()
        moveList = self.getNextMoves()
        while (moveList):
            print(moveList)
            self.executeMoves(moveList)
            self.printMap()
            moveList = self.getNextMoves()
        print("No more moves!")

    ########################################## MOVING FUNCTIONS ##################################################################

    def moveForward(self):
        next_cell = self.d.moveAgentForward()
        percepts = self.d.getPercepts()
        list(self.prolog.query("move(moveforward, " + str(percepts) + ")."))
        if next_cell == "empty":
            self.plam.moveForward()
            if self.d.checkCoin() == True:
                self.d.pickup()
                self.plam.pickup()
                percepts = self.d.getPercepts()
                list(self.prolog.query("move(pickup, " + str(percepts) + ")."))

        if next_cell == "portal":
            self.plam.resetMap()
            list(self.prolog.query("reposition."))
        if next_cell == "wumpus":
            self.plam.resetMap()
            list(self.prolog.query("reborn."))

    def turnRight(self):
        self.plam.turnRight()
        self.d.turnRight()
        percepts = self.d.getPercepts()
        list(self.prolog.query("move(turnright, " + str(percepts) + ")."))

    def turnLeft(self):
        self.plam.turnLeft()
        self.d.turnLeft()
        percepts = self.d.getPercepts()
        list(self.prolog.query("move(turnleft, " + str(percepts) + ")."))

    def shoot(self):
        self.d.agentShoot()
        percepts = self.d.getPercepts()
        list(self.prolog.query("move(shoot, " + str(percepts) + ")."))

    ########################################## MAPPING FUNCTIONS ##################################################################

    def printMap(self):
        self.updateCells()
        self.d.printWorld()
        self.plam.printMap()

    def updateCells(self):
        for y in range(self.plam.rows):
            for x in range(self.plam.columns):
                self.updateCell(y, x)

    def updateCell(self, y0, x0):
        x1, y1 = self.plam.getRelativeCellLoc(y0, x0)

        self.plam.map[y0][x0].wumpus = self.queryWumpus(x1, y1)
        self.plam.map[y0][x0].portal = self.queryConfundus(x1, y1)
        self.plam.map[y0][x0].tingle = self.queryTingle(x1, y1)
        self.plam.map[y0][x0].coin = self.queryGlitter(x1, y1)
        self.plam.map[y0][x0].stench = self.queryStench(x1, y1)
        self.plam.map[y0][x0].wall = self.queryWall(x1, y1)
        self.plam.map[y0][x0].visited = self.queryVisited(x1, y1)
        self.plam.map[y0][x0].safe = self.querySafe(x1, y1)

    def queryWumpus(self, x1, y1):
        if len(list(self.prolog.query("wumpus(" + str(x1) + "," + str(y1) + ")"))) == 0:
            return False
        return True

    def queryConfundus(self, x1, y1):
        if len(list(self.prolog.query("confundus(" + str(x1) + "," + str(y1) + ")"))) == 0:
            return False
        return True

    def queryTingle(self, x1, y1):
        if len(list(self.prolog.query("tingle(" + str(x1) + "," + str(y1) + ")"))) == 0:
            return False
        return True

    def queryGlitter(self, x1, y1):
        if len(list(self.prolog.query("glitter(" + str(x1) + "," + str(y1) + ")"))) == 0:
            return False
        return True

    def queryStench(self, x1, y1):
        if len(list(self.prolog.query("stench(" + str(x1) + "," + str(y1) + ")"))) == 0:
            return False
        return True

    def queryWall(self, x1, y1):
        if len(list(self.prolog.query("wall(" + str(x1) + "," + str(y1) + ")"))) == 0:
            return False
        return True

    def queryVisited(self, x1, y1):
        if len(list(self.prolog.query("visited(" + str(x1) + "," + str(y1) + ")"))) == 0:
            return False
        return True

    def querySafe(self, x1, y1):
        if len(list(self.prolog.query("safe(" + str(x1) + "," + str(y1) + ")"))) == 0:
            return False
        return True
