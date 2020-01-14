from window import basketballEnv
from QLearning import QLearning
from fileHandler import opponentsStateEncode,TrainingInfo

import random
import time
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-d","--directory", default="v0-Qlearning-model", help="Use the directory to place data model (default is 'v0-Qlearning-model')")
parser.add_argument("-v","--version", default="v0", help="Choose the version to train model (now have v0,v1,v2)(default is 'v0')")
parser.add_argument("-e","--epsGreedy", type=float, default=0.1, help="Give number of eps(default is 0.1)")
parser.add_argument("--end", type=int, default=-1, help="Expected number of operations, if number is -1 then not end operations(default is -1)")
args = parser.parse_args()

directory = args.directory
version = args.version

if not os.path.isdir(directory) :
    print("add the {} directory".format(directory))
    os.mkdir(directory)
    print("choose the {} version".format(version))
else:
    print("Great! {} is exists".format(directory))
    pass

opponentsStateFileName = "{}/{}.opponents".format(directory,version)
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
eps = args.epsGreedy



r = input("Do you want to Render?")
isRender = int(r)
if isRender :
    updateEpisode = 10
else:
    updateEpisode = 100
    
trainInfo = TrainingInfo("{}/{}_TrainingInfo.csv".format(directory,version))
# successAction = []
reward = None

if os.path.isfile(opponentsStateFileName) :
    env = basketballEnv(version,opponentsStateFileName)
else:
    env = basketballEnv(version)
    opponentsStateEncode(env.GetOpponentsState(),opponentsStateFileName)



qlearningBallFileName = "{}/{}_qlearningBall.npy".format(directory,version)
if os.path.isfile(qlearningBallFileName) :
    qlearningBall = QLearning(env.col,env.row,9,qTableFileName=qlearningBallFileName,learning_rate=0.1, reward_decay=0.9, eps=eps)
else:
    qlearningBall = QLearning(env.col,env.row,9,learning_rate=0.1, reward_decay=0.9, eps=eps)
    pass

qlearningShootFileName = "{}/{}_qlearningShoot.npy".format(directory,version)
if os.path.isfile(qlearningShootFileName) :
    qlearningShoot = QLearning(env.col,env.row,9,qTableFileName=qlearningShootFileName,learning_rate=0.1, reward_decay=0.9, eps=eps)
else:
    qlearningShoot = QLearning(env.col,env.row,9,learning_rate=0.1, reward_decay=0.9, eps=eps)
    pass

qlearningGetBallFileName = "{}/{}_qlearningGetBall.npy".format(directory,version)
if os.path.isfile(qlearningGetBallFileName) :
    qlearningGetBall = QLearning(env.col,env.row,9,qTableFileName=qlearningGetBallFileName,learning_rate=0.1, reward_decay=0.9, eps=eps)
else:
    qlearningGetBall = QLearning(env.col,env.row,9,learning_rate=0.1, reward_decay=0.9, eps=eps)
    pass
while args.end == -1 or args.end:
    
    if isRender :
        env.render()
    
    if nextState is not None :
        if done :
            env.reset()
            
        i += 1
        if i >= updateEpisode :
            

            trainInfo.trainingInfo["Episode"] += updateEpisode
            Episode = trainInfo.trainingInfo["Episode"]

            trainInfo.trainingInfo["RewardSum"] = round(rewardSum/updateEpisode,3)
            trainInfo.Save()
            # print(round(trainInfo.trainingInfo,3))
            trainInfo.InitBadInfoCount()
            print("*** {} Episode ***".format(Episode))

            i = 0
            rewardSum = 0


            qlearningBall.SaveQTable(qlearningBallFileName)
            qlearningShoot.SaveQTable(qlearningShootFileName)
            qlearningGetBall.SaveQTable(qlearningGetBallFileName)

            # if Episode < 1000 :
            #     qlearningBall.epsilon = 0.1 + 0.5/(1+Episode)
            #     qlearningShoot.epsilon = 0.1 + 0.5/(1+Episode)
            #     qlearningGetBall.epsilon = 0.1 + 0.5/(1+Episode)
            

            if trainInfo.IsEnd() :
                env.close()
                break
                
        originalState = nextState

        originalIsShoot = nextIsShoot
        originalIsGetBall = NextIsGetBall
        if not originalIsShoot :
            if NextIsGetBall :
                action = qlearningGetBall.epsGreedySearch(originalState)
            else:
                action = qlearningBall.epsGreedySearch(originalState)
        else:
            action = qlearningShoot.epsGreedySearch(originalState)
            pass
    else:
        action = int(random.random()*1000) % 9
        pass
    state, reward, done, info = env.step(action)
    nextState,nextIsShoot,NextIsGetBall = state
    rewardSum += reward
    for title in trainInfo.trainingInfo :
        if title in info :
            if info[title] :
                trainInfo.trainingInfo[title] += 1/updateEpisode
        

    
    if originalState is not None :
        if originalIsGetBall :
            qlearningGetBall.Learning(originalState,nextState,action,reward)
        elif originalIsShoot :
            qlearningShoot.Learning(originalState,nextState,action,reward)
        else:
            qlearningBall.Learning(originalState,nextState,action,reward)
            pass
        if not args.end == -1:
            args.end -= 1
    pass

