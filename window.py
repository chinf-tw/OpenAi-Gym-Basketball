import math
import time
import numpy as np
import gym
import random
class basketballEnv(gym.Env):
    """
    Description:
        In this assignment, you will compare the performance of several reinforcement learning algorithms in a simple basketball domain. You will also investigate the impact of different parameters on the performance of the reinforcement learning algorithm.

    Version of block number:
        version     blockColumn     blockRow
        v0:         9               6
        v1:         18              12
        v2:         36              24

    Observation: 
        Type: Box(2)
        Num	Observation                 Min         Max
        0	agent state x               0           blockColumn
        1	agent state y               0           blockRow

    Actions:
        Type: Discrete(9)
        Movement:
            Num	Action
            0	Push agent to the left
            1	Push agent to the right
            2   Push agent to the up
            3   Push agent to the down
        Ball Handling:
            Num	Action
            4   Agent dribble the ball to left
            5   Agent dribble the ball to right
            6   Agent dribble the ball to up
            7   Agent dribble the ball to down
        Shoot:
            Num	Action
            8   Agent shoot the ball

    Shoot:
        success rate:
            Note: the distance is Euclidean distance between the robot and the basket.

            1. Distance is less than 1 cell:        90%
            2. Distance is between 1 and 3 cell:    66%
            3. Distance is between 3 and 4 cell:    10%

        If the shot is unsuccessful, then the ball will be placed at location (0.8 * WIDTH, HEIGHT//2).


    Reward:
        Note: the distance is Euclidean distance between the robot and the basket.

        Succeed to shoot:
            1. Distance is less than 1 cell:        +10
            2. Distance is between 1 and 3 cell:    +10
            3. Distance is between 3 and 4 cell:    +30
        
        If the robot leaves the playing field, it will receive a penalty of -100.


    Starting State:
        Agent       is on the (0,0)
        Basketball  is on the (0,blockRow)
        basket      is on the (blockColumn*0.8,blockRow/2)

    Episode Termination:
        The episode will end if the robot scores a point or if the robot leaves the playing field.
    """
    def __init__(self,v="v0"):
        self.viewer = None

        self.screen_width = 600
        self.screen_height = 400
        if v == "v0":
            self.col = 9
            self.row = 6
            self.numberOfOpponent = 5
        elif v == "v1":
            self.col = 18
            self.row = 12
            self.numberOfOpponent = 50
        elif v == "v2":
            self.col = 36
            self.row = 24
            self.numberOfOpponent = 250
        
        self.block_width = self.screen_width / self.col
        self.block_height = self.screen_height / self.row

        # init all state
        self.initState()
        # init opponentsState
        self.opponentsState = []
        while len(self.opponentsState) < self.numberOfOpponent:
            x = int(random.random()*self.col - 1)
            y = int(random.random()*self.row - 1)
            if (x,y) not in self.opponentsState and (x,y) not in [self.agentState,self.basketballState] :
                self.opponentsState.append((x,y))
            pass

        if len(self.opponentsState) != self.numberOfOpponent :
            raise ValueError("opponents len isn't equal ")

        # init positionTable
        self.positionTable = np.zeros((2, self.row, self.col))
        for r in range(self.row):
            for c in range(self.col):
                for i in range(2):
                    # i is x or y coordinate
                    # r id number of x axis
                    # c id number of y axis
                    if i == 0 :
                        # for x coordinate
                        self.positionTable[i][r][c] = (self.block_width/2) + c*self.block_width
                    else:
                        # for y coordinate
                        self.positionTable[i][r][c] = (self.block_height/2) + r*self.block_height
                        pass
                    pass
                pass
            pass
        pass
        
    def initState(self):
        # self.agentState = (0,0)
        self.agentState = (int(random.random()*self.col - 1),int(random.random()*self.row - 1))
        self.basketballState = (0,self.row - 1)
        self.basketState = (self.col-1, (self.row-1)/2)
        

    def step(self,action):
        agentX,agentY = self.agentState
        ballX,ballY = self.basketballState
        reward = 0
        done = False
        # Movement
        if action < 4 :
            if action == 0:
                agentX -= 1
            elif action == 1:
                agentX += 1
            elif action == 2:
                agentY += 1
            elif action == 3:
                agentY -= 1
        # Ball Handling
        elif action < 8:
            if self.agentState == self.basketballState :
                if action == 4:
                    agentX -= 1
                    ballX -= 1
                elif action == 5:
                    agentX += 1
                    ballX += 1
                elif action == 6:
                    agentY += 1
                    ballY += 1
                elif action == 7:
                    agentY -= 1
                    ballY -= 1
                    pass
                pass
            pass
        # Shoot
        elif action == 8 and self.agentState == self.basketballState:
            basketX,basketY = self.basketState
            distance = math.sqrt((agentX-basketX)**2 + (agentY-basketY)**2)
            # Distance is less than 1 cell
            if distance < 1 :
                # success is +10
                if random.random() <= 0.9 :
                    reward = 10
                    # The episode will end if the robot scores a point.
                    done = True
                else:
                    self.shootfail()
                    pass
                pass
            # Distance is between 1 and 3 cell
            elif distance >= 1 and distance < 3:
                if random.random() <= 0.66 :
                    # success is +10
                    reward = 10
                    # The episode will end if the robot scores a point.
                    done = True
                else:
                    self.shootfail()
                    pass
            # Distance is between 3 and 4 cell
            elif distance >= 3 and distance < 4:
                if random.random() <= 0.10 :
                    # success is +30
                    reward = 30
                    # The episode will end if the robot scores a point.
                    done = True
                else:
                    self.shootfail()
                    pass
            else:
                self.shootfail()
            return np.array(self.agentState),reward, done, {}

        # Determine if the action is still in range
        isCorrectMove = (agentX < self.col) and (agentY < self.row) and (agentX >= 0 and agentY >= 0)
        done = not isCorrectMove
        if done :
            # If the robot leaves the playing field, it will receive a penalty of -100.
            # The episode will end if the robot leaves the playing field.
            reward = -100
            return np.array(self.agentState), reward, done, {}

        # Determine if the action is still in Observation
        isHitObservation = (agentX,agentY) in self.opponentsState
        # 
        # isMoveInBasket = (agentX,agentY) in self.basketState
        if isCorrectMove and not isHitObservation :
            self.agentState = (agentX,agentY)
            self.basketballState = (ballX,ballY)
            pass

        return np.array(self.agentState), reward, done, {}

    def shootfail(self):
        self.basketballState = (int(self.col*0.8),self.row//2)


    def render(self, mode='human'):
        screen_width = self.screen_width
        screen_height = self.screen_height
        col = self.col
        row = self.row
        
        

        personWidth = self.block_width * 0.8
        personHeight = self.block_height * 0.8
        minRadius = min(personWidth,personHeight)/2

        # make person point
        l,r,t,b = -personWidth/2, personWidth/2, personHeight/2, -personHeight/2
        personPoint = [(l,b), (l,t), (r,t), (r,b)]

        # init viewer
        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(screen_width, screen_height)
            
            # draw the col line
            for i in range(1,col):
                x = i*screen_width/col
                lineGeom = self.viewer.draw_line(start=(x,0),end=(x,screen_height))
                self.viewer.add_geom(lineGeom)
                pass

            # draw the col line
            for i in range(1,row):
                y = i*screen_height/row
                lineGeom = self.viewer.draw_line(start=(0,y),end=(screen_width,y))
                self.viewer.add_geom(lineGeom)
                pass
            
            # make the agent
            agent = rendering.FilledPolygon(personPoint)
            self.agenttrans = rendering.Transform()
            agent.add_attr(self.agenttrans)
            agent.set_color(195/255, 41/255, 109/255)
            self.viewer.add_geom(agent)

            # make the basketball
            basketball = self.viewer.draw_circle(minRadius)
            self.basketballtrans = rendering.Transform()
            basketball.add_attr(self.basketballtrans)
            basketball.set_color(222/255,194/255,31/255)
            self.viewer.add_geom(basketball)

            # make the basket
            # bottomx,bottomy = minRadius*math.cos(math.pi/12),minRadius*0.5
            # basket = rendering.FilledPolygon([(0,minRadius), (-bottomx,-bottomy), (bottomx,-bottomy)])
            basket = self.viewer.draw_circle(minRadius*1.4)
            self.baskettrans = rendering.Transform((self.screen_width,self.screen_height/2))
            basket.add_attr(self.baskettrans)
            basket.set_color(61/255,225/255,149/255)
            self.viewer.add_geom(basket)

            # make the Opponent
            # the size and shape is equal the agent
            self.opponenttrans = []
            for opponentPosition in self.opponentsState:
                opponent = rendering.FilledPolygon(personPoint)
                opponenttran = rendering.Transform(self.stateToPosition(opponentPosition))
                opponent.add_attr(opponenttran)
                self.opponenttrans.append(opponenttran)
                self.viewer.add_geom(opponent)
                pass

        
        if self.agentState is None: return None
        
        # update agent transform
        x,y = self.stateToPosition(self.agentState)
        self.agenttrans.set_translation(x,y)

        # update basketball transform
        x,y = self.stateToPosition(self.basketballState)
        self.basketballtrans.set_translation(x,y)
        return self.viewer.render(return_rgb_array = mode=='rgb_array')
    def stateToPosition(self,state):
        # positionTable[x or y coordinate][y axis][x axis]
        x,y = (self.positionTable[0][state[1]][state[0]],self.positionTable[1][state[1]][state[0]])
        return (x,y)
    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None
    def reset(self):
        self.initState()
        for i in range(len(self.opponenttrans)) :
            x,y = self.stateToPosition(self.opponentsState[i])
            self.opponenttrans[i].set_translation(x,y)
        pass