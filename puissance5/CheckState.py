from .Utils import *

winning_positions = []


def _check_horizontal(np_board):
    h, l = np_board.shape

    for i in range(h):
        redT = 0
        yelT = 0
        winning_positions.clear()
        for j in range(l):
            if np_board[i, j] == RED_TOKEN:
                winning_positions.append([i, j])
                redT += 1
                yelT = 0
            elif np_board[i, j] == YELLOW_TOKEN:
                winning_positions.append([i, j])
                redT = 0
                yelT += 1
            else:
                redT = 0
                yelT = 0
            if redT == TOKEN_WINNING_NUMBER:
                return RED_TOKEN
            elif yelT == TOKEN_WINNING_NUMBER:
                return YELLOW_TOKEN
    return 0


def _check_vertical(np_board):
    h, l = np_board.shape

    for j in range(l):
        redT = 0
        yelT = 0
        winning_positions.clear()
        for i in range(h - 1, -1, -1):
            if np_board[i, j] == RED_TOKEN:
                winning_positions.append([i, j])
                redT += 1
                yelT = 0
            elif np_board[i, j] == YELLOW_TOKEN:
                winning_positions.append([i, j])
                redT = 0
                yelT += 1
            else:
                break
            if redT == TOKEN_WINNING_NUMBER:
                return RED_TOKEN
            elif yelT == TOKEN_WINNING_NUMBER:
                return YELLOW_TOKEN
    return 0


def _check_diagonal(np_board, rotation_type):
    h, l = np_board.shape
    for i0 in range(h - (TOKEN_WINNING_NUMBER - 1)):
        redT = 0
        yelT = 0
        winning_positions.clear()
        for k in range(min(h - i0, l)):
            i = i0 + k
            j = k
            unrotated_i, unrotated_j = i, j
            if rotation_type == 1:
                unrotated_j = BOARD_LENGTH - j - 1
            elif rotation_type == 2:
                unrotated_i, unrotated_j = j, i + 1
            elif rotation_type == 3:
                unrotated_i, unrotated_j = j, i + 1
                unrotated_j = (BOARD_LENGTH - unrotated_j - 1)
            if np_board[i, j] == RED_TOKEN:
                winning_positions.append([unrotated_i, unrotated_j])
                redT += 1
                yelT = 0
            elif np_board[i, j] == YELLOW_TOKEN:
                winning_positions.append([unrotated_i, unrotated_j])
                redT = 0
                yelT += 1
            else:
                redT = 0
                yelT = 0
            if redT == TOKEN_WINNING_NUMBER:
                return RED_TOKEN
            elif yelT == TOKEN_WINNING_NUMBER:
                return YELLOW_TOKEN
    return 0


def check_state(np_board):
    resultat = _check_horizontal(np_board) or _check_vertical(np_board) \
               or _check_diagonal(np_board, 0) or _check_diagonal(np_board[:, ::-1], 1) \
               or _check_diagonal(np_board.T[1:, :], 2) or _check_diagonal(np_board[:, -2::-1].T, 3)
    if resultat:
        return resultat
    winning_positions.clear()

    if (np_board == 0).any():
        return UNFINISHED_STATE
    return EMPTY_CELL
