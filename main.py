from cmu_graphics import *
from utils import processImage

def onAppStart(app):
    app.sidebarColor = rgb(240, 240, 240)
    app.buttonTop, app.buttonLeft = 10, 10
    app.buttonWidth, app.buttonHeight = 180, 100
    app.imagePath = './test2.jpg'
    app.code = None
    
def redrawAll(app):
    drawRect(0, 0, 200, app.height, fill=app.sidebarColor)
    drawRect(10, 10, app.buttonWidth, app.buttonHeight, fill='white', border='darkGray')
    drawLabel('File Explorer', 10 + app.buttonWidth/ 2, 10 + app.buttonHeight/2, size=18)
    if app.code is not None:
        drawCode(app, 250, 20, app.code)
    drawRect(600, 500, 400, 500, fill=None, border='darkGray')
   
def drawCode(app, x, y, code):
    for i in range(len(code)):
        line = code[i]
        offset = 15 
        drawLabel(line, x, y + offset*i, size=18, align='left')

def onKeyPress(app, key):
    if key == 'enter':
        target = processImage(app.imagePath)
        app.code = target.splitlines()


def main(app):
    runApp(height=1000, width=1000)

if __name__ == '__main__':
    main(app)
