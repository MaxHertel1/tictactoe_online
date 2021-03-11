
import sys
import random 
#from main import round_num

class util:
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
        stop = 0
        while (stop < 9):
            i = random.randrange(0, 8, 1)
            if (gameBoard[i] == None):
                return i
            stop=+ 1

    def areMovesLeft(gameBoard: list):
        for each in gameBoard:
            if (each == None):
                return True

    def printBoard(gameBoard: list):
        print(gameBoard[0] or '_',gameBoard[1] or '_',gameBoard[2] or '_')
        print(gameBoard[3] or '_',gameBoard[4] or '_',gameBoard[5] or '_')
        print(gameBoard[6] or '_',gameBoard[7] or '_',gameBoard[8] or '_')

    def evaluateGame(gameBoard: list):
        eval = util.isGameOver(gameBoard)

        if (eval == 'X'): 
            return 10
        elif (eval == 'O'): 
            return -10
        else:
            return 0

    def miniMax(board: list, depth: int, isMax: bool):
        score = util.evaluateGame(board)

        if (score == 10):
            return score - depth
        elif (score == -10):
            return score + depth

        if (util.areMovesLeft(board) == False): return 0

        if (isMax):
            best = -10000

            for i, val in enumerate(board):
                if (val == None): 
                    board[i] = 'X'
                    best = max(best, util.miniMax(board, depth+1,  not isMax))
                    board[i] = None
            return best
        else:
            best = 10000

            for i, val in enumerate(board):
                if(val == None):
                    board[i] = 'O'
                    best = min(best, util.miniMax(board, depth+1,  not isMax))
                    board[i] = None
            return best

    def findBestMove(gameboard: list):
        bestChoice = -1
        bestVal = -1000
        
        for i, val in enumerate(gameboard):
            if (val == None):
                print('### - ', i)
                gameboard[i] = 'X'
                moveVal = util.miniMax(gameboard, 0, False)
                util.printBoard(gameboard)
                gameboard[i] = None
                print('move:', i, 'score:', moveVal)
                if (moveVal>bestVal):
                    bestChoice = i
                    bestVal = moveVal
        print('final move:', bestChoice, 'score:', bestVal)
        return bestChoice

    # debbuging
    if __name__ == '__main__':
        f = open("test.out", 'w')
        sys.stdout = f
        gameBoardd = [None] * 9
        
        # O X O 
        # X X O
        # _ _ _
        gameBoardd[2] = 'O'
        gameBoardd[1] = 'X'
        gameBoardd[0] = 'O'
        gameBoardd[3] = 'X'
        gameBoardd[4] = 'X'
        gameBoardd[5] = 'O'
        gameBoardd[findBestMove(gameBoardd)] = 'X'
        # gameBoardd[findRandomMove(gameBoardd)] = 'O'
        # gameBoardd[findBestMove(gameBoardd)] = 'X'
        # gameBoardd[findRandomMove(gameBoardd)] = 'O'
        # gameBoardd[findBestMove(gameBoardd)] = 'X'
        # gameBoardd[findRandomMove(gameBoardd)] = 'O'
        # gameBoardd[findBestMove(gameBoardd)] = 'X'
        # printBoard(gameBoardd)
        f.close()