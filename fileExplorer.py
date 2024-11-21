from cmu_graphics import * 
from grid import Grid, drawGrid
import os

def listFiles(path):
    files = os.listdir(path)
    print(files)

##########
#GRAPHICS#
##########

class FileExplorerGrid(Grid):

    def __init__(self,rows, cols, boardLeft, boardTop, 
                boardWidth, boardHeight, cellBorderWidth,
                selection, hovered, cellPadding, filesList):
        super().__init__(rows, cols, boardLeft, boardTop, 
                    boardWidth, boardHeight, cellBorderWidth,
                    selection, hovered, cellPadding)
        self.filesList = filesList


    def reshapeOneDimensionalList(L, rows, cols):
        # Reshape a 1d list to a 2d list with the given number of dimensions
        # Dimensions = 3x3
        # [1, 2, 3, 4, 5, 6] --> [[1, 2, 3], [4, 5, 6], [None, None, None]]
        newL = [[None]*cols for _ in range(rows)]

        for i in range(rows):
            for j in range(cols):
                pass

        
    def drawCell(app, grid, row, col, filesList):

        cellLeft, cellTop = grid.getCellLeftTop(row, col)
        cellWidth, cellHeight = grid.getCellSize()
        if (row, col) == grid.selection:
            color = 'cyan'
        elif (row, col) == grid.hovered:
            color = 'gold'
        else:
            color = 'gray'

def onAppStart(app):
    app.boardWidth = 600
    app.boardHeight = 600
    app.grid = FileExplorerGrid(
        rows = 5,
        cols = 5,
        boardLeft = app.width // 2 - app.boardWidth // 2,
        boardWidth = app.boardWidth,
        boardHeight = app.boardHeight,
        boardTop = 100,
        cellBorderWidth = 6,
        selection = None,
        hovered = None,
        cellPadding = 5,
    )
    app.selectedFilePath = 'foo'

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
    drawLabel(f'Current Path: {app.selectedFilePath}', app.width // 2, 750, size=18)

def main(app):
    runApp(width=800, height=800)

if __name__ == '__main__':
    # main(app)
    listFiles('.')