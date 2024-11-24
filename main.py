import io
import sys
from cmu_graphics import *
from utils import processImage
from textEditor import TextGrid, drawGrid, getCodeListAndDimensions, stringifyCodeList

ERR_MESSAGE = "There's an error somewhere!"

def onAppStart(app):
    app.lightGray = rgb(240, 240, 240)
    app.buttonTop, app.buttonLeft = 10, 10
    app.buttonWidth, app.buttonHeight = 180, 80
    app.lineOffset = 36
    app.imagePath = './images/test1.png'
    app.code = None
    app.output = None
    app.grid = None

def redrawAll(app):
    drawRect(0, 0, app.width, 100, fill=app.lightGray)
    # File Explorer Button
    drawRect(10, 10, app.buttonWidth, app.buttonHeight, fill='white', border='darkGray')
    drawLabel('File Explorer', 10 + app.buttonWidth/ 2, 10 + app.buttonHeight/2, size=18)

    # Editor Button
    drawRect(400, 500, app.width, 500, fill=None, border='darkGray')

    # Display Code and run button
    if app.code is not None:
        drawLine(30, 100, 30, app.height, fill='darkGray')
        drawLineNumbers(app, 15, 120)
        drawGrid(app, grid=app.grid)

        # Run button
        drawRect(250, 10, app.buttonWidth, app.buttonHeight, fill='white', border='darkGray')
        drawLabel('Run Code', 250 + app.buttonWidth/ 2, 10 + app.buttonHeight/2, size=18, fill='green')
        # print(stringifyCodeList(app.grid))

    # Display Output 
    if app.output is not None :
        drawOutput(app, 420, 530)

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
        print(ERR_MESSAGE)
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

def onMouseMove(app, mouseX, mouseY):
    if app.grid is not None:
        hoveredCell = app.grid.getCell(mouseX, mouseY)
        app.grid.hovered = hoveredCell  

def onKeyPress(app, key):
    if app.grid.selection is not None:
        row, col = app.grid.selection 
        if key == 'backspace':
            app.grid.codeList[row][col] = ''
        else:
            if key not in ['enter', 'escape', 'tab']:
                app.grid.codeList[row][col] = key
               
def onMousePress(app, mouseX, mouseY):

    if 10 <= mouseX <= 190 and 10 <= mouseY <= 90:
        target = processImage(app.imagePath)
        app.code = target.splitlines()
        setGridParams(app) 
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

def main(app):
    runApp(height=1000, width=1000)

if __name__ == '__main__':
    main(app)
