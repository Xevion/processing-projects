import random, time

def setup():
    size(1000, 1000)
    frameRate(60*1)
    noLoop()
    global Mover
    fromx, fromy = 0, height/2
    tox, toy = width, height
    Mover = MovingPoint(fromx, fromy, tox, toy)
    ellipse(fromx, fromy, 10, 10)
    ellipse(tox, toy, 10, 10)

class MovingPoint():
    def __init__(self, x, y, newx=None, newy=None):
        self.x, self.y = x, y
        self.duration = 100
        if newx == None or newy == None:
            if not newx == None and newy == None:
                print("newx and newy not set properly ({})".format((newx, newy)))
            self.running = False
        else:
            self.start(newx, newy)
    
    # Function that begins the movement of the point
    def start(self, newx, newy):
        self.frame = 0
        self.oldx, self.oldy = self.x, self.y
        self.newx, self.newy = newx, newy
        self.running = True
    
    # Function that ends the movement of the point
    def end(self):
        self.frame = self.duration
        self.oldx, self.oldy, self.newx, self.newy = 0, 0, 0, 0
        self.running = False
    
    def tick(self):
        if self.running:
            self.frame += 1
            self.x = self.easeInQuart(self.frame, self.oldx, self.newx-self.oldx, self.duration)
            self.y = self.easeInQuart(self.frame, self.oldy, self.newy-self.oldy, self.duration)
            if self.frame >= self.duration:
                print("finished")
                self.end()
        ellipse(self.x, self.y, 1, 1)
    
    def isRunning(self):
        return self.running
    
    # t=Current Time b=Start Value c=Change in Value d=Duration
    def easeInQuart(self, t, b, c, d):
            t, d = float(t), float(d)
            t = t / d
            return c * t * t * t * t + b

def reset():
    old = g.fillColor
    fill(204, 204, 204)
    rect(0, 0, width, height)
    fill(old)

def draw():
    global Mover
    if Mover.isRunning():
        Mover.tick()
    else:
        x, y = random.randint(0, width), random.randint(0, height)
        print("Going to {}".format((x,y)))
        Mover.start(x, y)

def mouseClicked():
    loop()
    
