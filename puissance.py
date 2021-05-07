import numpy as np
import random
from utils import *

tree = {}  # tuple: [tuple] | int
scores = {}  # tuple: int
depth_record = {}  # tuple: int
BLOCK_SCORE_YELLOW = {}
BLOCK_SCORE_RED = {}

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

########## EURISITIQUE###########
def gen_score(rge=12):
    assert (rge >= 5)
    t_last_iter = [((0, 0, 0, 0), 0), ((1, 0, 0, 0), 0.1), ((1, 1, 0, 0), 0.2), ((1, 1, 1, 0), 0.3), ((1, 1, 1, 1), 0.4), ((1, 1, 0, 1), 0.3), ((1, 0, 1, 0), 0.2), ((1, 0, 1, 1), 0.30000000000000004), ((1, 0, 0, 1), 0.2), ((0, 1, 0, 0), 0.1), ((0, 1, 1, 0), 0.2), ((0, 1, 1, 1), 0.3), ((0, 1, 0, 1), 0.2), ((0, 0, 1, 0), 0.1), ((0, 0, 1, 1), 0.2), ((0, 0, 0, 1), 0.1)]
    for i in range(4, rge):
        local_count = 0
        t = []
        for k, v in t_last_iter:
            t.append(([0] + list(k), v))
            t.append(([1] + list(k), v + 0.1))
            local_count += 2
        for k, v in t:
            #on applique un facteur pour que les tableaux correspondent aux valeurs des pions
            # -1 fois le tableaux -1 fois le score
            BLOCK_SCORE_RED[tuple([item * RED_TOKEN for item in k])] = v * RED_TOKEN
            BLOCK_SCORE_YELLOW[tuple([item * YELLOW_TOKEN for item in k])] = v * YELLOW_TOKEN
        t_last_iter = t


def heurHorizontal(npBoard):
    h, l = npBoard.shape
    score = 0

    #le but est de regarder les score par block au changement de couleur ou en fin de ligne
    for i in range(h):
        RED_BOX = []
        YELLOW_BOX = []
        for j in range(l):
            val = npBoard[i,j]
            #si on tombe sur un pion jaune
            if val == RED_TOKEN:
                #on va voir si le fragments avec des jetons jaunes peut être exploiter
                if len(YELLOW_BOX) >= 5:
                    #exploitable donc on va chercher le score qui correspond
                    score += BLOCK_SCORE_YELLOW[tuple(YELLOW_BOX)]

                YELLOW_BOX = []
                RED_BOX.append(val)
            #si on tombe sur un pion rouge
            elif val == YELLOW_TOKEN:
                #on va voir si le fragments avec des jetons rouges peut être exploiter
                if len(RED_BOX) >= 5:
                    #exploitable donc on va chercher le score qui correspond
                    score += BLOCK_SCORE_RED[tuple(RED_BOX)]

                YELLOW_BOX.append(val)
                RED_BOX = []

            else:
                lenY = len(YELLOW_BOX)
                lenR = len(RED_BOX)
                #dans le cas où on est en fin de grille et que la ligne n'est pas remplie de 0
                if j == l-1 :
                    if lenY >= 5 and lenY > lenR:
                        score += BLOCK_SCORE_YELLOW[tuple(YELLOW_BOX)]
                    elif lenR >= 5 and lenR > lenY:
                        score += BLOCK_SCORE_RED[tuple(RED_BOX)]
                else:
                    RED_BOX.append(val)
                    YELLOW_BOX.append(val)


    return score

def heurVertical(npBoard):
    h, l = npBoard.shape
    score = 0

    #le but est de regarder les scores par block dès qu'il n'y a plus de jeton dans la colonne
    for j in range(l):
        RED_BOX = []
        YELLOW_BOX = []
        for i in range(h):
            val = npBoard[i,j]
            #si on tombe sur un pion jaune
            if val == RED_TOKEN:

                YELLOW_BOX = []
                RED_BOX.append(val)

            #si on tombe sur un pion rouge
            elif val == YELLOW_TOKEN:

                YELLOW_BOX.append(val)
                RED_BOX = []

            #le reste de la colonne est vide
            else:
                lenY = len(YELLOW_BOX)
                lenR = len(RED_BOX)
                #nombre de vides pour compléter la colonne
                nbVides = h-i
                if lenY > 0:
                    for add in range(nbVides):
                        YELLOW_BOX.append(val)
                    if lenY >= 5:
                        score += BLOCK_SCORE_YELLOW[tuple(YELLOW_BOX)]
                elif lenR > 0:
                    for add in range(nbVides):
                        RED_BOX.append(val)
                    if lenR >= 5:
                        score += BLOCK_SCORE_RED[tuple(RED_BOX)]

                break


    return score

def heurDiagonal(npBoard):
    h, l = npBoard.shape
    score = 0

    #le but est de regarder les scores par block au changement de couleur ou en fin de diagonale
    for i0 in range(h-4):
        RED_BOX = []
        YELLOW_BOX = []
        for k in range(min(h-i0, l)):
            i = i0 + k
            j = k
            val = npBoard[i,j]
            #si on tombe sur un pion jaune
            if val == RED_TOKEN:
                #on va voir si le fragments avec des jetons jaunes peut être exploiter
                if len(YELLOW_BOX) >= 5:
                    #exploitable donc on va chercher le score qui correspond
                    score += BLOCK_SCORE_YELLOW[tuple(YELLOW_BOX)]

                YELLOW_BOX = []
                RED_BOX.append(val)
            #si on tombe sur un pion rouge
            elif val == YELLOW_TOKEN:
                #on va voir si le fragments avec des jetons rouges peut être exploiter
                if len(RED_BOX) >= 5:
                    #exploitable donc on va chercher le score qui correspond
                    score += BLOCK_SCORE_RED[tuple(RED_BOX)]

                YELLOW_BOX.append(val)
                RED_BOX = []

            else:
                lenY = len(YELLOW_BOX)
                lenR = len(RED_BOX)
                #dans le cas où on est en fin de grille et que la diagonale n'est pas remplie de 0
                if j == l-1 :
                    if lenY >= 5 and lenY > lenR:
                        score += BLOCK_SCORE_YELLOW[tuple(YELLOW_BOX)]
                    elif lenR >= 5 and lenR > lenY:
                        score += BLOCK_SCORE_RED[tuple(RED_BOX)]
                else:
                    RED_BOX.append(val)
                    YELLOW_BOX.append(val)
    return score

def heuristic(npBoard):
    # heuristeam ¯\_(ツ)_/¯
    score = heurHorizontal(npBoard) + heurVertical(npBoard[::-1,:]) + heurDiagonal(npBoard) + heurDiagonal(npBoard[:,::-1]) + heurDiagonal(npBoard.T[1:,:]) + heurDiagonal(npBoard[:,-2::-1].T)
    return score


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
    if board in tree and tree[board] != [] or depth == 0:
        # print(f'tree[board] = {tree[board]}')
        if depth_record[board] < depth and type(tree[board]) == list:
            for child_board in tree[board]:
                minimax(child_board, depth - 1, not is_red, length, height)
        return
    npboard = tuple_to_array(board)
    state = checkState(npboard)
    # print(state, npboard)
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
        tree[board] = []
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
            if npBoard[i, j] == RED_TOKEN:
                redT += 1
                yelT = 0
            elif npBoard[i, j] == YELLOW_TOKEN:
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


def checkVertical(npBoard):
    h, l = npBoard.shape

    for j in range(l):
        redT = 0
        yelT = 0
        for i in range(h):
            if npBoard[i, j] == RED_TOKEN:
                redT += 1
                yelT = 0
            elif npBoard[i, j] == YELLOW_TOKEN:
                redT = 0
                yelT += 1
            else:
                break
            if redT == 5:
                return RED_TOKEN
            elif yelT == 5:
                return YELLOW_TOKEN

    return 0


def checkDiagonal(npBoard):
    h, l = npBoard.shape
    for i0 in range(h - 4):
        redT = 0
        yelT = 0
        for k in range(min(h - i0, l)):
            i = i0 + k
            j = k
            if npBoard[i, j] == RED_TOKEN:
                redT += 1
                yelT = 0
            elif npBoard[i, j] == YELLOW_TOKEN:
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


def checkState(npBoard):
    resultat = checkHorizontal(npBoard) or checkVertical(npBoard[::-1, :]) or checkDiagonal(npBoard) or checkDiagonal(
        npBoard[:, ::-1]) or checkDiagonal(npBoard.T[1:, :]) or checkDiagonal(npBoard[:, -2::-1].T)

    if resultat:
        return resultat

    if (npBoard == 0).any():
        return None
    return EMPTY_CELL


def decision(board, bot_is_red):
    val, child_board = -float('inf') if bot_is_red else float('inf'), TUPLE_ORIGINAL
    for child in tree[board]:
        if bot_is_red and val < scores[child] or not bot_is_red and val > scores[child]:
            val = scores[child]
            child_board = child
    diff = 0
    while diff < BOARD_SIZE and child_board[diff] == board[diff]:
        diff += 1
    return diff


gen_score()
minimax(TUPLE_ORIGINAL, 5)

