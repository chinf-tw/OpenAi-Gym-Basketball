from window import basketballEnv
from QLearning import QLearning
import random
import time

env = basketballEnv("v0")
nextState = None
originalState = None
speed = 0.1
done = False
nextIsShoot = False
originalIsShoot = False

NextIsGetBall = False
originalIsGetBall = False

qlearningBall = QLearning(env.col,env.row,9,learning_rate=0.1, reward_decay=0.9, e_greedy=0.2)
qlearningShoot = QLearning(env.col,env.row,9,learning_rate=0.1, reward_decay=0.9, e_greedy=0.2)
qlearningGetBall = QLearning(env.col,env.row,9,learning_rate=0.1, reward_decay=0.9, e_greedy=0.2)
i = 0
successAction = []
reward = None
while True:
    env.render()
    
    if nextState is not None :
        if done :
            env.reset()
            
            i += 1
            if i > 100 :
                print("***100次了***")
                i = 0
            if reward == 10 or reward == 30 :
                print(successAction)
            successAction = []
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
    successAction.append(action)
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

