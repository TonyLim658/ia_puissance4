from Utils import *


def _check_horizontal(np_board):
    h, l = np_board.shape

    for i in range(h):
        redT = 0
        yelT = 0
        for j in range(l):
            if np_board[i, j] == RED_TOKEN:
                redT += 1
                yelT = 0
            elif np_board[i, j] == YELLOW_TOKEN:
                redT = 0
                yelT += 1
            else:
                redT = 0
                yelT = 0
            if redT == 5:
                return RED_TOKEN
            elif yelT == 5:
                return YELLOW_TOKEN

    return 0


def _check_vertical(np_board):
    h, l = np_board.shape

    for j in range(l):
        redT = 0
        yelT = 0
        for i in range(h):
            if np_board[i, j] == RED_TOKEN:
                redT += 1
                yelT = 0
            elif np_board[i, j] == YELLOW_TOKEN:
                redT = 0
                yelT += 1
            else:
                break
            if redT == 5:
                return RED_TOKEN
            elif yelT == 5:
                return YELLOW_TOKEN

    return 0


def _check_diagonal(np_board):
    h, l = np_board.shape
    for i0 in range(h - 4):
        redT = 0
        yelT = 0
        for k in range(min(h - i0, l)):
            i = i0 + k
            j = k
            if np_board[i, j] == RED_TOKEN:
                redT += 1
                yelT = 0
            elif np_board[i, j] == YELLOW_TOKEN:
                redT = 0
                yelT += 1
            else:
                redT = 0
                yelT = 0
            if redT == 5:
                return RED_TOKEN
            elif yelT == 5:
                return YELLOW_TOKEN
    return 0


def check_state(np_board):
    resultat = _check_horizontal(np_board) or _check_vertical(np_board[::-1, :]) or _check_diagonal(
        np_board) or _check_diagonal(
        np_board[:, ::-1]) or _check_diagonal(np_board.T[1:, :]) or _check_diagonal(np_board[:, -2::-1].T)

    if resultat:
        return resultat

    if (np_board == 0).any():
        return UNFINISHED_STATE
    return EMPTY_CELL
