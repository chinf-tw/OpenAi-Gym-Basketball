from window import basketballEnv
from QLearning import QLearning
from fileHandler import opponentsStateEncode

import random
import time
import os

opponentsStateFileName = "v0.opponents"
nextState = None
originalState = None
speed = 0.1
done = False
nextIsShoot = False
originalIsShoot = False

NextIsGetBall = False
originalIsGetBall = False

i = 0
Episode = 0
# successAction = []
reward = None

if os.path.isfile(opponentsStateFileName) :
    env = basketballEnv("v0",opponentsStateFileName)
else:
    env = basketballEnv("v0")
    opponentsStateEncode(env.GetOpponentsState(),opponentsStateFileName)



qlearningBallFileName = "qlearningBall.npy"
if os.path.isfile(qlearningBallFileName) :
    qlearningBall = QLearning(env.col,env.row,9,qTableFileName=qlearningBallFileName,learning_rate=0.1, reward_decay=0.9, e_greedy=0.2)
else:
    qlearningBall = QLearning(env.col,env.row,9,learning_rate=0.1, reward_decay=0.9, e_greedy=0.2)
    pass

qlearningShootFileName = "qlearningShoot.npy"
if os.path.isfile(qlearningShootFileName) :
    qlearningShoot = QLearning(env.col,env.row,9,qTableFileName=qlearningShootFileName,learning_rate=0.1, reward_decay=0.9, e_greedy=0.2)
else:
    qlearningShoot = QLearning(env.col,env.row,9,learning_rate=0.1, reward_decay=0.9, e_greedy=0.2)
    pass

qlearningGetBallFileName = "qlearningGetBall.npy"
if os.path.isfile(qlearningGetBallFileName) :
    qlearningGetBall = QLearning(env.col,env.row,9,qTableFileName=qlearningGetBallFileName,learning_rate=0.1, reward_decay=0.9, e_greedy=0.2)
else:
    qlearningGetBall = QLearning(env.col,env.row,9,learning_rate=0.1, reward_decay=0.9, e_greedy=0.2)
    pass
while True:
    env.render()
    
    if nextState is not None :
        if done :
            env.reset()
            
            i += 1
            if i > 100 :
                Episode += 1
                print("*** {} Episode ***".format(Episode*100))
                i = 0
                qlearningBall.SaveQTable(qlearningBallFileName)
                qlearningShoot.SaveQTable(qlearningShootFileName)
                qlearningGetBall.SaveQTable(qlearningGetBallFileName)
            # if reward == 10 or reward == 30 :
                # print(successAction)
            # successAction = []
        originalState = nextState

        originalIsShoot = nextIsShoot
        originalIsGetBall = NextIsGetBall
        if not originalIsShoot :
            if NextIsGetBall :
                action = qlearningGetBall.epsGreedy(originalState)
            else:
                action = qlearningBall.epsGreedy(originalState)
        else:
            action = qlearningShoot.epsGreedy(originalState)
            pass
    else:
        action = int(random.random()*1000) % 9
        pass
    state, reward, done, _ = env.step(action)
    nextState,nextIsShoot,NextIsGetBall = state
    # successAction.append(action)
    # if isShoot :
    #     print(action)
    #     i += 1
    #     if i > 100 :
    #         break

    
    if originalState is not None :
        if originalIsGetBall :
            qlearningGetBall.Learning(originalState,nextState,action,reward)
        elif originalIsShoot :
            qlearningShoot.Learning(originalState,nextState,action,reward)
        else:
            qlearningBall.Learning(originalState,nextState,action,reward)
            pass
    pass

