import numpy as np
import random

class QLearning(object):
    
    def __init__(self, colLen, rowLen, actionLen, qTableFileName=None, learning_rate=0.01, reward_decay=0.9, e_greedy=0.9):
        self.colLen, self.rowLen = colLen,rowLen
        if not qTableFileName == None :
            self.qTable = np.load(qTableFileName)
        else:
            self.initQTable(colLen, rowLen, actionLen)
        # self.actions = actions      # a list
        self.lr = learning_rate     # 學習率
        self.gamma = reward_decay   # 奖励衰减
        self.epsilon = e_greedy     # 貪婪度
        pass
    
    def initQTable(self, colLen, rowLen, actionLen):
        self.qTable = np.zeros((colLen*rowLen,actionLen))
        pass
    def numberToStateConverter(self, stateNumber):
        maxY = len(self.qTable[0])
        x = stateNumber // maxY
        y = stateNumber % maxY
        return (x,y)
    def stateToNumberConverter(self, state):
        x,y = state
        number = x*self.rowLen + y
        return number
    def choose_action(self, observation):
        number = self.stateToNumberConverter(observation)
        observationTable = self.qTable[number]
        maxActions = np.where(observationTable == np.amax(observationTable))[0]
        
        if len(maxActions) > 1 :
            i = int(random.random()*1000) % len(maxActions)
            action = maxActions[i]
        else:
            action = maxActions[0]
            pass
        return action
    def epsGreedy(self, observation):
        isRandom = self.epsilon > random.random()
        action = None
        if isRandom :
            action = int(random.random()*1000) % 9
        else:
            action = self.choose_action(observation)
            pass
        return action
    def Learning(self, oldState, newState, actionNumber, reward):
        oldStateNumber = self.stateToNumberConverter(oldState)
        newStateNumber = self.stateToNumberConverter(newState)
        maxQ = self.qTable[newStateNumber][self.choose_action(newState)]
        self.qTable[oldStateNumber][actionNumber] = self.qTable[oldStateNumber][actionNumber] + self.lr*(reward + self.gamma*maxQ - self.qTable[oldStateNumber][actionNumber])
        pass
    pass
    def SaveQTable(self, fileName):
        np.save(fileName,self.qTable)
        pass