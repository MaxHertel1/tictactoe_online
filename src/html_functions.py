from selenium import webdriver

class html_functions:
    # HTML functions
    def updateGameBoardHtml(current_session: webdriver):

        # get data directly from website
        element = current_session.find_element_by_class_name('board')
        elements = element.find_elements_by_xpath('./*')

        gameBoard = [None] * 9

        for i, element in enumerate(elements):

            val = str(element.find_element_by_xpath('./*').get_attribute('class')).lower()

            if (val == 'x'):
                gameBoard[i] = 'X'
            elif (val == 'o'):
                gameBoard[i] = 'O'
            else:
                gameBoard[i] = None
                
            i=i+1
        
        return gameBoard