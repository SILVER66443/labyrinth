from random import sample

import gym
import time

env = gym.make('labyrinth-v0')
env.reset()
env.render()
time.sleep(1)
action = ['u', 'u', 'u', 'u', 'r', 'r', 'd', 'd', 'd', 'd', 'r', 'r', 'u', 'u', 'u', 'u']
for a in action:
    temp, r, done, error = env.step(a)
    env.render()
    time.sleep(1)
    if done:
        break

time.sleep(5)
env.close()
