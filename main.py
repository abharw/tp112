from cmu_graphics import *
from utils import processImage, loadColors, getScaledImageSize, reloadColors
from textEditor import (
    TextGrid, drawGrid, getCodeListAndDimensions, 
    stringifyCodeList, updateGridColors)
from traceCode import trace

import io, sys, os

ERR_MESSAGE = "There's an error somewhere!"

def onAppStart(app):
    # MAIN SCREEN PARAMS
    app.buttonTop, app.buttonLeft = 10, 10
    app.buttonWidth, app.buttonHeight = 180, 80
    app.lineOffset = 36
    app.imagePath = None

    app.rows = None
    app.cols = None
    app.codeList = None


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

    app.traceButtonX = 500
    app.traceButtonY = 10

    app.outputBoxX = 400
    app.outputBoxY = 500
    app.outputBoxHeight = 500

###############
# MAIN SCREEN #
###############

def drawOutput(app, x, y):
    for i in range(len(app.output)):
        line = app.output[i]
        drawLabel(line, x, y + app.lineOffset*i, size=30, align='left', font='Courier', fill=app.tertiary)

def drawColorschemeSwitcher(app, x, y):
    im_width, im_height = getScaledImageSize(app.colorSchemeSwitcherUrl, 7)

    drawImage(app.colorSchemeSwitcherUrl, x, y, 
            width=im_width, height=im_height, 
            align='center', opacity=40)

def drawTextButton(app, text, x, y, width, height, fill):
    drawRect(x, y, width, height, fill=app.primary, border=app.secondary)
    drawLabel(text, x + width // 2, y + height // 2, size=18, fill=fill)

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
    print(app.imagePath)
    app.codeList, app.rows, app.cols = getCodeListAndDimensions(app.imagePath)

    if app.rows is not None and app.cols is not None:
        app.grid = TextGrid(
            rows = app.rows,
            cols = app.cols,
            boardLeft = 35,
            boardWidth = app.boardWidth - 400,
            boardHeight = app.boardHeight - 100,
            boardTop = 150,
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
    if (app.fileExplorerButtonX <= mouseX <= app.fileExplorerButtonX + app.buttonWidth and 
        app.fileExplorerButtonY <= mouseY <= app.fileExplorerButtonY + app.buttonHeight):
        setActiveScreen('fileTree')
    # check if run button is clicked
    if app.code is not None:
        if (app.runButtonX <= mouseX <= app.runButtonX + app.buttonWidth and 
            app.runButtonY <= mouseY <= app.runButtonY + app.buttonHeight):
            getOutput(app)
    # check if trace button is clicked
    if app.code is not None:
        if (app.traceButtonX <= mouseX <= app.traceButtonX + app.buttonWidth and 
            app.traceButtonY <= mouseY <= app.traceButtonY + app.buttonHeight):
            setActiveScreen('trace')
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
        if app.grid != None:
            updateGridColors(app, grid=app.grid)

def main_redrawAll(app):

    # file explorer button
    drawTextButton(app, 'File Explorer', app.fileExplorerButtonX, app.fileExplorerButtonY, 
             app.buttonWidth, app.buttonHeight, fill=app.textColor)

    # output box
    drawRect(app.outputBoxX, app.outputBoxY, app.width, app.outputBoxHeight, 
             fill=None, border=app.secondary)
    # colorscheme switcher
    drawColorschemeSwitcher(app, app.colorSchemeSwitcherX, app.colorSchemeSwitcherY)

    # display code and run button
    if app.code is not None:
        drawLine(0, 100, app.width, 100, fill=app.secondary)  
        if app.grid is not None:      
            drawGrid(app, grid=app.grid)
        # run button
        drawTextButton(app, 'Run Code', app.runButtonX, app.runButtonY, 
                app.buttonWidth, app.buttonHeight, fill=app.green)
        # trace button
        drawTextButton(app, 'Trace Code', app.traceButtonX, app.traceButtonY, 
                       app.buttonWidth, app.buttonHeight, fill=app.textColor)
        
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
    app.fileTreeTop = app.height // 2 - (len(app.files) * app.lineOffset) + 200
    app.characterWidth = 20
    app.characterHeight = 20
    app.selectedFile = getCurrentFilePath(app)
    app.selectedFileIsImage = False
    app.flashImageOpenError = False

    app.backButtonX = 10
    app.backButtonY = 10
    
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
    absolutePath = os.path.abspath(path)

    files = []
    dirs = []
    for file in os.listdir(absolutePath):
        if os.path.isdir(os.path.join(absolutePath, file)):
            dirs.append(file)
        else:
            files.append(file)
    return dirs + files

def getCurrentFilePath(app):
    return os.path.abspath(app.files[app.selectedFileIndex])

def joinPaths(app):
    currentDirectory = app.fileStack[-1]
    selectedFile = app.files[app.selectedFileIndex]
    return os.path.join(currentDirectory, selectedFile)

def fileTree_onKeyPress(app, key):
    app.flashImageOpenError = False
    if key == 'up' and app.selectedFileIndex > 0:
        app.selectedFileIndex -= 1
        app.selectedFile = joinPaths(app)
        isImage(app)
    elif key == 'down' and app.selectedFileIndex < len(app.files) - 1:
        print(app.selectedFile)
        app.selectedFileIndex += 1
        app.selectedFile = joinPaths(app)
        isImage(app)
    elif key == 'enter' and os.path.isdir(getCurrentFilePath(app)):
        app.fileStack.append(getCurrentFilePath(app))
        app.files = listFiles(getCurrentFilePath(app))
        app.selectedFileIndex = 0
        app.selectedFile = joinPaths(app)
        isImage(app)
    elif key == 'backspace' and len(app.fileStack) > 1:
        app.fileStack.pop()
        previousDir = app.fileStack[-1]
        app.files = listFiles(previousDir)
        app.selectedFileIndex = 0
        app.selectedFile = joinPaths(app)
        isImage(app)
    elif key == 'tab':
        app.selectedFile = joinPaths(app)
        if app.selectedFileIsImage:
            app.imagePath = app.selectedFile
            target = processImage(app.selectedFile)
            app.code = target.splitlines()
            setGridParams(app) 
            setActiveScreen('main')
        else:
            app.flashImageOpenError = True

def fileTree_onMousePress(app, mouseX, mouseY):
    if (app.backButtonX <= mouseX <= app.backButtonX + app.buttonWidth and 
        app.backButtonY <= mouseY <= app.backButtonY + app.buttonHeight):
        setActiveScreen('main')

def fileTree_redrawAll(app):
    drawFiles(app)
    drawSelectedFileLine(app)
    # draw back button
    drawTextButton(app, 'Go Back', app.backButtonX, app.backButtonY, 
                app.buttonWidth, app.buttonHeight, fill=app.textColor)
    drawLabel(app.selectedFile, 10, 130, size=24, fill=app.textColor, align='left', font='Courier')
    drawLine(0, 150, app.width, 150, fill=app.secondary)
    if app.flashImageOpenError:
        drawImageOpenError(app)

def main(app):
    runAppWithScreens(height=1000, width=1000, initialScreen='main')

#########
# TRACE #
#########

def trace_onScreenActivate(app):
    app.backButtonX = 10
    app.backButtonY = 10
    app.traceHistory = trace(app.grid.codeList)
    app.currentLine = 0

def trace_onKeyPress(app, key):
    pass
def trace_onMousePress(app, mouseX, mouseY):
    if (app.backButtonX <= mouseX <= app.backButtonX + app.buttonWidth and 
        app.backButtonY <= mouseY <= app.backButtonY + app.buttonHeight):
        setActiveScreen('main')

def trace_redrawAll(app):
    # draw a back button
    drawTextButton(app, 'Go Back', app.backButtonX, app.backButtonY, 
                   app.buttonWidth, app.buttonHeight, fill=app.textColor)
    drawGrid(app, grid=app.grid)


if __name__ == '__main__':
    main(app)