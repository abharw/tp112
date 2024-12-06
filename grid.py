import math 
from cmu_graphics import *

# adapted largely from CMU CS academy example 
# main difference is distinction between hovering and selecting
class Grid:
    def __init__(self,rows, cols, gridLeft, gridTop, 
                gridWidth, gridHeight, cellBorderWidth,
                selection, hovered, cellBorderColor, cellColor):
        self.rows = rows
        self.cols = cols
        self.gridLeft = gridLeft
        self.gridTop = gridTop
        self.gridWidth = gridWidth
        self.gridHeight = gridHeight
        self.cellBorderWidth = cellBorderWidth
        self.selection = selection
        self.hovered = hovered
        self.cellBorderColor = cellBorderColor
        self.cellColor = cellColor

    def getCell(self, x, y):
        dx = x - self.gridLeft
        dy = y - self.gridTop
        cellWidth, cellHeight = self.getCellSize()
        row = math.floor(dy / cellHeight)
        col = math.floor(dx / cellWidth)
        if (0 <= row < self.rows) and (0 <= col < self.cols):
            return (row, col)
        else:
            return None

    def getCellLeftTop(self, row, col):
        cellWidth, cellHeight = self.getCellSize()
        cellLeft = self.gridLeft + col * cellWidth
        cellTop = self.gridTop + row * cellHeight
        return (cellLeft, cellTop)

    def getCellSize(self):
        cellWidth = self.gridWidth / self.cols
        cellHeight = self.gridHeight / self.rows
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
