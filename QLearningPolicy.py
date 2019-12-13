from window import basketballEnv
from QLearning import QLearning
import random
import time

env = basketballEnv("v0")
newState = None
oldState = None
speed = 0.1
done = False
qlearning = QLearning(env.col,env.row,9,learning_rate=0.01, reward_decay=0.9, e_greedy=0.5)
while True:
    env.render()
    
    if newState is not None :
        if done :
            env.reset()
            print(qlearning.qTable)
        oldState = newState
        action = qlearning.epsGreedy(oldState)
    else:
        action = int(random.random()*8)
        pass
    newState, reward, done, _ = env.step(action)
    time.sleep(speed)
    if oldState is not None :
        qlearning.Learning(oldState,newState,action,reward)
    pass

# print(qlearning.stateToNumberConverter((1,1)))