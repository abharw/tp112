import io
import sys
from cmu_graphics import *
from utils import processImage
from textEditor import TextGrid, drawGrid, getCodeListDimensions

"""Do screen functionality"""
"""Properly align period characters"""

def onAppStart(app):
    app.lightGray = rgb(240, 240, 240)
    app.buttonTop, app.buttonLeft = 10, 10
    app.buttonWidth, app.buttonHeight = 180, 80
    app.lineOffset = 25
    app.imagePath = './images/test1.png'
    app.code = None
    app.output = None
    
###################   
### MAIN SCREEN ###
###################

def main_redrawAll(app):
    drawRect(0, 0, app.width, 100, fill=app.lightGray)
    # File Explorer Button
    drawRect(10, 10, app.buttonWidth, app.buttonHeight, fill='white', border='darkGray')
    drawLabel('File Explorer', 10 + app.buttonWidth/ 2, 10 + app.buttonHeight/2, size=18)

    # Editor Button
    drawRect(250, 10, app.buttonWidth, app.buttonHeight, fill='white', border='darkGray')
    drawLabel('Code Editor', 250 + app.buttonWidth/ 2, 10 + app.buttonHeight/2, size=18)

    drawRect(400, 500, app.width, 500, fill=None, border='darkGray')

    # Display Code and run button
    if app.code is not None:
        drawLine(30, 100, 30, app.height, fill='darkGray')
        drawCode(app, 50, 120)
        drawLineNumbers(app, 15, 120)

        # Run button
        drawRect(490, 10, app.buttonWidth, app.buttonHeight, fill='white', border='darkGray')
        drawLabel('Run Code', 490 + app.buttonWidth/ 2, 10 + app.buttonHeight/2, size=18, fill='green')
    
    # Display Output 
    if app.output is not None :
        drawOutput(app, 420, 530)
 
def main_onMousePress(app, mouseX, mouseY):
    if 10 <= mouseX <= 190 and 10 <= mouseY <= 90:
        target = processImage(app.imagePath)
        app.code = target.splitlines()
    if app.code is not None:
        if 250 <= mouseX <= 430 and 10 <= mouseY <= 90:
            setActiveScreen('editor')
        if 490 <= mouseX <= 670 and 10 <= mouseY <= 90:
            getOutput(app)

def drawLineNumbers(app, x, y):
    lineNumbers = list(range(len(app.code)))
    lineNumbers = [num + 1 for num in lineNumbers]
    for i in range(len(lineNumbers)):
        lineNumber = lineNumbers[i]
        drawLabel(lineNumber, x, y + app.lineOffset*i, size=20, align='center', font='Roboto Mono')

def drawCode(app, x, y):
    for i in range(len(app.code)):
        line = app.code[i]
        drawLabel(line, x, y + app.lineOffset*i, size=30, align='left', font='Roboto Mono')

def drawOutput(app, x, y):
    for i in range(len(app.output)):
        line = app.output[i]
        drawLabel(line, x, y + app.lineOffset*i, size=30, align='left', font='Roboto Mono', fill='gray')

def getOutput(app):
    # https://docs.python.org/3/library/functions.html#exec 
    # used chatGPT to figure out how to get the exec output as a string

    # define a string buffer to capture output
    outputBuffer = io.StringIO()
    # redirect stdout to the buffer
    sys.stdout = outputBuffer
    # execute the code
    exec('\n'.join(app.code))
    # reset stdout to default
    sys.stdout = sys.__stdout__
    # retrieve the captured output
    capturedOutput = outputBuffer.getvalue()
    app.output = capturedOutput.splitlines()

############################
#### CODE EDITOR SCREEN ####
############################


def editor_onScreenActivate(app):
    app.boardWidth = 650
    app.boardHeight = 200
    app.codeList, app.rows, app.cols = getCodeListDimensions(app.imagePath)
    app.grid = TextGrid(
        rows = app.rows,
        cols = app.cols,
        boardLeft = app.width // 2 - app.boardWidth // 2,
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

def editor_onMousePress(app, mouseX, mouseY):
    selectedCell = app.grid.getCell(mouseX, mouseY)
    if selectedCell != None:
        if selectedCell == app.grid.selection:
            app.grid.selection = None
        else:
            app.grid.selection = selectedCell
            app.grid.hovered = None

def editor_onMouseMove(app, mouseX, mouseY):
    hoveredCell = app.grid.getCell(mouseX, mouseY)
    app.grid.hovered = hoveredCell  


def editor_onKeyPress(app, key):
    if app.grid.selection is not None:
        row, col = app.grid.selection 
        if key == 'backspace':
            app.codeList[row][col] = ''
        else:
            if key not in ['enter', 'escape', 'tab']:
                app.codeList[row][col] = key

def editor_redrawAll(app):
    drawGrid(app, grid=app.grid)

def main(app):
    runAppWithScreens(height=1000, width=1000, initialScreen='main')

if __name__ == '__main__':
    main(app)
