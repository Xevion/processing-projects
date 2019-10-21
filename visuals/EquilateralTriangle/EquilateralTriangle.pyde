def setup():
    size(750, 750)
    noLoop()
    
def equiTriangle(center, side):
    
    altitude = side * (sqrt(3) / 2.0)
    AM = (2.0/3.0) * altitude
    BF = (1.0 / 2.0) * side
    FM = (1.0 / 3.0) * altitude
    
    a = (center[0], center[1] + AM)
    b = (center[0] - BF, center[1] - FM)
    c = (center[0] + BF, center[1] - FM)
            
    return a, b, c
    
i = 0
def draw():
    global i
    i += 1
    
    # background(204)
    translate(width / 2.0, height / 2.0)
    rotate(radians(i))
    
    a, b, c = equiTriangle((0, 0), i)
    triangle(a[0], a[1], b[0], b[1], c[0], c[1])

def mouseClicked():
    loop()
