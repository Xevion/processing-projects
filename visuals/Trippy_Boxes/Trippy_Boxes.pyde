class RGB:
    def __init__(self, r, g, b):
        self.r, self.g, self.b = r, g, b
        self.rgb = (r,g,b)

def setup():
    size(750, 750, P3D)
    colorMode(HSB, 5, 5, 5)
    
def drawMatrix(i):
    multi = 200
    for x in range(5):
        for y in range(5):
            for z in range(5):
                pushMatrix()
                translate(200, 200)
                translate(x * multi, y * multi, z * multi)
                rotateX(i)
                rotateY(i)
                stroke(i % 5, 5, 5, 240)
                fill(i % 5, 5, 5, 255/8)
                strokeWeight(3)
                box(100)
                popMatrix()
i = 0
def draw():
    global i
    i += 0.02
    background(5)
    drawMatrix(i)
    
