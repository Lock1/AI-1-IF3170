import random
from copy import deepcopy
from math import inf
from time import time
from src.model.piece import Piece

from src.model import Board
from src.constant import ColorConstant, ShapeConstant,GameConstant

from src.model import State
from src.utility import place, is_out


from typing import Tuple, List

ListShape = [ShapeConstant.CIRCLE,ShapeConstant.CROSS]

class Minimax:
    def __init__(self):
        self.__objective_multiplier = 100
        self.__objective_extrema    = 10000
        
    #jangan di run, rung iso lapo-lapo arek iki

    
    def __streak_eval(self, streak: List[Piece]) -> int:
        # Assuming streak[0] is non-empty piece
        # Different shape -> shape_obj = 0
        # Different color -> color_obj = 0
        # shape_obj & color_obj = streak_length * streak_value_multiplier * player_multiplier
        # Objective function = shape_obj + color_obj

        streak_shape = streak[0].shape
        streak_color = streak[0].color
        shape_length = 0
        color_length = 0
        for i in range(1, GameConstant.N_COMPONENT_STREAK - 1):
            if streak[i].shape == streak_shape:
                shape_length += 1
            elif streak[i].shape != ShapeConstant.BLANK:
                shape_length = -GameConstant.N_COMPONENT_STREAK

            if streak[i].color == streak_color:
                color_length += 1
            elif streak[i].color != ColorConstant.BLACK:
                color_length = -GameConstant.N_COMPONENT_STREAK

        shape_obj = 0
        color_obj = 0
        if shape_length > 0:
            if self.players[0].shape == streak_shape:
                shape_multiplier = -1
            else:
                shape_multiplier = 1

            if shape_length == GameConstant.N_COMPONENT_STREAK:
                shape_obj = self.__objective_extrema * shape_multiplier
            else:
                shape_obj = self.__objective_multiplier * shape_multiplier * shape_length

        if color_length > 0:
            if self.players[0].color == streak_color:
                color_multiplier = -1
            else:
                color_multiplier = 1

            if color_length == GameConstant.N_COMPONENT_STREAK:
                shape_obj = self.__objective_extrema * color_multiplier
            else:
                shape_obj = self.__objective_multiplier * color_multiplier * color_length

        return shape_obj + color_obj

    def __objective_function(self, board: Board) -> int:
        # Player 1 -> Minimizer
        # Player 2 -> Maximizer
        min_value = 0
        max_value = 0
        streak_direction = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for row in range(board.row):
            for col in range(board.col):
                current_piece = board[row, col]
                if current_piece.shape == ShapeConstant.BLANK:
                    continue

                for row_ax, col_ax in streak_direction:
                    streak_length = 0
                    streak_list   = [current_piece]
                    row_ = row + row_ax
                    col_ = col + col_ax
                    for _ in range(GameConstant.N_COMPONENT_STREAK - 1):
                        if is_out(board, row_, col_):
                            break

                        streak_list.append(board[row_, col_])
                        row_ += row_ax
                        col_ += col_ax
                        streak_length += 1

                    if streak_length == GameConstant.N_COMPONENT_STREAK - 1:
                        objective_value = self.__streak_eval(streak_list)
                        max_value = max(max_value, objective_value)
                        min_value = min(min_value, objective_value)

        return max_value + min_value
    
    def eval(self,board : Board):
        #fungsi objektif
        random.randint(0,board.col)
    
    def drop_piece(self,board,column,shape,color):
        #fungsi untuk menjatuhkan piece
         for row in range(board.row - 1, -1, -1):
            if board[row, column].shape == ShapeConstant.BLANK:
                piece = Piece(shape, color)
                board.set_piece(row, column, piece)
                return 0


    def MinimaxAlghorithm(self,board : Board,depth : int,alpha,beta,maximizing : bool, start_time : float, thinking_time : float):
        timenow = time()
        elapsedtime = timenow - start_time
        if (depth == 0 or elapsedtime > thinking_time) :
            return [None,self.__objective_function(board)]
        
        if (maximizing):
            color = ColorConstant.RED
            value = -inf
            col = 0
            for column in range(board.col):
                for shapes in ListShape:
                    new_board = deepcopy(board)
                    self.drop_piece(new_board,column,shapes,color)
                    # score = self.__objective_function(new_board)
                    # print("\n\n board baru {0} depth {1} maximize, score : {2} \n\n".format(column,depth,score))
                    # print(new_board)
                    new_score = self.MinimaxAlghorithm(new_board,depth-1,alpha,beta,False,start_time,thinking_time)[1]
                    if new_score > value:
                        value = new_score
                        col = column
                        shape = shapes
                        alpha = max(alpha, value)
                    if alpha >= beta:
                        break
            return [(col,shape),value]

        else : #minimizing
            color = ColorConstant.BLUE
            value = inf
            col = 0
            for column in range(board.col):
                for shapes in ListShape:
                    new_board = deepcopy(board)
                    self.drop_piece(new_board,column,shapes,color)
                    # score = self.__objective_function(new_board)
                    # print("\n\n board baru {0} depth {1} maximize, score : {2} \n\n".format(column,depth,score))
                    # print(new_board)
                    new_score = self.MinimaxAlghorithm(new_board,depth-1,alpha,beta,True,start_time,thinking_time)[1]
                    if new_score < value:
                        value = new_score
                        col = column
                        shape = shapes
                        alpha = max(alpha, value)
                    if alpha >= beta:
                        break
            return [(col,shape),value]
                


    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        self.players       = state.players

        start_time = time()
        piece = Piece(state.players[n_player].shape,state.players[n_player].color)
        # best_movement = (random.randint(0, state.board.col), random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])) #minimax algorithm
        col = self.MinimaxAlghorithm(state.board,2,-inf,inf,False,start_time,thinking_time)[0]
        best_movement = col #minimax algorithm
        return best_movement
    
