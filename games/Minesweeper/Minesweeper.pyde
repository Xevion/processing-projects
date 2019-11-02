import random

# Simple object to manage all the colors on the board
# Use as a global object to access quickly
class Images():
    def __init__(self):
        names = ["0", "1", "2", "3", "4", "5", "6", "7", "8",
                 "flag", "questionmark", "unopened_square", "bomb"]
        self.images = {}
        for name in names:
            build = "Minesweeper_{}.gif".format(name)
            img = loadImage(build, 'gif')
            self.images[name] = img

# A class showing the nodes on a board
# Despite it's inclusio, the `parent` parameter has no use in the code, at all.
# Based off a A* algorithm I found online, but has been tweaked and "optimized" personally
class MovingNode():
    def __init__(self, parent=None, position=None):
        self.parent, self.position = parent, position
    
    def __eq__(self, other):
        return self.position == other.position

# The Board Object
# Manages and stores all node values, as well as performs actions such as flagging and tapping
class Board():
    def __init__(self, sizeX, sizeY, default=None, composition=0.1, showall=True):
        self.sizeX, self.sizeY, self.composition, self.showall = sizeX, sizeY, composition, showall
        self.board = []
        # Generate all bombs on the board, as well as create nodes for it.
        self.generate()
        # The calculated pixel size of every square is calculated here
        self.xDiv = width / float(self.sizeX)
        self.yDiv = height / float(self.sizeY)
        
        # Show all the nodes on the board IF the `showall` parameter is on
        if self.showall:
            for nodeList in self.board:
                for node in nodeList:
                    node.hidden = False
        print("{} bombs placed".format(len(self.bombLocations)))
    
    # A raw mouse position's tap, it is translated into a board node 'tap'
    def tapRaw(self, x, y, type): 
        self.tap(int(x // self.xDiv), int(y // self.yDiv), type)
    
    # A 'tap' on the board
    def tap(self, x, y, type):
        if type == LEFT:
            self.board[x][y].flagged = False
            if self.board[x][y].bomb:
                self.board[x][y].hidden = False
                print("You tapped at bomb at {}".format((x,y)))
            if self.board[x][y].hidden:
                if self.board[x][y].value == 0:
                    self.traverse(x, y)
                else:
                    self.board[x][y].hidden = False
        elif type == RIGHT:
            if self.board[x][y].hidden:
                self.board[x][y].flagged = not self.board[x][y].flagged
    def outOfBounds(self, x, y):
        return x < 0 or y < 0 or x > (self.sizeX - 1) or y > (self.sizeY - 1)
    
    #  Reveal all near board nodes if they are hidden
    def traverse(self, x, y):
        start_node = MovingNode(position=(x, y))
        openList, closedList = [start_node], []
        
        # While open nodes are available
        while len(openList) > 0:
            current_node = openList.pop(0)
            closedList.append(current_node)
            
            children = []
            cardinals = [(1, 0), (0, 1), (-1, 0), (0, -1)]
            # Whether you want nodes to traverse diagonally or not,
            # if not, simply remove the diagonals from being added to the cardinal directions arary
            diagonals = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
            cardinals += diagonals
            for offset in cardinals:
                new_position = offset[0] + current_node.position[0], offset[1] + current_node.position[1]
                new_node = MovingNode(parent=current_node, position=new_position)
                if self.outOfBounds(new_position[0], new_position[1]):
                    continue
                if new_node not in openList:
                    if new_node not in closedList:
                        if self.board[new_position[0]][new_position[1]].value != 0:
                            closedList.append(new_node)
                        else:
                            openList.append(new_node)
        print("Traversal from {}, {} nodes opened".format((x, y), len(closedList)))
        for closed_node in closedList:
            x,y = closed_node.position
            self.board[x][y].hidden = False

    # Function to render the board on the screen
    def render(self):
        for x in range(self.sizeX):
            for y in range(self.sizeY):
                global images
                imageMode(CENTER)
                offsetX, offsetY = (x + 0.5) * self.xDiv, (y + 0.5) * self.yDiv
                # Draw a Unhidden bomb
                if self.board[x][y].bomb and not self.board[x][y].hidden:
                    image(images.images['bomb'], offsetX, offsetY, self.xDiv, self.yDiv)
                # Draw a Unhidden Node
                elif not self.board[x][y].hidden:
                    image(images.images[str(self.board[x][y].value)], offsetX, offsetY, self.xDiv, self.yDiv)
                # Draw a Flagged Node
                elif self.board[x][y].flagged:
                    image(images.images['flag'], offsetX, offsetY, self.xDiv, self.yDiv)
                # Draw a Hidden Node
                elif self.board[x][y].hidden:
                    image(images.images['unopened_square'], offsetX, offsetY, self.xDiv, self.yDiv)
                
                # Draw the Rectangle
                stroke(0)
                fill(0, 0, 0, 0)
                # rect(cornerX1, cornerY1, cornerX2, cornerY2)
    
    # Generates the board's elements, including the bomb's locations
    def generate(self):
        if self.composition < 1.0:
            bombNum = self.sizeX * self.sizeY
            bombNum *= self.composition
            bombNum = min(self.sizeX * self.sizeY - 1, bombNum)
            bombNum = int(bombNum)
        else:
            bombNum = int(self.composition)
        self.bombLocations = set([])
        while len(self.bombLocations) < bombNum:
            self.bombLocations.add((random.randint(0, self.sizeX), random.randint(0, self.sizeY)))
        
        self.board = list(range(self.sizeX))
        for x in range(self.sizeX):
            self.board[x] = list(range(self.sizeY))
            for y in range(self.sizeY):
                if (x, y) in self.bombLocations:
                    newNode = Node((x, y), self.bombLocations, self.sizeX, self.sizeY, bomb=True, flagged=False)
                else:
                    newNode = Node((x, y), self.bombLocations, self.sizeX, self.sizeY, bomb=False, flagged=False)
                self.board[x][y] = newNode
class Node():
    def __init__(self, position, bombLocations, sizeX, sizeY, hidden=True, bomb=False, flagged=False):
        self.bomb, self.flagged, self.position, self.hidden = bomb, flagged, position, hidden
        self.bombLocations, self.sizeX, self.sizeY, self.value = bombLocations, sizeX, sizeY, 0
        self.calc()
        
    def flag(self):
        self.flagged = True
    
    def outOfBounds(self, x, y):
        return x < 0 or y < 0 or x > self.sizeX or y > self.sizeY
    
    # Calculates the number of bombs around the node (not including itself)
    def calc(self):
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for offset in directions:
            checkPosition = self.position[0] + offset[0], self.position[1] + offset[1]
            if self.outOfBounds(checkPosition[0], checkPosition[1]):
                continue
            if checkPosition in self.bombLocations:
                self.value += 1
                
# The setup function, just creates the board, as well as inits the colorset
def setup():
    size(1920/2, 1080/2)
    global board, images
    images = Images()
    board = Board(width/16, height/16, composition=0.1, showall=False)
    noLoop()
    redraw()
    redraw()
    
# The simple rendering loop
def draw():
    background(0)
    global board
    board.render()

# Manages the tapping action
def mouseClicked():
    global board
    board.tapRaw(mouseX, mouseY, mouseButton)
    redraw()
