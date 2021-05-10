# Create your views here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import JsonResponse
from django.shortcuts import render

from timeit import default_timer

from .Puissance import *

import json

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


def gameplayUpdate(typeCell, position):

    #stateG 1 : fin de partie ; 2 : tour suivant ; 3 : rejouer

    if isPositionable(position[0],position[1]):
        GAME_BOARD[position[0]][position[1]] = typeCell

        state = check_state(GAME_BOARD)
        if state != UNFINISHED_STATE:
            stateEOG = state
            stateG = 1
        else :
            stateEOG = -2
            stateG = 2

        return [stateEOG, stateG]

    else:
        stateEOG = -2
        stateG = 3
        return [stateEOG, stateG]


def playerTurn(cellType, position):
    return gameplayUpdate(cellType, position)


def botTurn(cellType):
    position = decision(GAME_BOARD, cellType)
    return [position, gameplayUpdate(cellType, position)]


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
        'stateEOG': res[0],
        'state': res[1],
        'token': token,
        'winPos': json.dumps(winning_positions[-5:])
    }

    return JsonResponse(data)

def playBot(request):
    token = request.POST.get('token', None)

    start = default_timer()

    if token == "RED_TOKEN" :
        res = botTurn(RED_TOKEN)
        token = "YELLOW_TOKEN"

    else :
        res = botTurn(YELLOW_TOKEN)
        token = "RED_TOKEN"

    duration = default_timer() - start

    data = {
        'duration': duration,
        'stateEOG': res[1][0],
        'state': res[1][1],
        'posI': res[0][0],
        'posJ': res[0][1],
        'token': token,
        'winPos': json.dumps(winning_positions[-5:])
    }

    return JsonResponse(data)

def restart(request):
    global GAME_BOARD
    GAME_BOARD = np.copy(BOARD_ORIGINAL)
    return JsonResponse({'ok':True})
