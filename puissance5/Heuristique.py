from .Utils import *

BLOCK_SCORE_YELLOW = {}
BLOCK_SCORE_RED = {}


def factoriel(n):
    if n in [0, 1]:
        return 1
    if n == 2:
        return 2
    return factoriel(n-1) * factoriel(n-2)


def gen_score(rge=12):
    assert (rge >= TOKEN_WINNING_NUMBER)
    t_last_iter = [((0, 0, 0, 0), 0), ((1, 0, 0, 0), 1), ((1, 1, 0, 0), 2), ((1, 1, 1, 0), 3),
                   ((1, 1, 1, 1), 4), ((1, 1, 0, 1), 3), ((1, 0, 1, 0), 2), ((1, 0, 1, 1), 3),
                   ((1, 0, 0, 1), 2), ((0, 1, 0, 0), 1), ((0, 1, 1, 0), 2), ((0, 1, 1, 1), 3),
                   ((0, 1, 0, 1), 2), ((0, 0, 1, 0), 1), ((0, 0, 1, 1), 2), ((0, 0, 0, 1), 1)]

    for i in range(TOKEN_WINNING_NUMBER - 1, rge):
        t = []
        for k, v in t_last_iter:
            t.append(([0] + list(k), v))
            t.append(([1] + list(k), v + 1))
        for k, v in t:
            # on applique un facteur pour que les tableaux correspondent aux valeurs des pions
            # -1 fois le tableaux -1 fois le score
            BLOCK_SCORE_RED[tuple([item * RED_TOKEN for item in k])] = factoriel(v) * RED_TOKEN
            BLOCK_SCORE_YELLOW[tuple([item * YELLOW_TOKEN for item in k])] = factoriel(v) * YELLOW_TOKEN
        t_last_iter = t


def _heur_horizontal(np_board):
    h, l = np_board.shape
    score = 0

    # le but est de regarder les score par block au changement de couleur ou en fin de ligne
    for i in range(h):
        RED_BOX = []
        YELLOW_BOX = []
        for j in range(l):
            val = np_board[i, j]
            # si on tombe sur un pion jaune
            if val == RED_TOKEN:
                # on va voir si le fragments avec des jetons jaunes peut être exploiter
                if len(YELLOW_BOX) >= TOKEN_WINNING_NUMBER:
                    # exploitable donc on va chercher le score qui correspond
                    score += BLOCK_SCORE_YELLOW[tuple(YELLOW_BOX)]

                YELLOW_BOX = []
                RED_BOX.append(val)
            # si on tombe sur un pion rouge
            elif val == YELLOW_TOKEN:
                # on va voir si le fragments avec des jetons rouges peut être exploiter
                if len(RED_BOX) >= TOKEN_WINNING_NUMBER:
                    # exploitable donc on va chercher le score qui correspond
                    score += BLOCK_SCORE_RED[tuple(RED_BOX)]

                YELLOW_BOX.append(val)
                RED_BOX = []

            else:
                lenY = len(YELLOW_BOX)
                lenR = len(RED_BOX)
                # dans le cas où on est en fin de grille et que la ligne n'est pas remplie de 0
                if j == l - 1:
                    if lenY >= TOKEN_WINNING_NUMBER and lenY > lenR:
                        score += BLOCK_SCORE_YELLOW[tuple(YELLOW_BOX)]
                    elif lenR >= TOKEN_WINNING_NUMBER and lenR > lenY:
                        score += BLOCK_SCORE_RED[tuple(RED_BOX)]
                else:
                    RED_BOX.append(val)
                    YELLOW_BOX.append(val)
    return score


def _heur_vertical(np_board):
    h, l = np_board.shape
    score = 0

    # le but est de regarder les scores par block dès qu'il n'y a plus de jeton dans la colonne
    for j in range(l):
        RED_BOX = []
        YELLOW_BOX = []
        for i in range(h):
            val = np_board[i, j]
            # si on tombe sur un pion jaune
            if val == RED_TOKEN:

                YELLOW_BOX = []
                RED_BOX.append(val)

            # si on tombe sur un pion rouge
            elif val == YELLOW_TOKEN:

                YELLOW_BOX.append(val)
                RED_BOX = []

            # le reste de la colonne est vide
            else:
                lenY = len(YELLOW_BOX)
                lenR = len(RED_BOX)
                # nombre de vides pour compléter la colonne
                nbVides = h - i
                if lenY > 0:
                    for add in range(nbVides):
                        YELLOW_BOX.append(val)
                    if lenY >= TOKEN_WINNING_NUMBER:
                        score += BLOCK_SCORE_YELLOW[tuple(YELLOW_BOX)]
                elif lenR > 0:
                    for add in range(nbVides):
                        RED_BOX.append(val)
                    if lenR >= TOKEN_WINNING_NUMBER:
                        score += BLOCK_SCORE_RED[tuple(RED_BOX)]
                break
    return score


def _heur_diagonal(np_board):
    h, l = np_board.shape
    score = 0

    # le but est de regarder les scores par block au changement de couleur ou en fin de diagonale
    for i0 in range(h - (TOKEN_WINNING_NUMBER - 1)):
        RED_BOX = []
        YELLOW_BOX = []
        for k in range(min(h - i0, l)):
            i = i0 + k
            j = k
            val = np_board[i, j]
            # si on tombe sur un pion jaune
            if val == RED_TOKEN:
                # on va voir si le fragments avec des jetons jaunes peut être exploiter
                if len(YELLOW_BOX) >= TOKEN_WINNING_NUMBER:
                    # exploitable donc on va chercher le score qui correspond
                    score += BLOCK_SCORE_YELLOW[tuple(YELLOW_BOX)]

                YELLOW_BOX = []
                RED_BOX.append(val)
            # si on tombe sur un pion rouge
            elif val == YELLOW_TOKEN:
                # on va voir si le fragments avec des jetons rouges peut être exploiter
                if len(RED_BOX) >= TOKEN_WINNING_NUMBER:
                    # exploitable donc on va chercher le score qui correspond
                    score += BLOCK_SCORE_RED[tuple(RED_BOX)]

                YELLOW_BOX.append(val)
                RED_BOX = []

            else:
                lenY = len(YELLOW_BOX)
                lenR = len(RED_BOX)
                # dans le cas où on est en fin de grille et que la diagonale n'est pas remplie de 0
                if j == l - 1:
                    if lenY >= TOKEN_WINNING_NUMBER and lenY > lenR:
                        score += BLOCK_SCORE_YELLOW[tuple(YELLOW_BOX)]
                    elif lenR >= TOKEN_WINNING_NUMBER and lenR > lenY:
                        score += BLOCK_SCORE_RED[tuple(RED_BOX)]
                else:
                    RED_BOX.append(val)
                    YELLOW_BOX.append(val)
    return score


def heuristic(np_board):
    # heuristeam ¯\_(ツ)_/¯
    score = _heur_horizontal(np_board) + _heur_vertical(np_board[::-1, :]) + _heur_diagonal(np_board) + _heur_diagonal(
        np_board[:, ::-1]) + _heur_diagonal(np_board.T[1:, :]) + _heur_diagonal(np_board[:, -2::-1].T)
    return score
