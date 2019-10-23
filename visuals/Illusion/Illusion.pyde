def setup():
    size(750, 750)
    frameRate(250)
    background(0)

s = 0
multi = 12.0    
def draw():
    global s, multi
    s += 1
    if multi <= 0.3:
        noLoop()
    multi -= 0.3
    pushMatrix();
    translate(width/2,height/2);
    rotate(s*radians(0.3));
    stroke(255)
    fill(0, 0, 0, 0)
    triangle(-30*multi, 30*multi, 0, -30*multi, 30*multi, 30*multi); 
    popMatrix();
