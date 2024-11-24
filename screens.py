from cmu_graphics import * 

def onAppStart(app):
    app.sidebarColor = rgb(240, 240, 240)
    app.buttonTop, app.buttonLeft = 10, 10
    app.buttonWidth, app.buttonHeight = 180, 100
    app.imagePath = './images/test1.png'
    app.code = None
    app.fileExplorerSelected = False 
    app.codeEditorSelected = False 


def codeEditor_redrawAll(app):


### Bac