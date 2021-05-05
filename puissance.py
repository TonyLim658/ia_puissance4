tree = {}  # tuple: [tuple] | int
scores = {}  # tuple: int
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
# TUPLE_ORIGINAL = (
#     EMPTY_CELL, EMPTY_CELL,
#     EMPTY_CELL, EMPTY_CELL,)

# [0 , 1 , 2 , 3 , 4 , 5 , 6 , 7 , 8 , 9 , 10, 11]
# [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
# [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
# [36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47]
# [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59]
# [60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]
# [72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83]
# [84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95]


def test():
    assert (tuple_to_array((1, 0, -1, 0), 2, 2) == [[1, 0], [-1, 0]])
    assert (tuple_to_array((1, 0, -1, 0, 1, 1), 3, 2) == [[1, 0, -1], [0, 1, 1]])
    assert (tuple_to_array(TUPLE_ORIGINAL) == [[EMPTY_CELL for _ in range(BOARD_LENGTH)] for _ in range(BOARD_HEIGHT)])

    assert (array_to_tuple([[1, 0], [-1, 0]]) == (1, 0, -1, 0))
    assert (array_to_tuple([[1, 0, -1], [0, 1, 1]]) == (1, 0, -1, 0, 1, 1))

    assert (get_index_token_positionable(TUPLE_ORIGINAL) == [84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95])
    assert (get_index_token_positionable((
                  EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
                  EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
                  EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
                  EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
                  EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
                  EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
                  RED_TOKEN, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, YELLOW_TOKEN, EMPTY_CELL, EMPTY_CELL,
                  RED_TOKEN, EMPTY_CELL, YELLOW_TOKEN, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, YELLOW_TOKEN, EMPTY_CELL, RED_TOKEN, RED_TOKEN, EMPTY_CELL, EMPTY_CELL,
                 )) == [60, 85, 74, 87, 88, 89, 78, 91, 80, 69, 94, 95])

    # CheckState tests
    assert (checkState((
        RED_TOKEN, RED_TOKEN, RED_TOKEN, RED_TOKEN, RED_TOKEN, RED_TOKEN, RED_TOKEN, RED_TOKEN, EMPTY_CELL, EMPTY_CELL,
        EMPTY_CELL, EMPTY_CELL,
        EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
        EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
        EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
        EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
        EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
        EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
        EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
        EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
        EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
        EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
        EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
        EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
        EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
        EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
    )) == RED_TOKEN)

    assert (checkState((
        EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
        EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
        RED_TOKEN, RED_TOKEN, RED_TOKEN, RED_TOKEN, RED_TOKEN, RED_TOKEN, RED_TOKEN, RED_TOKEN, EMPTY_CELL, EMPTY_CELL,
        EMPTY_CELL, EMPTY_CELL,
        EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
        EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
        EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
        EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
        EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
        EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
        EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
        EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
        EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
        EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
        EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
        EMPTY_CELL, EMPTY_CELL, EMPTY_CELL,
    )) == RED_TOKEN)


def update_tuple(tuple_to_update, index, val):
    tuple_updated = list(tuple_to_update)
    tuple_updated[index] = val
    tuple_updated = tuple(tuple_updated)
    return tuple_updated


def tuple_to_array(tuple_to_update, length=BOARD_LENGTH, height=BOARD_HEIGHT):
    list_returned = [[] for _ in range(height)]
    for i, v in enumerate(tuple_to_update):
        list_returned[i // length].append(v)
    return list_returned


def array_to_tuple(array_to_update):
    one_dimensional_array = []
    for row in array_to_update:
        for cell in row:
            one_dimensional_array.append(cell)
    return tuple(one_dimensional_array)


# def value_of_tuple_from_x_y(tuple_to_search, x, y, length=BOARD_LENGTH):
#     return tuple_to_search[y*length+x]


def get_index_token_positionable(board, length=BOARD_LENGTH, height=BOARD_HEIGHT):
    indexes = []
    board_to_list = tuple_to_array(board, length, height)
    for x in range(length):
        for y in range(height-1, -1, -1):
            # print((x, y, y*length+x, board_to_list[y][x]))
            if board_to_list[y][x] == EMPTY_CELL:
                indexes.append(y*length+x)
                break
    # print(indexes)
    return indexes


def minimax(board, is_red=True, length=BOARD_LENGTH, height=BOARD_HEIGHT):
    if board in tree:
        return
    # state = check_state(board)
    # if type(state) == int:
    #     tree[board] = state
    #     # scores[board] = state
    #     return
    # else:
    #     tree[board] = []
    tree[board] = []
    # TODO calculate score
    # score = -float('inf') if is_red else float('inf')
    # TODO changer parcours
    for i in get_index_token_positionable(board, length, height):
        # Modification du tuple pour inscrire la case dans laquelle on joue
        child_board = update_tuple(board, i, RED_TOKEN if is_red else YELLOW_TOKEN)

        tree[board].append(child_board)
        minimax(child_board, not is_red, length, height)
        # score = max(score, scores[child_board]) if is_red else min(score, scores[child_board])
    # scores[board] = score


def checkState(board):
    # lines
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_LENGTH):
            if j + 4 >= BOARD_LENGTH:
                break

            case = i * BOARD_LENGTH + j
            if board[case] == board[case + 1] and board[case + 1] == board[case + 2] and board[case + 2] == board[
                case + 3] and board[case + 3] == board[case + 4] and board[case] != EMPTY_CELL:
                return board[case]

    # columns
    for j in range(BOARD_LENGTH):
        for i in range(BOARD_HEIGHT):

            if i + 4 >= BOARD_HEIGHT:
                break

            case = i * BOARD_LENGTH + j
            if board[case] == board[case + 1 * BOARD_LENGTH] and board[case + 1 * BOARD_LENGTH] == board[
                case + 2 * BOARD_LENGTH] and board[case + 2 * BOARD_LENGTH] == board[case + 3 * BOARD_LENGTH] and board[
                case + 3 * BOARD_LENGTH] == board[case + 4 * BOARD_LENGTH] and board[case] != EMPTY_CELL:
                return board[case]

    # diagonales
    for i in range(BOARD_HEIGHT):
        for j in range(3, BOARD_LENGTH):
            if j + 4 >= BOARD_LENGTH or i + 4 >= BOARD_HEIGHT:
                break

            case = i * BOARD_LENGTH + j
            if board[case] == board[case + 1 * BOARD_LENGTH + 1] and board[case + 1 * BOARD_LENGTH + 1] == board[
                case + 2 * BOARD_LENGTH + 2] and board[case + 2 * BOARD_LENGTH + 2] == board[
                case + 3 * BOARD_LENGTH + 3] and board[case + 3 * BOARD_LENGTH + 3] == board[
                case + 4 * BOARD_LENGTH + 4] and board[case] != EMPTY_CELL:
                return board[case]

            if board[case] == board[case + 1 * BOARD_LENGTH - 1] and board[case + 1 * BOARD_LENGTH - 1] == board[
                case + 2 * BOARD_LENGTH - 2] and board[case + 2 * BOARD_LENGTH - 2] == board[
                case + 3 * BOARD_LENGTH - 3] and board[case + 3 * BOARD_LENGTH - 3] == board[
                case + 4 * BOARD_LENGTH - 4] and board[case] != EMPTY_CELL:
                return board[case]

    return


def decision(board, bot_is_red):
    pass


test()
minimax((0,0,0,0), True, 2, 2)
count = 0
for k, v in tree.items():
    count += 1
print(tree)
print(count)

