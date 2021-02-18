from selenium import webdriver
from time import sleep
from os import error, remove, replace
from PIL import Image, ImageOps
import pytesseract
import cv2
import os

from selenium.webdriver.safari.webdriver import WebDriver

pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'

gameBoard = [None] * 9
imageSet = [None] * 9
webElements = [None] * 9

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
    # TODO: vergleich auf symbole

    # check for winner
    # from left to right all rows
    if (gameBoard[0]==gameBoard[1]==gameBoard[2]): return True
    if (gameBoard[3]==gameBoard[4]==gameBoard[5]): return True
    if (gameBoard[6]==gameBoard[7]==gameBoard[8]): return True
    
    # from top to down all columns
    if (gameBoard[0]==gameBoard[3]==gameBoard[6]): return True
    if (gameBoard[1]==gameBoard[4]==gameBoard[7]): return True
    if (gameBoard[2]==gameBoard[5]==gameBoard[8]): return True

    # from top to down all columns
    if (gameBoard[0]==gameBoard[4]==gameBoard[8]): return True
    if (gameBoard[2]==gameBoard[4]==gameBoard[6]): return True

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

def updateGameBoardHtml(current_session: webdriver):

    # get data directly from website
    element = current_session.find_element_by_class_name('board')
    elements = element.find_elements_by_xpath('.//*')

    for i, element in enumerate(elements):
        # name = element.get_attribute('class')

        # save WebElements in Array

        webElements[i] = element
        try:
            print(element.find_element_by_xpath('.//*').get_attribute('class'))
        except:
            print('NF')


    return

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


#####################
try:
    driver = webdriver.Safari() 
    driver.get('https://playtictactoe.org')
    driver.set_window_size(1000,1000)

    # accept cookies => clean vision
    element = driver.find_element_by_id('consent')
    element.click()

    # getting all web ellements and save in array
    # (for clicking operation)
    element = driver.find_element_by_class_name('board')
    elements = element.find_elements_by_xpath('.//*')
    
    i = 0
    for element in elements:
        option = element.get_attribute('class')
        option = option.replace( ' ','')
        option = option.replace('\n','')
        if (option != ''):
            print(str(i) + option)
            i=i+1
            webElements[i] = element

        # try:
        #     print(element.find_element_by_xpath('.//*').get_attribute('class'))
        # except:
        #     print('NF')
        # new_element = driver.find_element_by_class_name(option)
        # print(driver.find_element_by_class_name(option))


except error as e:
    print(e.strerror)
finally:
    sleep(3)
    driver.quit()
    print('ende')


