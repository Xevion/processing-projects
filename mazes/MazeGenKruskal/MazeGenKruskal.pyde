import random, time, string

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.identity = None
        self.right, self.bottom, self.visited, self.current, self.start = True, True, False, False, False
    def __str__(self):
        return 'Cell({}, {}, bottom: {}, right: {}, visited: {})'.format(self.x, self.y, self.bottom, self.right, self.visited)
        
    def neighbors(self, identityCheck=True):
        global offsets
        neighbors = []
        for offset in offsets:
            neighbor = (self.x + offset[0], self.y + offset[1])
            # If the neighbor isn't real
            if not valid(neighbor):
                continue
            # If the neighbor hasn't been claimed
            elif not grid[neighbor[0]][neighbor[1]].visited:
                neighbors.append(neighbor)
                continue
            # We're checking for their identity
            elif identityCheck:
                # If the neighbor isn't like me
                if grid[neighbor[0]][neighbor[1]].identity != self.identity:
                    neighbors.append(neighbor)
                    continue
        return neighbors
    
    def render(self):
        global divX, divY, showNumbers
        translate(self.x * divX, self.y * divY)
        # Drawing Cell Background
        # Visited, Unvisited, Highlighted
        if self.visited:
            fill(0, 42, 135)
        else:
            fill(0, 2, 30)
        
        if self.current:
            fill(0, 127, 196)
            self.current = False
        noStroke()
        rect(0, 0, divX+1, divY+1)
        
        # Drawing Cell Lines
        stroke(255)
        fill(255)
        strokeWeight(2.5)
        if showNumbers:
            textSize(24)
            textAlign(CENTER, CENTER)
            text(symbolize(self.identity), divX / 2.0, divY / 2.0)
        if not self.visited:
            noStroke()
        if self.bottom:
            line(0, divY, divX, divY)
        if self.right:
            line(divX, 0, divX, divY)
        resetMatrix()

def openWalls(x1, y1, x2, y2):
    global offsets, grid
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

def symbolize(n):
    stri = ''
    while n > 0:
        curLetter = (n - 1) % 26
        stri += string.ascii_uppercase[curLetter]
        n = (n - (curLetter + 1)) / 26
    return stri
    

def valid(coordinate):
    global columns, rows
    return not (coordinate[0] < 0 or coordinate[0] >= columns or coordinate[1] < 0 or coordinate[1] >= rows)

def generate():
    global columns, rows, grid, divX, divY, offsets
    # Bottom, Right, Left, Top
    offsets = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    columns, rows = 25, 25
    divX, divY = width / float(columns), height / float(rows)
    grid = [[Cell(x, y) for y in range(rows)] for x in range(columns)]
    
    global treeSet, i, nodesAdded, showNumbers
    try:
        showNumbers
    except:
        showNumbers = False
    i = 0
    nodesAdded = 0
    treeSet = []

# Tree Class. But it's really not a tree.
class Tree:
    def __init__(self, identity):
        self.tree = []
        self.identifier = identity
    
    def append(self, node):
        self.tree.append(node)
        grid[node[0]][node[1]].identity = self.identifier
        grid[node[0]][node[1]].visited = True
    
    # Merge another tree with this tree
    def merge(self, other):
        for node in other.tree:
            grid[node[0]][node[1]].identity = self.identifier
            self.tree.append(node)
    
    # Find a node in the list with an edge
    def getEdge(self, debug=False):
        random.shuffle(self.tree)
        # For every node in the tree
        for index, node in enumerate(self.tree):
            # if the node has any neighbors that aren't like us, return it
            if len(grid[node[0]][node[1]].neighbors()) > 0:
                return node
        print('Couldn\'t find an edge')

def setup():
    size(1000, 1000)
    noLoop()
    generate()
    frameRate(10)
    redraw()
    
def checkMaze():
    for row in grid:
        for cell in row:
            if not cell.visited:
                return False
    return True
    
# Kruskall's algorithm
def tick():
    # choose a node, find it's tree
    # if it has no tree, create a tree with a unvisited neighbor and open a wall between them
    # if it's in a tree
    # get the tree to return a node on the edge (has a neighbor that isn't in it's own tree)
    # merge the two trees together (the neighboring node's tree is added to the edge node's tree)
    # open the wall between the two nodes and the two trees have been merged properly
    # continue until no edges can be found in any tree (how to implement this without guesswork or expensive iterating?)
    
    global treeSet, i, nodesAdded
    # choose a random cell to work on, whether it's in a 'tree' or is unvisited
    choice = random.randint(0, columns-1), random.randint(0, rows-1)
    
    if nodesAdded == columns * rows:
        print('Maze completed ({} cells)'.format(nodesAdded))
        noLoop()
        return True
    
    # If the node is unclaimed
    if grid[choice[0]][choice[1]].identity == None:
        # Find it's unclaimed neighbors (if any)
        neighbors = grid[choice[0]][choice[1]].neighbors()
        neighbors = [neighbor for neighbor in neighbors if grid[neighbor[0]][neighbor[1]].identity == None]
        # We got a unclaimed lone node, just skip it for now (crap implementation, but needless work)
        if len(neighbors) == 0:
            return
        else:
            tree = Tree(i)
            i += 1
            nodesAdded += 2
            neighbor = random.choice(neighbors)
            openWalls(choice[0], choice[1], neighbor[0], neighbor[1])
            tree.append(choice)
            tree.append(neighbor)
            treeSet.append(tree)
    else:
        # get the identifier of our choice
        choiceIdentity = grid[choice[0]][choice[1]].identity
        # find an edge of the treeset and change our choice cell to that edge
        choice = treeSet[choiceIdentity].getEdge()
        neighbors = grid[choice[0]][choice[1]].neighbors()
        # get the neighbors of it that are different
        neighbor = random.choice(neighbors)
        # If the neighbor to the chosen cell's treeSet's edge cell is in another treeSet
        if grid[neighbor[0]][neighbor[1]].identity != None:
            get = treeSet[grid[neighbor[0]][neighbor[1]].identity]
            treeSet[grid[neighbor[0]][neighbor[1]].identity] = None
            treeSet[choiceIdentity].merge(get)
        # If it's just an unclaimed cell
        else:
            nodesAdded  += 1
            treeSet[choiceIdentity].append(neighbor)
        openWalls(choice[0], choice[1], neighbor[0], neighbor[1])

# Render the maze   
def render():
    background(0)
    for column in grid:
        for cell in column:
            cell.render()
 
def draw():
    for _ in range(columns):
        # if the maze is complete, it'll return True instead of None, if so, break the loop
        if tick():
            break
    render()

# Switch off the number display
def keyPressed():
    global showNumbers
    showNumbers = not showNumbers
    redraw()
    
# Regenerate the maze
def mouseClicked():
    loop()
    generate()
