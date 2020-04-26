import gym
import pyboyenv

env = gym.make('PyBoy-v0', game='DX.gbc', visible=True)

env.set_reward_rule(0xDB5A, 'increase', 1, "Health") # Label ('health') is not required
env.set_reward_rule(0xDB5A, 'decrease', -1, "Health") # Health
env.set_reward_rule(0xDB5E, 'increase', 1, "Money") # Money
env.set_reward_rule(0xDB45, 'increase', 1, "Arrows") # Arrows
env.set_reward_rule(0xDB4D, 'increase', 1, "Bombs") # Bombs
env.set_reward_rule(0xDBD0, 'increase', 1, "Keys") # Keys
env.set_reward_rule(0xDBCF, 'increase', 5, "Big Keys") # Big Keys
env.set_reward_rule(0xD368, 'equals 3', -25, "Death") # Death
env.set_reward_rule(0xD360, 'equals 3', 1, "Hit Enemy") # Hit enemy
env.set_reward_rule(0xD360, 'equals 1', 2, "Loot") # Loot
env.set_reward_rule(0xD368, 'in 59,15,16,21,49,24,25,27,30,33,34,39', 25, "Event") # Events
env.set_done_rule(0xD368, 'equals 3', "Death") # Done if player dies

cumul = 0
done = False
while not done:
    state, reward, done, info = env.step(16) # 16 = nothing..
    cumul += reward
    for i in info:
        print(f"{i[0]}: {i[1]}")
