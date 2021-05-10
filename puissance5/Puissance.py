from .Utils import *
from .Heuristique import heuristic, gen_score
from .CheckState import check_state, winning_positions

scores = {}  # tuple: int
COEFFICIENT_STATE = float('inf')
minimax_count = 0


def _get_index_token_positionable(npboard, length=BOARD_LENGTH, height=BOARD_HEIGHT):
    indexes = []
    for x in range(length):
        for y in range(height-1, -1, -1):
            if npboard[y, x] == EMPTY_CELL:
                indexes.append((y*length+x, (y, x)))
                break
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
        val = heuristic(npboard)
        scores[tuple_board] = val
        return val
    value = -float('inf') if is_red else float('inf')
    for i, positions in _get_index_token_positionable(npboard):
        npboard[positions] = RED_TOKEN if is_red else YELLOW_TOKEN
        child_board = update_tuple(tuple_board, i, RED_TOKEN if is_red else YELLOW_TOKEN)
        minimax_value = _minimax(child_board, npboard, depth - 1, alpha, beta, not is_red)
        value = max(value, minimax_value) if is_red else min(value, minimax_value)
        scores[child_board] = value
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
    for i, positions in _get_index_token_positionable(np_board):
        child_board = update_tuple(tuple_board, i, token)
        print(f'{i, positions} = {scores[child_board]}')
        if scores[child_board] == scores[tuple_board]:
            break
    print(f'minimax_count = {minimax_count}')
    return positions


gen_score()
_minimax(TUPLE_ORIGINAL, BOARD_ORIGINAL, 5, -float('inf'), float('inf'), True)
