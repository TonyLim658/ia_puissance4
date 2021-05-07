from Utils import *
from Heuristique import heuristic, gen_score
from CheckState import check_state

scores = {}  # tuple: int


def get_index_token_positionable(npboard, length=BOARD_LENGTH, height=BOARD_HEIGHT):
    indexes = []
    for x in range(length):
        for y in range(height-1, -1, -1):
            if npboard[y, x] == EMPTY_CELL:
                indexes.append(y*length+x)
                break
    return indexes


def minimax(board, depth, alpha, beta, is_red=True):
    npboard = tuple_to_array(board)
    state = check_state(npboard)
    if depth == 0 or state != UNFINISHED_STATE:
        if state != UNFINISHED_STATE:
            # Il s'agit d'une feuille terminale
            scores[board] = state
            return state
        # Il s'agit d'une feuille non terminale
        val = heuristic(npboard)
        scores[board] = val
        return val
    value = -float('inf') if is_red else float('inf')
    for i in get_index_token_positionable(npboard):
        child_board = update_tuple(board, i, RED_TOKEN if is_red else YELLOW_TOKEN)
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
    scores[board] = value
    return value


# # TODO adapter au tree qui a été supprimé
# def decision(board, bot_is_red):
#     val, child_board = -float('inf') if bot_is_red else float('inf'), TUPLE_ORIGINAL
#     for child in tree[board]:
#         if bot_is_red and val < scores[child] or not bot_is_red and val > scores[child]:
#             val = scores[child]
#             child_board = child
#     diff = 0
#     while diff < BOARD_SIZE and child_board[diff] == board[diff]:
#         diff += 1
#     return diff


if __name__ == "__main__":
    print('main launching')
    gen_score()
    minimax(TUPLE_ORIGINAL, 6, -float('inf'), float('inf'))
    count = 0
    for k, v in scores.items():
        count += 1
    print(scores)
    print(count)
