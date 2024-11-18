import os
from cmu_graphics import * 

def onAppStart(app):
    pass

def redrawAll(app):
    pass

def main(app):
    runApp()

def fileExplorer(path='.'):
    if os.path.isfile(path):
        if '.png' in path:
            print(path)
    else:
        for filename in os.listdir(path):
            fileExplorer(path + '/' + filename)


if __name__ == '__main__':
    main()