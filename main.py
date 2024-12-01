from cmu_graphics import *
from utils import processImage, loadColors, getScaledImageSize, reloadColors
from textEditor import TextGrid, drawGrid, getCodeListAndDimensions, stringifyCodeList, updateGridColors
import io, sys, os

ERR_MESSAGE = "There's an error somewhere!"

def onAppStart(app):
    # MAIN SCREEN PARAMS
    app.buttonTop, app.buttonLeft = 10, 10
    app.buttonWidth, app.buttonHeight = 180, 80
    app.lineOffset = 36
    app.imagePath = './images/test1.png'
    app.code = None
    app.output = None
    app.grid = None

    app.colorSchemeIsLight = True

    (app.primary, app.secondary, app.tertiary,
    app.green, app.red, app.textColor, app.lightUrl, 
    app.darkUrl) = loadColors(app.colorSchemeIsLight)
    
    app.background = app.primary 
    
    app.colorSchemeSwitcherUrl = app.lightUrl if app.colorSchemeIsLight else app.darkUrl
    app.fileExplorerButtonX = 10
    app.fileExplorerButtonY = 10
    
    app.runButtonX = 250
    app.runButtonY = 10
    
    app.colorSchemeSwitcherX = 800
    app.colorSchemeSwitcherY = 50

    app.outputBoxX = 400
    app.outputBoxY = 500
    app.outputBoxHeight = 500

###############
# MAIN SCREEN #
###############

# FIX THIS
def drawLineNumbers(app, x, y):
    lineNumbers = list(range(len(app.code)))
    lineNumbers = [num + 1 for num in lineNumbers]
    for i in range(len(lineNumbers)):
        lineNumber = lineNumbers[i]
        drawLabel(lineNumber, x, y + app.lineOffset*i, align='center', font='Courier', size=30, fill='gray')

def drawOutput(app, x, y):
    for i in range(len(app.output)):
        line = app.output[i]
        drawLabel(line, x, y + app.lineOffset*i, size=30, align='left', font='Courier', fill=app.tertiary)

def drawColorschemeSwitcher(app, x, y):
    im_width, im_height = getScaledImageSize(app.colorSchemeSwitcherUrl, 7)

    drawImage(app.colorSchemeSwitcherUrl, x, y, 
            width=im_width, height=im_height, 
            align='center')


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
        cellColor=None,
        textColor=app.textColor
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
    # check if file explorer is clicked
    if 10 <= mouseX <= 190 and 10 <= mouseY <= 90:
        setActiveScreen('fileTree')
    # check if run button is clicked
    if app.code is not None:
        if 250 <= mouseX <= 430 and 10 <= mouseY <= 90:
            getOutput(app)
    # grid highlighting logic
    if app.grid is not None:
        selectedCell = app.grid.getCell(mouseX, mouseY)
        if selectedCell != None:
            if selectedCell == app.grid.selection:
                app.grid.selection = None
            else:
                app.grid.selection = selectedCell
                app.grid.hovered = None
    # chenk if colorscheme switcher is clicked
    im_width, im_height = getScaledImageSize(app.colorSchemeSwitcherUrl, 7)
    if (app.colorSchemeSwitcherX - im_width // 2 <= mouseX <= app.colorSchemeSwitcherX + im_width // 2 and 
        app.colorSchemeSwitcherY - im_height // 2 <= mouseY <= app.colorSchemeSwitcherY + im_height // 2):
        reloadColors(app)
        updateGridColors(app, grid=app.grid)

def main_redrawAll(app):

    # file explorer button
    drawRect(app.fileExplorerButtonX, app.fileExplorerButtonY, 
             app.buttonWidth, app.buttonHeight, fill=app.primary, 
             border=app.secondary)
    
    drawLabel('File Explorer', app.fileExplorerButtonX + app.buttonWidth // 2, 
              app.fileExplorerButtonY + app.buttonHeight // 2, size=18, fill=app.textColor)

    # output box
    drawRect(app.outputBoxX, app.outputBoxY, app.width, app.outputBoxHeight, 
             fill=None, border=app.secondary)

    # colorscheme switcher
    drawColorschemeSwitcher(app, app.colorSchemeSwitcherX, app.colorSchemeSwitcherY)

    # display code and run button
    if app.code is not None:
        drawLine(0, 100, app.width, 100, fill=app.secondary)
        drawLine(30, 100, 30, app.height, fill=app.secondary)
        # drawLineNumbers(app, 15, 120)
        
        drawGrid(app, grid=app.grid)

        # run button
        drawRect(app.runButtonX, app.runButtonY, app.buttonWidth, app.buttonHeight, fill=app.primary, border=app.secondary)
        drawLabel('Run Code', app.runButtonX + app.buttonWidth // 2, 
                  app.runButtonY + app.buttonHeight // 2, size=18, fill=app.green)

    # display Output 
    if app.output is not None :
        drawOutput(app, 420, 530)

    if app.grid == None:
        drawLabel(f'Select an image file from the file explorer to get started!', 35, 300, 
                  font='Courier', size=20, bold=True, align='left', fill=app.secondary)

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
    app.fileTreeTop = app.height // 2 - (len(app.files) * app.lineOffset) + 100
    app.characterWidth = 20
    app.characterHeight = 20
    app.selectedFile = getCurrentFilePath(app)
    app.selectedFileIsImage = False
    app.flashImageOpenError = False
    
def drawFiles(app):
    for i in range(len(app.files)):
        file = app.files[i]
        isBold = True if os.path.isdir(file) else False
        drawLabel(file, app.fileTreeLeft, app.fileTreeTop + app.lineOffset*i, 
                  align='left', font='Courier', size=30, fill=app.tertiary, bold=isBold)
     
def drawSelectedFileLine(app):
    drawLine(
        app.fileTreeLeft, 
        app.fileTreeTop + app.lineOffset * app.selectedFileIndex + app.characterHeight,
        app.fileTreeLeft + len(app.files[app.selectedFileIndex]) * app.characterWidth, 
        app.fileTreeTop + app.lineOffset * app.selectedFileIndex + app.characterHeight,
        lineWidth = 3, fill=app.textColor)

def drawImageOpenError(app):
    x, y = app.width // 2, app.height // 2 + 300
    drawLabel('The currently selected file is not an image!', x, y, 
              size=30, fill=app.red, font='Courier', bold=True)

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