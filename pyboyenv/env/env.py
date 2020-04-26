# Used some code by @MathisFederico
import numpy as np
from gym import Env
from gym.spaces import Discrete, Box
from pyboy import PyBoy, WindowEvent

class PyBoyEnv(Env):
    """ Operators :
        - increase
        - decrease
        - equal <val>
        - smaller <val>
        - bigger <val>
        - in <val_1>,<val_2>,...,<val_n> (no spaces between values plz)
    """

    def __init__(self,
                 game,
                 window='SDL2',
                 visible=False,
                 colors=(0xfff6d3, 0xf9a875, 0xeb6b6f, 0x7c3f58),
                 buttons_press_mode='toggle'):
        # Build game
        super().__init__()
        self._pyboy = PyBoy(game, window_type=window, color_palette=colors, disable_renderer=not visible)
        self._pyboy.set_emulation_speed(0)

        self._manager = self._pyboy.botsupport_manager()
        self._screen = self._manager.screen()


        self.actions = {
            0: WindowEvent.PRESS_ARROW_UP,
            1: WindowEvent.PRESS_ARROW_DOWN,
            2: WindowEvent.PRESS_ARROW_LEFT,
            3: WindowEvent.PRESS_ARROW_RIGHT,
            4: WindowEvent.PRESS_BUTTON_A,
            5: WindowEvent.PRESS_BUTTON_B,
            6: WindowEvent.PRESS_BUTTON_SELECT,
            7: WindowEvent.PRESS_BUTTON_START,
            8: WindowEvent.RELEASE_ARROW_UP,
            9: WindowEvent.RELEASE_ARROW_DOWN,
            10: WindowEvent.RELEASE_ARROW_LEFT,
            11: WindowEvent.RELEASE_ARROW_RIGHT,
            12: WindowEvent.RELEASE_BUTTON_A,
            13: WindowEvent.RELEASE_BUTTON_B,
            14: WindowEvent.RELEASE_BUTTON_SELECT,
            15: WindowEvent.RELEASE_BUTTON_START,
            16: WindowEvent.PASS
        }
        self.action_space = Discrete(len(self.actions))
        self.observation_space = Box(low=0, high=255, shape=(160, 144, 3), dtype=np.uint8)
        # Format : {"addr":<address> "op":<operator> "reward":<reward> "val":<latest value>}
        self._reward_rules = list()
        self._refresh_values()

    def _refresh_values(self):
        """ Refresh values for each rule
        """
        for x in self._reward_rules:
            x['val'] = self._pyboy.get_memory_value(x['addr'])

    def _get_observation(self):
        """ Returns screen
        """
        return np.asarray(self._screen.screen_ndarray(), dtype=np.uint8)

    def _get_reward(self):
        """ Use reward rules in order to create reward
        """
        r = 0
        for x in self._reward_rules:
            if 'increase' in x['op']:
                if x['val'] < self._pyboy.get_memory_value(x['addr']):
                    r += x['reward']
            elif 'decrease' in x['op']:
                if x['val'] > self._pyboy.get_memory_value(x['addr']):
                    r += x['reward']
            elif 'equal' in x['op']:
                if self._pyboy.get_memory_value(x['addr']) == int(x['op'].split()[1]):
                    r += x['reward']
            elif 'bigger' in x['op'] or 'greater' in x['op']:
                if self._pyboy.get_memory_value(x['addr']) > int(x['op'].split()[1]):
                    r += x['reward']
            elif 'smaller' in x['op'] or 'less' in x['op']:
                if self._pyboy.get_memory_value(x['addr']) < int(x['op'].split()[1]):
                    r += x['reward']
            elif 'in' in x['op']:
                for i in x['op'].split(' ')[1].split(','):
                    if self._pyboy.get_memory_value(x['addr']) == int(i):
                        print("ok")
                        r += x['reward']
            else:
                raise ValueError(f"Invalid custom reward operator: {x['op']}")
        self._refresh_values()
        return r

    def set_reward_rule(self, address, operator, reward):
        # More user friendly ?
        self._reward_rules.append({"addr": address, "op": operator, "reward": reward, "val": 0})

    def step(self, action_id): # same thing as gymboy (no toggle)
        action = self.actions[action_id]
        self._pyboy.send_input(action)
        return self._get_observation(), self._get_reward(), self._pyboy.tick(), {}

    def reset(self): # ?? Done rules ??
        return self._get_observation()

    def render(self): # ??
        pass
