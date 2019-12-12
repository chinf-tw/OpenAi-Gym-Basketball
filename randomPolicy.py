from window import basketballEnv
import random
import time
env = basketballEnv("v0")

state = None

speed = 0.1


for _ in range(1000):
    
    env.render()
    if state is not None:
        # print("action: {} , state: {}".format(action,state))
        if done :
            env.reset()
    action = int(random.random()*7)
    time.sleep(speed)
    
    state, reward, done, _ = env.step(action)
    
    pass