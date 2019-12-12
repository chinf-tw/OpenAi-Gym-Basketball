
from window import basketballEnv



env = basketballEnv("v0")

key = ''
while True:
    env.render()
    action = input("action: ")
    if action == 'q':
        break
    state, reward, done, _ = env.step(int(action))
    print("action: {} , state: {} , reward: {}".format(action,state,reward))
    if done :
        env.reset()
    pass
env.close()