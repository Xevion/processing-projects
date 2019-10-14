from random import choice, randint
import sys, os

def setup():
    readSettings()
    frameRate(45)
    size(1280, 720)
    fill(0, 0, 0)
    rect(0, 0, width, height)
    
    global img, rectX, rectY
    rectX, rectY = randint(1, width-rectWidth), randint(1, height-rectHeight)
    img = loadImage("image.jpg")
    # img = loadImage("DVD_video_logo.png")

# Create and/or overwrite the settings.json file in the directory
def createSettings():
    settingsJSON = {
                "height" : 1280,
                "width" : 720,
                "colorRGB" : [255, 255, 255]
                }
    with open(os.path.join(sys.path[2], 'settings.json'), 'w+') as settingsfile:
        json.dump(settingsfile, settingsJSON)

# Read the settings file, importing and setting the variables in the script to correlate
def readSettings():
    try:
        with open(os.path.join(sys.path[2], 'settings.json'), 'r+') as settingsfile:
            data = json.load(settingsfile)
            setup(data["height"], data["width"])
    except IOError:
        print("No settings file found. Creating one now.")
        createSettings()
        os.exec()
        # print("Settings file created. Exiting program")
        # sys.exit()
Xspeed, Yspeed = 5,5
if(choice([True, False])):
    Xspeed *= -1
if(choice([True, False])):
    Yspeed *= -1
rectWidth, rectHeight = 600/2, 400/2
renderpos = False
count = 1

def collision():
    global Xspeed, Yspeed, rectX, rectWidth, rectY, rectHeight
    xcollide, ycollide = False, False
    if rectX <= 0 or rectX+rectWidth >= width:
        xcollide = True
        Xspeed *= -1
    if rectY <= 0 or rectY+rectHeight >= height:
        ycollide = True
        Yspeed *= -1
    if xcollide and ycollide:
        global count
        count +=1
        print("Corner hit while at ({}, {})".format(rectX, rectY))
    
def mouseClicked():
    global renderpos
    renderpos = not renderpos

def draw():
    global slope, rectX, rectY, rectWidth, rectHeight, Xspeed, Yspeed, renderpos, count
    rectX, rectY = rectX+Xspeed, rectY+Yspeed
    
    if count > 0:
        fill(255,255,255)
        textAlign(CENTER)
        textSize(20)
        text("Corner Hits: " + str(count), 20, 20)
    
    fill(0, 0, 0)
    rect(0, 0, width, height)
    
    fill(255, 255, 255)
    image(img, rectX, rectY, rectWidth, rectHeight)
    # rect(rectX, rectY, rectWidth, rectHeight)
    if(renderpos):
        fill(255, 255, 255)
        textAlign(CENTER)
        textSize(20)
        x, y = rectX, rectY
        x2, y2 = rectX + (rectWidth)/2, rectY + (rectHeight)/2
        text("({}, {})".format(x, y), x, y)
        line(x2, y2, x2 + (Xspeed*500), y2 + (Yspeed*500))
    collision()
