from selenium import webdriver
from time import sleep
from os import remove
from PIL import Image, ImageOps
from array import array

w, h = 2, 2
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

def analyzeBoard():
    # opening the cropped/inverted picture
    img_final = Image.open('final.png')
    width, height = img_final.size 

    for row in 2:
        for column in 2:

            left = width/3 * column+1
            top = height/3 * row+1
            right = width/3 * 3 - column+1
            bottom = height-200

            imageSet[row, column] = 
    # updating the Array
    return


driver = webdriver.Safari() 
driver.get('https://playtictactoe.org')

sleep(1)
driver.set_window_size(1000,1000)


#while (not isGameOver):
makeScreenshot(driver)
analyzeBoard()



#remove('input.png')
# ending session
sleep(5)
driver.quit()
print('ende')

#do while not win
    #get picture

    #analyze picture

    #do move

    #delete picture
