def setup():
    size(500, 500)

def drawLine(i):
    stroke(0)
    fill(0)
    translate(width/2, height/2)
    rotate(radians(i))
    line(0, 0, 240, 0)
    textSize(15)
    text(i, 240, 0)
    resetMatrix()
    
i = 0
def draw():
    background(204)
    global i
    i += 1
    i = i % 360
    if i % 90 == 0:
        fill(255, 0, 0)
    else:
        fill(0)
    textAlign(CENTER, CENTER)
    textSize(40)
    text(str(i), 500-40, 500-20)
    drawLine(i)
    for x in range(0, 360, 15):
        drawLine(x)
