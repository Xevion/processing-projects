import random, time

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.right, self.bottom, self.visited, self.current, self.start = True, True, False, False, False
    def __str__(self):
        return 'Cell({}, {}, bottom: {}, right: {}, visited: {})'.format(self.x, self.y, self.bottom, self.right, self.visited)
    
    def getNeighbor(self):
        possible = self.neighbors()
        possible = [thing for thing in possible if thing != None]
        if possible:
            choice = random.choice(possible)
            return grid[choice[0]][choice[1]]
        return None
    
    # def getNeighbor(self):
    #     possible = self.neighbors()
    #     if any([thing != None for thing in possible]):
    #         xchoice = None
    #         while xchoice == None:
    #             xchoice = random.choices(possible, weights=[2, 1, 1, 2], k=1)[0]
    #         return grid[xchoice[0]][xchoice[1]]
    #     else:
    #         return None
    
    def neighbors(self):
        global offsets
        neighbors = []
        for offset in offsets:
            neighbor = (self.x + offset[0], self.y + offset[1])
            if not valid(neighbor):
                neighbors.append(None)
                continue
            if grid[neighbor[0]][neighbor[1]].visited:
                neighbors.append(None)
                continue
            neighbors.append(neighbor)
        return neighbors
    
    def render(self):
        global divX, divY
        translate(self.x * divX, self.y * divY)
        # Drawing Cell Background
        # Visited, Unvisited, Highlighted
        
        if self.start:
            fill(28, 147, 158)
        elif self.visited:
            fill(0, 42, 135)
        else:
            fill(0, 2, 30)
        
        if self.current:
            fill(0, 127, 196)
            self.current = False
        noStroke()
        rect(0, 0, divX, divY)
        
        # Drawing Cell Lines
        stroke(255)
        fill(255)
        strokeWeight(2.5)
        if not self.visited:
            noStroke()
        if self.bottom:
            line(0, divY, divX, divY)
        if self.right:
            line(divX, 0, divX, divY)
        resetMatrix()

def openWalls(x1, y1, x2, y2):
    global offsets
    # Bottom, Right, Left, Top
    offset = (x2 - x1, y2 - y1)
    if offset == offsets[0]:
        grid[x1][y1].bottom = False
    if offset == offsets[1]:
        grid[x1][y1].right = False
    if offset == offsets[2]:
        grid[x2][y2].right = False
    if offset == offsets[3]:
        grid[x2][y2].bottom = False


def valid(coordinate):
    global columns, rows
    return not (coordinate[0] < 0 or coordinate[0] >= columns or coordinate[1] < 0 or coordinate[1] >= rows)

def generate():
    global complete, columns, rows, grid, divX, divY, current, offsets
    # Bottom, Right, Left, Top
    complete = 0
    offsets = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    columns, rows = 50, 50
    divX, divY = width / float(columns), height / float(rows)
    grid = [[Cell(x, y) for y in range(rows)] for x in range(columns)]
    current = grid[random.randint(0, columns-1)][random.randint(0, rows-1)]
    current.visited = True
    current.start = True

def setup():
    size(750, 750)
    frameRate(10000)
    generate()
    noLoop()
def mazeGenTick(loops=500):
    global current, next, i
    for _ in range(loops):
        next = current.getNeighbor()
        if next:
            i = 0
            next.parent = current
            openWalls(current.x, current.y, next.x, next.y)
            current = next
            grid[current.x][current.y].current = True
            current.visited = True
        else:
            try:
                current.parent
                current = current.parent
                grid[current.x][current.y].current = True
            except:
                global complete
                complete += 1
    
def render():
    background(0)
    for column in grid:
        for cell in column:
            cell.render()

i = 0
def draw():
    render()
    global complete
    if complete > 10:
        # saveFrame("maze-###.png")
        time.sleep(2.0)
        generate()
    if complete > 1:
        for _ in range(300):
            mazeGenTick()
        render()
    else:
        mazeGenTick(1)

def mouseClicked():
    loop()
