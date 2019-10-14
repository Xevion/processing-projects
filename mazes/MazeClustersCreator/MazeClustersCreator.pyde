import random

class Mover:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.active = True
        global grid
        self.current = grid[x][y]
        self.hue = random.randint(0, 360)
    
    def tick(self):
        global grid
        if not grid[self.current.x][self.current.y].visited:
            grid[self.x][self.y].active = True
            grid[self.current.x][self.current.y].visited = True
            grid[self.current.x][self.current.y].hue = self.hue
        neighbors = self.current.getNeighbors()
        if neighbors:
            neighbor = random.choice(neighbors)
            neighbor = grid[neighbor[0]][neighbor[1]]
            neighbor.parent = self.current
            openBetween(self.current.x, self.current.y, neighbor.x, neighbor.y)
            self.current = neighbor
        else:
            if self.current.parent:
                self.current = self.current.parent
        
class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.visited = False
        self.hue = -1
        self.active, self.bottom, self.right = False, True, True
        self.parent, self.visited = None, None
        
    def getNeighbors(self):
        neighbors = []
        global grid, offsets
        for pos, offset in enumerate(offsets):
            neighbor = (self.x + offset[0], self.y + offset[1])
            if cellExists(neighbor):
                if not grid[neighbor[0]][neighbor[1]].visited:
                    neighbors.append(neighbor)
        return neighbors
    
    def render(self):
        global divX, divY
        translate(divX * self.x, divY * self.y)
        if self.visited:
            noStroke()
            fill(self.hue, 360, 360)
            rect(1, 1, divX - 1, divY - 1)
        # if self.active:
        #     self.active = False
        #     noStroke()
        #     fill(0, 360, 0)
        #     rect(1, 1, divX - 1, divY - 1)
        if self.right:
            line(divX, 0, divX, divY)
        if self.bottom:
            line(0, divY, divX, divY)
        resetMatrix()

def openBetween(x1, y1, x2, y2):
    global offsets
    # Down, Right, Left, Up
    if not cellExists((x1, y1)) or not cellExists((x2, y2)):
        return
    offset = (x2 - x1, y2 - y1)
    if offset == offsets[0]:
        grid[x1][y1].bottom = False
    elif offset == offsets[1]:
        grid[x1][y1].right = False
    elif offset == offsets[2]:
        grid[x2][y2].right = False
    elif offset == offsets[3]:
        grid[x2][y2].bottom = False

def cellExists(coordinate):
    x, y = coordinate
    return not (x < 0 or x >= columns or y < 0 or y >= rows)
                
def setup():
    size(750, 750)
    colorMode(HSB, 360)
    global divX, divY, columns, rows, grid, movers, offsets
    columns, rows = 100, 100
    divX, divY = width / float(columns), height / float(rows)
    grid = [[Cell(x, y) for y in range(rows)] for x in range(columns)]
    # Down, Right, Left, Up
    offsets = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    movers = [Mover(random.randint(0, columns-1), random.randint(0, rows-1)) for _ in range(columns * rows / 1000)]
    frameRate(99999)
def draw():
    global grid, movers
    background(204)
    for _ in range(50):
        for mover in movers:
            mover.tick()
    for row in grid:
        for cell in row:
            cell.render()
