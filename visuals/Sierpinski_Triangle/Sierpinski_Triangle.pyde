import time

class Point:
    def __init__(self, x, y, sdraw=False):
        self.x, self.y = x, y
    
    def s(self):
        ellipse(self.x, self.y, 5, 5)
    
    def mid(self, other):
        return Point((self.x + other.x) / 2, (self.y + other.y) / 2)

def siepinski(i, a, b, c):
    if i <= 0:
        return
    else:
        triangle(a.x, a.y, b.x, b.y, c.x, c.y)
        x = a.mid(b)
        y = b.mid(c)
        z = c.mid(a)
        siepinski(i - 1, a, x, z)
        siepinski(i - 1, x, b, y)
        siepinski(i - 1, z, y, c)
        # siepinski(i - 1, x, y, z)

def setup():
    size(1000, 1000)
    noLoop()

def equilateral(center, side):
    
    altitude = side * (sqrt(3) / 2.0)
    AM = (2.0/3.0) * altitude
    BF = (1.0 / 2.0) * side
    FM = (1.0 / 3.0) * altitude
    
    a = Point(center.x, center.y + AM)
    b = Point(center.x - BF, center.y - FM)
    c = Point(center.x + BF, center.y - FM)
            
    return a, b, c

i = 1
def draw():
    
    global i
    a, b, c = equilateral(Point(0, 0), 750)
    translate(width/2, height/2)
    siepinski(i, a, b, c)
    
    time.sleep(1)
    i += 1

def mouseClicked():
    loop()
