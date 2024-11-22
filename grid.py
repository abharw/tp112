import math 
from cmu_graphics import *

# adapted largely from CMU CS academy example 
class Grid:
    
    def __init__(self,rows, cols, boardLeft, boardTop, 
                boardWidth, boardHeight, cellBorderWidth,
                selection, hovered, cellBorderColor, cellColor):
        self.rows = rows
        self.cols = cols
        self.boardLeft = boardLeft
        self.boardTop = boardTop
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        self.cellBorderWidth = cellBorderWidth
        self.selection = selection
        self.hovered = hovered
        self.cellBorderColor = cellBorderColor
        self.cellColor = cellColor

    def getCell(self, x, y):
        dx = x - self.boardLeft
        dy = y - self.boardTop
        cellWidth, cellHeight = self.getCellSize()
        row = math.floor(dy / cellHeight)
        col = math.floor(dx / cellWidth)
        if (0 <= row < self.rows) and (0 <= col < self.cols):
            return (row, col)
        else:
            return None

    def getCellLeftTop(self, row, col):
        cellWidth, cellHeight = self.getCellSize()
        cellLeft = self.boardLeft + col * cellWidth
        cellTop = self.boardTop + row * cellHeight
        return (cellLeft, cellTop)

    def getCellSize(self):
        cellWidth = self.boardWidth / self.cols
        cellHeight = self.boardHeight / self.rows
        return (cellWidth, cellHeight)

def drawGrid(app, grid: Grid):
    for row in range(grid.rows):
        for col in range(grid.cols):
            drawCell(app, grid, row, col)

def drawCell(app, grid: Grid, row, col):
    cellLeft, cellTop = grid.getCellLeftTop(row, col)
    cellWidth, cellHeight = grid.getCellSize()
    if (row, col) == grid.selection:
        color = 'cyan'
    elif (row, col) == grid.hovered:
        color = 'gold'
    else:
        color = grid.cellColor

    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border= grid.cellBorderColor,
             borderWidth=grid.cellBorderWidth)

def onAppStart(app):
    app.boardWidth = 600
    app.boardHeight = 600
    app.grid = Grid(
        rows = 5,
        cols = 5,
        boardLeft = app.width // 2 - app.boardWidth // 2,
        boardWidth = app.boardWidth,
        boardHeight = app.boardHeight,
        boardTop = 100,
        cellBorderWidth = 6,
        selection = None,
        hovered = None,
        cellBorderColor='white',
        cellColor='gray'
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