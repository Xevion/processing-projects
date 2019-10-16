import random, time
from timeit import default_timer as timer

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.right, self.bottom, self.visited, self.current, self.start, self.end = True, True, False, False, False, False
        self.parent = None
        self.marked = False
   
    def __str__(self):
        return 'Cell({}, {}, bottom: {}, right: {}, visited: {})'.format(self.x, self.y, self.bottom, self.right, self.visited)
    
    def getNeighbor(self):
        possible = self.neighbors()
        possible = [thing for thing in possible if thing != None]
        if possible:
            choice = random.choice(possible)
            return grid[choice[0]][choice[1]]
        return None
    
    def pathingNeighbors(self):
        pass
    
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
    
    def crender(self):
        global divX, divY
        translate(self.x * divX, self.y * divY)
        # Drawing Cell Background
        # Visited, Unvisited, Highlighted
    
        
        if self.start:
            fill(190, 10, 10)
        elif self.end:
            fill(190, 10, 10)
        elif self.marked:
            fill(35, 155, 165)
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

class PathingCell:
    def __init__(self, coords, parent=None):
        self.coords = coords
        self.parent = parent
        self.h, self.g, self.f = 0, 0, 0
    
    def __eq__(self, other):
        return self.coords == other.coords

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
    global complete, columns, rows, grid, divX, divY, current, offsets, start, end
    # Bottom, Right, Left, Top
    complete = False
    offsets = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    columns, rows = 100, 100
    divX, divY = width / float(columns), height / float(rows)
    grid = [[Cell(x, y) for y in range(rows)] for x in range(columns)]
    current = grid[random.randint(0, columns-1)][random.randint(0, rows-1)]
    start = current
    ends = [(random.randint(0, columns-1), random.randint(0, rows-1)) for _ in range(5)]
    end = ends.pop(0)
    prevDist = 0 
    for coord in ends:
        dist = distance(start.x, start.y, coord[0], coord[1])
        if dist > prevDist:
            prevDist = dist
            end = coord
    end = grid[end[0]][end[1]]
    end.end = True
    current.visited = True
    current.start = True

def setup():
    size(750, 750)
    # random.seed(1)
    generate()
    # noLoop()

def astar(grid, start, end):
    start_cell = PathingCell(start, None)
    end_cell = PathingCell(end, None)
    
    open_list = [start_cell]
    closed_list = []
    
    # While the open list is not empty
    while len(open_list) > 0:
        # Find the best cell to loop no
        current_cell, current_index = open_list[0], 0
        for index, cell in enumerate(open_list):
            if current_cell.f > cell.f:
                current_cell = cell
                current_index = index
        
        # Remvoe the new current cell from the open list and to the closed list
        closed_list.append(current_cell)
        open_list.pop(current_index)
        
        # Check if the current cell is the end cell (we've found the exit)
        if current_cell == end_cell:
            current = current_cell
            path = []
            while current is not None:
                path.append(current.coords)
                current = current.parent
            return path[::-1]
    
        children = []
        # Bottom, Right, Left, Top
        # Find neighbor cells we can move into
        for index, offset in enumerate(offsets):
            # Calculate the coordinate of the adjacent neighbor we're looking at
            new_coord = (current_cell.coords[0] + offset[0], current_cell.coords[1] + offset[1])
            # If the coordinate we're looking at is valid
            if valid(new_coord):
                # Create a new pathing cell
                new_cell = PathingCell(new_coord, current_cell)
                # is the bottom open?
                if index == 0:
                    if not grid[current_cell.coords[0]][current_cell.coords[1]].bottom:
                        children.append(new_cell)
                # is the right open?
                elif index == 1:
                    if not grid[current_cell.coords[0]][current_cell.coords[1]].right:
                        children.append(new_cell)
                # is the left side open?
                elif index == 2:
                    if not grid[new_coord[0]][new_coord[1]].right:
                        children.append(new_cell)
                # is the top open?
                elif index == 3:
                    if not grid[new_coord[0]][new_coord[1]].bottom:
                        children.append(new_cell)
        
        for child in children:
            # is the child we looked at already closed?
            skip = False
            for closed_child in closed_list:
                if child == closed_child:
                    skip = True
            if skip:
                continue
            
            # calculate algorithmic values
            child.g = current_cell.g + 1
            child.h = ((current_cell.coords[0] - end_cell.coords[0]) ** 2) + ((current_cell.coords[1] - end_cell.coords[1]) ** 2)
            child.f = child.g + child.h
        
            # is the cell already open? is the cell we made worst in path iterations?
            for open_cell in open_list:
                if child == open_cell and child.g > open_cell.g:
                    continue
            
            # open the new cell
            open_list.append(child)

def randomizeOpen(chance=0.05):
    global grid
    for row in grid:
        for cell in row:
            if random.random() < chance:
                if random.choice([True, False]):
                    cell.right = False
                else:
                    cell.bottom = False

def mazeGenTick():
    global current, next, i
    for _ in range(500):
        next = current.getNeighbor()
        if next:
            next.parent = current
            openWalls(current.x, current.y, next.x, next.y)
            current = next
            grid[current.x][current.y].current = True
            current.visited = True
        else:
            if current.parent != None:
                current.parent
                current = current.parent
                grid[current.x][current.y].current = True
            else:
                global start
                if current == start and current.getNeighbor() == None:
                    global complete
                    complete = True
                    print('Done')

def distance(x1, y1, x2, y2):
    return sqrt(((x2 - x1) ** 2) + ((y2 - y1) ** 2))

# Render the maze itself
def render():
    background(0)
    for column in grid:
        for cell in column:
            cell.crender()

# Render the path of coordinates connecting them with ellipses and lines
def renderpath(path):
    fill(48, 255, 103)
    stroke(48, 255, 103)
    for index, coord in enumerate(path[:-1]):
        ellipse(coord[0] * divX + (divX * 0.5), coord[1] * divY + (divY * 0.5), divX / 3, divY / 3)
        line(coord[0] * divX + (divX * 0.5), coord[1] * divY + (divY * 0.5), path[index + 1][0] * divX + (divX * 0.5), path[index + 1][1] * divY + (divY * 0.5))
    ellipse(path[-1][0] * divX + (divX * 0.5), path[-1][1] * divY + (divY * 0.5), divX / 3, divY / 3)

def draw():
    render()
    global complete
    if complete:
        # randomizeOpen(0.15)
        startTime = timer()
        path = astar(grid, (start.x, start.y), (end.x, end.y))
        endTime = timer()
        # for coord in path:
        #     grid[coord[0]][coord[1]].marked = True
        render()
        print('Maze is {} x {} tiles with a solve path length of {} tiles.'.format(columns, rows, len(path)))
        print('The solve path took about {}s to complete.'.format(round(endTime - startTime, 3)))
        renderpath(path)
        noLoop()
    else:
        mazeGenTick()
