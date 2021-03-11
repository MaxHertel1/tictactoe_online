from selenium import webdriver
from PIL import Image, ImageOps
from os import error, lseek, remove
import os
import cv2
import pytesseract
import numpy
from time import sleep
import math 

pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.1.1/bin/tesseract'

# OCR functions
def updateGameBoardOcr(current_session: webdriver):
    gameBoard = [None] * 9

    # make Screencapture and save
    current_session.get_screenshot_as_file('./img/input.png')

    getIndividualBoxes()

    # return gameboard
    return

def getIndividualBoxes():
    # open Screencapture
    try:
        img_in = Image.open('./img/input.png')

    except error as e:
        print(e.strerror)
        return

    if img_in.mode == 'RGBA':
        r, g, b, a = img_in.split() # no alpha needed
        img_rgb = Image.merge('RGB', (r, g, b))
        img_inverted = ImageOps.invert(img_rgb)
    else:
        img_inverted = ImageOps.invert(img_in)

    img_inverted.save('./img/inverted.png')

    img_in = cv2.imread('./img/inverted.png')
  
    # resize image
    img_h, img_w = img_in.shape[:2]

    # img_h *= .9
    # img_w *= .8

    crop_img = img_in[int(img_h*.15):int(img_h*.7), int(img_w*.35):int(img_w*.65)]

    img_h, img_w = crop_img.shape[:2]
 
    # fill list with default point 
    cropPoints_x = [1]
    cropPoints_y = [img_h-1]

    cv2.imwrite('./img/cropped.png',crop_img)

    newimg = crop_img

    in_line = False
    # find where to crop at the x axis
    for x, row in enumerate(crop_img[0,:]):
        if(0 in row and not in_line):
            cropPoints_x.append(x-1)
            in_line = True
        elif (255 in row and in_line):
            cropPoints_x.append(x)
            in_line = False

    in_line = False 
    # find where to crop at the y axis
    for y, column in enumerate(crop_img[:, 0]):
        if(0 in column and not in_line):
            cropPoints_y.append(y-1)
            in_line = True
        elif (255 in column and in_line):
            cropPoints_y.append(y)
            in_line = False

    cropPoints_x.append(img_w+1)
    cropPoints_y.append(1)

    cropPoints_x.sort()
    cropPoints_y.reverse()
    cropPoints_y.sort()

    Arr_cropPoints_x = numpy.array(cropPoints_x)

    Arr_cropPoints_y = numpy.array(cropPoints_y)

    for i, val in enumerate(Arr_cropPoints_y):
        print(i, Arr_cropPoints_y[i])
    
    print(Arr_cropPoints_x)
    print(Arr_cropPoints_y)

    box_imgs = []
    print('-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#-#')
    i = crop_img[1 : 257, 283 : 582]

    cv2.imshow('',i)
    cv2.waitKey(0)

    png_output = 0
    for ii in range(0,5,2):
        for jj in range(0,5,2):

            h1 = int(Arr_cropPoints_y[jj])
            h2 = int(Arr_cropPoints_y[jj+1])
            w1 = int(Arr_cropPoints_x[ii])
            w2 = int(Arr_cropPoints_x[ii+1])

            # newimg = cv2.line(newimg,(1,h1),(1,h2),(255,0,0),3)
            # newimg = cv2.line(newimg,(w1,1),(w2,1),(0,255,0),3)

            # newimg = cv2.circle(newimg, (w1,h1),2,(0,255,0),2)
            # newimg = cv2.circle(newimg, (w2,h2),2,(0,255,0),2)
            # cv2.imshow('str(i)', newimg) 
            # cv2.waitKey(0)

            # cropped_img = Image.open('../img/cropped.png')

            # h,w = cropped_img.size
            # box_img = cropped_img.crop((w1,w-w2,h1,h-h1))

            # box_img.save(f'../img/sliced/\{i}.png')

            # newimg = cv2.rectangle(newimg,(w1,h1), (w2,h2), (0,0,255),3)

            # print(h1, h2, w1, w2)
            cropped_img = cv2.imread('./img/cropped.png')
            box_img = cropped_img[w1:w2, h1:h2]

            scale_percent = 3 # percent of original size
            width = int(box_img.shape[1] * scale_percent / 100)
            height = int(box_img.shape[0] * scale_percent / 100)
            dim = (width, height)
            
            # resize image
            resized = cv2.resize(box_img, dim, interpolation = cv2.INTER_AREA)

            for row in resized:
                output = ""
                for column in row:
                    for i in row:
                        if(0 in i):
                            output = output + "#"
                        else:
                            output = output + "_"
                print(output)

            cv2.imwrite(f'./img/sliced/{png_output}.png', box_img)
            png_output+=1
            # i = crop_img.crop()
            # # i = crop_img[w1:h1, w2:h2]

            # # box_imgs.append(crop_img[Arr_cropPoints_y[i]:Arr_cropPoints_y[i+1], Arr_cropPoints_x[j]:Arr_cropPoints_x[j+1]])
            # # i = crop_img[Arr_cropPoints_y[i]:Arr_cropPoints_y[i+1], Arr_cropPoints_x[j]:Arr_cropPoints_x[j+1]]
            # # print(Arr_cropPoints_y[i], Arr_cropPoints_y[i+1], Arr_cropPoints_x[j], Arr_cropPoints_x[j+1])
    

    
    # i = crop_img[h1:h2, w1:w2]

    # for i, box_img in enumerate(box_imgs):
    #     cv2.imwrite('../img/sliced/\{i}.png', box_img)


    
    # box_img = crop_img[0:200, 0:200]

    
    # sleep(.5)
    # cv2.imshow('str(i)', box_img2)
    # cv2.waitKey(0)

    # print(cropPoints_y[i], cropPoints_y[i+1])
    # print(cropPoints_x[j], cropPoints_x[j+1])
    # print(box_img)
    # fill list with default point
    # print(cropPoints_x)
    # cropPoints_y.reverse()
    # print(cropPoints_y)

    # box_imgs = []
    # for i, x in enumerate(cropPoints_x):
    #     if i < len(cropPoints_x)-1:
    #         for j, y in enumerate(cropPoints_y):
    #             if j < len(cropPoints_y)-1:

    #                 crop_img = cv2.rectangle(crop_img,(cropPoints_y[i],cropPoints_y[i+1]), (cropPoints_x[j],cropPoints_x[j+1]), (255, 000, 000),4)
    #                 # box_imgs.append(crop_img[cropPoints_y[i]:cropPoints_y[i+1], cropPoints_x[j]:cropPoints_x[j+1]])
    #                 # print(y,cropPoints_x[j+1], x, cropPoints_y[i+1])
    
    # print(len(box_imgs))
    # for i, box_img in enumerate(box_imgs):

    # cv2.imshow('str(i)', box_img)
    # cv2.waitKey(0)
    # sleep(1)

    # cv2.imshow(i, box_img)
    # cv2.waitKey(0)
    # cropPoints_y[i] : cropPoints_y[i+1], 0 : cropPoints_y[i]
    # [cropPoints_x[i],cropPoints_x[i]]
        
    # for i in range(3):
    #     for j in range(3):

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

# if __name__ == '__main__':
#     try:
#         webElements = [None]*9
#         driver = webdriver.Safari()
#         driver.get('https://playtictactoe.org')
#         driver.set_window_position(0,0)

#         driver.maximize_window()

#         # accept cookies => clean vision
#         element = driver.find_element_by_id('consent')
#         element.click()
        
#         element = driver.find_element_by_class_name('board')
#         elements = element.find_elements_by_xpath('./*')

#         for i, element in enumerate(elements):
#             webElements[i] = element

#         webElements[0].click()
#         sleep(.5)
#         updateGameBoardOcr(driver)
#     except error as e:
#         print(e.strerror)
#     finally:
#         driver.close()

if __name__ == '__main__':
    getIndividualBoxes()