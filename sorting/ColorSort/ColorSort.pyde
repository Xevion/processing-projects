import colorsys, random

def setup():
    size(180 * 2, 180 * 2)
    global array, carray
    frameRate(1000)
    
    array = [x for x in range(max(width, height))]
    carray = [getRGB(x, precision=max(width, height)) for x in array]
    
    combined = zip(array, carray)
    random.shuffle(combined)
    array[:], carray[:] = zip(*combined)
    noLoop()
    
def getRGB(n, precision=360.0):
    r, g, b = colorsys.hsv_to_rgb(n / float(precision), 1, 1)
    return r * 255, g * 255, b * 255

def getRGBArray(array):
    out = [getRGB(x, precision=len(array)) for x in array]
    return out

def randHSV():
    h = random.random()
    r, g, b = colorsys.hsv_to_rgb(h, 1, 1)
    return r * 255, g * 255, b * 255

def visualize(array, carray):
    for pos, value in enumerate(array):
        r, g, b = carray[pos]
        stroke(r, g, b)
        line((width/2) - value/2, pos, (width/2) + value/2, pos)

def bubbleSort(array, carray):
    def swap(x1, x2):
        array[x1], array[x2] = array[x2], array[x1]
        carray[x1], carray[x2] = carray[x2], carray[x1]
    for pos, value in enumerate(array[:-1]):
            if value > array[pos + 1]:
                swap(pos, pos+1)
    return array, carray

def pieChartRender(diameter, array, carray=None):
    lastAngle = 0
    div = 360.0 / len(array)
    
    for pos, var in enumerate(array):
        fill(*carray[pos])
        arc(width/2, height/2, diameter, diameter, lastAngle, lastAngle + radians(div))
        lastAngle += radians(div)

i = 1
array = []
def draw():
    global array, carray
    background(255)
    pieChartRender(width-10, array, carray)
    array, carray = bubbleSort(array, carray)

def mouseClicked():
    loop()
