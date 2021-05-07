from .Utils import *
from .Heuristique import heuristic, gen_score
from .CheckState import check_state

scores = {}  # tuple: int


def get_index_token_positionable(npboard, length=BOARD_LENGTH, height=BOARD_HEIGHT):
    indexes = []
    for x in range(length):
        for y in range(height-1, -1, -1):
            if npboard[y, x] == EMPTY_CELL:
                indexes.append((y*length+x, (x, y)))
                break
    return indexes


def minimax(tuple_board, depth, alpha, beta, is_red=True):
    npboard = tuple_to_array(tuple_board)
    state = check_state(npboard)
    if depth == 0 or state != UNFINISHED_STATE:
        # Je suis une feuille
        if state != UNFINISHED_STATE:
            # Il s'agit d'une feuille terminale
            scores[tuple_board] = state * 1000  # [-1000, 0, 1000]
            return state
        # Il s'agit d'une feuille non terminale
        val = heuristic(npboard)
        scores[tuple_board] = val
        return val
    value = -float('inf') if is_red else float('inf')
    for i, positions in get_index_token_positionable(npboard):
        child_board = update_tuple(tuple_board, i, RED_TOKEN if is_red else YELLOW_TOKEN)
        if child_board in scores:
            value = scores[child_board]
        else:
            minimax_value = minimax(child_board, depth - 1, alpha, beta, not is_red)
            value = max(value, minimax_value) if is_red else min(value, minimax_value)
            scores[child_board] = value
        if is_red:
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # beta cutoff
        else:
            beta = min(beta, value)
            if beta >= alpha:
                break  # alpha cutoff
    scores[tuple_board] = value
    return value


def decision(np_board, token, depth=5):
    """
    return the position of the decision where the bot want to play his token
    :param np_board: board of the game of type numpy array
    :param token: RED_TOKEN if the bot is red YELLOW_TOKEN if the bot is yellow
    :param depth: height of the tree for the minimax algorithm set at 5 by default
    :return: tuple (x,y) positions
    """
    bot_is_red = token == RED_TOKEN
    val, positions_token = -float('inf') if bot_is_red else float('inf'), (-1, -1)
    tuple_board = array_to_tuple(np_board)
    minimax(tuple_board, depth, -float('inf'), float('inf'))
    for i, positions in get_index_token_positionable(np_board):
        child_board = update_tuple(tuple_board, i, token)
        if bot_is_red and val < scores[child_board] or not bot_is_red and val > scores[child_board]:
            val = scores[child_board]
            positions_token = positions
    return positions_token


if __name__ == "__main__":
    print('main launching')
    gen_score()
    minimax(TUPLE_ORIGINAL, 6, -float('inf'), float('inf'))
    count = 0
    for k, v in scores.items():
        count += 1
    print(scores)
    print(count)
