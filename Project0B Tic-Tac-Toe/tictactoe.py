"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x = 0
    for row in board:
        for state in row:
            if state == X:
                x+=1
            elif state == O:
                x-=1
    if x <= 0:
        return "X";
    else:
        return "O";


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action = []
    order = [(0, 1), (1, 2), (2, 1), (0, 0), (1, 1), (2, 0), (0, 2), (2, 2), (1, 0)]

    for i, j in order:
        if board[i][j] == EMPTY:
            action.append((i, j))
    result = {(i, j) for i, j in action}
    return result


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action[0] < 0 or action[0] > 2 or action[1] < 0 or action[1] > 2 or board[action[0]][action[1]] != None:
        raise NotImplementedError
    new_board = copy.deepcopy(board)
    new_board[action[0]][action[1]] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    num = utility(board)
    if num == 1:
        return X
    elif num == -1:
        return O
    else:
        return


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if utility(board) != 0:
        return True
    for row in board:
        for state in row:
            if state == EMPTY:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winning_conditions = [
    [(0, 0), (0, 1), (0, 2)],
    [(1, 0), (1, 1), (1, 2)],
    [(2, 0), (2, 1), (2, 2)],
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 1), (2, 1)],
    [(0, 2), (1, 2), (2, 2)],
    [(0, 0), (1, 1), (2, 2)],
    [(0, 2), (1, 1), (2, 0)]]
    
    for condition in winning_conditions:
        if all(board[x][y] == X for x, y in condition):
            return 1
        elif all(board[x][y] == O for x, y in condition):
            return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return

    d = {}
    pl = player(board)
    for action in actions(board):
        num = getnum(result(board, action), 1 if pl == X else 0)
        if d.get(num, None) == None:
            d[num] = action
            
    if pl == X:
        if 1 not in d:
            return d[1]
        elif 0 not in d:
            return d[0]
        else:
            return d[-1]
    else:
        if -1 not in d:
            return d[-1]
        elif 0 not in d:
            return d[0]
        else:
            return d[1]
    

def getnum(board, mini):
    if terminal(board):
        match winner(board):
            case "X":
                return 1
            case "O":
                return -1
            case None:
                return 0

    scores = []
    for action in actions(board):
        num = getnum(result(board, action), 1 - mini)
        scores.append(num)
            
    if mini == 0:
        return max(scores)
    else:
        return min(scores)