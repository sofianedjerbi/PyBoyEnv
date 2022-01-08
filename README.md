# PyBoyEnv
This package allow you to turn any gameboy memory event into a reinforcement learning environment rule.

<p align="center">
    <img src="demo.gif"><br/>
    (generated with test.py)
</p>

## Installation
Install the dependencies:

```bash
pip install -r requirements.txt
```

Install the package with `pip`:

```bash
pip install ./
```

## Quickstart 
```python
import gym
import pyboyenv

# Create the environment
env = gym.make('Pyboy-v0', game=<FILE>)

# Add rules
env.set_reward_rule(ADDRESS, TYPE, VALUE, LABEL)

# Available rules:
# - increase: add VALUE if the memory at the address ADDRESS increases
# - decrease: add VALUE if the memory at the address ADDRESS decreases
# - smaller X: add VALUE if the memory at the address ADDRESS is smaller than X
# - bigger X: add VALUE if the memory at the address ADDRESS is bigger than X
# - equals X: add VALUE if the memory at the address ADDRESS equals X
# - in X1,..,XN: add VALUE if the memory at the address ADDRESS is equal to X1 or ... or XN

# Useful values
cumul = 0 # Sum of rewards 
done = False # Is the game done ?
action = 16 # Initial action (action list available below, 16=nothing)

# Game loop
while not done:
    # State = Window screen
    state, reward, done, info = env.step(action)
    cumul += reward
    action = Agent.get_action(state, cumul, reward) # Next action
    # Print infos
    for i in info:
        print(f"{i[0]}: {i[1]}")
```

## Actions
- 0: `WindowEvent.PRESS_ARROW_UP`
- 1: `WindowEvent.PRESS_ARROW_DOWN`
- 2: `WindowEvent.PRESS_ARROW_LEFT`
- 3: `WindowEvent.PRESS_ARROW_RIGHT`
- 4: `WindowEvent.PRESS_BUTTON_A`
- 5: `WindowEvent.PRESS_BUTTON_B`
- 6: `WindowEvent.PRESS_BUTTON_SELECT`
- 7: `WindowEvent.PRESS_BUTTON_START`
- 8: `WindowEvent.RELEASE_ARROW_UP`
- 9: `WindowEvent.RELEASE_ARROW_DOWN`
- 10: `WindowEvent.RELEASE_ARROW_LEFT`
- 11: `WindowEvent.RELEASE_ARROW_RIGHT`
- 12: `WindowEvent.RELEASE_BUTTON_A`
- 13: `WindowEvent.RELEASE_BUTTON_B`
- 14: `WindowEvent.RELEASE_BUTTON_SELECT`
- 15: `WindowEvent.RELEASE_BUTTON_START`
- 16: `WindowEvent.PASS`
