import os, math
from cmu_graphics import * 

def onAppStart(app):

    app.rows = 5
    app.cols = 5
    app.boardLeft = 50
    app.boardTop = 50
    app.boardWidth = 400
    app.boardHeight = 400
    app.cellBorderWidth = 6
    app.selection = None
    app.hovered = None
    app.cellPadding = 5

def redrawAll(app):
    drawLabel('File Explorer', app.width//2, 25, size=20)
    drawBoard(app, 5, 6, 50, 50, 400, 400, 6, None, None)


def drawBoard(app, rows, cols, boardLeft, boardTop, boardWidth, boardHeight, cellBorderWidth, selection=None, hovered=None, cellPadding=5):
    app.rows = rows
    app.cols = cols
    app.boardLeft = boardLeft 
    app.boardTop = boardTop 
    app.boardWidth = boardWidth 
    app.boardHeight = boardHeight
    app.cellBorderWidth = cellBorderWidth
    app.selection = selection
    app.hovered = hovered

    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col)

def drawCell(app, row, col):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    if (row, col) == app.selection:
        color = 'cyan'
    elif (row, col) == app.hovered:
        color = 'gold'
    else:
        color = 'gray'

    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='white',
             borderWidth=app.cellBorderWidth)

def onMousePress(app, mouseX, mouseY):
    selectedCell = getCell(app, mouseX, mouseY)
    if selectedCell != None:
      if selectedCell == app.selection:
          app.selection = None
      else:
          app.selection = selectedCell
          app.hovered = None

def onMouseMove(app, mouseX, mouseY):
    hoveredCell = getCell(app, mouseX, mouseY)
    app.hovered = hoveredCell  

def getCell(app, x, y):
    dx = x - app.boardLeft
    dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.rows) and (0 <= col < app.cols):
      return (row, col)
    else:
      return None

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

def fileExplorer(path='.'):
    dirsList = []
    filesList = []
    for root, dirs, files, in os.walk(path):
        dirsList.append(dirs)
        filesList.append(files)
    
    print(dirsList[0])
    print(filesList[0])

def main(app):
    runApp(width=500, height=500)

if __name__ == '__main__':
    # main(app)
    fileExplorer()
