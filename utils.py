import pytesseract
import cv2 as cv
import os
from cmu_graphics import *

# def processImage(img_path):
#     abs_path = os.path.abspath(img_path)
#     img = cv.imread(abs_path)
#     img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
#     img = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)[1]
#     target = pytesseract.image_to_string(img, config='--psm 6')
#     return target

import cv2 as cv
import pytesseract
import os

def processImage(img_path):
    # Verify the file path
    abs_path = os.path.abspath(img_path)
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"The file at {abs_path} does not exist.")
    
    # Attempt to read the image
    img = cv.imread(abs_path)
    if img is None:
        raise ValueError(f"Failed to load the image. Ensure it's a valid image file: {abs_path}")
    
    # Convert to grayscale
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    # Apply thresholding
    _, img = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    
    # Extract text using pytesseract
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

def reloadColors(app):
    app.colorSchemeIsLight = not app.colorSchemeIsLight
    (app.primary, app.secondary, app.tertiary, 
    app.green, app.red, app.textColor, app.lightUrl, app.darkUrl) = loadColors(app.colorSchemeIsLight)
    app.background = app.primary
    app.colorSchemeSwitcherUrl = app.lightUrl if app.colorSchemeIsLight else app.darkUrl

if __name__ == '__main__':
    print(processImage('/Users/aravbhardwaj/Documents/Code/TERM-PROJ/images/Screenshot 2024-12-03 at 10.22.45.png'))
    