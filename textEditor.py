from cmu_graphics import * 
from grid import Grid  
from utils import processImage, listifyCode

class TextGrid(Grid):
    def __init__(self, rows, cols, boardLeft, boardTop, 
                 boardWidth, boardHeight, cellBorderWidth,
                 selection, hovered, codeList, cellBorderColor, cellColor):
        
        super().__init__(rows, cols, boardLeft, boardTop, 
                         boardWidth, boardHeight, cellBorderWidth,
                         selection, hovered, cellBorderColor, cellColor)

        self.codeList = codeList


def drawGrid(app, grid: TextGrid):
    for row in range(grid.rows):
        for col in range(grid.cols):
            drawCell(app, grid, row, col)

def drawCell(app, grid: TextGrid, row, col):
    cellLeft, cellTop = grid.getCellLeftTop(row, col)
    cellWidth, cellHeight = grid.getCellSize()
    if (row, col) == grid.selection:
        color = 'cyan'
    elif (row, col) == grid.hovered:
        color = 'gold'
    else:
        color = grid.cellColor


    print(f'Grid: {row},{col}: {grid.codeList[row][col]}')
    
    character = grid.codeList[row][col]
    centerX = grid.boardLeft + (cellWidth * col) + cellWidth // 2
    centerY = grid.boardTop + (cellHeight * row) + cellHeight // 2
    drawLabel(character, centerX, centerY)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border=grid.cellBorderColor,
             borderWidth=grid.cellBorderWidth)

def getCodeListDimensions(imagePath):
    target = processImage(imagePath)
    L = listifyCode(target)
    rows = len(L)
    cols = len(L[0])
    return (L, rows, cols)

def onAppStart(app):
    app.boardWidth = 650
    app.boardHeight = 200
    app.imagePath = './images/test1.png'
    app.codeList, app.rows, app.cols = getCodeListDimensions(app.imagePath)
    app.grid = TextGrid(
        rows = app.rows,
        cols = app.cols,
        boardLeft = app.width // 2 - app.boardWidth // 2,
        boardWidth = app.boardWidth,
        boardHeight = app.boardHeight,
        boardTop = 100,
        cellBorderWidth = 1,
        selection = None,
        hovered = None,
        codeList=app.codeList,
        cellBorderColor='black',
        cellColor=None
    )
def onMousePress(app, mouseX, mouseY):
    selectedCell = app.grid.getCell(mouseX, mouseY)
    if selectedCell != None:
        if selectedCell == app.grid.selection:
            app.grid.selection = None
        else:
            app.grid.selection = selectedCell
            app.grid.hovered = None

def onMouseMove(app, mouseX, mouseY):
    hoveredCell = app.grid.getCell(mouseX, mouseY)
    app.grid.hovered = hoveredCell  
    
def redrawAll(app):
    drawGrid(app, grid=app.grid)

def main(app):
    runApp(width=800, height=800)

if __name__ == '__main__':
    main(app)
