from cmu_graphics import *
from utils import processImage
from textEditor import TextGrid, drawGrid, getCodeListAndDimensions, stringifyCodeList
import io, sys, os

ERR_MESSAGE = "There's an error somewhere!"

# imagets from flaticons
def setColorScheme(mode):
    pass


def onAppStart(app):
    # MAIN SCREEN PARAMS
    app.lightGray = rgb(240, 240, 240)
    app.buttonTop, app.buttonLeft = 10, 10
    app.buttonWidth, app.buttonHeight = 180, 80
    app.lineOffset = 36
    app.imagePath = './images/test1.png'
    app.code = None
    app.output = None
    app.grid = None
    app.colorScheme = 'light'

###############
# MAIN SCREEN #
###############

def drawLineNumbers(app, x, y):
    lineNumbers = list(range(len(app.code)))
    lineNumbers = [num + 1 for num in lineNumbers]
    for i in range(len(lineNumbers)):
        lineNumber = lineNumbers[i]
        drawLabel(lineNumber, x, y + app.lineOffset*i, align='center', font='Courier', size=30, fill='gray')

def drawOutput(app, x, y):
    for i in range(len(app.output)):
        line = app.output[i]
        drawLabel(line, x, y + app.lineOffset*i, size=30, align='left', font='Courier', fill='gray')

def getOutput(app):
    # https://docs.python.org/3/library/functions.html#exec 
    # used chatGPT to figure out how to get the exec output as a string
    # define a string buffer to capture output
    outputBuffer = io.StringIO()
    # redirect stdout to the buffer
    sys.stdout = outputBuffer
    # execute the code
    try:
        exec(stringifyCodeList(app.grid))
    except:
        print("There's an error in the code!")
    # reset stdout to default
    sys.stdout = sys.__stdout__
    # retrieve the captured output
    capturedOutput = outputBuffer.getvalue()
    app.output = capturedOutput.splitlines()

def setGridParams(app):

    app.boardWidth = 800
    app.boardHeight = 350
    app.codeList, app.rows, app.cols = getCodeListAndDimensions(app.imagePath)
    app.grid = TextGrid(
        rows = app.rows,
        cols = app.cols,
        boardLeft = 35,
        boardWidth = app.boardWidth - 400,
        boardHeight = app.boardHeight - 100,
        boardTop = 100,
        cellBorderWidth = 1,
        selection = None,
        hovered = None,
        codeList=app.codeList,
        cellBorderColor=None,
        cellColor=None
    )

def main_onMouseMove(app, mouseX, mouseY):
    if app.grid is not None:
        hoveredCell = app.grid.getCell(mouseX, mouseY)
        app.grid.hovered = hoveredCell  

def main_onKeyPress(app, key):
    if app.grid.selection is not None:
        row, col = app.grid.selection 
        if key == 'backspace':
            app.grid.codeList[row][col] = ''
        else:
            if key not in ['enter', 'escape', 'tab']:
                app.grid.codeList[row][col] = key
               
def main_onMousePress(app, mouseX, mouseY):

    if 10 <= mouseX <= 190 and 10 <= mouseY <= 90:
        setActiveScreen('fileTree')
    if app.code is not None:
        if 250 <= mouseX <= 430 and 10 <= mouseY <= 90:
            getOutput(app)
    if app.grid is not None:
        selectedCell = app.grid.getCell(mouseX, mouseY)
        if selectedCell != None:
            if selectedCell == app.grid.selection:
                app.grid.selection = None
            else:
                app.grid.selection = selectedCell
                app.grid.hovered = None

def main_redrawAll(app):
    drawRect(0, 0, app.width, 100, fill=app.lightGray)
    # File Explorer Button
    drawRect(10, 10, app.buttonWidth, app.buttonHeight, fill='white', border='darkGray')
    drawLabel('File Explorer', 10 + app.buttonWidth/ 2, 10 + app.buttonHeight/2, size=18)

    # Editor Button
    drawRect(400, 500, app.width, 500, fill=None, border='darkGray')

    # Display Code and run button
    if app.code is not None:
        drawLine(30, 100, 30, app.height, fill='darkGray')
        # drawLineNumbers(app, 15, 120)
        drawGrid(app, grid=app.grid)

        # Run button
        drawRect(250, 10, app.buttonWidth, app.buttonHeight, fill='white', border='darkGray')
        drawLabel('Run Code', 250 + app.buttonWidth/ 2, 10 + app.buttonHeight/2, size=18, fill='green')

    # Display Output 
    if app.output is not None :
        drawOutput(app, 420, 530)

    if app.grid == None:
        drawLabel(f'Select an image file from the file explorer to get started!', 35, 300, font='Courier', size=20, bold=True, align='left')

#############
# FILE TREE #
#############

def fileTree_onScreenActivate(app):
    app.files = listFiles()
    # https://docs.python.org/3/library/os.html  
    app.fileStack = [os.getcwd()]

    app.previousFiles = app.files
    app.lineOffset = 30
    app.selectedFileIndex = 0
    app.fileTreeLeft = 40
    app.fileTreeTop = app.height // 2 - (len(app.files) * app.lineOffset) + 30
    app.characterWidth = 20
    app.characterHeight = 20
    app.selectedFile = getCurrentFilePath(app)
    app.selectedFileIsImage = False
    app.flashImageOpenError = False

def drawFiles(app):
    for i in range(len(app.files)):
        file = app.files[i]
        isBold = True if os.path.isdir(file) else False
        drawLabel(file, app.fileTreeLeft, app.fileTreeTop + app.lineOffset*i, align='left', font='Courier', size=30, fill='gray', bold=isBold)
     
def drawSelectedFileLine(app):
    drawLine(
        app.fileTreeLeft, 
        app.fileTreeTop + app.lineOffset * app.selectedFileIndex + app.characterHeight,
        app.fileTreeLeft + len(app.files[app.selectedFileIndex]) * app.characterWidth, 
        app.fileTreeTop + app.lineOffset * app.selectedFileIndex + app.characterHeight,
        lineWidth = 3
    )

def drawImageOpenError(app):
    x, y = app.width // 2, app.height // 2 + 300
    drawLabel('The currently selected file is not an image!', x, y, size=30, fill='red', font='Courier', bold=True)

def isImage(app):
    fileSuffixes = ('.png', '.jpg')
    app.selectedFileIsImage = True if app.selectedFile.endswith(fileSuffixes) else False

def listFiles(path='.'):
    files = []
    dirs = []
    for file in os.listdir(path):
        if os.path.isdir(file):
            dirs.append(file)
        else:
            files.append(file)
    return dirs + files

def getCurrentFilePath(app):
    return os.path.abspath(app.files[app.selectedFileIndex])

def fileTree_onKeyPress(app, key):
    app.flashImageOpenError = False
    if key == 'up' and app.selectedFileIndex > 0:
        app.selectedFileIndex -= 1
        app.selectedFile = app.files[app.selectedFileIndex]
        isImage(app)
    elif key == 'down' and app.selectedFileIndex < len(app.files) - 1:
        app.selectedFileIndex += 1
        app.selectedFile = app.files[app.selectedFileIndex]
        isImage(app)
    elif key == 'enter' and os.path.isdir(getCurrentFilePath(app)):
        app.fileStack.append(getCurrentFilePath(app))
        app.files = listFiles(getCurrentFilePath(app))
        app.selectedFileIndex = 0
        app.selectedFile = app.files[app.selectedFileIndex]
        isImage(app)
    elif key == 'backspace' and len(app.fileStack) > 1:
        app.fileStack.pop()
        previousDir = app.fileStack[-1]
        app.files = listFiles(previousDir)
        app.selectedFileIndex = 0
        app.selectedFile = app.files[app.selectedFileIndex]
        isImage(app)
    elif key == 'tab':
        if app.selectedFileIsImage:
            target = processImage(app.imagePath)
            app.code = target.splitlines()
            setGridParams(app) 
            setActiveScreen('main')
        else:
            app.flashImageOpenError = True

def fileTree_redrawAll(app):
    drawFiles(app)
    drawSelectedFileLine(app)
    if app.flashImageOpenError:
        drawImageOpenError(app)

def main(app):
    runAppWithScreens(height=1000, width=1000, initialScreen='main')

if __name__ == '__main__':
    main(app)