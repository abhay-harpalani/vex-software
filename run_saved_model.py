import torch
import torch.nn as nn
import torch.optim as optim
import gymnasium as gym
import random
import json

from q_network import QNetwork
from replay_buffer import ReplayBuffer

# BUFFER_SIZE = 100000
# BATCH_SIZE = 64
# GAMMA = 0.99
# LR = 1e-3
# EPSILON = 1.0
# EPSILON_MIN = 0.01
# EPSILON_DECAY = 0.995
# TARGET_UPDATE_FREQ = 10

# set render_mode=None if you want to train your model (will not open a pygame window and will just simulate it)
env = gym.make("LunarLander-v3", render_mode="human")

env.action_space.seed(42)
input_dim = env.observation_space.shape[0]
output_dim = 4

q_network = QNetwork(input_dim, output_dim)
q_network.load_state_dict(torch.load('q_network_4_layers.pth'))

# target_network = QNetwork(input_dim, output_dim)
# target_network.load_state_dict(q_network.state_dict())
# target_network.eval()
# 
# optimizer = optim.Adam(q_network.parameters(), lr=LR)
# loss_fn = nn.MSELoss()

# replay_buffer = ReplayBuffer(BUFFER_SIZE, BATCH_SIZE)

observation, info = env.reset(seed=40)
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

num_episodes = 5
for episode in range(num_episodes):
    state, _ = env.reset()
    state = torch.tensor(state, dtype=torch.float32)
    total_reward = 0

    while True:
        # if random.random() < EPSILON:
        #     action = env.action_space.sample()
        # else:
        with torch.no_grad():
            action = torch.argmax(q_network(state)).item()

        next_state, reward, terminated, truncated, _ = env.step(action)
        next_state = torch.tensor(next_state, dtype=torch.float32)
        done = terminated or truncated

        # replay_buffer.store((state, action, reward, next_state, done))

        state = next_state
        total_reward += reward

        # if replay_buffer.size() >= BATCH_SIZE:
        #     batch = replay_buffer.sample()
        #     states, actions, rewards, next_states, dones = zip(*batch)
        #
        #     states = torch.stack(states)
        #     actions = torch.tensor(actions).unsqueeze(1)
        #     rewards = torch.tensor(rewards, dtype=torch.float32).unsqueeze(1)
        #     next_states = torch.stack(next_states)
        #     dones = torch.tensor(dones, dtype=torch.float32).unsqueeze(1)
        #
        #     q_values = q_network(states).gather(1, actions)
        #     with torch.no_grad():
        #         max_next_q_values = target_network(next_states).max(1, keepdim=True)[0]
        #         target_q_values = rewards + GAMMA * max_next_q_values * (1 - dones)
        #
        #     loss = loss_fn(q_values, target_q_values)
        #
        #     optimizer.zero_grad()
        #     loss.backward()
        #     optimizer.step()

        if done:
            break

    # EPSILON = max(EPSILON_MIN, EPSILON * EPSILON_DECAY)
    #
    # if episode % TARGET_UPDATE_FREQ == 0:
    #     target_network.load_state_dict(q_network.state_dict())

    # print(f"Episode {episode}, Total Reward: {total_reward}, Epsilon: {EPSILON:.3f}")

env.close()
