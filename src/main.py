from html_functions import *
from ocr_functions import *
from util import *

from selenium import webdriver
from time import sleep
from os import error
from selenium.webdriver.safari.webdriver import WebDriver

gameBoard = [None] * 9
webElements = [None] * 9
gameCount = 20

if __name__ == "__main__":
    try:
        driver = webdriver.Safari() 
        driver.get('https://playtictactoe.org')
        # driver.set_window_size(1000,1000)
        driver.maximize_window()

        # accept cookies => clean vision
        element = driver.find_element_by_id('consent')
        element.click()

        # getting all web ellements and save in webElements-list
        # (for clicking operation)
        element = driver.find_element_by_class_name('board')
        elements = element.find_elements_by_xpath('./*')

        for i, element in enumerate(elements):
            webElements[i] = element

        wins = 0
        losses = 0
        unsettled = 0
        i = 0
        # starting main loop 
        for i in range(gameCount):

            # reset the website when playing mulitple rounds
            if (i>0):
                element = driver.find_element_by_class_name('game')
                restart = element.find_element_by_xpath('./div[2]')
                restart.click()

                # reset gameboard for new game
                for i, val in enumerate(gameBoard):
                    gameBoard[i] = None
                print(gameBoard)

                # wait so website can make a move
                sleep(1)

            # check if website made first move
            
            # gameBoard = updateGameBoardHtml(driver, gameBoard)
            # if ('O' not in gameBoard):
            #     # webiste made no move => first move is random
            #     randomMove = findRandomMove(gameBoard)
            #     webElements[randomMove].click()
            
            makeScreenshot(driver)
            
            '''
            while (True):
                sleep(1)
                gameBoard = updateGameBoardHtml(driver, gameBoard)

                gameContainer = driver.find_element_by_class_name('game')
                board = gameContainer.find_element_by_xpath('./div[1]')

                # check if its a win, loose or draw (checking website for board class)
                if (isGameOver(gameBoard) != False or board.get_attribute('class') != 'board'):
                    break
                else:
                    bestMove = findBestMove(gameBoard)
                    print('bester Zug:', bestMove)
                    webElements[bestMove].click()

            print('Endstand: ', gameBoard)
            if (isGameOver(gameBoard) == 'X'):
                wins = wins + 1
            elif (isGameOver(gameBoard) == 'O'):
                losses = losses + 1
            else:
                unsettled = unsettled + 1

            print('############# ROUND ' + str(wins+losses+unsettled) + ' #############')
            print('Winner: ' + str(isGameOver(gameBoard)))
            sleep(2)
            '''
    except error as e:
        print(e.strerror)
    finally:
        sleep(1)
        driver.quit()

        # final Output
        print('')
        print('wins: ' + str(wins))
        print('losses: ' + str(losses))
        print('unsettled: ' + str(unsettled))
        print('')
        