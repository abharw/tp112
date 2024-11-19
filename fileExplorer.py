from cmu_graphics import * 
from utils import listifyCode, processImage
from grid import Grid, drawBoard

def onAppStart(app):
    app.grid = Grid(
        rows = 5,
        cols = 5,
        boardLeft = 50,
        boardTop = 50,
        boardWidth = 400,
        boardHeight = 400,
        cellBorderWidth = 6,
        selection = None,
        hovered = None,
        cellPadding = 5,
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
    drawBoard(app, grid=app.grid)

def main(app):
    runApp(width=500, height=500)

if __name__ == '__main__':
    main(app)