import random
from time import time

from src.constant import ShapeConstant, GameConstant, ColorConstant
from src.model import State, Piece, Board

from typing import Tuple, List

from src.utility import place, is_out

from copy import deepcopy


class LocalSearchGroup10:
    def __init__(self):
        self.__objective_multiplier = 100
        self.__objective_extrema    = 1000000

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

    def __compare_obj(self, current_best_value: int, compared_value: int, n_player: int):
        if n_player == 0:
            return compared_value < current_best_value
        elif n_player == 1:
            return compared_value > current_best_value

    def find(self, state: State, n_player: int, thinking_time: float) -> Tuple[str, str]:
        self.thinking_time = time() + thinking_time
        self.players       = state.players

        ret_code = -1
        neighbor = {
            'shape'    : None,
            'index_col': None,
            'value'    : None,
            'win'      : None
        }

        current_best = {
            'shape'    : None,
            'index_col': None,
            'value'    : None,
            'win'      : None
        }

        # value initiation
        while time() <= self.thinking_time:
            temp_state            = deepcopy(state)
            neighbor['index_col'] = random.randint(0, state.board.col - 1)
            neighbor['shape']     = random.choice([ShapeConstant.CROSS, ShapeConstant.CIRCLE])
            ret_code              = place(temp_state, n_player, neighbor['shape'], neighbor['index_col'])
            neighbor['value']     = self.__objective_function(temp_state.board)

            # Percobaan pengecekan kemenangan
            player1_win     = (n_player == 0 and neighbor['value'] == -self.__objective_extrema)
            player2_win     = (n_player == 1 and neighbor['value'] == self.__objective_extrema)
            neighbor['win'] = player1_win or player2_win

            first_iteration      = (current_best['value'] is None)
            if not first_iteration:
                compare_condition  = (ret_code != -1 and self.__compare_obj(current_best['value'], neighbor['value'], n_player))

            if first_iteration or (compare_condition and not current_best['win']):
                current_best['shape']     = neighbor['shape']
                current_best['index_col'] = neighbor['index_col']
                current_best['value']     = neighbor['value']
                current_best['win']       = neighbor['win']

        best_movement = (current_best['index_col'], current_best['shape'])
        return best_movement
