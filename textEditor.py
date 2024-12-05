from utils import processImageFile, processPythonFile, listifyCode
from cmu_graphics import * 
from grid import Grid  

# inherits from the Grid superclass, but adds text rendering
class TextGrid(Grid):
    def __init__(self, rows, cols, boardLeft, boardTop, 
                 boardWidth, boardHeight, cellBorderWidth,
                 selection, hovered, codeList, cellBorderColor, cellColor,textColor):
        
        super().__init__(rows, cols, boardLeft, boardTop, 
                         boardWidth, boardHeight, cellBorderWidth,
                         selection, hovered, cellBorderColor, cellColor)

        self.codeList = codeList
        self.textColor = textColor

def drawGrid(grid: TextGrid):
    for row in range(grid.rows):
        for col in range(grid.cols):
            drawCell(grid, row, col)

def getCellSize(grid):
    cellWidth = grid.boardWidth / grid.cols
    cellHeight = grid.boardHeight / grid.rows
    return (cellWidth, cellHeight)

def drawCell(grid: TextGrid, row, col):
    cellLeft, cellTop = grid.getCellLeftTop(row, col)
    cellWidth, cellHeight = getCellSize(grid)
    if (row, col) == grid.selection:
        color = 'cyan'
    elif (row, col) == grid.hovered:
        color = 'gold'
    else:
        color = grid.cellColor

    character = grid.codeList[row][col]
    posX = grid.boardLeft + (cellWidth * col) + cellWidth // 2
    # align characters better vertically in the grid
    posY = grid.boardTop + (cellHeight * row) + cellHeight - 6
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border=grid.cellBorderColor,
             borderWidth=grid.cellBorderWidth)
    
    # period characters need to be aligned differently
    align = 'center' if character == '.' else 'bottom'

    drawLabel(character, posX, posY, font='Courier', align=align, size=30, fill=grid.textColor)

def getCodeListAndDimensions(filePath):
    if '.py' in filePath:
        target = processPythonFile(filePath)
    else:
        target = processImageFile(filePath)
    grid = listifyCode(target)
    rows = len(grid)
    cols = len(grid[0])
    return (grid, rows, cols)

def updateGridColors(app, grid: TextGrid):
    grid.textColor = app.textColor

def stringifyCodeList(grid: TextGrid):
    s = ''
    for line in grid.codeList:
        s += (''.join(line) + '\n')
    return s