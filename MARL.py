import gym
import numpy as np
import random
import matplotlib.pyplot as plt

class CrackDetectionEnv(gym.Env):
    def __init__(self):
        super(CrackDetectionEnv, self).__init__()
        self.action_space = gym.spaces.Discrete(3)  # Actions: Detect, Ignore, Review
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(4,), dtype=np.float32)
        self.state = np.random.rand(4)  # Simulated state
        self.total_cracks = 10
        self.detected_cracks = 0
        self.step_count = 0
        self.max_steps = 50  # Max steps per episode

    def reset(self):
        self.state = np.random.rand(4)
        self.detected_cracks = 0
        self.step_count = 0
        return self.state

    def step(self, action):
        self.step_count += 1
        reward = 0
        
        if action == 0:  # Detect
            is_crack = self.detect_crack()
            if is_crack:
                reward = 1  # Positive reward for correct detection
                self.detected_cracks += 1
            else:
                reward = -1  # Negative reward for false detection

        elif action == 1:  # Ignore
            reward = -1  # Negative reward for ignoring potential cracks

        elif action == 2:  # Review
            reward = self.review_crack()  # Reward for reviewing cracks

        self.state = np.random.rand(4)  # Update state
        done = self.detected_cracks >= self.total_cracks or self.step_count >= self.max_steps  # End conditions
        return self.state, reward, done, {}

    def detect_crack(self):
        # Simulate crack detection logic
        return random.choice([True, False])  # Randomly simulate detection

    def review_crack(self):
        # Simulate reviewing a detected crack
        return 0.5  # Reward for reviewing

class Agent:
    def __init__(self, action_size):
        self.action_size = action_size
        self.q_table = np.zeros((16, action_size))  # Initialize Q-table
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.1
        self.epsilon_decay = 0.995
        self.learning_rate = 0.1
        self.gamma = 0.9  # Discount factor

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:  # Epsilon-greedy strategy
            return random.randint(0, self.action_size - 1)
        return np.argmax(self.q_table[state])

    def update(self, state, action, reward, next_state):
        # Q-learning update formula
        td_target = reward + self.gamma * np.max(self.q_table[next_state])
        td_delta = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.learning_rate * td_delta

        # Epsilon decay
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

class MultiAgentSystem:
    def __init__(self, num_agents):
        self.env = CrackDetectionEnv()
        self.agents = [Agent(self.env.action_space.n) for _ in range(num_agents)]
        self.num_agents = num_agents

    def run(self, episodes):
        rewards_per_episode = []

        for episode in range(episodes):
            states = [self.env.reset() for _ in range(self.num_agents)]
            total_reward = 0
            done = False

            while not done:
                actions = [agent.choose_action(int(state[0] * 4)) for agent, state in zip(self.agents, states)]
                next_states, rewards, done_flags, _ = zip(*[self.env.step(action) for action in actions])
                
                for i, agent in enumerate(self.agents):
                    agent.update(int(states[i][0] * 4), actions[i], rewards[i], int(next_states[i][0] * 4))

                states = next_states
                total_reward += sum(rewards)

            rewards_per_episode.append(total_reward)
            if episode % 100 == 0:
                print(f"Episode: {episode}, Total Reward: {total_reward}")

        self.plot_rewards(rewards_per_episode)

    def plot_rewards(self, rewards):
        plt.plot(rewards)
        plt.title('Total Rewards per Episode')
        plt.xlabel('Episodes')
        plt.ylabel('Total Rewards')
        plt.show()

def main():
    num_agents = 3
    episodes = 1000
    multi_agent_system = MultiAgentSystem(num_agents)
    multi_agent_system.run(episodes)

if __name__ == "__main__":
    main()
