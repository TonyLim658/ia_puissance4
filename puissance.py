import numpy as np
import random

tree = {}  # tuple: [tuple] | int
scores = {}  # tuple: int
depth_record = {}  # tuple: int
RED_TOKEN = 1
YELLOW_TOKEN = -1
EMPTY_CELL = 0
BOARD_LENGTH = 12
BOARD_HEIGHT = 8
BOARD_SIZE = BOARD_HEIGHT * BOARD_LENGTH  # hauteur*largeur
TUPLE_ORIGINAL = (
                  EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
                  EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
                  EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
                  EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
                  EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
                  EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
                  EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
                  EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
                 )

BOARD_ORIGINAL = np.array(
                        [[EMPTY_CELL,  EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL],
                         [EMPTY_CELL,  EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL],
                         [EMPTY_CELL,  EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL],
                         [EMPTY_CELL,  EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL],
                         [EMPTY_CELL,  EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL],
                         [EMPTY_CELL,  EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL],
                         [EMPTY_CELL,  EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL],
                         [EMPTY_CELL,  EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL]]
                        )

# [0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10, 11]
# [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
# [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
# [36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47]
# [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
# [60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]
# [72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83]
# [84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95]


def update_tuple(tuple_to_update, index, val):
    tuple_updated = list(tuple_to_update)
    tuple_updated[index] = val
    tuple_updated = tuple(tuple_updated)
    return tuple_updated


def tuple_to_array(tuple_to_update, length=BOARD_LENGTH, height=BOARD_HEIGHT):
    list_returned = [[] for _ in range(height)]
    for i, v in enumerate(tuple_to_update):
        list_returned[i // length].append(v)
    return np.array(list_returned)


def array_to_tuple(array_to_update):
    one_dimensional_array = []
    for row in array_to_update:
        for cell in row:
            one_dimensional_array.append(cell)
    return tuple(one_dimensional_array)


def heuristic(npboard):
    # TODO complete by heuristeam ¯\_(ツ)_/¯
    return random.random()*2-1


def get_index_token_positionable(npboard, length=BOARD_LENGTH, height=BOARD_HEIGHT):
    indexes = []
    for x in range(length):
        for y in range(height-1, -1, -1):
            # print((x, y))
            # print(y*length+x, board_array[y, x])
            if npboard[y, x] == EMPTY_CELL:
                indexes.append(y*length+x)
                break
    return indexes


def minimax(board, depth, is_red=True, length=BOARD_LENGTH, height=BOARD_HEIGHT):
    if board in tree or depth == 0:
        # if depth_record[board] < depth and type(tree[board]) == list:
        #     for child_board in tree[board]:
        #         minimax(child_board, depth - 1, not is_red, length, height)
        return
    npboard = tuple_to_array(board)
    state = checkState(npboard)
    print(state, npboard)
    if type(state) == int:
        tree[board] = state
        scores[board] = state
        return
    else:
        tree[board] = []
    depth_record[board] = depth
    # S'il s'agit d'une feuille non terminale
    if depth == 1:
        val = heuristic(npboard)
        tree[board] = val
        scores[board] = val
        return
    score = -float('inf') if is_red else float('inf')
    for i in get_index_token_positionable(npboard, length, height):
        # Modification du tuple pour inscrire la case dans laquelle on joue
        child_board = update_tuple(board, i, RED_TOKEN if is_red else YELLOW_TOKEN)

        tree[board].append(child_board)
        minimax(child_board, depth-1, not is_red, length, height)
        score = max(score, scores[child_board]) if is_red else min(score, scores[child_board])
    scores[board] = score


def checkHorizontal(npBoard):
    h, l = npBoard.shape

    for i in range(h):
        redT = 0
        yelT = 0
        for j in range(l):
            if npBoard[i,j] == RED_TOKEN:
                redT += 1
                yelT = 0
            elif npBoard[i, j] == YELLOW_TOKEN:
                redT = 0
                yelT +=1
            else:
                redT = 0
                yelT = 0
            if redT == 5 :
                return RED_TOKEN
            elif yelT == 5:
                return YELLOW_TOKEN

    return 0


def checkVertical(npBoard):
    h, l = npBoard.shape

    for j in range(l):
        redT = 0
        yelT = 0
        for i in range(h):
            if npBoard[i,j] == RED_TOKEN:
                redT += 1
                yelT = 0
            elif npBoard[i, j] == YELLOW_TOKEN:
                redT = 0
                yelT +=1
            else:
                break
            if redT == 5 :
                return RED_TOKEN
            elif yelT == 5:
                return YELLOW_TOKEN

    return 0


def checkDiagonal(npBoard):
    h, l = npBoard.shape
    for i0 in range(h-4):
        redT = 0
        yelT = 0
        for k in range(min(h-i0, l)):
            i = i0 + k
            j = k
            if npBoard[i,j] == RED_TOKEN:
                redT += 1
                yelT = 0
            elif npBoard[i, j] == YELLOW_TOKEN:
                redT = 0
                yelT +=1
            else:
                redT = 0
                yelT = 0
            if redT == 5 :
                return RED_TOKEN
            elif yelT == 5:
                return YELLOW_TOKEN
    return 0


def checkState(npBoard):
    resultat = checkHorizontal(npBoard) or checkVertical(npBoard[::-1,:]) or checkDiagonal(npBoard) or checkDiagonal(npBoard[:,::-1]) or checkDiagonal(npBoard.T) or checkDiagonal(npBoard.T[:,::-1])

    if resultat:
        return resultat

    if (npBoard == 0).all():
        return None
    return EMPTY_CELL


def decision(board, bot_is_red):
    # TODO COMPLETE
    pass

# minimax((0,0,0,0), 2, True, 2, 2)
# minimax((0,0,1,0), 2, True, 2, 2)
minimax(TUPLE_ORIGINAL, 6)
count = 0
for k, v in tree.items():
    count += 1
print(tree)
print(scores)
print(count)

