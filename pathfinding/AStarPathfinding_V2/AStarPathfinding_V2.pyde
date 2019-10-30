class Node():
    def __init__(self,  position, parent=None, wall=False, open=False, closed=False, path=False):
        self.parent, self.position, self.wall, self.open, self.closed, self.path = parent, position, wall, open, closed, path
        self.g = self.h = self.f = 10
        
    
    def __eq__(self, other):
        return self.position == other.position

class Board():
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.xDiv, self.yDiv = width / float(self.x), height / float(self.y)
        self.board = []
        self.start, self.end, self.limit = None, None, 10
        self.openList, self.closedList, self.pathList = [], [], []
        
    # A Raw 'Tap' ont the board
    def tapRaw(self, x, y, type):
        self.tap(int(x // self.xDiv), int(y // self.yDiv), type)
    
    # Checks whether a set of coordinates is valid
    def outOfBounds(self, x, y):
        return x < 0 or y < 0 or x > (self.x - 1) or y > (self.y - 1)
    
    # Generates the board's elements, including the bomb's locations
    def generate(self):
        self.board = list(range(self.x))
        for x in range(self.x):
            self.board[x] = list(range(self.y))
            for y in range(self.y):
                self.board[x][y] = Node(parent=None, position=(x, y), wall=False, open=False, closed=False)
    
    def tap(self, x, y, type):
        # Move the start position to the specified coords
        if type == LEFT:
            self.placeStart(x, y)
        # Move the end position to the specified coords
        elif type == RIGHT:
            self.placeEnd(x, y)
        # Place a wall at the specificed coords
        elif type == CENTER:
            self.placeWall(x, y)
        # Tick the limiter up
        elif type == UP:
            self.tick(True)
        # Tick the limiter down
        elif type == DOWN:
            self.tick(False)
    
    # Places the start path position at the given coordinates
    def placeStart(self, x, y):
        self.start = x, y
    
    # Places the end path position at the given coordinates
    def placeEnd(self, x, y):
        self.end = x, y
    
    # Places (or unplaces) a wall at the given coordinates
    def placeWall(self, x, y):
        self.board[x][y].wall = not self.board[x][y].wall
    
    # Tick up or down the limiter
    def tick(self, up=True):
        if up:
            self.limit += 1
        elif not up:
            if self.limit == 0:
                return
            self.limit -= 1
    
    # A* pathfinding, slightly deviated for limiter
    def path(self, manual=None):
        def getPath(node=None, index=None):
            # If the limit is reached and thus we're not supplied anything, just pick randomly
            everything = self.openList + self.closedList # Just combine both lists so we get mostly optimal results
            if node == None and index == None:
                check_node, check_index = everything[0], 0
                for index, item in enumerate(everything):
                    if item.f < check_node.f:
                        check_node = item
                        check_index = index
            path = []
            while check_node is not None:
                path.append(check_node.position)
                check_node = check_node.parent
            return path[::-1]
        if manual == None:
            startX, startY = self.start
            targetX, targetY = self.end
        else:
            startX, startY, targetX, targetY = manual
        print(startX, startY, targetX, targetY)
        start_node = Node(parent=None, position=(startX, startY))
        end_node = Node(parent=None, position=(targetX, targetY))
        self.openList, self.closedList = [start_node], []
        
        while len(self.openList) > 0:
            # Find the best node to use
            current_node, current_index = self.openList[0], 0
            for index, item in enumerate(self.openList):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index
            # Remove the current node from the openList and append to the closedList
            self.closedList.append(self.openList.pop(index))
            print("---------NEW WLOOP: {} ---------".format(current_node.position))
            if current_node == end_node:
                print("Finished pathfinding")
                self.pathList = getPath(current_node, current_index)
                return None
            else:
                print("{} is not the end node {}".format(current_node.position, end_node.position))
                
            children = []
            cardinals = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            for offset in cardinals:
                # New position with offset applied
                new_position = current_node.position[0] + offset[0], current_node.position[1] + offset[1]
                new_node = Node(parent=current_node, position=new_position)
                
                # If node is a wall
                if self.board[new_position[0]][new_position[1]].wall:
                    print(str(new_node.position) + " is a wall")
                    continue
                # If node is out of bounds
                if self.outOfBounds(new_position[0], new_position[1]):
                    print(str(new_node.position) + " is out of bounds")
                    continue
                print(str(new_node.position) + " was accepted as a possible child")
                children.append(new_node)
            for child in children:
                # If node is already closed
                if child in self.closedList:
                    print(str(child.position) + " already in closedList")
                    continue
                
                # If node is already opened
                if child in self.openList:
                    print(str(child.position) + " already in openList")
                    continue
                
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h
                
                # This node is ready, append to the openList
                print(str(child.position) + " was appended to openList")
                self.openList.append(child)
                
            print("While loop finish: " + str([node.position for node in self.openList]) + " ... " + str([node.position for node in self.closedList]))
    
    def render(self):
        for x in range(self.x):
            for y in range(self.y):
                if (x, y) == self.start:
                    fill(0, 255, 0)
                elif (x, y) == self.end:
                    fill(255, 0, 0)
                elif (x, y) in self.pathList:
                    fill(100)
                elif (x, y) in [node.position for node in self.closedList]:
                    fill(255, 0, 255, 10)
                else:
                    fill(255)
                stroke(0)
                rect(x * self.xDiv, y * self.yDiv, (x + 1) * self.xDiv, (y + 1) * self.yDiv)
    
    def doPath(self):
        if self.start != None and self.end != None:
            print("Pathing start with limit " + str(self.limit))
            self.path()
            print("-------------PATHING ENDED-------------")
            
def setup():
    size(500, 500)
    global board
    board = Board(int(width/50), int(height/50))
    board.generate()
    noLoop()
    redraw()
    board.start = (0, 0)
    board.end = (6, 6)
    
def draw():
    global board
    background(204)
    board.doPath()
    board.render()
    print(board.pathList)

def mouseClicked():
    global board
    board.tapRaw(mouseX, mouseY, mouseButton)
    redraw()
    
def mouseWheel(event):
    # Just process the event for what it is, we'll use UP and DOWN
    # to define what it is, even though they're completely different things
    def handle():
        e = event.getCount()
        if e == -1:
            return UP
        elif e == 1:
            return DOWN
        else:
            return None
            
    # do it
    global board
    board.tapRaw(0, 0, handle())
    redraw()
