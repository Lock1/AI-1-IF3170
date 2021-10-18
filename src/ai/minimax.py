import random
from copy import deepcopy
from math import inf
from time import time
from src.model.piece import Piece

from src.model import Board
from src.constant import ShapeConstant
from src.model import State

from typing import Tuple, List


class Minimax:
    def __init__(self):
        pass
    #jangan di run, rung iso lapo-lapo arek iki
    
    def eval(self,board : Board):
        #fungsi objektif
        random.randint(0,board.col)
    
    def drop_piece(self,board,column):
        #fungsi untuk menjatuhkan piece
        pass

    def MinimaxAlghorithm(self,board : Board,depth : int,maximizing : bool):
        if (depth == 0) :
            return [None,eval(board)]
        
        if (maximizing):
            value = -inf 
            for column in range(board.col):
                new_board = board.copy()
                self.drop_piece(new_board,column)
                self.MinimaxAlghorithm(new_board,depth-1,False)

        else : #minimizing
            value = inf
            for column in range(board.col):
                new_board = board.copy()
                self.drop_piece(new_board,column)
                self.MinimaxAlghorithm(new_board,depth-1,True)
                


    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time

        piece = Piece(state.players[n_player].shape,state.players[n_player].color)
        # best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm
        best_movement = (0, piece.shape) #minimax algorithm
        return best_movement
    
