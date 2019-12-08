import time
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
        self.state = (self.block_width/2,self.block_height/2)
    def step(self,action):
        
        x = 0
        y = 0
        if action == 0:
            x = -self.block_width
        elif action == 1:
            x = self.block_width
        elif action == 2:
            y = self.block_height
        elif action == 3:
            y = -self.block_height
        state = (self.state[0] + x,self.state[1] + y)
        self.state = state
    def render(self, mode='human'):
        screen_width = self.screen_width
        screen_height = self.screen_height
        col = self.col
        row = self.row
        
        

        agentWidth = self.block_width * 0.8
        agentHeight = self.block_height * 0.8
        minRadius = min(agentWidth,agentHeight)/2
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
            self.basketballtrans = rendering.Transform((self.block_width/2,self.block_height/2 + (self.row-1)*self.block_height))
            basketball.add_attr(self.basketballtrans)
            basketball.set_color(222/255,194/255,31/255)
            self.viewer.add_geom(basketball)

            # make the basket



        
        if self.state is None: return None

        x = self.state
        cartx,carty = x
        self.agenttrans.set_translation(cartx, carty)
        return self.viewer.render(return_rgb_array = mode=='rgb_array')
    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None

env = testEnv("v0")
import random
for i in range(6):
    env.render()
    if i < 4 :
        action = 1
    else:
        action = 2
        pass
    env.step(action)
    time.sleep(0.5)
for _ in range(10):
    
    env.render()
    action = int(random.random()*3)
    
    env.step(action)
    time.sleep(0.5)
    pass
env.close()