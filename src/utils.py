import pytesseract
import cv2 as cv
import os
from cmu_graphics import *

# this helper function processes Python files into a string
def processPythonFile(filePath):
    # get absolute path
    absPath = os.path.abspath(filePath)
    # check if the file exists
    if not os.path.exists(absPath):
        raise FileNotFoundError(f"The file at {absPath} does not exist.")
    # open and read the file content
    # https://stackoverflow.com/questions/3758147/easiest-way-to-read-write-a-files-content-in-python 
    with open(filePath, 'r') as file:
        fileContent = file.read()
    
    return fileContent

# this helper function scans image files into a string
def processImageFile(filePath):
    # verify the file path
    abs_path = os.path.abspath(filePath)
    if not os.path.exists(abs_path):
        raise FileNotFoundError(f"The file at {abs_path} does not exist.")
    # attempt to read the image
    img = cv.imread(abs_path)
    if img is None:
        raise ValueError(f"Failed to load the image. Ensure it's a valid image file: {abs_path}")
    
    # convert to grayscale
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    # apply thresholding
    _, img = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    custom_config = r'--psm 4'
    
    # extract text using pytesseract
    target = pytesseract.image_to_string(img, config=custom_config)

    return target    

# this helper function creates a grid out of a multi-line string
def listifyCode(code):
    # number of lines in code becomes the number of rows for 2d list
    rows = len(code.splitlines())
    # length of longest string becomes number of columns, to keep list rectangular
    cols = max(len(line) for line in code.splitlines())
    # create a 2d grid to represent the code 
    grid = [['']* cols for _ in range(rows)]
    # populate the grid
    rowIndex = colIndex = characterIndex = 0
    while rowIndex < rows and characterIndex < len(code):
        # if there is a newline, go to a next row and set col
        # index to the beginning 
        if code[characterIndex] == '\n':
            rowIndex += 1
            colIndex = 0
        else:    
            # map character to position in grid
            grid[rowIndex][colIndex] = code[characterIndex]
            colIndex += 1
        characterIndex += 1
    return grid

# this helper function is used to set the colorscheme
def loadColors(colorSchemeIsLight):
    primary = 'white' if colorSchemeIsLight else 'black'
    secondary = 'darkGray' if colorSchemeIsLight else 'silver'
    tertiary = 'gray' if colorSchemeIsLight else 'gainsboro'
    green = 'green' if colorSchemeIsLight else 'lightGreen' 
    red = 'red' if colorSchemeIsLight else 'salmon'
    text = 'black' if colorSchemeIsLight else 'white'
    # images from https://www.flaticon.com/free-icons/light-mode 
    lightPath =  "/Users/aravbhardwaj/Documents/Code/TERM-PROJ/assets/light-mode.png"
    darkPath = "/Users/aravbhardwaj/Documents/Code/TERM-PROJ/assets/night-mode.png"

    return primary, secondary, tertiary, green, red, text, lightPath, darkPath

# this helper function reloads the app-level colors
def reloadColors(app):
    app.colorSchemeIsLight = not app.colorSchemeIsLight
    (app.primary, app.secondary, app.tertiary, 
    app.green, app.red, app.textColor, app.lightUrl, app.darkUrl) = loadColors(app.colorSchemeIsLight)
    app.background = app.primary
    app.colorSchemeSwitcherUrl = app.lightUrl if app.colorSchemeIsLight else app.darkUrl

# this helper function scales images down
def getScaledImageSize(path, shrinkFactor):
    width, height = getImageSize(path)
    return width // shrinkFactor, height // shrinkFactor

# this helper function counts the number of whitespace
def countWhiteSpace(line):
    count = 0
    for char in line:
        if char.isspace():
            count += 1
        else:
            break
    return count  