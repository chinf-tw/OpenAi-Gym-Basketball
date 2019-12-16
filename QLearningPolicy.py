from window import basketballEnv
from QLearning import QLearning
from fileHandler import opponentsStateEncode,TrainingInfo

import random
import time
import os

v0_dir = "./v0-Qlearning-model"
version = "v0"
opponentsStateFileName = "{}/{}.opponents".format(v0_dir,version)
nextState = None
originalState = None
speed = 0.1
done = False
nextIsShoot = False
originalIsShoot = False

NextIsGetBall = False
originalIsGetBall = False

i = 0
rewardSum = 0

isRender = True
if isRender :
    updateEpisode = 100
else:
    updateEpisode = 1000
    
trainInfo = TrainingInfo("{}/{}_TrainingInfo.json".format(v0_dir,version))
# successAction = []
reward = None

if os.path.isfile(opponentsStateFileName) :
    env = basketballEnv(version,opponentsStateFileName)
else:
    env = basketballEnv(version)
    opponentsStateEncode(env.GetOpponentsState(),opponentsStateFileName)



qlearningBallFileName = "{}/{}_qlearningBall.npy".format(v0_dir,version)
if os.path.isfile(qlearningBallFileName) :
    qlearningBall = QLearning(env.col,env.row,9,qTableFileName=qlearningBallFileName,learning_rate=0.1, reward_decay=0.9, e_greedy=0.1)
else:
    qlearningBall = QLearning(env.col,env.row,9,learning_rate=0.1, reward_decay=0.9, e_greedy=0.1)
    pass

qlearningShootFileName = "{}/{}_qlearningShoot.npy".format(v0_dir,version)
if os.path.isfile(qlearningShootFileName) :
    qlearningShoot = QLearning(env.col,env.row,9,qTableFileName=qlearningShootFileName,learning_rate=0.1, reward_decay=0.9, e_greedy=0.2)
else:
    qlearningShoot = QLearning(env.col,env.row,9,learning_rate=0.1, reward_decay=0.9, e_greedy=0.1)
    pass

qlearningGetBallFileName = "{}/{}_qlearningGetBall.npy".format(v0_dir,version)
if os.path.isfile(qlearningGetBallFileName) :
    qlearningGetBall = QLearning(env.col,env.row,9,qTableFileName=qlearningGetBallFileName,learning_rate=0.1, reward_decay=0.9, e_greedy=0.1)
else:
    qlearningGetBall = QLearning(env.col,env.row,9,learning_rate=0.1, reward_decay=0.9, e_greedy=0.8)
    pass
while True:
    if isRender :
        env.render()
    
    if nextState is not None :
        if done :
            env.reset()
            
            i += 1
            if i > updateEpisode :
                

                trainInfo.Episode += updateEpisode
                trainInfo.RewardSum = rewardSum
                trainInfo.Save()

                print("*** {} Episode ***".format(trainInfo.Episode))

                i = 0
                rewardSum = 0


                qlearningBall.SaveQTable(qlearningBallFileName)
                qlearningShoot.SaveQTable(qlearningShootFileName)
                qlearningGetBall.SaveQTable(qlearningGetBallFileName)

                if trainInfo.IsEnd() :
                    env.close()
                    break
                
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
    rewardSum += reward
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

