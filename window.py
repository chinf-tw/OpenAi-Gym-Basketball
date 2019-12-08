import math
import time
import numpy as np
class testEnv(object):
    """
    Actions:
        Type: Discrete(2)
        Num	Action
        0	Push cart to the left
        1	Push cart to the right
        2   Push cart to the up
        3   Push cart to the down

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
        x,y = self.agentState
        if action == 0:
            x -= 1
        elif action == 1:
            x += 1
        elif action == 2:
            y += 1
        elif action == 3:
            y -= 1
        if x <= self.col or y <= self.row :
            self.agentState = (x,y)
        return self.agentState

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

env = testEnv("v0")
import random
state = None
for i in range(6):
    env.render()
    if state :
        print(state)
    if i < 4 :
        action = 1
    else:
        action = 2
        pass
    state = env.step(action)
    time.sleep(0.5)
for _ in range(10):
    
    env.render()
    action = int(random.random()*3)
    time.sleep(2)
    env.step(action)
    
    pass
env.close()