import Test

t = Test.Test(agent="Agent.pl")
env1_actions = ['moveforward','moveforward','moveforward',
                'turnright','moveforward',
                'turnright','moveforward',
                'turnright','moveforward','moveforward',
                'turnright','turnright']
#t.env1_test1_localMapping(actions = env1_actions)
#t.env1_test2_SensoryInteference(actions = env1_actions)
#t.env1_test3_PortalReset(actions = env1_actions, arrow=True)
#t.env1_test4_explore()
#t.env1_test5_GameReset(actions = env1_actions, arrow=True)
t.randomExplore()
