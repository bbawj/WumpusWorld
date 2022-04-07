import Agent
import WorldMap
import Driver
import Player

a = Agent.Agent()
w = WorldMap.WorldMap()
d = Driver.Driver(agent=a, world=w)
p = Player.Player(driver=d)
p.play()

