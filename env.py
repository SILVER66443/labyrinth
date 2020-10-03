import logging
import random
import gym
import numpy as np

logger = logging.getLogger(__name__)


class LabyEnv(gym.Env):
    metadata = {}

    def __init__(self):

        self.gamma = 0.8  # 折扣因子
        self.viewer = None
        self.state = 1
        # 状态空间
        self.states = np.array(range(1, 26))

        # 动作空间
        self.actions = ['u', 'd', 'l', 'r']
        # action set

        # 终止状态
        # terminate=[]
        terminate = [2, 7, 12, 17, 9, 14, 19, 24, 25]
        self.end_states = dict()
        for i in terminate:
            self.end_states[i] = 1;

        # 回报空间
        punish = [2, 7, 12, 17, 9, 14, 19, 24]
        self.reward = dict()
        for s in self.states:

            if s in self.end_states:
                continue

            for a in self.actions:
                a_temp = self.stateMove(s, a)
                if a_temp in punish:
                    key = "%d_%s" % (s, a)
                    self.reward[key] = -1.0
                elif a_temp == 25:
                    key = "%d_%s" % (s, a)
                    self.reward[key] = 1.0

        self.x = [75, 175, 275, 375, 475]
        self.y = [75, 175, 275, 375, 475]

    # 状态转移方法
    def stateMove(self, s, a):

        if a == 'u' and s < 21:  # up
            new_s = s + 5
        elif a == 'd' and s > 5:  # down
            new_s = s - 5
        elif a == 'l' and (s - 1) % 5 != 0:  # left
            new_s = s - 1
        elif a == 'r' and s % 5 != 0:  # right
            new_s = s + 1
        else:
            new_s = -1
        return new_s

    #
    def getTerminal(self):
        return self.end_states

    def getGamma(self):
        return self.gamma

    def getState(self):
        return self.states

    def getActions(self):
        return self.actions

    def reset(self):
        self.state = 1
        return self.state

    def transform(self, state, action):
        key = "%d_%s" % (state, action)  # 将状态和动作组成字典的键值
        r = 0.0
        s = -1
        if key in self.reward:
            r = self.reward[key]
        # if self.stateMove(state,action) not in self.end_states:
        s = self.stateMove(state, action)
        return s, r

    def step(self, action):
        state = self.state
        if state in self.end_states:
            return state, 0, True, {}
        key = "%d_%s" % (state, action)
        next_state = self.stateMove(self.state, action)

        if next_state != 0:
            self.state = next_state

        is_terminate = False
        if next_state in self.end_states:
            is_terminate = True
        if key not in self.reward:
            r = 0.0
        else:
            r = self.reward[key]
        return self.state, r, is_terminate, {}

    def render(self, mode='human', close=False):
        if close:
            if self.viewer is not None:
                self.viewer.close()
                self.viewer = None
            return
        screen_width = 550
        screen_height = 550

        if self.viewer is None:
            from gym.envs.classic_control import rendering
            self.viewer = rendering.Viewer(screen_width, screen_height)

            self.line1 = rendering.Line((25, 25), (525, 25))
            self.line2 = rendering.Line((25, 125), (525, 125))
            self.line3 = rendering.Line((25, 225), (525, 225))
            self.line4 = rendering.Line((25, 325), (525, 325))
            self.line5 = rendering.Line((25, 425), (525, 425))
            self.line12 = rendering.Line((25, 525), (525, 525))
            self.line6 = rendering.Line((25, 25), (25, 525))
            self.line7 = rendering.Line((125, 25), (125, 525))
            self.line8 = rendering.Line((225, 25), (225, 525))
            self.line9 = rendering.Line((325, 25), (325, 525))
            self.line10 = rendering.Line((425, 25), (425, 525))
            self.line11 = rendering.Line((525, 25), (525, 525))

            # 创建墙
            self.kulo1 = rendering.make_circle(40)
            self.circletrans = rendering.Transform(translation=(175, 75))
            self.kulo1.add_attr(self.circletrans)
            self.kulo1.set_color(0, 0, 0)

            self.kulo2 = rendering.make_circle(40)
            self.circletrans = rendering.Transform(translation=(175, 175))
            self.kulo2.add_attr(self.circletrans)
            self.kulo2.set_color(0, 0, 0)

            self.kulo3 = rendering.make_circle(40)
            self.circletrans = rendering.Transform(translation=(175, 275))
            self.kulo3.add_attr(self.circletrans)
            self.kulo3.set_color(0, 0, 0)

            self.kulo4 = rendering.make_circle(40)
            self.circletrans = rendering.Transform(translation=(175, 375))
            self.kulo4.add_attr(self.circletrans)
            self.kulo4.set_color(0, 0, 0)

            self.kulo11 = rendering.make_circle(40)
            self.circletrans = rendering.Transform(translation=(375, 175))
            self.kulo11.add_attr(self.circletrans)
            self.kulo11.set_color(0, 0, 0)

            self.kulo22 = rendering.make_circle(40)
            self.circletrans = rendering.Transform(translation=(375, 275))
            self.kulo22.add_attr(self.circletrans)
            self.kulo22.set_color(0, 0, 0)

            self.kulo33 = rendering.make_circle(40)
            self.circletrans = rendering.Transform(translation=(375, 375))
            self.kulo33.add_attr(self.circletrans)
            self.kulo33.set_color(0, 0, 0)

            self.kulo44 = rendering.make_circle(40)
            self.circletrans = rendering.Transform(translation=(375, 475))
            self.kulo44.add_attr(self.circletrans)
            self.kulo44.set_color(0, 0, 0)

            # 终点
            self.gold = rendering.make_circle(40)
            self.circletrans = rendering.Transform(translation=(475, 475))
            self.gold.add_attr(self.circletrans)
            self.gold.set_color(1, 0.9, 0)
            # 机器人
            self.robot = rendering.make_circle(30)
            self.robotrans = rendering.Transform()
            self.robot.add_attr(self.robotrans)
            self.robot.set_color(0.8, 0.6, 0.4)

            self.viewer.add_geom(self.line1)
            self.viewer.add_geom(self.line2)
            self.viewer.add_geom(self.line3)
            self.viewer.add_geom(self.line4)
            self.viewer.add_geom(self.line5)
            self.viewer.add_geom(self.line6)
            self.viewer.add_geom(self.line7)
            self.viewer.add_geom(self.line8)
            self.viewer.add_geom(self.line9)
            self.viewer.add_geom(self.line10)
            self.viewer.add_geom(self.line11)
            self.viewer.add_geom(self.line12)
            self.viewer.add_geom(self.kulo1)
            self.viewer.add_geom(self.kulo2)
            self.viewer.add_geom(self.kulo3)
            self.viewer.add_geom(self.kulo4)
            self.viewer.add_geom(self.kulo11)
            self.viewer.add_geom(self.kulo22)
            self.viewer.add_geom(self.kulo33)
            self.viewer.add_geom(self.kulo44)
            self.viewer.add_geom(self.gold)
            self.viewer.add_geom(self.robot)

        if self.state is None: return None
        # self.robotrans.set_translation(self.x[self.state-1],self.y[self.state-1])
        self.robotrans.set_translation(self.x[self.state % 5 - 1], self.y[int((self.state - 1) / 5)])

        return self.viewer.render(return_rgb_array=mode == 'rgb_array')
