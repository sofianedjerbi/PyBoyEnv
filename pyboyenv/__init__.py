from gym.envs.registration import register

register(
    id='PyBoy-v0',
    entry_point='pyboyenv.env:PyBoyEnv',
)
