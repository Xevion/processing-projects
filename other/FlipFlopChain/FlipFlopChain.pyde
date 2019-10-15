'''
    :param int length: The number of objects to be simulated.
    :param float objPad: Space between each object. Will constrict the diameter of nearby objects
    :param float sidePad: The padding between where the objects are rendered and the leftmost and rightmost sides of the application
    :param float objDelta: The space between the center-y of the application that a object takes when it flips from on to off states
'''
class FlipFlopChain:
    def __init__(self, length, objPad, sidePad, objDelta):
        self.length = length
        self.objPad = objPad
        self.sidePad = sidePad
        self.objDelta = objDelta
        
        self.bools = [False for _ in range(length)]
        objSpace = (width - (2 * self.sidePad)) - (self.length - 1) * self.objPad
        self.objDiameter = objSpace / float(self.length)
        self.objRadius = self.objDiameter / 2.0
        
    def flip(self, i):
        if i >= len(self.bools) - 1:
            self.bools = [False for _ in range(len(self.bools))]
            print('Completed one rotation')
            return True
        else:
            self.bools[i] ^= True
    
    def get(self, i):
        return self.bools[i]
    
    def tick(self, i=1):
        place = 0
        self.flip(place)
        while not self.get(place):
            place += 1
            if self.flip(place):
                break
    
    def render(self):
        translate(self.sidePad, height / 2.0)
        for boolValue in self.bools:
            translate(self.objRadius, 0)
            if boolValue:
                ellipse(0, -1 * self.objDelta, self.objDiameter, self.objDiameter)
            else:
                ellipse(0, self.objDelta, self.objDiameter, self.objDiameter)
            translate(self.objRadius + self.objPad, 0)

def setup():
    size(1500, 300)

    global flipflopchain
    flipflopchain = FlipFlopChain(30, 10, 45, 100)
    
def draw():
    background(204)
    global flipflopchain
    for _ in range(100):
        flipflopchain.tick()
    flipflopchain.render()
