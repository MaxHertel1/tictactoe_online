import cv2
from numpy import array

class Compare:
    X = [
        [0,0,0,0,0,0,0,0,0],
        [0,1,0,0,0,0,0,1,0],
        [0,0,1,0,0,0,1,0,0],
        [0,0,0,1,0,1,0,0,0],
        [0,0,0,0,1,0,0,0,0],
        [0,0,0,1,0,1,0,0,0],
        [0,0,1,0,0,0,1,0,0],
        [0,1,0,0,0,0,0,1,0],
        [0,0,0,0,0,0,0,0,0],
    ]

    O = [
        [0,0,0,0,0,0,0,0,0],
        [0,0,0,1,1,1,0,0,0],
        [0,0,1,0,0,0,1,0,0],
        [0,1,0,0,0,0,0,1,0],
        [0,1,0,0,0,0,0,1,0],
        [0,1,0,0,0,0,0,1,0],
        [0,0,1,0,0,0,1,0,0],
        [0,0,0,1,1,1,0,0,0],
        [0,0,0,0,0,0,0,0,0],
    ]

    def detectSymbol(Symbol: list):
        '''
        find how out how much to resize (in nine by nine)
        '''

        scale_percent = 9/len(Symbol[0]) # percent of original size
        width = int(Symbol.shape[1] * scale_percent / 100)
        height = int(Symbol.shape[0] * scale_percent / 100)
        dim = (width, height)
        
        # resize Array
        resized = cv2.resize(Symbol, dim, interpolation = cv2.INTER_AREA)

        comparable = array()

        for i, row in enumerate(resized):
            for j, column in enumerate(resized):
                if 0 in column:
                    comparable[i][j] = 1
                else:
                    comparable[i][j] = 0
        
        print(comparable)
        
        return

    if (__name__ == '__main__'):
        img = cv2.imread('./img/sliced/0.png')
        print(detectSymbol(img))

