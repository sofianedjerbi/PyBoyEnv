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
        # Format :
        # {'addr':<address>, 'op':<operator>, 'reward':<reward>, 'val':<latest value>, 'lab':<label>}
        self._reward_rules = list()
        self._done_rules = list()
        self._refresh_values()

    def _refresh_values(self):
        """ Refresh values for each rule
        """
        for x in self._reward_rules + self._done_rules:
            x['val'] = self._pyboy.get_memory_value(x['addr'])

    def _get_observation(self):
        """ Returns screen
        """
        return np.asarray(self._screen.screen_ndarray(), dtype=np.uint8)

    def _handle_rule(self, rule):
        if rule['rule_type'] == 'reward':
            done = False
            reward = rule['reward'] # Set reward and label
            label = [rule['lab'], rule['reward']]
        elif rule['rule_type'] == 'done':
            done = True
            reward = 0
            label = [rule['lab'], "Done"]
        return reward, done, label


    def _scan_memory(self):
        """ Scan memory in order to apply rules
        """
        reward = 0
        done = False
        label = list()
        for x in self._reward_rules + self._done_rules:
            r, d, lab = 0, False, None
            if x['op'] == 'increase': # INCREASE
                if x['val'] < self._pyboy.get_memory_value(x['addr']):
                    r, d, lab = self._handle_rule(x)
            elif x['op'] == 'decrease': # DECREASE
                if x['val'] > self._pyboy.get_memory_value(x['addr']):
                    r, d, lab = self._handle_rule(x)
            elif  x['op'] == 'equal' : # EQUAL
                if self._pyboy.get_memory_value(x['addr']) == int(x['op'].split()[1]):
                    r, d, lab = self._handle_rule(x)
            elif x['op'] == 'bigger' or x['op']== 'greater': # BIGGER
                if self._pyboy.get_memory_value(x['addr']) > int(x['op'].split()[1]):
                    r, d, lab = self._handle_rule(x)
            elif  x['op'] == 'smaller' or x['op'] == 'less' : # SMALLER
                if self._pyboy.get_memory_value(x['addr']) < int(x['op'].split()[1]):
                    r, d, lab = self._handle_rule(x)
            elif x['op'] == in: # IN
                if self._pyboy.get_memory_value(x['addr']) in x['op'].split(' ')[1].split(','):
                    r, d, lab = self._handle_rule(x)
            else:
                raise ValueError(f"Invalid custom reward operator: {x['op']}")
            reward += r
            done = done or d
            label.append(lab) if lab is not None else None
        self._refresh_values()
        return reward, done, label

    def set_reward_rule(self, address, operator:str, reward, label:str):
        # More user friendly ?
        self._reward_rules.append({'rule_type': 'reward',
                                   'addr': address,
                                   'op': operator.lower(),
                                   'reward': reward,
                                   'val': 0,
                                   'lab': label})

     # No reward here but some action to pass screen etc if needed ?
    def set_done_rule(self, address, operator, label):
        self._done_rules.append({'rule_type': 'done',
                                 'addr': address,
                                 'op': operator,
                                 'val': 0,
                                 'lab': label})

    def step(self, action_id): # same thing as gymboy (no toggle)
        action = self.actions[action_id]
        self._pyboy.send_input(action)
        done_tick = self._pyboy.tick()
        reward, done, info = self._scan_memory()
        obs = self._get_observation()
        return obs, reward, done or done_tick, info

    def reset(self): # ?? Done rules ??
        return self._get_observation()

    def render(self): # there's a way to toggle visible screen??
        pass
