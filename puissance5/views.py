# Create your views here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.shortcuts import render

from .Puissance import *

tree = {}  # tuple: [tuple] | int
scores = {}  # tuple: int
depth_record = {}  # tuple: int
BLOCK_SCORE_YELLOW = {}
BLOCK_SCORE_RED = {}

GAME_BOARD = np.copy(BOARD_ORIGINAL)

def handler404(request, exception):
    return render(request, "errors/404.html")


def handler500(request):
    return render(request, "errors/500.html")

def game(request):
    global GAME_BOARD
    GAME_BOARD = np.copy(BOARD_ORIGINAL)
    return render(request, "game.html", {'iLines': [0,1,2,3,4,5,6,7], 'jColumns': [0,1,2,3,4,5,6,7,8,9,10,11]})


###### PARTIE JEU ############
def isPositionable(positionX, positionY):
    if GAME_BOARD[positionX][positionY] == EMPTY_CELL:
        return True
    else:
        return False


def endOfTheGame(state):
    if state == EMPTY_CELL:
        message = "Egalité. Rejouez!"
        return message
    elif state == YELLOW_TOKEN:
        message = "Les jaunes gagnent la partie ! "
        return message
    else:
        message = "Les rouges gagnent la partie ! "
        return message


def gameplayUpdate(typeCell, position):

    #stateG 1 : fin de partie ; 2 : tour suivant ; 3 : rejouer

    if isPositionable(position[0],position[1]):
        GAME_BOARD[position[0]][position[1]] = typeCell

        state = check_state(GAME_BOARD)
        if state != UNFINISHED_STATE:
            message = endOfTheGame(state)
            stateG = 1
        else :
            message = "Au tour du joueur suivant."
            stateG = 2

        return [message, stateG]

    else:
        message = "Position impossible. Jouez un autre coup."
        stateG = 3
        return [message, stateG]


def playerTurn(cellType, position):
    return gameplayUpdate(cellType, position)


def botTurn(isFirst, cellType, position):
    return gameplayUpdate(cellType, position)


def askForBegin():
    ans = input("Do you want to start? (y/n) : ")
    if ans == "y":
        return False
    elif ans == "n":
        return True
    else:
        return askForBegin()

def play(request):
    column = int(request.POST.get('col', None))
    line = int(request.POST.get('line', None))
    token = request.POST.get('token', None)

    if token == "RED_TOKEN" :
        res = playerTurn(RED_TOKEN, [line, column])
        token = "YELLOW_TOKEN"
    else :
        res = playerTurn(YELLOW_TOKEN, [line, column])
        token = "RED_TOKEN"


    data = {
        #'line': line,
        #'column': column,
        'message': res[0],
        'state': res[1],
        'token': token
    }

    return JsonResponse(data)

def restart(request):
    global GAME_BOARD
    GAME_BOARD = np.copy(BOARD_ORIGINAL)
    return JsonResponse({'ok':True})
