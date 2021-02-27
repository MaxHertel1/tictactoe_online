from html_functions import *
from ocr_functions import *
from util import *

from selenium import webdriver
from time import sleep
from os import error
from selenium.webdriver.safari.webdriver import WebDriver

gameBoard = [None] * 9
webElements = [None] * 9
gameCount = 2
boardUpdateMode = False

def printArgError():
    print('\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-')
    print('incorrect number of arguments')
    print('python3 main.py <board_update_method>')
    print('arg: ocr - using screenshots to update the board')
    print('     html - using html (xpth/classname functions) to update board')
    print('#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-\n')
    return

def printHelp():
    print('\n#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-')
    print('python3 main.py <board_update_method>')
    print('arg: ocr - using screenshots to update the board')
    print('     html - using html (xpth/classname functions) to update board')
    print('#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-\n')
    return

if (len(sys.argv) != 2):
    printArgError()
    exit()
elif (sys.argv[1] == 'ocr'):
    boardUpdateMode = True
elif (sys.argv[1] == 'html'):
    boardUpdateMode = False
elif (sys.argv[1] == 'help'):
    printHelp()
    exit()

print(boardUpdateMode, sys.argv)
exit()
# main
try:
    driver = webdriver.Safari() 
    driver.get('https://playtictactoe.org')
    driver.maximize_window

    # accept cookies => clean vision
    element = driver.find_element_by_id('consent')
    element.click()

    # getting all web ellements and save in webElements-list
    # (for clicking operation)
    element = driver.find_element_by_class_name('board')
    elements = element.find_elements_by_xpath('./*')

    for i, element in enumerate(elements):
        webElements[i] = element

    # resseting all count-variables
    wins = 0
    losses = 0
    draw = 0

    # starting main loop 
    for i in range(0, gameCount):
        # reset the website when playing mulitple rounds
        if (i>0):
            element = driver.find_element_by_class_name('game')
            restart = element.find_element_by_xpath('./div[2]')
            restart.click()

            # reset gameboard for new game
            for j, val in enumerate(gameBoard):
                gameBoard[j] = None
            print('reset:', gameBoard)

            # wait so website can make a move
            # sleep(0.5)

        # check if website made first move
        gameBoard = updateGameBoardHtml(driver, gameBoard)
        if ('O' not in gameBoard):
            # webiste made no move => first move is random
            randomMove = findRandomMove(gameBoard)
            webElements[randomMove].click()

        while (True):
            sleep(0.5)
            gameBoard = updateGameBoardHtml(driver, gameBoard)

            gameContainer = driver.find_element_by_class_name('game')
            board = gameContainer.find_element_by_xpath('./div[1]')

            # check if its a win, loose or draw (checking website for board class)
            if (isGameOver(gameBoard) != False or board.get_attribute('class') != 'board'):
                break
            else:
                sleep(0.5)
                gameBoard = updateGameBoardHtml(driver, gameBoard)
                bestMove = findBestMove(gameBoard)
                webElements[bestMove].click()

        print('Endstand: ')
        printBoard(gameBoard)
        if (isGameOver(gameBoard) == 'X'):
            wins = wins + 1
        elif (isGameOver(gameBoard) == 'O'):
            losses = losses + 1
        else:
            draw = draw + 1

        print('############# ROUND ' + str(wins+losses+draw) + ' #############')
        print('Winner: ' + str(isGameOver(gameBoard)))
        sleep(2)
        
except error as e:
    print(e.strerror)
finally:
    sleep(1)
    driver.quit()

    # final Output
    print('')
    print('wins: ' + str(wins))
    print('losses: ' + str(losses))
    print('draws: ' + str(draw))
    print('')

