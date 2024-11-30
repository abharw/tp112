import pytesseract
import cv2 as cv
from cmu_graphics import *

def processImage(img_path):
    img = cv.imread(img_path)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    img = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]
    target = pytesseract.image_to_string(img, config='--psm 6')
    return target

def listifyCode(code):
    # number of lines in s becomes the number of rows for 2d list
    rows = len(code.splitlines())
    # length of longest string becomes number of columns, to keep list rectangular
    cols = max(len(line) for line in code.splitlines())
    # create a 2d "board" to represent the code 
    L = [ ['']*cols for _ in range(rows) ]
    
    i = j = k = 0
    while i < rows:
        if code[k] == '\n':
            i += 1
            j = 0
        else:    
            L[i][j] = code[k]
            j += 1
        k += 1
    
    return L

def prettyPrint(d):

    for key in d:
        print(f'{key} -> {d[key]}')

def loadColors(colorSchemeIsLight):
    
    primary = 'white' if colorSchemeIsLight else 'black'
    secondary = 'darkGray' if colorSchemeIsLight else 'silver'
    tertiary = 'gray' if colorSchemeIsLight else 'gainsboro'
    green = 'green' if colorSchemeIsLight else 'lightGreen' 
    red = 'red' if colorSchemeIsLight else 'salmon'
    text = 'black' if colorSchemeIsLight else 'white'

    lightUrl =  "/Users/aravbhardwaj/Documents/Code/TERM-PROJ/assets/light-mode.png"
    darkUrl = "/Users/aravbhardwaj/Documents/Code/TERM-PROJ/assets/night-mode.png"

    return primary, secondary, tertiary, green, red, text, lightUrl, darkUrl

def getScaledImageSize(url, shrinkFactor):
    width, height = getImageSize(url)
    return width // shrinkFactor, height // shrinkFactor

if __name__ == '__main__':
    target = processImage(img_path='./images/test1.png')

    
