import Test
import sys

### UPDATE FILE NAMES BELOW ###
file_name = "StopMug-testPrintout-Self-Self.txt"
agent_name = "Agent.pl"
###############################

stdoutOrigin = sys.stdout
sys.stdout = open(file_name, "w")

t = Test.Test(agent=agent_name)
env1_actions = ['moveforward', 'moveforward', 'moveforward',
                'turnright', 'moveforward',
                'turnright', 'moveforward',
                'turnright', 'moveforward', 'moveforward',
                'turnright', 'turnright']

print("TEST 1 --- LOCALISATION AND MAPPING ABILITIES")
t.env1_test1_localMapping(actions=env1_actions)

print("\n\nTEST 2 --- SENSORY INFERENCE")
t.env1_test2_SensoryInteference(actions=env1_actions)

print("\n\nTEST 3 --- PORTAL MEMORY MANAGEMENT")
t.env1_test3_PortalReset(actions=env1_actions, arrow=True)

print("\n\nTEST 4 --- EXPLORATION CAPABILITIES")
t.env1_test4_explore()

print("\n\nTEST 5 --- END GAME RESET MEMORY MANAGEMENT")
t.env1_test5_GameReset(actions=env1_actions, arrow=True)

# t.randomExplore()

sys.stdout.close()
sys.stdout = stdoutOrigin
