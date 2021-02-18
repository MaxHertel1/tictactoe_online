from selenium import webdriver
from time import sleep
from os import error, remove, replace
from PIL import Image, ImageOps
import pytesseract
import cv2
import os
import random

from selenium.webdriver.safari.webdriver import WebDriver

pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'

gameBoard = [None] * 9
imageSet = [None] * 9
webElements = [None] * 9
helpBoard = [None] * 9

# OCR functions
def makeScreenshot(current_session: webdriver):

    # make Screencapture and save
    current_session.get_screenshot_as_file('input.png')

    # open Screencapture
    img_in = Image.open('input.png')
    remove('input.png')

    # get size
    width, height = img_in.size 

    # Setting the points for cropped image 
    left = 160
    top = height-900
    right = width -160
    bottom = height-200

    # doing the crop
    img_cropped = img_in.crop((left, top, right, bottom))

    # cannot invert image with transparancies
    if img_cropped.mode == 'RGBA':
        r, g, b, a = img_cropped.split()
        img_rgb = Image.merge('RGB', (r, g, b))
        img_inverted = ImageOps.invert(img_rgb)
    else:
        img_inverted = ImageOps.invert(img_cropped)

    img_in.close()
    img_cropped.close()

    # try deleting the old (last) picture
    try:
        remove('final.png')
    except:
        print('No final.png found => First Loop')

    # save new picture
    img_inverted.save('final.png')
    img_inverted.close()

def analyzeBoard():
    # opening the cropped/inverted picture
    img_final = Image.open('final.png')
    width, height = img_final.size
    i=0
    for column in range(0, 3):
        for row in range(0, 3):
            # get single pictures

            # cuts off a little bit more for the edge
            crop_off = 30
            top = int(height/3 * row) + crop_off
            bottom = int(height - (height/3 * (3-(row+1)))) - crop_off
            left = int(width/3 * column) + crop_off
            right = int(width - (width/3 * (3-(column+1)))) - crop_off

            print('x' + str(row+1) + 'y' + str(column+1))
            # print('top: ' + str(top))
            # print('bottom: ' + str(bottom))
            # print('left: ' + str(left))
            # print('right: ' + str(right))

            # print(left, top, right, bottom)
            imageSet[i] = img_final.crop((left, top, right, bottom))
            imageSet[i].save('board/pos' + str(i+1) + '.png')
            i=i+1
            print(interpreteSymbol('board/pos' + str(i+1) + '.png'))

    # updating the Array
    return

def interpreteSymbol(input: str):
    # interpretiere ein übereichtes Bild und gebe ein Symbol zurück (X oder O)
    image = cv2.imread(input)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    gray = cv2.threshold(gray, 0, 255,
    cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    gray = cv2.medianBlur(gray, 3)
    
    filename = input.format(os.getpid())
    cv2.imwrite(filename, gray)

    text = pytesseract.image_to_string(gray)

    return text

# HTML functions
def updateGameBoardHtml(current_session: webdriver):

    # get data directly from website
    element = current_session.find_element_by_class_name('board')
    elements = element.find_elements_by_xpath('./*')

    for i, element in enumerate(elements):

        # save WebElements in Array
        val = str(element.find_element_by_xpath('./*').get_attribute('class')).lower()
        # print(str(i) + val)
        if (val == 'x'):
            gameBoard[i] = 'X'
        elif (val == 'o'):
            gameBoard[i] = 'O'
        else:
            gameBoard[i] = None
            
        i=i+1
    
    return

# gameBoard functions
def isGameOver(board: list):
    # TODO: vergleich auf symbole

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

def makeRandomMove():
    while (True):
        i = random.randrange(0, 8, 1)
        if (gameBoard[i] == None):
            webElements[i].click()
            break

def calculateBestMove(virtBoard: list, score: int, turn: str):
    # MinMax Algo for calculating move with best proper outcome
    for i, val in enumerate(virtBoard):
        if (val == None):
            virtBoard[i] = turn
            print(virtBoard)
            calculateBestMove(virtBoard, 0, 'O') if (turn=='X') else calculateBestMove(virtBoard, 0, 'X')
        if (isGameOver(virtBoard) == 'X') : score = score + 1
    return score

def makeBestMove():
    # MinMax Algo for calculating move with best proper outcome
    highestScore = None
    bestCoice = None
    
    for i, val in enumerate(gameBoard):
        # print(val)
        # print(i, val)
        print(str(val) + ' - ' + str(i))
        if (gameBoard[i] == None):
            for ii in range(8):
                helpBoard[ii] = gameBoard[i]
            
            score = calculateBestMove(helpBoard, 0, 'X')
            
            if (highestScore == None): 
                highestScore = score
                bestCoice = 1
            elif (score>highestScore):
                bestCoice = i
        print(str(val) + ' - ' + str(i) + ' = score: ' + str(score))

    # print('best Choice: ' + str(bestCoice))
    if (bestCoice == None):
        makeRandomMove()
    else:
        webElements[bestCoice].click()
    return 

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

    # starting main loop 
    for i in range(1):
        while (True):
            sleep(2)
            updateGameBoardHtml(driver)
            print(gameBoard)
            if (isGameOver(gameBoard) != False):
                break
            else:
                # makeRandomMove()
                makeBestMove()

        if (isGameOver(gameBoard) == 'X'):
            wins = wins + 1
        elif (isGameOver(gameBoard) == 'O'):
            losses = losses + 1
        else:
            unsettled = unsettled + 1

        print('############# ROUND ' + str(wins+losses+unsettled) + ' #############')
        print('Winner: ' + str(isGameOver(gameBoard)))
        print('')
        print('wins: ' + str(wins))
        print('losses: ' + str(losses))
        print('unsettled: ' + str(unsettled))
        print('')

except error as e:
    print(e.strerror)
finally:
    sleep(1)
    driver.quit()
    


