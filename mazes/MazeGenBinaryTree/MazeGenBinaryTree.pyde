import random, time

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
def generate(xx=25, yy=25):
    global columns, rows, offsets
    # Bottom, Right, Left, Top
    offsets = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    columns, rows = xx, yy
    
    global grid, divX, divY
    divX, divY = width / float(columns), height / float(rows)
    grid = [[Cell(x, y) for y in range(rows)] for x in range(columns)]
    
    global current, moveSet, moveConst
    # Starts from NorthWest, moves SouthEast
    # current = 0, 0
    # moveset = [(0, 1), (1, 0)]
    
    # Starts from NorthEast, moves SouthWest
    # current = columns - 1, 0
    # moveset = [(0, 1), (-1, 0)]
    
    # Starts from SouthWest, moves NorthEast
    # current = 0, rows - 1
    # moveset = [(0, -1), (1, 0)]
    
    # Starts from SouthEast, moves NorthWest
    current = columns - 1, rows - 1
    moveSet = [(0, -1), (-1, 0)]
    moveConst = (-1, -1)
    
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
    global current, moveSet, moveConst
    
    # Check if we're done
    if current[1] < 0:
        noLoop()
        return True
    
    x = (current[0] + moveSet[0][0], current[1] + moveSet[0][1]) # North
    y = (current[0] + moveSet[1][0], current[1] + moveSet[1][1]) # West
    
    if valid(current):
        grid[current[0]][current[1]].visited = True
    
    # Check if on edge
    if current[0] <= 0:
        openWalls(current[0], current[1], x[0], x[1])
        # Set the new current to the next row on the first cell
        current = columns - 1, current[1] + moveConst[1]
        tick()
        return
    # Not on a horozontal edge
    else:
        # Not on a vertical edge
        if current[1] > 0:
            # Choose between the two offsets
            if random.choice([True, False]):
                openWalls(current[0], current[1], y[0], y[1])
            else:
                openWalls(current[0], current[1], x[0], x[1])
        # On a vertical edge
        else:
            openWalls(current[0], current[1], y[0], y[1])
    
    # Move the current cell.
    current = current[0] + moveConst[0], current[1]
    return False
    
s = False
def draw():
    if s:
        for _ in range(columns):
            tick()
        time.sleep(2.5 // rows)
        render()
        
def mouseClicked():
    global s
    s = True
    loop()
    generate(*[min(mouseX, mouseY)] * 2)
