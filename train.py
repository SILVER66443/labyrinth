import gym
import random
import time
import os

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1"


env = gym.make('labyrinth-v0')
print(env.env)
print(env.env.states)
STEP = 100


class Train:
    def __init__(self, laby_mdp):
        # 初始化v(s)
        self.v = dict()
        for s in laby_mdp.states:
            self.v[s] = 0
        self.pi = dict()
        for state in laby_mdp.states:
            self.pi[state]=self.get_action(state,laby_mdp)
    # 得到行为
    def get_action(self, state, laby_mdp):
        a_temp = []
        for a in laby_mdp.actions:
            s_temp = laby_mdp.stateMove(state, a)
            if s_temp != -1:
                a_temp.append(a)
        return random.choice(a_temp)

    def policy_iterate(self, laby_mdp):
        for i in range(1000):
            self.policy_evaluate(laby_mdp)
            self.policy_improve(laby_mdp)

    def policy_evaluate(self, laby_mdp):
        for i in range(1000):
            delta = 0.0
            for state in laby_mdp.states:
                if state in laby_mdp.end_states: continue

                # 得到一个随机的action
                action = self.pi[state]
                # 状态矩阵、下一个状态、reward
                s, r = laby_mdp.transform(state, action)

                if s != -1:
                    new_v = r + laby_mdp.gamma * self.v[s]
                    delta += abs(self.v[state] - new_v)
                    self.v[state] = new_v

            # 收敛就退出评估
            if (delta < 1e-6):
                print(" *done ")
                break

    def policy_improve(self, laby_mdp):
        for state in laby_mdp.states:
            if state in laby_mdp.end_states:
                continue
            a1 = self.get_action(state, laby_mdp)  # grid_mdp.actions[0]
            s, r = laby_mdp.transform(state, a1)
            if s != -1:
                v1 = r + laby_mdp.gamma * self.v[s]
                for action in laby_mdp.actions:
                    s, r = laby_mdp.transform(state, action)
                    if s != -1:
                        if v1 < r + laby_mdp.gamma * self.v[s]:
                            a1 = action
                            v1 = r + laby_mdp.gamma * self.v[s]
                self.pi[state] = a1

    def action(self, state):
        return self.pi[state]


state = env.reset()
gm = env.env
train = Train(gm)

train.policy_iterate(gm)

total_reward = 0
for j in range(STEP):
    env.render()
    a = train.action(state)  # direct action for test
    state, reward, done, _ = env.step(a)
    total_reward += reward
    time.sleep(0.5)
    if done:
        env.render()
        break
