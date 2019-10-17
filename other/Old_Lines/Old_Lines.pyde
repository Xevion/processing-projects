def setup():
    size(500, 500)
    
arr = []
def draw():
    global arr
    print(len(arr))
    
    buffersize = 100
    arr.insert(0, (mouseX, mouseY))
    if len(arr) > buffersize:
        arr = arr[:buffersize]
        oldx, oldy = (arr[-1])
        line(oldx, oldy, mouseX, mouseY)
