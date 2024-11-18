import pytesseract
import cv2 as cv


def processImage(img_path):
    img = cv.imread(img_path)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]

    target = pytesseract.image_to_string(img, lang='eng_best')
    return target

def listifyCode(code):
    # number of lines in s becomes the number of rows for 2d list
    rows = len(code.splitlines())
    # length of longest string becomes number of columns, to keep list rectangular
    cols = max(len(line) for line in code.splitlines())
    # create a 2d "board" to represent the code 
    L = [ [None]*cols for _ in range(rows) ]
    
    i = j = k = 0
    while i < rows:

        if code[k] == '\n':

            i += 1
            j = 0
        else:    
            L[i][j] = code[k]
            j += 1
        k += 1

if __name__ == '__main__':
    
    target = processImage(img_path='./test2.jpg')
    print(target)
    
