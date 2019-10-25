class Triangle:
    def __init__(self, a, b, c, orient):
        self.a, self.b, self.c, self.orient = a, b, c, orient
    
    def render(self, points=False):
        rotate(radians(self.orient))
        triangle(self.a.x, self.a.y, self.b.x, self.b.y, self.c.x, self.c.y)
        if points:
            self.a.render()
            self.b.render()
            self.c.render()
            
class Point:
    def __init__(self, x, y, diameter=5):
        self.x, self.y, self.diamter = x, y, diameter
        
    def render(self):
        ellipse(self.x, self.y, self.diameter, self.diameter)

def setup():
    size(500, 500)
    
    global triangleArray
    triangleArray = []
    
def equilateral(center, side):
    altitude = side * (sqrt(3) / 2.0)
    AM = (2.0 / 3.0) * altitude
    BF = (1.0 / 2.0) * side
    FM = (1.0 / 3.0) * altitude
    a = Point(center.x, center.y + AM)
    b = Point(center.x - BF, center.y - FM)
    c = Point(center.x + BF, center.y - FM)
    return a, b, c

x = 0
def draw():
    global x, triangleArray
    for _ in range(1):
        x += 1
        i = sin(x / 100.0) * 400
        if i >= 400:
            i = 0
            
        a, b, c = equilateral(Point(0, 0), i)
        triangleArray.insert(0, Triangle(a, b, c, i))
        triangleArray = triangleArray[:30]
        
        background(204)
        for e,tri in enumerate(triangleArray):
            # if e == len(triangleArray) - 1:
            #     fill(204)
            #     noStroke()
            # else:
            #     stroke(0)
            #     fill(255)
            resetMatrix()
            translate(width / 2.0, height / 2.0)
            tri.render()
        
def mouseClicked():
    loop()
