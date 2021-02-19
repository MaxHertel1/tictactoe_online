from html_functions import *
from ocr_functions import *
from util import *

from selenium import webdriver
from time import sleep
from os import error
from selenium.webdriver.safari.webdriver import WebDriver

webElements = [None] * 9
gameCount = 10

# main
try:
    driver = webdriver.Safari() 
    driver.get('https://playtictactoe.org')
    driver.set_window_size(1000,1000)

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
    for i in range(1):

        # reset gameboard for new game
        gameBoard = [None] * 9
    
        # first move is random
        webElements[findRandomMove(gameBoard)].click()
        while (True):
            sleep(1)
            gameboard = updateGameBoardHtml(driver, gameBoard)
            if (isGameOver(gameBoard) != False):
                break
            else:
                # webElements[findRandomMove()].click()
                webElements[findBestMove(gameBoard)].click()

        if (isGameOver(gameBoard) == 'X'):
            wins = wins + 1
        elif (isGameOver(gameBoard) == 'O'):
            losses = losses + 1
        else:
            unsettled = unsettled + 1

        print('############# ROUND ' + str(wins+losses+unsettled) + ' #############')
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
    print('unsettled: ' + str(unsettled))
    print('')
    