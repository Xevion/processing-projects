import time

def setup():
    size(750, 750)
    frameRate(60)
    background(0)
s = 0
multi = 12.0
    
curColor = 0
def nextColor():
    global curColor
    colors = [(255,0,0), (255, 127,0), (255,255,0), (0,255,0), (0,0,255), (75,0,130), (148,0,211)]
    curColor += 1
    return colors[curColor % len(colors)]

def draw():
    multi = 12.0
    s = 0
    for _ in range(int(12//0.3)):
        if multi <= 0:
            noLoop()
            time.sleep(1)
            s = 0
            multi = 12.0
        s += 1
        multi -= 0.3
        pushMatrix();
        translate(width/2,height/2);
        # rotate(s*radians(0.6));
        stroke(255)
        R, G, B = nextColor()
        stroke(R, G, B)
        fill(0, 0, 0)
        x1, y1, x2, y2, x3, y3 = -30*multi, 30*multi, 0, -30*multi, 30*multi, 30*multi
        # triangle(x1, y1, x2, y2, x3, y3);
        ellipse(0, 0, 100*multi, 100*multi)
        popMatrix();
