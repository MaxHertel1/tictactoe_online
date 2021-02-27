from selenium import webdriver
from PIL import Image, ImageOps
from os import error, lseek, remove
import os
import cv2
import pytesseract
import numpy
from time import sleep

pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'

# OCR functions
def updateGameBoardOcr(current_session: webdriver):
    gameBoard = [None] * 9

    # make Screencapture and save
    current_session.get_screenshot_as_file('../img/input.png')

    getIndividualBoxes()

    # return gameboard
    return

def getIndividualBoxes():
    # open Screencapture
    img_in = Image.open('../img/input.png')
    # remove('./input.png')

    if img_in.mode == 'RGBA':
        r, g, b, a = img_in.split() # no alpha needed
        img_rgb = Image.merge('RGB', (r, g, b))
        img_inverted = ImageOps.invert(img_rgb)
    else:
        img_inverted = ImageOps.invert(img_in)

    img_inverted.save('../img/inverted.png')

    img_in = cv2.imread('../img/inverted.png')
  
    # resize image
    img_h, img_w = img_in.shape[:2]

    # img_h *= .9
    # img_w *= .8

    crop_img = img_in[int(img_h*.15):int(img_h*.7), int(img_w*.35):int(img_w*.65)]

    # cv2.imshow('crop_img', crop_img)
    # cv2.waitKey(0)

    output = ""
    help = False
    # fill list with default point (left upper corner)
    cropPoints_x = [[0,img_h]]
    cropPoints_y = [[img_h,0]]

    # find where to crop at the x axis
    for y, row in enumerate(crop_img[0:1]):
        for x, column in enumerate(row):
            if(0 in column and not help):
                cropPoints_x.append([x-1,y])
                help = True
            elif (not 0 in column and help):
                cropPoints_x.append([x,y])
                help = False

            if (len(cropPoints_x) == 4): break
        if (len(cropPoints_x) == 4): break
    
    # find where to crop at the y axis
    for x, row in enumerate(crop_img[:1, 1:]):
        for y, column in enumerate(row):
            if(0 in column and not help):
                cropPoints_y.append([x,y-1])
                help = True
            elif (not 0 in column and help):
                cropPoints_y.append([x,y])
                help = False

    cropPoints_x.append([img_w,0])
    cropPoints_y.append([0, img_w])
    
    print(cropPoints_x)
    print(cropPoints_y)
        
        
    for i in range(9):


        # output = ""
        # for i in row:
        #     if(0 in i):
        #         output = output + "#"
        #     else:
        #         output = output + "_"
            
    #     print(output)
    # print(img_in)
    # h = 20
    # w = 20
    # crop_img = img_in[d_height//2:d_height//2, d_width:d_width+w]

    # # img = cv2.rectangle(img_in, (0+offset, d_height-offset), (d_width-offset,0+offset),(0,200,0),5)
    # cv2.imshow('image', crop_img)
    # cv2.waitKey(0)
    exit()

    # get size
    width, height = img_in.size 

    # TODO size adjustments needs to be dynamic to get good results on every windowsize
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
        remove('./final.png')
    except:
        print('No final.png found => First Loop')

    # save new picture
    img_inverted.save('./final.png')
    img_inverted.close()

def analyzeBoard(imageSet: list):
    # opening the cropped/inverted picture
    imageSet = [None] * 9
    img_final = Image.open('./final.png')
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
            imageSet[i].save('./board/pos' + str(i+1) + '.png')
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

if __name__ == '__main__':
    try:
        webElements = [None]*9
        driver = webdriver.Safari()
        driver.get('https://playtictactoe.org')
        driver.set_window_position(0,0)

        driver.maximize_window()

        # accept cookies => clean vision
        element = driver.find_element_by_id('consent')
        element.click()
        
        element = driver.find_element_by_class_name('board')
        elements = element.find_elements_by_xpath('./*')

        for i, element in enumerate(elements):
            webElements[i] = element

        webElements[0].click()
        sleep(.5)
        updateGameBoardOcr(driver)
    except error as e:
        print(e.strerror)
    finally:
        driver.close()
