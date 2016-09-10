# -*- coding: utf-8 -*-
import pg
import gym
import numpy as np


GAMMA = 0.98

def get_episode_returns(episode_rewards,final_value,gamma=GAMMA):
    n = len(episode_rewards)
    episode_returns = [0. for i in range(n)]
    episode_returns[-1] = episode_rewards[-1] + gamma * final_value
    for i in range(n-2,-1,-1):
        episode_returns[i] = episode_rewards[i] + gamma* episode_returns[i+1]
    return episode_returns
assert get_episode_returns([1,0,0,4],1,0.5) == [1 + 0.5**3 * 4 + 0.5**4,0.5**2 * 4 + 0.5**3, 0.5 * 4 + 0.5**2, 4 + 0.5]

env = gym.make("CartPole-v0") # 環境を立ち上げる 
ac = pg.PolicyNet(4,15,2) 






l = []
tmax = 300
for k in range(1000):
    #tmax = min(tmax+1,100)                                                                                                                                                                                 
    episode_rewards = []
    episode_actions = []
    episode_states = []
    state = env.reset()
    for epi in range(tmax):
        env.render()
        episode_states.append(state)
        action = ac.getAction(state)
        state, reward, terminal, info = env.step(np.argmax(action))
        episode_rewards.append(reward)
        episode_actions.append(action)
        if terminal or epi == tmax - 1:
            if terminal:
                final_value = 0.
            elif epi == tmax - 1:
                final_value = ac.getValue(state)[0]
            episode_returns = get_episode_returns(episode_rewards,final_value)
            ac.trainNetworkV(episode_states,episode_returns)
            ac.trainNetworkP(episode_states,episode_actions,episode_returns)
            eptr = sum(episode_rewards)
            print k,eptr
            l.append(eptr)
            break

from matplotlib import pyplot as plt
import pandas
plt.plot(pandas.rolling_mean(np.array(l),100,1))
plt.show()