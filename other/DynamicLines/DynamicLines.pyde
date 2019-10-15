import random, string

def setup():
    size(1000, 1000)
    frameRate(10000)
    
curDraw = False
oldLines = []
curStroke = 1

# Get the current line
def getCurLine():
    global startCurX, startCurY, curStroke
    pg = createGraphics(width, height)
    pg.beginDraw()
    pg.fill(255, 0, 0)
    pg.strokeWeight(curStroke)
    pg.line(startCurX, startCurY, mouseX, mouseY)
    pg.endDraw()
    return pg

# Start a new 'current line' and stop drawing the 'old lines'
def mousePressed():
    if mouseButton == LEFT:
        global curDraw, startCurX, startCurY
        curDraw = True
        startCurX, startCurY = mouseX, mouseY
    elif mouseButton == RIGHT:
        global curStroke
        if keyPressed:
            if keyCode == SHIFT:
                curStroke -= 1
        else:
            curStroke += 1
        # if curStroke < 0:
        #     curStroke = 0
        print(curStroke)

def keyPressed():
    print("keyPressed({})".format(key))
    if keyCode == BACKSPACE:
        global oldLines
        oldLines = []
        draw()
        print("BACKSPACE pressed")

def mouseReleased():
    if mouseButton == LEFT:
        global curDraw, endCurX, endCurY, startCurX, startCurY, oldLines, curStroke
        curDraw = False
        endCurX, endCurY = mouseX, mouseY
        compile = (startCurX, startCurY, endCurX, endCurY, curStroke)
        oldLines.append(compile)
    
# Get all old lines into a PGraphics Object
def getOldLines():
    global oldLines
    pg = createGraphics(width, height)
    pg.beginDraw()
    for x1,y1,x2,y2,stroke in oldLines:
        pg.strokeWeight(stroke)
        pg.line(x1, y1, x2, y2)
    pg.endDraw()
    return pg

def draw():
    global curDraw
    background(204)
    image(getOldLines(), 0, 0)
    if curDraw:
        image(getCurLine(), 0, 0)
