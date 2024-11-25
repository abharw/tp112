from cmu_graphics import * 
import os 

def onAppStart(app):

    app.files = listFiles()
    # https://docs.python.org/3/library/os.html  
    app.fileStack = [os.getcwd()]
    app.previousFiles = app.files
    app.lineOffset = 30
    app.selectedFileIndex = 0
    app.fileTreeLeft = 40
    app.fileTreeTop = app.height // 2 - (len(app.files) * app.lineOffset)
    app.characterWidth = 20
    app.characterHeight = 20
    app.selectedFile = getCurrentFilePath(app)


def drawFiles(app):
    for i in range(len(app.files)):
        file = app.files[i]
        isBold = True if os.path.isdir(file) else False
        drawLabel(file, app.fileTreeLeft, app.fileTreeTop + app.lineOffset*i, align='left', font='Courier', size=30, fill='gray', bold=isBold)

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

def drawSelectedFileLine(app):
    drawLine(
        app.fileTreeLeft, 
        app.fileTreeTop + app.lineOffset * app.selectedFileIndex + app.characterHeight,
        app.fileTreeLeft + len(app.files[app.selectedFileIndex]) * app.characterWidth, 
        app.fileTreeTop + app.lineOffset * app.selectedFileIndex + app.characterHeight,
        lineWidth = 3
    )

def onKeyPress(app, key):
    if key == 'up' and app.selectedFileIndex > 0:
        app.selectedFileIndex -= 1
    elif key == 'down' and app.selectedFileIndex < len(app.files) - 1:
        app.selectedFileIndex += 1
    elif key == 'enter' and os.path.isdir(getCurrentFilePath(app)):
        app.fileStack.append(getCurrentFilePath(app))
        app.files = listFiles(getCurrentFilePath(app))
        app.selectedFileIndex = 0
    elif key == 'backspace' and len(app.fileStack) > 1:
        app.fileStack.pop()
        previousDir = app.fileStack[-1]
        app.files = listFiles(previousDir)
        app.selectedFileIndex = 0

def redrawAll(app):
    drawFiles(app)
    drawSelectedFileLine(app)

def main(app):
    runApp(width=1000, height=1000)

if __name__ == '__main__':
    # print(listFiles(app))
    main(app)