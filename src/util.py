
import random 

# gameBoard functions
def isGameOver(board: list):
    # check for winner
    # from left to right all rows
    if (board[0] != None and (board[0]==board[1]==board[2])): return board[0]
    if (board[3] != None and (board[3]==board[4]==board[5])): return board[3]
    if (board[6] != None and (board[6]==board[7]==board[8])): return board[6]
    
    # from top to down all columns
    if (board[0] != None and (board[0]==board[3]==board[6])): return board[0]
    if (board[1] != None and (board[1]==board[4]==board[7])): return board[1]
    if (board[2] != None and (board[2]==board[5]==board[8])): return board[2]

    # from top to down all columns
    if (board[0] != None and (board[0]==board[4]==board[8])): return board[0]
    if (board[2] != None and (board[2]==board[4]==board[6])): return board[2]

    return False

def findRandomMove(gameBoard: list):
    while (True):
        i = random.randrange(0, 8, 1)
        if (gameBoard[i] == None):
            return i

def areMovesLeft(gameBoard: list):
    for each in gameBoard:
        if (each == None):
            return True

def evaluateGame(gameBoard: list):
    if (isGameOver(gameBoard) == 'X'): return 10
    if (isGameOver(gameBoard) == 'O'): return -10
    return 0

def miniMax(board: list, depth: int, isMax: int):
    score = evaluateGame(board)
    
    if (score == 10): return score

    if (score == -10): return score

    if (areMovesLeft == False): return 0

    if (isMax):
        best = -10000

        for i, val in enumerate(board):
            if (val == None): 
                board[i] = 'X'
                best = max(best, miniMax(board, depth+1, not isMax))
                board[i] = None
        
        return best
    else:
        best = 10000

        for i, val in enumerate(board):
            if(val == None):
                board[i] = 'O'
                best = min(best, miniMax(board, depth+1, not isMax))
                board[i] = None
        return best

def findBestMove(gameboard: list):
    bestChoice = -1
    bestVal = -1000
    for i, val in enumerate(gameboard):
        if (val == None):
            gameboard[i] = 'X'
            moveVal = miniMax(gameboard, 0, False)
            gameboard[i] = None
            print('move:', i, 'score:', moveVal)
            if (moveVal>bestChoice):
                bestChoice = i
                bestVal = moveVal

    print('# best move: ', bestChoice, 'score: ', bestVal)
    print('')
    return bestChoice
