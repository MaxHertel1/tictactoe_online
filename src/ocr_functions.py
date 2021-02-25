# from AppKit import NSScreen
from selenium import webdriver
from PIL import Image, ImageOps
from os import error, remove
import os
import cv2
import pytesseract
import numpy as np
import math

pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'

# OCR functions
def makeScreenshot(current_session: webdriver):

    # make Screencapture and save
    current_session.get_screenshot_as_file('./input.png')

    # open Screencapture
    # img_in = Image.open('./input.png')

    img_input = cv2.imread('./input.png')
    img_input = cv2.cvtColor(img_input, cv2.COLOR_BGR2GRAY)

    img_input = cv2.threshold(img_input, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    img_input = cv2.medianBlur(img_input, 3)
    
    # detecting all lines
    lines = cv2.HoughLines(img_input,1, np.pi / 180, 150, None, 0, 0)

    if lines is not None:
            for i in range(0, len(lines)):
                rho = lines[i][0][0]
                theta = lines[i][0][1]
                a = math.cos(theta)
                b = math.sin(theta)
                x0 = a * rho
                y0 = b * rho
                pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
                pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
                cv2.line(cdst, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)

    # if len(matches) != 0:
    #     print(len(matches))
    #     print(matches[0])
    # else:
    #     print('no matches')
        # for (x, y, width, height) in matches: 
        
        #     # We draw a green rectangle around 
        #     # every recognized sign 
        #     cv2.rectangle(gray, (x, y),  
        #                 (x + height, y + width),  
        #                 (0, 255, 0), 5) 
            
        #     # Creates the environment of  
        #     # the picture and shows it 

        #     cv2.imshow(gray) 





    return
    remove('./input.png')

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
    
    # detecting if its a circle
    matches = cv2.HoughCircles(gray)

    if len(matches) != 0:
        print(len(matches))

        for (x, y, width, height) in matches: 
        
            # We draw a green rectangle around 
            # every recognized sign 
            cv2.rectangle(gray, (x, y),  
                        (x + height, y + width),  
                        (0, 255, 0), 5) 
            
            # Creates the environment of  
            # the picture and shows it 

            cv2.imshow(gray) 



    filename = input.format(os.getpid())
    cv2.imwrite(filename, gray)

    text = pytesseract.image_to_string(gray)

    return text
