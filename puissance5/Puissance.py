from .Utils import *
from .Heuristique import heuristic, gen_score
from .CheckState import check_state, winning_positions

scores = {}  # tuple: int
scores_heuristic = {}  # tuple: int
COEFFICIENT_STATE = float('inf')
minimax_count = 0


def _get_index_token_positionable(tuple_board, npboard, is_red, length=BOARD_LENGTH, height=BOARD_HEIGHT):
    indexes = []
    for x in range(length):
        for y in range(height-1, -1, -1):
            if npboard[y, x] == EMPTY_CELL:
                npboard[y, x] = RED_TOKEN if is_red else YELLOW_TOKEN
                child_tuple = update_tuple(tuple_board, y*length+x, RED_TOKEN if is_red else YELLOW_TOKEN)
                if child_tuple in scores_heuristic:
                    score_heuristic = scores_heuristic[child_tuple]
                else:
                    score_heuristic = heuristic(npboard)
                    scores_heuristic[child_tuple] = score_heuristic
                npboard[y, x] = EMPTY_CELL
                indexes.append((child_tuple, (y, x), score_heuristic))
                break
    indexes.sort(key=lambda tup: tup[2], reverse=is_red)
    return indexes


def _minimax(tuple_board, npboard, depth, alpha, beta, is_red):
    global minimax_count
    minimax_count += 1
    if tuple_board in scores:
        return scores[tuple_board]
    state = check_state(npboard)
    if depth == 0 or state != UNFINISHED_STATE:
        # Je suis une feuille
        if state != UNFINISHED_STATE:
            # Il s'agit d'une feuille terminale
            state_coeff = state * COEFFICIENT_STATE
            scores[tuple_board] = state_coeff
            return state_coeff
        # Il s'agit d'une feuille non terminale
        if tuple_board in scores_heuristic:
            score_heuristic = scores_heuristic[tuple_board]
        else:
            score_heuristic = heuristic(npboard)
            scores_heuristic[tuple_board] = score_heuristic
        scores[tuple_board] = score_heuristic
        return score_heuristic
    value = -float('inf') if is_red else float('inf')
    for child_tuple, positions, score_heuristic in _get_index_token_positionable(tuple_board, npboard, is_red):
        y, x = positions
        npboard[y, x] = RED_TOKEN if is_red else YELLOW_TOKEN
        minimax_value = _minimax(child_tuple, npboard, depth - 1, alpha, beta, not is_red)
        value = max(value, minimax_value) if is_red else min(value, minimax_value)
        scores[child_tuple] = value
        npboard[positions] = EMPTY_CELL
        if is_red:
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # beta cutoff
        else:
            beta = min(beta, value)
            if beta <= alpha:
                break  # alpha cutoff
    scores[tuple_board] = value
    return value


def decision(np_board, token, depth=5):
    """
    return the position of the decision where the bot want to play his token
    :param np_board: board of the game of type numpy array
    :param token: RED_TOKEN if the bot is red YELLOW_TOKEN if the bot is yellow
    :param depth: height of the tree for the minimax algorithm set at 5 by default
    :return: tuple (y,x) positions where the bot wants to play
    """
    global minimax_count
    minimax_count = 0
    bot_is_red = token == RED_TOKEN
    tuple_board = array_to_tuple(np_board)
    scores.clear()
    _minimax(tuple_board, np_board, depth, -float('inf'), float('inf'), bot_is_red)
    for child_tuple, positions, score_heuristic in _get_index_token_positionable(tuple_board, np_board, bot_is_red):
        if scores[child_tuple] == scores[tuple_board]:
            break
    print(f'minimax_count = {minimax_count}')
    return positions, minimax_count


gen_score()
