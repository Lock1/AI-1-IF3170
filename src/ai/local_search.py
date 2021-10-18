import random
from time import time

from src.constant import ShapeConstant
from src.model import State

from typing import Tuple, List

from utility import place

from copy import deepcopy


class LocalSearch:
    def __init__(self):
        pass

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        best_value_so_far = countObjective(state)

        row = -1
        neighbor = {
            'state': None,
            'shape': None,
            'col': None,
            'value': None
        }
        selected = {
            'state': state,
            'shape': None,
            'col': None,
            'value': best_value_so_far
        }

        # value initiation
        while(time.time() <= self.thinking_time):
            neighbor['state'] = deepcopy(state)
            neighbor['col'] = random.randint(0, state.board.col)
            neighbor['shape'] = random.choice(
                [ShapeConstant.CROSS, ShapeConstant.CIRCLE])
            row = place(neighbor['state'], n_player,
                        neighbor['shape'], neighbor['col'])
            neighbor['value'] = countObjective(neighbor['state'])

            if(row != -1 and neighbor['value'] >= selected['value']):
                selected['state'] = neighbor['state']
                selected['shape'] = neighbor['shape']
                selected['col'] = neighbor['col']
                selected['value'] = neighbor['value']
        
        best_movement = (selected['col'], selected['shape'])

        return best_movement
