import pprint, random, colorsys

def blend(fromRGB, toRGB, midpoints=10):
    arr = []
    R1, G1, B1 = fromRGB
    R2, G2, B2 = toRGB
    Rdiv = (R1 - R2) / float(midpoints)
    Gdiv = (G1 - G2) / float(midpoints)
    Bdiv = (B1 - B2) / float(midpoints)
    for x in range(floor(midpoints+1)):
        R = R1 - (Rdiv * x)
        G = G1 - (Gdiv * x)
        B = B1 - (Bdiv * x)
        arr.append((R, G, B))
    return arr

def rndTuple(n):
    return random.randint(0, n), random.randint(0, n), random.randint(0, n)

def HSVtuple():
    preH, preS, preV = random.randint(0, 360) / 360.0, 1, 1
    preR, preG, preB = colorsys.hsv_to_rgb(preH, preS, preV)
    return preR * 255, preG * 255, preB * 255

def regen():
    global arr, precision
    precision = 1000.0
    # Generated via RGB randomization
    RGB1, RGB2 = rndTuple(255), rndTuple(255)
    
    # Generated via HSV to RGB randomization
    RGB1, RGB2 = HSVtuple(), HSVtuple()
    arr = blend(RGB1, RGB2, midpoints=precision)

def setup():
    size(1000, 1000)
    regen()
    
pp = pprint.PrettyPrinter()

def draw():
    global arr, precision
    xDiv = width/precision
    for x in range(floor(precision)):
        fill(*arr[x])
        stroke(0, 0, 0, 0)
        rect(0, x * xDiv, width, (x + 1) * xDiv)

def mouseClicked():
    regen()
