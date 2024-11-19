import math 

class Grid:
    def __init__(self,rows, cols, boardLeft, boardTop, 
                boardWidth, boardHeight, cellBorderWidth,
                selection, hovered, cellPadding):
        self.rows = rows
        self.cols = cols
        self.boardLeft = boardLeft
        self.boardTop = boardTop
        self.boardWidth = boardWidth
        self.boardHeight = boardHeight
        self.cellBorderWidth = cellBorderWidth
        self.selection = selection
        self.hovered = hovered
        self.cellPadding = cellPadding

    """
    probably need to move onMouse stuff out
    """
    # def onMousePress(self, mouseX, mouseY):
    #     selectedCell = self.getCell(self, mouseX, mouseY)
    #     if selectedCell != None:
    #         if selectedCell == self.selection:
    #             self.selection = None
    #         else:
    #             self.selection = selectedCell
    #             self.hovered = None

    # def onMouseMove(self, mouseX, mouseY):
    #     hoveredCell = self.getCell(self, mouseX, mouseY)
    #     self.hovered = hoveredCell  

    def getCell(self, x, y):
        dx = x - self.boardLeft
        dy = y - self.boardTop
        cellWidth, cellHeight = self.getCellSize(self)
        row = math.floor(dy / cellHeight)
        col = math.floor(dx / cellWidth)
        if (0 <= row < self.rows) and (0 <= col < self.cols):
            return (row, col)
        else:
            return None

    def getCellLeftTop(self, row, col):
        cellWidth, cellHeight = self.getCellSize(self)
        cellLeft = self.boardLeft + col * cellWidth
        cellTop = self.boardTop + row * cellHeight
        return (cellLeft, cellTop)

    def getCellSize(self):
        cellWidth = self.boardWidth / self.cols
        cellHeight = self.boardHeight / self.rows
        return (cellWidth, cellHeight)
