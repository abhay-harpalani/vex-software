"""
blackjack simulation
"""

import gymnasium as gym
gym.make('Blackjack-v1', natural=False, sab=False)

env = gym.make("Blackjack-v1", render_mode="human")
env.action_space.seed(42)
observation, info = env.reset(seed=42)

for _ in range(1000):
    # choose random action from action space
    # (edit this part)
    action = env.action_space.sample()

    # take the chosed action and get the next state and reward
    observation, reward, terminated, truncated, info = env.step(action)

    # if we have reached an end state, reset the environment
    if terminated or truncated:
        observation, info = env.reset()
env.close()
