from window import basketballEnv
from QLearning import QLearning
import random
import time

env = basketballEnv("v0")
newState = None
oldState = None
speed = 0.1
done = False
isShoot = False

qlearningBall = QLearning(env.col,env.row,9,learning_rate=0.1, reward_decay=0.9, e_greedy=0.2)
qlearningShoot = QLearning(env.col,env.row,9,learning_rate=0.1, reward_decay=0.9, e_greedy=0.2)
qlearningGetBall = QLearning(env.col,env.row,9,learning_rate=0.1, reward_decay=0.9, e_greedy=0.2)
i = 0
successAction = []
reward = None
while True:
    env.render()
    
    if newState is not None :
        if done :
            env.reset()
            
            i += 1
            if i > 100 :
                print("***100次了***")
                i = 0
            if reward == 10 or reward == 30 :
                print(successAction)
            successAction = []
            # if not isShoot :
            #     print(qlearningBall.qTable.astype(int))
            # else:
            #     print(qlearningShoot.qTable.astype(int))
            #     pass
        oldState = newState


        if not isShoot :
            action = qlearningBall.epsGreedy(oldState)
        else:
            action = qlearningShoot.epsGreedy(oldState)
            pass
    else:
        action = int(random.random()*1000) % 9
        pass
    state, reward, done, _ = env.step(action)
    newState,isShoot,isGetBall = state
    successAction.append(action)
    # if isShoot :
    #     print(action)
    #     i += 1
    #     if i > 100 :
    #         break

    
    if oldState is not None :
        if isGetBall :
            qlearningGetBall.Learning(oldState,newState,action,reward)
        elif isShoot :
            qlearningShoot.Learning(oldState,newState,action,reward)
        else:
            qlearningBall.Learning(oldState,newState,action,reward)
            pass
    pass

