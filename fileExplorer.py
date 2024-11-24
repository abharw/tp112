from cmu_graphics import * 
from grid import Grid, drawGrid
import os

class FileExplorerGrid(Grid):

    def __init__(self,rows, cols, boardLeft, boardTop, 
                boardWidth, boardHeight, cellBorderWidth,
                selection, hovered, cellPadding, rootPath, cellBorderColor):
        super().__init__(rows, cols, boardLeft, boardTop, 
                    boardWidth, boardHeight, cellBorderWidth,
                    selection, hovered, cellPadding)
        
        self.rootPath = rootPath

    @staticmethod
    def listFiles(path):
        files = os.listdir(path)
        print(files)

    @staticmethod
    def reshapeOneDimensionalList(L, rows, cols):
        # Reshape a 1d list to a 2d list with the given number of dimensions
        # Dimensions = 3x3
        # [1, 2, 3, 4, 5, 6] --> [[1, 2, 3], [4, 5, 6], [None, None, None]]
        newL = [[None]*cols for _ in range(rows)]
        i = j = k = 0
        while i < rows:
            if k == len(L): break
            newL[i][j] = L[k]
            j += 1
            if j >= cols:
                i += 1
                j = 0
            k += 1
        return newL
    
    def drawGrid(self, app, grid: Grid):
        filesList = FileExplorerGrid.listFiles(self.rootPath)
        reshapedFilesList = FileExplorerGrid.reshapeOneDimensionalList(filesList, self.rows, self.cols)
        for row in range(grid.rows):
            for col in range(grid.cols):
                self.drawCell(self, app, grid, row, col, reshapedFilesList)

    def drawCell(self, app, grid, row, col, reshapedFilesList):
        cellLeft, cellTop = grid.getCellLeftTop(row, col)
        cellWidth, cellHeight = grid.getCellSize()
        # if (row, col) == grid.selection:
        #     color = 'cyan'
        # elif (row, col) == grid.hovered:
        #     color = 'gold'
        # else:
        #     color = 'gray'
        """
        draw the label instead of the color 
        """

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
        cellBorderColor= 'white',
        rootPath = '.'
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
    drawLabel(f'Current Path: {app.selectedFilePath}', app.width // 2, 750, size=18)

def main(app):
    runApp(width=800, height=800)

if __name__ == '__main__':
    main(app)

