import random

def setup():
    size(750, 750)
    frameRate(99999999)
    colorMode(HSB, 100)
    noLoop()
top = 0
def draw():
    global top
    top += 0.3 + (top / 10000)
    translate(width/2, height/2)
    # background(100)
    strokeWeight(0.1)
    # for rot in range(1, top):
    rot = top
    rot = rot/10.0
    fill((rot / 10) % 100, 100, 100)
    pushMatrix()
    rotate(degrees(rot))
    translate(rot / 10.0, 0)
    translate(rot, rot)
    rect(0, 0, 50, 50)
    popMatrix()

def mouseClicked():
    loop()
