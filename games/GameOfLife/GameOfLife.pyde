class Board:
    def __init__(self, x, y):
        self.width, self.height = x, y
        self.divX, self.divY = width / float(self.width), height / float(self.height)
        self.board = [[False for _ in range(self.width)] for _ in range(self.height)]
        
    def render(self):
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                translate(self.divX * x, self.divY * y)
                if cell:
                    fill(212, 226, 15)
                elif not cell:
                    fill(99, 99, 97)
                stroke(204)
                rect(0, 0, self.divX, self.divY)
                textAlign(CENTER, CENTER)
                fill(255)
                # text(str(self.neighbors(x,y)), self.divX / 2.0, self.divY / 2.0)
                resetMatrix()
                
    def neighbors(self, x, y):
        global offsets
        # (X, Y, Active)
        neighbors = []
        for offX, offY in offsets:
            newX, newY = (x + offX, y + offY)
            if not self.valid(newX, newY):
                continue
            elif self.board[newY][newX]:
                neighbors.append((newX, newY))
        return len(neighbors)
    
    def tick(self):
        temp = []
        for y, row in enumerate(self.board):
            for x, cell in enumerate(row):
                neighbors = self.neighbors(x, y)
                # populated
                if cell:
                    if neighbors < 2 or neighbors > 3:
                        temp.append((x, y))
                    # elif neighbors >= 2 and <= 3:
                    #     pass
                # unpopulated
                elif not cell:
                    if neighbors == 3:
                        temp.append((x, y))
        for togX, togY in temp:
            self.toggle(togX, togY)
    
    def click(self, x, y):
        x /= self.divX
        y /= self.divY
        x, y = int(x), int(y)
        self.toggle(x, y)
        return x, y
        
    def toggle(self, x, y):
        self.board[y][x] = not self.board[y][x]
    
    def valid(self, x, y):
        return not(x < 0 or y < 0 or x >= self.width or y >= self.height)
    
def setup():
    size(750, 750)
    global board, paused, offsets
    board = Board(50, 50)
    paused = True
    offsets = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    frameRate(60)
    
def draw():
    global board, paused
    background(0)
    if not paused:
        board.tick()
    board.render()

def mouseClicked():
    x, y = board.click(mouseX, mouseY)
    
def keyPressed():
    global paused
    paused = not paused
    if paused:
        frameRate(60)
    elif not paused:
        frameRate(10)
    print('Paused' if paused else 'Resumed')
