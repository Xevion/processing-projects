import random

x, y = random.randint(1,500), random.randint(1,500)
xSpeed, ySpeed = random.randint(1,3), random.randint(1,3)

def reverseX():
    global xSpeed
    xSpeed *= -1

def reverseY():
    global ySpeed
    ySpeed *= -1

def collision():
    global x, y, xSpeed, ySpeed
    if x < 0 or x > width:
        reverseX()
        print("X Collision at ({}, {})".format(x, y))
    if y < 0 or y > height:
        reverseY()
        print("Y Collision at ({}, {})".format(x, y))
    
def tick():
    global x,y, xSpeed, ySpeed
    collision()
    x += xSpeed
    y += ySpeed
    ellipse(x, y, 1, 1)
def setup():
    size(500, 500)
    
def draw():
    tick()
    
