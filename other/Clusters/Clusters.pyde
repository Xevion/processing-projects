import random

class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

def ddist(x1, y1, x2, y2):
    return sqrt((abs(y2 - y1) ** 2) + (abs(x2 - x1) ** 2))

def clusterize(cpoints, points):
    clusters = [[] for _ in range(len(cpoints))]
    for point in points:
        distances = []
        # Get distances from current point to all the cluster points
        for cpoint in cpoints:
            distances.append(ddist(point.x, point.y, cpoint.x, cpoint.y))
            
        curPos, curDist = 0, distances[0]
        # Get the index of the lowest distance
        for pos, dist in enumerate(distances):
            if curDist > dist:
                curPos = pos
                curDist = dist
        clusters[curPos].append(point)
    return clusters

def avgPoint(points):
    Xs = [point.x for point in points]
    Ys = [point.y for point in points]
    return Point(sum(Xs) / len(points), sum(Ys) / len(points))

def reclusterize(cpoints, points, n=10):    
    for _ in range(n):
        clusters = clusterize(cpoints, points)
        for pos, _ in enumerate(cpoints):
            if len(clusters[pos]) > 0:
                cpoints[pos] = avgPoint(clusters[pos])
    return cpoints, clusters

def rndPoints(n, topX, topY):
    return [Point(random.randint(0, topX), random.randint(0, topY)) for _ in range(n)]
    
def allButIndex(arrs, index):
    return [arr for pos, arr in enumerate(arrs) if pos != index]

def concat(arrs):
    while type(arrs[0]) is list:
        temp = []
        for arr in arrs:
            temp += arr
        arrs = temp
    return arrs
def displayClusters(clusters):
    global colors, colorDiv
    pColorDiv = 100 / len(clusters)
    if pColorDiv != colorDiv:
        print('Colors regenerated.')
        colorDiv = pColorDiv
        offset = random.randint(0, 360)
        colors = [((colorDiv * n) + offset) % 100 for n in range(len(clusters))]
    for pos, cluster in enumerate(clusters):
        fill(colors[pos], 100, 100)
        stroke(0,0,0)

        strokeWeight(0)
        for p1pos, point1 in enumerate(cluster):            
            # ellipse(point1.x, point1.y, 5, 5)
            curdist = 999999999999
            # line(point1.x, point1.y, cpoints[pos].x, cpoints[pos].y)
            # for p2pos, point2 in enumerate(cluster):
            #     if p1pos != p2pos:
            #         dddist = ddist(point1.x, point1.y, point2.x, point2.y)
            #         if dddist < 250:
            #             stroke(colors[pos], 100, 100, 50)
            #             line(point1.x, point1.y, point2.x, point2.y)
            for p2pos, point2 in enumerate(concat(allButIndex(clusters, pos))):
                if p1pos != p2pos:
                    newdist = ddist(point1.x, point1.y, point2.x, point2.y)
                    if curdist > newdist:
                        curdist = newdist
            fill(colors[pos], 100, 100, 5)
            noStroke()
            ellipse(point1.x, point1.y, int(curdist) * 2, int(curdist) * 2)
        fill(colors[pos], 100, 100)
        ellipse(cpoints[pos].x, cpoints[pos].y, 10, 10)

def generate():
    global numClusters, numPoints, numIterations, cpoints, points, clusters
    cpoints = rndPoints(numClusters, width, height)
    points = rndPoints(numPoints, width, height)
    cpoints, clusters = reclusterize(cpoints, points, n=numIterations)

def setup():
    size(750, 750)
    colorMode(HSB, 100)
    blendMode(BLEND)
    global numClusters, numPoints, numIterations
    numClusters, numPoints, numIterations = 6, 150, 1
    generate()
    global colors, colorDiv
    colors = []
    colorDiv = 0
    noLoop()
    redraw()
    
def draw():
    background(0, 0, 90)
    global clusters
    displayClusters(clusters)

def keyPressed():
    if key == TAB:
        global cpoints, points, clusters
        cpoints, clusters = reclusterize(cpoints, points, n=1)
        print('Reclustered.')
        redraw()
    elif key == ENTER:
        generate()
        print('Regenerated.')
        redraw()
