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
def generate(xx=None, yy=None):
    global columns, rows, offsets
    # Bottom, Right, Left, Top
    offsets = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    columns, rows = 50, 50
    
    global grid, divX, divY
    divX, divY = width / float(columns), height / float(rows)
    grid = [[Cell(x, y) for y in range(rows)] for x in range(columns)]
    
    global switch
    switch = True
    global cellList
    cellList = []
    if xx != None and yy != None:
        start = pixelToCoordinates(xx, yy)
    else:
        start = (random.randint(0, columns-1), random.randint(0, rows-1))
    cellList.append(start)

def pixelToCoordinates(x, y): 
    return int(x / float(divX)), int(y / float(divY))

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
    for _ in range(columns + rows):
        if len(cellList) > 0:
            global switch
            if switch:
                # most recent
                # index = len(cellList) - 1
                # select = cellList[index]
                
                # oldest
                index = 0
                select = cellList[0]
            else:
                # most random
                index = random.randint(0, len(cellList)-1)
                select = cellList[index]
            
                
            
            neighbors = grid[select[0]][select[1]].neighbors()
            if len(neighbors) < 1:
                grid[select[0]][select[1]].live = False
                cellList.pop(index)
            else:
                new = random.choice(neighbors)
                openWalls(select[0], select[1], new[0], new[1])
                grid[new[0]][new[1]].visited = True
                grid[new[0]][new[1]].live = True
                cellList.append(new)
        else:
            # time.sleep(2)
            return
        
def draw():
    global switch
    switch = not switch
    render()
    # if len(cellList) == 0:
    #     generate()
    tick()
    
def mouseClicked():
    generate(mouseX, mouseY)
