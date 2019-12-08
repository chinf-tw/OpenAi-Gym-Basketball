import math
import time
import numpy as np
class basketballEnv(object):
    """
    Actions:
        Type: Discrete(2)
        Num	Action
        0	Push agent to the left
        1	Push agent to the right
        2   Push agent to the up
        3   Push agent to the down
        4   Agent dribble the ball to left
        5   Agent dribble the ball to right
        6   Agent dribble the ball to up
        7   Agent dribble the ball to down

    """
    def __init__(self,v="v0"):
        self.viewer = None

        self.screen_width = 600
        self.screen_height = 400
        if v == "v0":
            self.col = 9
            self.row = 6
        elif v == "v1":
            self.col = 18
            self.row = 12
        elif v == "v2":
            self.col = 36
            self.row = 24
        
        self.block_width = self.screen_width / self.col
        self.block_height = self.screen_height / self.row
        self.agentState = (0,0)
        self.basketballState = (0,self.row - 1)
        self.basketState = (self.col-1, int(self.row/2))

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
        
        

    def step(self,action):
        agentX,agentY = self.agentState
        ballX,ballY = self.basketballState
        if action < 4 :
            if action == 0:
                agentX -= 1
            elif action == 1:
                agentX += 1
            elif action == 2:
                agentY += 1
            elif action == 3:
                agentY -= 1
        else:
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
        done = False
        if agentX < self.col and agentY < self.row and agentX >= 0 and agentY >= 0 :
            self.agentState = (agentX,agentY)
            self.basketballState = (ballX,ballY)
        else:
            done = True
            pass
        return np.array(self.agentState), done

    def render(self, mode='human'):
        screen_width = self.screen_width
        screen_height = self.screen_height
        col = self.col
        row = self.row
        
        

        agentWidth = self.block_width * 0.8
        agentHeight = self.block_height * 0.8
        minRadius = min(agentWidth,agentHeight)/2

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
            l,r,t,b = -agentWidth/2, agentWidth/2, agentHeight/2, -agentHeight/2
            agent = rendering.FilledPolygon([(l,b), (l,t), (r,t), (r,b)])
            self.agenttrans = rendering.Transform()
            agent.add_attr(self.agenttrans)
            self.viewer.add_geom(agent)

            # make the basketball
            basketball = self.viewer.draw_circle(minRadius)
            self.basketballtrans = rendering.Transform()
            basketball.add_attr(self.basketballtrans)
            basketball.set_color(222/255,194/255,31/255)
            self.viewer.add_geom(basketball)

            # make the basket
            bottomx,bottomy = minRadius*math.cos(math.pi/12),minRadius*0.5
            basket = rendering.FilledPolygon([(0,minRadius), (-bottomx,-bottomy), (bottomx,-bottomy)])
            self.baskettrans = rendering.Transform(self.stateToPosition(self.basketState))
            basket.add_attr(self.baskettrans)
            self.viewer.add_geom(basket)

        
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
        self.agentState = (0,0)
        self.basketballState = (0,self.row - 1)
        pass

env = basketballEnv("v0")
import random
state = None

speed = 0.1

for i in range(10):
    env.render()
    if state is not None :
        print("action: {} , state: {}".format(action,state))
        if done :
            env.reset()
    if i < 5 :
        action = 2
    else:
        action = 5
        pass
    state, done = env.step(action)
    time.sleep(speed)
    
for _ in range(100):
    
    env.render()
    if state is not None:
        print("action: {} , state: {}".format(action,state))
        if done :
            env.reset()
    action = int(random.random()*7)
    time.sleep(speed)
    
    state, done = env.step(action)
    
    pass
env.close()