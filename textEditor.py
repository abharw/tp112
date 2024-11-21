from cmu_graphics import * 
from grid import Grid, drawGrid
from utils import processImage, listifyCode

def getCodeList(imagePath):
    target = processImage(imagePath)
    L = listifyCode(target)
    return L

def onAppStart(app):
    app.imagePath = './images/test1.png'
    app.code = getCodeList(app.imagePath)
    app.codeLeft = 50
    app.codeTop = 50
    app.codeLineOffset = 30
    app.codeTextSize = 30

def drawCode(app, code):
    
    rows = len(code)
    cols = len(code[0])

    
    for i in range(rows):
        y = rounded(app.codeTop + i * app.codeLineOffset)
        for j in range(cols):
            x = rounded(app.codeLeft + j * 10)
            char = code[i][j]

            drawLabel(char, x, y, font='monospace')


def drawCursor(app):
    pass

def onKeyPress(app):
    pass

def redrawAll(app):
    drawCode(app, app.code)
    drawCursor(app)

def main(app):
    runApp(width=500, height=500)

if __name__ == '__main__':
    main(app)