import random

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.right, self.bottom, self.visited, self.live = True, True, False, False
    
    # Identify the neighbors of the cell
    def neighbors(self):
        global offsets
        neighbors = []
        for offset in offsets:
            neighbor = (self.x + offset[0], self.y + offset[1])
            if not valid(neighbor):
                continue
            if grid[neighbor[0]][neighbor[1]].visited:
                continue
            neighbors.append(neighbor)
        return neighbors
    
    # Render the single cell
    def render(self):
        global divX, divY
        translate(self.x * divX, self.y * divY)
        # Drawing Cell Background
        # Visited, Unvisited, Highlighted
        
        if self.live:
            fill(244, 117, 117)
        elif self.visited:
            fill(255)
        else:
            fill(204)
        noStroke()
        rect(0, 0, divX, divY)
        
        # Drawing Cell Lines
        stroke(0)
        fill(255)
        strokeWeight(2.5)
        if self.bottom:
            line(0, divY, divX, divY)
        if self.right:
            line(divX, 0, divX, divY)
        resetMatrix()

# Open walls between two cells on the grid
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

# Validates whether a coordinate is valid with the curret columns and rows set
def valid(coordinate):
    global columns, rows
    return not (coordinate[0] < 0 or coordinate[0] >= columns or coordinate[1] < 0 or coordinate[1] >= rows)

# Generates a new grid and cellList (with start) for the maze generation.
# Serves mostly to ease the process of regenerating a maze without restarting the Sketch
def generate(xx=None, yy=None):
    global columns, rows, offsets
    # Bottom, Right, Left, Top
    offsets = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    columns, rows = 25, 25
    
    global grid, divX, divY
    divX, divY = width / float(columns), height / float(rows)
    grid = [[Cell(x, y) for y in range(rows)] for x in range(columns)]
    
    global current, runSet, runSetActive
    current = 0, 0
    runSet = []
    runSetActive = False
    
def pixelToCoordinates(x, y): 
    return int(x / float
           (divX)), int(y / float(divY))

def setup():
    size(750, 750)
    generate()
    
# Runs the cell.render() action on every cell    
def render():
    background(0)
    for row in grid:
        for cell in row:
            cell.render()
            
def tick():
    global current, runSet, runSetActive
    if runSetActive:
        if len(runSet) > 0:
            print('a')
            get = runSet[0]
            if get == []:
                return
            print('b')
            print(runSet, get)
            choice = random.choice(get)
            print('c')
            openWalls(choice[0], choice[1], choice[0], choice[1] - 1)
            print('d')
            del runSet[0]
            return
        else:
            runSet = [[]]
            runSetActive = False
            
    # Are we done with the maze?
    if current[0] == columns and current[1] == rows - 1:
        if len(runSet) > 0:
            runSetActive = True
            return
        print('Done')
        render()
        noLoop()
    # Are we on the horozontal edge?
    elif current[0] == columns:
        if not runSetActive:
            if current[1] > 0:
                for coord in runSet[-1]:
                    grid[coord[0]][coord[1]].live = False
            runSetActive = True
            current = 0, current[1] + 1
    # Keep carving runSets
    else:
        # If you're on the ceiling of the maze, just carve and skip the whole thing.
        if current[1] == 0:
            openWalls(current[0], current[1], current[0] + 1, current[1])
        # Keep carving east
        elif current[0] == 0 or not random.choice([True, False]):
            runSet[-1].append((current[0], current[1]))
            grid[current[0]][current[1]].live = True
            openWalls(current[0], current[1], current[0] + 1, current[1])
        # Break out new runSet
        else:
            for coord in runSet[-1]:
                grid[coord[0]][coord[1]].live = False
            runSet.append([(current[0], current[1])])
    if not runSetActive:
        current = current[0] + 1, current[1]
    
def draw():
    for _ in range(columns):
        tick()
    render()
    
def mouseClicked():
    loop()
    generate(mouseX, mouseY)
