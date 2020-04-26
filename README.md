# Example:
```python
import gym
import pyboyenv

env = gym.make('PyBoy-v0', game='DX.gbc', visible=True)

env.set_reward_rule(0xDB5A, 'increase', 1) # Health
env.set_reward_rule(0xDB5A, 'decrease', -1) # Health
env.set_reward_rule(0xDB5E, 'increase', 1) # Money
env.set_reward_rule(0xDB45, 'increase', 1) # Arrows
env.set_reward_rule(0xDB4D, 'increase', 1) # Bombs
env.set_reward_rule(0xDBD0, 'increase', 1) # Keys
env.set_reward_rule(0xDBCF, 'increase', 5) # Big Keys
env.set_reward_rule(0xD368, 'equals 3', -5) # Death
env.set_reward_rule(0xD360, 'equals 3', 1) # Hit enemy
env.set_reward_rule(0xD360, 'equals 1', 2) # Loot
env.set_reward_rule(0xD368, 'in 59,15,16,21,49,24,25,27,30,33,34,39', 25) # Events

state = env.reset()
done = False

cumul = 0

while not done:
    state, reward, done, _ = env.step(16) # 16 = nothing...
    print(cumul)
    cumul += reward
```
