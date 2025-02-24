import random
from collections import deque

class ReplayBuffer:
    def __init__(self, buffer_size, batch_size):
        self.buffer = deque(maxlen=buffer_size)
        self.batch_size = batch_size
    def store(self, experience):
        self.buffer.append(experience)
    def sample(self):
        return random.sample(self.buffer, self.batch_size)
    def size(self):
        return len(self.buffer)