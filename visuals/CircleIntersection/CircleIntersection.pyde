import random

class Circle:
    def __init__(self, x, y, radius):
        self.x, self.y, self.radius = x, y, radius
    
    def render(self):
        ellipse(self.x, self.y, self.radius, self.radius)

def dist(x1, y1, x2, y2):
    return sqrt(((x2-x1) ** 2) + ((y2 - y1) ** 2))

def circleIntersectCircle(c1, c2):
    d = dist(c1.x, c1.y, c2.x, c2.y)
    return c1.radius > d or c2.radius > d

def setup():
    size(500, 500)
    global circles, upperRadius, s
    s = 0
    upperRadius = 500
    circles = []
    noLoop()
    
def draw():
    # background(204)
    global circles
    print(len(circles))
    for _ in range(5):
        skip = False
        x = random.randint(0, width)
        y = random.randint(0, height)
        r = random.randint(0, 100)
        circle = Circle(x, y, r)
        for c in circles:
            if circleIntersectCircle(c, circle):
                skip = True
                break
        if not skip:
            circles.append(circle)
            circle.render()

    # for circle in circles:
    #     circle.render()

def mouseClicked():
    loop()
