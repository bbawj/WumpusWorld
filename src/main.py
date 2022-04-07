import Agent
import WorldMap
import Driver
import Player
import Cell

a = Agent.Agent()
w = WorldMap.WorldMap(num_coins=3)
d = Driver.Driver(agent=a, world=w)
p = Player.Player(driver=d)
p.play()