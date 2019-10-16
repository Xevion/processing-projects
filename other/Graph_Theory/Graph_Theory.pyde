import random

class MovingPoint:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.xSpeed, self.ySpeed = random.randint(-5, 5), random.randint(-5, 5)
        self.rotation = random.randint(0, 360)
    
    def tick(self):
        def rnd():
            lower, upper, minimum, maximum = -5, 5, -5, 5
            self.xSpeed = self.xSpeed + random.choice([_ for _ in range(lower, upper)])
            self.ySpeed = self.ySpeed + random.choice([_ for _ in range(lower, upper)])
            self.xSpeed = max(min(self.xSpeed, maximum), minimum)
            self.ySpeed = max(min(self.ySpeed, maximum), minimum)
        if self.x >= width:
            rnd()
            self.x = 0
        elif self.x <= 0:
            self.x = width
            rnd()
        if self.y >= height:
            self.y = 0
            rnd()
        elif self.y <= 0:
            self.y = height
            rnd()
        self.x, self.y = self.x + self.xSpeed, self.y + self.ySpeed

    def render(self):
        def lowest(mpoint, points):
            dists = []
            for point in points:
                dists.append((dist(self.x, self.y, point[0], point[1])))
            tupled = zip(points, dists)
            tupled.sort(key=lambda x: x[1])
            return [x[0] for x in tupled[1:3]]
            
        def dist(x1, y1, x2, y2):
            return sqrt((abs(x1 - x2) ** 2) + (abs(y1 - y2) ** 2))
        ellipse(self.x, self.y, 5, 5)
        
        global MovingPoints
        for point in lowest((self.x, self.y), [(MV.x, MV.y) for MV in MovingPoints]):
            line(self.x, self.y, point[0], point[1])
        resetMatrix()

def setup():
    size(500, 500)
    frameRate(15)
    
    global MovingPoints
    MovingPoints = []
    for _ in range(70):
        MovingPoints.append(MovingPoint(random.randint(0, width), random.randint(0, height)))

def draw():
    global MovingPoints
    background(204)
    
    for MP in MovingPoints:
        MP.tick()
        MP.render()
