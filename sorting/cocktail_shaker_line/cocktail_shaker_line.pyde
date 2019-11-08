import random, time

def setup():
    global array
    size(1000, 1000)
    array = list(range(height))
    random.shuffle(array)
    colorMode(HSB, height)
    
def draw():
    background(height)
    global array
    done = True
    for index in range(len(array)-1):
        if array[index] < array[index + 1]:
            array[index], array[index + 1] = array[index + 1], array[index]
            done = False
    for index in list(range(len(array)-1))[::-1]:
        if array[index] < array[index + 1]:
            array[index], array[index + 1] = array[index + 1], array[index]
            done = False
            
    for index, num in enumerate(array):
        fill(num, height, height)
        stroke(num, height, height)
        ellipse(num, index, 5, 5)
    
    if done:
        time.sleep(0.5)
        random.shuffle(array)
