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

        row = -1
        current_best = {
            'state': None,
            'shape': None,
            'col': None,
        }

        #value initiation
        while(row == -1 and time.time() <= self.thinking_time):
            current_best['state'] = deepcopy(state)
            current_best['col'] = random.randint(0, state.board.col)
            current_best['shape'] = random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])
            row = place(current_best['state'], n_player, current_best['shape'], current_best['col'])

        #local search
        while time.time() <= self.thinking_time:

            #TODO: implement local_search


            best_movement = () #minimax algorithm

        return best_movement