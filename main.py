from selenium import webdriver
from time import sleep
from os import error, remove
from PIL import Image, ImageOps
import pytesseract
import cv2
import os

from selenium.webdriver.safari.webdriver import WebDriver

pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'

w, h = 3, 3
gameBoard = [[0 for x in range(w)] for y in range(h)]
imageSet = [[0 for x in range(w)] for y in range(h)]

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

def isGameOver():
    # check for winner
    # from left to right all rows
    if (gameBoard[0][0]==gameBoard[0][1]==gameBoard[0][2]): return True
    if (gameBoard[1][0]==gameBoard[1][1]==gameBoard[1][2]): return True
    if (gameBoard[2][0]==gameBoard[2][1]==gameBoard[2][2]): return True

    # from top to down all columns
    if (gameBoard[0][0]==gameBoard[1][0]==gameBoard[2][0]): return True
    if (gameBoard[0][1]==gameBoard[1][1]==gameBoard[2][1]): return True
    if (gameBoard[0][2]==gameBoard[1][2]==gameBoard[2][2]): return True

    # from top to down all columns
    if (gameBoard[0][0]==gameBoard[1][1]==gameBoard[2][2]): return True
    if (gameBoard[0][2]==gameBoard[1][1]==gameBoard[2][0]): return True

    print ('checked game')
    return True

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

def interpreteWeb(current_session: webdriver):
    # get data directly from website
    element = current_session.find_element_by_class_name('board')
    elements = element.find_elements_by_xpath('.//*')
    for element in elements:
        print(element.get_attribute('class'))

def analyzeBoard():
    # opening the cropped/inverted picture
    img_final = Image.open('final.png')
    width, height = img_final.size

    print(img_final.size)
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
            imageSet[row][column] = img_final.crop((left, top, right, bottom))

            imageSet[row][column].save('board/x' + str(row+1) + 'y' + str(column+1) + '.png')
            print(interpreteSymbol('board/x' + str(row+1) + 'y' + str(column+1) + '.png'))
    # updating the Array
    return


#####################
try:
    driver = webdriver.Safari() 
    driver.get('https://playtictactoe.org')
    driver.set_window_size(1000,1000)

    # accept cookies => clean vision
    element = driver.find_element_by_id('consent')
    element.click()
    
except error as e:
    print(e.strerror)
finally:
    sleep(1)
    # 
    #####################

    #while (not isGameOver):
    # makeScreenshot(driver)
    # analyzeBoard()



    #remove('input.png')
    # ending session
    #####################
    # sleep(5)
    driver.quit()
    #####################
    print('ende')


