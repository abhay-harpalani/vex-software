import gymnasium as gym
import numpy as np

# set render_mode=None if you want to train your model (will not open a pygame window and will just simulate it)
env = gym.make("LunarLander-v3", render_mode="human")
env.action_space.seed(42)

observation, info = env.reset(seed=42)
print("env.observation_space", env.observation_space)
print("env.action_space", env.action_space)
print("env.observation_space.sample()", env.observation_space.sample())

# observation:
# [0]  x-coordinate
# [1]  y-coordinate
# [2]  x-velocity
# [3]  y-velocity
# [4]  angle
# [5]  angular velocity
# [6]  left leg touching ground
# [7]  right leg touching ground

# action space:
#  0 - do nothing
#  1 - left engine
#  2 - main engine
#  3 - right engine

for _ in range(1000):
    action = env.action_space.sample()
    observation, reward, terminated, truncated, info = env.step(action)
    print("observation", observation)
    if terminated or truncated:
        observation, info = env.reset()
env.close()
