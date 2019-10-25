import random

def setup():
    size(1440, 1440)
    frameRate(99999999)
    colorMode(HSB, 100)
top = 0
def draw():
    global top
    top += 1
    translate(width/2, height/2)
    # background(100)
    strokeWeight(0.1)
    # for rot in range(1, top):
    rot = top
    rot = rot/10.0
    fill((rot / 9.0) % 100, 100, 100)
    pushMatrix()
    rotate(degrees(rot))
    translate(rot / 10.0, 0)
    translate(rot, rot)
    rect(0, 0, 50, 50)
    popMatrix()
    # noLoop()
