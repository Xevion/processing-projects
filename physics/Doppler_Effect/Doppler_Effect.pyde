# Represents a single wave emission
class SoundWave(object):
    def __init__(self, x, y, speed=1, radius=1):
        self.x, self.y = x, y
        self.speed, self.radius = speed, radius
        
    def tick(self):
        self.radius += self.speed

    # Moved into a function to allow fast adjustment of opacity degradation
    # whilst still observing current opacity from external "garbage collectors"
    @property
    def stroke(self):
        return self.radius * 0.75
    
    def render(self):
        stroke(self.stroke) # Opacity Controls
        circle(self.x, self.y, self.radius * 2) # diameter

def setup():
    size(750, 750)

    noFill()
    
    global sounds, x, y
    sounds = []
    x, y = width // 2 - 250, height // 2

i = 0
XRATE = 2
def draw():
    global sounds, XRATE, x, y, i
    
    x += XRATE
    i += 1
    if i % (15 // XRATE) == 0:
        sounds.append(SoundWave(x, y, 0.1 + XRATE))

    if i % 200 == 0:
        sounds = [s for s in sounds if s.stroke < 255]

    if x >= 1300:
        x = -100

    print(len(sounds))

    background(255)
    for sound in sounds:
        sound.tick()
        sound.render()
