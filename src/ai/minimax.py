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

class MinimaxGroup10:
    def __init__(self):
        self.__objective_multiplier = 100
        self.__objective_extrema    = 1000000

    #jangan di run, rung iso lapo-lapo arek iki
    def __streak_eval(self, streak: List[Piece]) -> int:
        # Assuming streak[0] is non-empty piece
        # Different shape -> shape_obj = 0
        # Different color -> color_obj = 0
        # shape_obj & color_obj = streak_length * streak_value_multiplier * player_multiplier
        # Objective function = if won -> return extrema value for player, else -> shape_obj + color_obj

        streak_shape = streak[0].shape
        streak_color = streak[0].color
        shape_length = 1
        color_length = 1
        for i in range(1, GameConstant.N_COMPONENT_STREAK):
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
                return self.__objective_extrema * shape_multiplier
            else:
                shape_obj = self.__objective_multiplier * shape_multiplier * shape_length

        if color_length > 0:
            if self.players[0].color == streak_color:
                color_multiplier = -1
            else:
                color_multiplier = 1

            if color_length == GameConstant.N_COMPONENT_STREAK:
                return self.__objective_extrema * color_multiplier
            else:
                color_obj = self.__objective_multiplier * color_multiplier * color_length

        return shape_obj + color_obj

    def __objective_function(self, board: Board) -> int:
        # Player 1 -> Minimizer
        # Player 2 -> Maximizer
        min_value = self.__objective_extrema
        max_value = -self.__objective_extrema
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

        if max_value == self.__objective_extrema:
            return self.__objective_extrema
        elif min_value == -self.__objective_extrema:
            return -self.__objective_extrema
        else:
            return max_value + min_value


    def drop_piece(self,board,column,shape,color):
        #fungsi untuk menjatuhkan piece
         for row in range(board.row - 1, -1, -1):
            if board[row, column].shape == ShapeConstant.BLANK:
                piece = Piece(shape, color)
                board.set_piece(row, column, piece)
                return 0


    # score = self.__objective_function(new_state)
    # print("\n\n board baru {0} depth {1} maximize, score : {2} \n\n".format(column,depth,score))
    # print(new_state)

    # print(f"{obj_val} skornya")
    # print(board, f"<{obj_val}>")
    def __minimax(self, state : State, depth : int, alpha : int, beta : int, maximizing : bool, start_time: float, thinking_time : float):
        time_now = time()
        elapsed_time = time_now - start_time
        if (depth == 0 or elapsed_time > thinking_time):
            obj_val = self.__objective_function(state.board)
            return [None, obj_val]

        # Maximizer
        if maximizing:
            color = self.players[1].color
            value = -inf
            col   = 0
            for column in range(state.board.col):
                for shapes in ListShape:
                    new_state = deepcopy(state)
                    ret_code  = place(new_state, 1, shapes, column)

                    if ret_code != -1:
                        new_score = self.__minimax(new_state, depth-1, alpha, beta, False,start_time,thinking_time)[1]
                        if new_score > value:
                            value = new_score
                            col   = column
                            shape = shapes
                            alpha = max(alpha, value)

                    if alpha >= beta:
                        break

        # Minimizer
        else:
            color = self.players[0].color
            value = inf
            col   = 0
            for column in range(state.board.col):
                for shapes in ListShape:
                    new_state = deepcopy(state)
                    ret_code  = place(new_state, 0, shapes, column)
                    if ret_code != -1:
                        new_score = self.__minimax(new_state, depth-1, alpha, beta, True,start_time,thinking_time)[1]
                        if new_score < value:
                            value = new_score
                            col   = column
                            shape = shapes
                            beta  = min(beta, value)
                    if alpha >= beta:
                        break

        move = [(col,shape), value]
        return move

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        self.players       = state.players

        start_minimax= time()
        is_maximizer  = (n_player == 1)
        best_movement = self.__minimax(state, 4, -inf, inf, is_maximizer,start_minimax,thinking_time)[0]
        return best_movement