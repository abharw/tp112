# standard imports
import io, sys, os, string
# miscellaneous utility functions, see utils.py
from utils import (
    processImageFile, 
    processPythonFile,
    loadColors, 
    getScaledImageSize, 
    reloadColors,
)
# text editor functionality, see textEditor.py
from textEditor import (
    TextGrid, 
    drawGrid, 
    getCodeListAndDimensions, 
    stringifyCodeList, 
    updateGridColors
)
# trace algorithm, see tracCode.py
from traceCode import trace
from cmu_graphics import *

# standard error message
ERR_MESSAGE = "There's an error somewhere!"
# found this on https://stackoverflow.com/questions/5891453/how-do-i-get-a-list-of-all-the-ascii-characters-using-python
ACCEPTED_CHARACTERS = string.printable

####################
# BASE APPLICATION #
####################

def onAppStart(app):
    # MAIN SCREEN PARAMS
    app.buttonTop, app.buttonLeft = 10, 10
    app.buttonWidth, app.buttonHeight = 180, 80
    app.lineOffset = 36
    app.filePath = None

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

def drawTextButton(app, text, x, y, width, height, fill):
    drawRect(x, y, width, height, fill=app.primary, border=app.secondary)
    drawLabel(text, x + width // 2, y + height // 2, size=18, fill=fill, font='Courier')

################
# START SCREEN # 
################

def start_redrawAll(app):
    drawLabel('Welcome to PyScan Pro', app.width // 2, 
              app.height // 2 - 100, size=60, 
              fill=app.textColor, font='Courier')
    drawLabel('Click anywhere to get started!', app.width // 2, 
              app.height // 2, size=30, 
              fill=app.secondary, font='Courier')
    
def start_onMousePress(app, mouseX, mouseY):
    setActiveScreen('main')

###############
# MAIN SCREEN #
###############

def main_onScreenActivate(app):
    app.fileExplorerButtonX, app.fileExplorerButtonY = 10, 10
    app.runButtonX, app.runButtonY = 250, 10
    app.traceButtonX, app.traceButtonY = 490, 10
    app.colorSchemeSwitcherX, app.colorSchemeSwitcherY = 800, 50
    app.textModeButtonX, app.textModeButtonY = 700, 120

    app.outputBoxX, app.outputBoxY = 400, 500
    app.outputBoxHeight = 500
    
    app.isInsertMode = True

def main_onMouseMove(app, mouseX, mouseY):
    if app.grid is not None:
        hoveredCell = app.grid.getCell(mouseX, mouseY)
        app.grid.hovered = hoveredCell  

def main_onKeyPress(app, key):
    # prevents user from pressing keys if grid is not loaded
    if app.grid is not None:
        if app.grid.selection is not None:
            row, col = app.grid.selection 
            if key == 'backspace':
                if app.isInsertMode:
                    app.grid.codeList[row].pop(col)
                    app.grid.codeList[row].append('')
                else:
                    app.grid.codeList[row][col] = ''
            elif key == 'space':
                app.grid.codeList[row].insert(col, '')
            elif key == 'space':
                app.grid.codeList[row].insert(col, '')
            elif key == 'right' and col < len(app.grid.codeList[0]) - 1:
                app.grid.selection = (row, col + 1)
            elif key == 'left' and col > 0:
                app.grid.selection = (row, col - 1)
            elif key == 'up' and row > 0:
                app.grid.selection = (row - 1, col)
            elif key == 'down' and row < len(app.grid.codeList) - 1:
                app.grid.selection = (row + 1, col)
            else:
                if key in ACCEPTED_CHARACTERS:
                    if app.isInsertMode:
                        app.grid.codeList[row].insert(col, key)
                    else:
                        app.grid.codeList[row][col] = key
            
def main_onMousePress(app, mouseX, mouseY):
    # check if file explorer is clicked
    if (app.fileExplorerButtonX <= mouseX <= app.fileExplorerButtonX + app.buttonWidth and 
        app.fileExplorerButtonY <= mouseY <= app.fileExplorerButtonY + app.buttonHeight):
        setActiveScreen('fileTree')
    
     # check if colorscheme switcher is clicked
    im_width, im_height = getScaledImageSize(app.colorSchemeSwitcherUrl, 7)
    if (app.colorSchemeSwitcherX - im_width // 2 <= mouseX <= app.colorSchemeSwitcherX + im_width // 2 and 
        app.colorSchemeSwitcherY - im_height // 2 <= mouseY <= app.colorSchemeSwitcherY + im_height // 2):
        # reload app colors
        reloadColors(app)
        if app.grid != None:
            # reload grid colors
            updateGridColors(app, grid=app.grid)
    
    # this functionality only makes sense when there is code
    if app.code is not None:
        # check if run button is clicked
        if (app.runButtonX <= mouseX <= app.runButtonX + app.buttonWidth and 
            app.runButtonY <= mouseY <= app.runButtonY + app.buttonHeight):
            getOutput(app)
        # check if trace button is clicked
        elif (app.traceButtonX <= mouseX <= app.traceButtonX + app.buttonWidth and 
            app.traceButtonY <= mouseY <= app.traceButtonY + app.buttonHeight):
            setActiveScreen('trace')
        # check if text mode button is clicked
        elif (app.textModeButtonX <= mouseX <= app.textModeButtonX + app.buttonWidth * 1.5 and 
        app.textModeButtonY <= mouseY <= app.textModeButtonY + app.buttonHeight // 2):
            app.isInsertMode = not app.isInsertMode 
        # grid highlighting logic
        selectedCell = app.grid.getCell(mouseX, mouseY)
        if selectedCell != None:
            if selectedCell == app.grid.selection:
                app.grid.selection = None
            else:
                app.grid.selection = selectedCell
                app.grid.hovered = None

def main_redrawAll(app):
    # file explorer button
    drawTextButton(app, 'File Explorer', app.fileExplorerButtonX, app.fileExplorerButtonY, 
             app.buttonWidth, app.buttonHeight, fill=app.textColor)
    # colorscheme switcher
    drawColorschemeSwitcher(app, app.colorSchemeSwitcherX, app.colorSchemeSwitcherY)
    # display code and run button
    if app.code is not None:
        drawLine(0, 100, app.width, 100, fill=app.secondary)  
        if app.grid is not None:      
            drawGrid(grid=app.grid)
        # run button
        drawTextButton(app, 'Run Code', app.runButtonX, app.runButtonY, 
                app.buttonWidth, app.buttonHeight, fill=app.green)
        # trace button
        drawTextButton(app, 'Trace Code', app.traceButtonX, app.traceButtonY, 
                       app.buttonWidth, app.buttonHeight, fill=app.textColor)
    # draw output box and text edit mode button
    if app.grid is not None:
        drawRect(app.outputBoxX, app.outputBoxY, app.width, app.outputBoxHeight, 
                fill=None, border=app.secondary)
        otherMode = 'Replace' if app.isInsertMode else 'Insert'
        drawTextButton(app, f'Switch to {otherMode} mode', app.textModeButtonX, app.textModeButtonY,
                   app.buttonWidth * 1.5, app.buttonHeight // 2, fill=app.textColor)
    # display output 
    if app.output is not None:
        drawOutput(app, 420, 530)
    # starter message
    if app.grid == None:
        drawLabel(f'Select an image file from the file explorer to get started!', 
                  app.width // 2, app.height // 2, font='Courier', size=25, bold=True, 
                  fill=app.secondary)

def drawOutput(app, x, y):
    for i in range(len(app.output)):
        line = app.output[i]
        drawLabel(line, x, y + app.lineOffset*i, size=30, align='left', font='Courier', fill=app.tertiary)

def drawColorschemeSwitcher(app, x, y):
    # images from https://www.flaticon.com/free-icons/light-mode 
    im_width, im_height = getScaledImageSize(app.colorSchemeSwitcherUrl, 7)

    drawImage(app.colorSchemeSwitcherUrl, x, y, 
            width=im_width, height=im_height, 
            align='center', opacity=40)

def getOutput(app):
    # https://docs.python.org/3/library/functions.html#exec 
    # used chatGPT to figure out how to get the exec output as a string, so basically this entire function
    
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
    # set the board width 
    app.boardWidth = 800 
    # adjust the grid size based on the board width and height
    app.codeList, app.rows, app.cols = getCodeListAndDimensions(app.filePath)

    if app.rows is not None and app.cols is not None:
        app.grid = TextGrid (
            rows=app.rows,
            cols=app.cols,
            boardLeft=35,
            boardWidth=app.boardWidth - 400,
            boardHeight=app.rows * 40 - 100,
            boardTop=150,
            cellBorderWidth=1,
            selection=None,
            hovered=None,
            codeList=app.codeList,
            cellBorderColor=None,
            cellColor=None,
            textColor=app.textColor
        )

####################
# FILE TREE SCREEN #
####################

def fileTree_onScreenActivate(app):
    # file tree parameters
    app.files = listFiles()
    # found this function on https://docs.python.org/3/library/os.html  
    app.fileStack = [os.getcwd()]
    app.previousFiles = app.files
    app.lineOffset = 30
    app.selectedFileIndex = 0
    app.fileTreeLeft = 40
    app.fileTreeTop = 200
    app.characterWidth = 20
    app.characterHeight = 20
    app.selectedFile = getCurrentFilePath(app)
    app.selectedFileIsValid = False
    app.flashFileOpenError = False
    
    # button parameters
    app.helpClicked = False
    app.backButtonX, app.backButtonY = 10, 10
    app.helpButtonX, app.helpButtonY = 250, 10
    app.helpBoxX, app.helpBoxY = 490, 10

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

def drawFileOpenError(app):
    x, y = app.width // 2, app.height // 2 + 300
    drawLabel('The currently selected file is not valid!', x, y, 
              size=30, fill=app.red, font='Courier', bold=True)

def drawHelpBox(app):
    rectWidth = 460
    rectHeight = 100
    textLeft = 500
    textTop = 30
    drawRect(app.helpBoxX, app.helpBoxY,
             rectWidth, rectHeight, fill=app.primary, border=app.textColor, borderWidth=3)
    drawLabel("Use 'up' or 'down' arrow keys to navigate", textLeft, textTop, 
              fill=app.textColor, font='Courier', size=18, align='left')
    drawLabel("Click 'enter' to enter a folder", textLeft, textTop+20,
              fill=app.textColor, font='Courier', size=18, align='left')
    drawLabel("Click 'backspace' to exit a folder", textLeft, textTop+40,
              fill=app.textColor, font='Courier', size=18, align='left')
    drawLabel("Click 'tab' to run the selected file", textLeft, textTop+60,
              fill=app.textColor, font='Courier', size=18, align='left')

def fileIsValid(app):
    fileSuffixes = ('.png', '.jpg', '.py')
    app.selectedFileIsValid = True if app.selectedFile.endswith(fileSuffixes) else False

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

def moveFileSelection(app, index):
    app.selectedFileIndex = index
    app.selectedFile = joinPaths(app)
    fileIsValid(app)

def fileTree_onKeyPress(app, key):
    app.flashFileOpenError = False
    if key == 'up' and app.selectedFileIndex > 0:
        moveFileSelection(app, app.selectedFileIndex -1)
    elif key == 'down' and app.selectedFileIndex < len(app.files) - 1:
        moveFileSelection(app, app.selectedFileIndex +1)
    elif key == 'enter' and os.path.isdir(getCurrentFilePath(app)):
        app.fileStack.append(getCurrentFilePath(app))
        app.files = listFiles(getCurrentFilePath(app))
        moveFileSelection(app, 0)
    elif key == 'backspace' and len(app.fileStack) > 1:
        app.fileStack.pop()
        previousDir = app.fileStack[-1]
        app.files = listFiles(previousDir)
        moveFileSelection(app, 0)
    elif key == 'tab':
        app.selectedFile = joinPaths(app)
        if app.selectedFileIsValid:
            app.filePath = app.selectedFile
            if '.py' in app.filePath:
                target = processPythonFile(app.selectedFile)
            else:
                target = processImageFile(app.selectedFile)
            app.code = target.splitlines()
            setGridParams(app) 
            setActiveScreen('main')
        else:
            app.flashFileOpenError = True

def fileTree_onMousePress(app, mouseX, mouseY):
    # clicking anywhere closes the helpbox
    if app.helpClicked:
        app.helpClicked = not app.helpClicked
    elif (app.backButtonX <= mouseX <= app.backButtonX + app.buttonWidth and 
        app.backButtonY <= mouseY <= app.backButtonY + app.buttonHeight):
        setActiveScreen('main')
    elif (app.helpButtonX <= mouseX <= app.helpButtonX + app.buttonWidth and 
        app.helpButtonY <= mouseY <= app.helpButtonY + app.buttonHeight):
        app.helpClicked = not app.helpClicked

def fileTree_redrawAll(app):
    # draw file tree
    drawFiles(app)
    # draw file indicator
    drawSelectedFileLine(app)
    # draw back button
    drawTextButton(app, 'Go Back', app.backButtonX, app.backButtonY, 
                app.buttonWidth, app.buttonHeight, fill=app.textColor)
    # draw help button
    drawTextButton(app, 'Help', app.helpButtonX, app.helpButtonY,
                   app.buttonWidth, app.buttonHeight, fill=app.textColor)
    # draw user's current path
    drawLabel(app.selectedFile, 10, 130, size=24, fill=app.textColor, align='left', font='Courier')
    drawLine(0, 150, app.width, 150, fill=app.secondary)
    # draw help box if user clicks the button
    if app.helpClicked:
        drawHelpBox(app)
    # draw error if user tries to open invalid file
    if app.flashFileOpenError:
        drawFileOpenError(app)

################
# TRACE SCREEN #
################

def drawCodeSteps(app):
    # storage for codeSteps that go off the screen
    tempStorage = []
    # default message
    if app.codeStepsOnScreen == []:
        drawLabel("Click 'Next Step' to trace the code!", app.codeStepsX, 
                app.codeStepsY, fill=app.secondary, align='left', 
                font='Courier', size=30)
    # draw all steps
    stepListIndex = 0
    stepIndexOnScreen = 0
    while stepListIndex < len(app.codeStepsOnScreen):
        currentStep = app.codeStepsOnScreen[stepListIndex]
        codeStepYValue = app.codeStepsY + (stepIndexOnScreen * app.codeStepsYOffset)

        drawLabel(currentStep, app.codeStepsX, 
            codeStepYValue, fill=app.secondary, align='left', 
            font='Courier', size=30)
        stepIndexOnScreen += 1
        stepListIndex += 1
        # vertical text wrap
        if codeStepYValue > app.height:
            tempStorage = app.codeStepsOnScreen
            stepIndexOnScreen = 0

def trace_onScreenActivate(app):
    app.codeStepsList = trace(stringifyCodeList(app.grid))
    app.codeStepsYOffset = 25
    
    app.codeStepsX = 45
    app.codeStepsY = 520

    app.previousButtonX = 250
    app.previousButtonY = 10

    app.nextButtonX = 490
    app.nextButtonY = 10

    app.currentCodeStepIndex = 0
    app.codeStepsOnScreen = []

def trace_onMousePress(app, mouseX, mouseY):
    # check if back button pressed
    if (app.backButtonX <= mouseX <= app.backButtonX + app.buttonWidth and 
        app.backButtonY <= mouseY <= app.backButtonY + app.buttonHeight):
        setActiveScreen('main') 
    # check if previous step button pressed
    elif (app.previousButtonX <= mouseX <= app.previousButtonX + app.buttonWidth and 
        app.previousButtonY <= mouseY <= app.previousButtonY + app.buttonHeight):
        if len(app.codeStepsOnScreen) > 0:
            app.codeStepsOnScreen.pop()
            # make sure to index is never below 0
            if app.currentCodeStepIndex > 0:
                app.currentCodeStepIndex -= 1
            else:
                app.currentCodeStepIndex = 0
    # check if next step button pressed
    elif (app.nextButtonX <= mouseX <= app.nextButtonX + app.buttonWidth and 
        app.nextButtonY <= mouseY <= app.nextButtonY + app.buttonHeight):
        if app.currentCodeStepIndex < len(app.codeStepsList):
            nextStep = app.codeStepsList[app.currentCodeStepIndex]
            app.codeStepsOnScreen.append(nextStep)
            app.currentCodeStepIndex += 1
    # check if colorscheme switcher is clicked
    im_width, im_height = getScaledImageSize(app.colorSchemeSwitcherUrl, 7)
    if (app.colorSchemeSwitcherX - im_width // 2 <= mouseX <= app.colorSchemeSwitcherX + im_width // 2 and 
        app.colorSchemeSwitcherY - im_height // 2 <= mouseY <= app.colorSchemeSwitcherY + im_height // 2):
        # reload app colors
        reloadColors(app)
        if app.grid != None:
            # reload grid colors
            updateGridColors(app, grid=app.grid)

def trace_redrawAll(app):
    # drawing necessary buttons
    drawTextButton(app, 'Go Back', app.backButtonX, app.backButtonY, 
            app.buttonWidth, app.buttonHeight, fill=app.textColor)
    drawTextButton(app, 'Previous Step', app.previousButtonX, app.previousButtonY, 
            app.buttonWidth, app.buttonHeight, fill=app.textColor)
    drawTextButton(app, 'Next Step', app.nextButtonX, app.nextButtonY, 
            app.buttonWidth, app.buttonHeight, fill=app.textColor)
    # reuse the grid for display purposes
    drawGrid(grid=app.grid)
    # lines for UI
    drawLine(0, 100, app.width, 100, fill=app.secondary)
    drawLine(0, app.height // 2, app.width, app.height // 2, fill=app.secondary)
    # core UI for code tracing
    drawCodeSteps(app)
    # colorscheme switcher
    drawColorschemeSwitcher(app, app.colorSchemeSwitcherX, app.colorSchemeSwitcherY)

def main(app):
    runAppWithScreens(height=1000, width=1000, initialScreen='start')

if __name__ == '__main__': 
    main(app)
