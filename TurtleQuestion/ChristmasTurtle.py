#TODO:
#Remove debug code
#Optimise - remove redundant code i.e. multiple instances of setting speed when it hasn't changed

import random
from turtle import *
from math import radians, tan #Needed to calculate center of some ornaments

def setupTurtle(t, pen_state="up", coordTuple=None, heading=0, speed=0, pencolor="black", fillcolor="black", shape="turtle", turtlesize=(1,1,1), width=1):
    '''Sets up the turtle with a variety of attributes. Only Turtle (t) is mandatory.'''
    t.speed(0) #For teleporting to coords
    t.up()
    if coordTuple is not None: t.goto(coordTuple)
    t.speed(speed)
    if pen_state == "down": t.down()
    t.seth(heading)
    t.fillcolor(fillcolor)
    t.pencolor(pencolor)
    t.shape(shape)
    t.turtlesize(turtlesize[0],turtlesize[1],turtlesize[2])
    t.width(width)

def setupRoom(t):
    '''Sets up the room background and draws windows.'''
    #Floor
    hgt = t.screen.window_height()
    wdt = t.screen.window_width()
    setupTurtle(t, "down", ((wdt * -0.5),(hgt * -0.3)), fillcolor="brown", speed=0)
    t.begin_fill()
    t.goto((wdt * 0.5),(hgt * -0.3))
    t.goto((wdt * 0.5),(hgt * -0.5))
    t.goto((wdt * -0.5),(hgt * -0.5))
    t.end_fill()
    #Wall
    setupTurtle(t, "down", ((wdt * -0.5),(hgt * -0.3)), fillcolor=(50,50,70), speed=0)
    t.begin_fill()
    t.goto((wdt * -0.5),(hgt * 0.5))
    t.goto((wdt * 0.5),(hgt * 0.5))
    t.goto((wdt * 0.5),(hgt * -0.3))
    t.end_fill()
    #Windows
    drawWindow(t, (wdt * -0.3, 0), 1)
    drawWindow(t, (wdt * 0.3, 0), 1)

def drawWindow(t, coordTuple, scale):
    '''Draws a window with 4 glass panes.'''
    setupTurtle(t, coordTuple=coordTuple, speed=0)
    glass = [(22.5*scale,22.5*scale), (22.5*scale,-22.5*scale), (-22.5*scale,22.5*scale), (-22.5*scale,-22.5*scale)]
    drawCentredSquare(t, scale, "brown")
    for i in glass:
        t.goto(coordTuple)
        t.goto(t.pos() + i)
        drawCentredSquare(t, 0.35*scale, "cyan")

def drawTree(t, scale, x, y):
    '''Draws the Christmas tree.'''
    #Calculates the multiplier needed for 1x scale to take up 90% of the screen height. 649 is the true height of the tree.
    scale = scale * ((t.screen.window_height() * 0.9) / 649)
    setupTurtle(t, "down", (x,y), width=5, speed=0, fillcolor=(102,26,26))

    #Trunk
    t.begin_fill()
    t.fd(20*scale)
    t.lt(90)
    t.fd(60*scale)
    t.lt(90)
    t.fd(40*scale)
    t.lt(90)
    t.fd(60*scale)
    t.lt(90)
    t.fd(40*scale)
    t.end_fill()
    t.lt(90)
    t.fd(60*scale)
    t.rt(90)
    
    #Leaves
    t.begin_fill()
    t.fillcolor(0,153,0)
    t.fd(180*scale)
    t.lt(120)
    t.fd(240*scale)
    t.rt(120)
    t.fd(80*scale)
    t.lt(120)
    t.fd(200*scale)
    t.rt(120)
    t.fd(60*scale)
    t.lt(120)
    t.fd(240*scale)
    t.lt(120)
    t.fd(240*scale)
    t.lt(120)
    t.fd(60*scale)
    t.rt(120)
    t.fd(200*scale)
    t.lt(120)
    t.fd(80*scale)
    t.rt(120)
    t.fd(240*scale)
    t.lt(120)
    t.fd(220*scale)
    t.end_fill()

def drawCentredSquare(t, scale, color):
    '''Draws a square centred at the current position.'''
    setupTurtle(t, "down", (t.pos() - (50*scale,50*scale)), fillcolor=color)
    t.begin_fill()
    for i in range(4):
        t.fd(100*scale)
        t.lt(90)
    t.end_fill()
    t.up() #Necessary as other functions do not t.up between drawing squares

def drawOval(t, radius):
    ''''Draws an oval, initially 45 degrees to the right.'''
    for i in range(2):
        t.circle(radius, 90)
        t.circle(radius/2, 90)

def drawPresent(t, coordTuple, box_color, ribbon_color, scale):
    '''Draws a present at the specified position, with the box and a ribbon.'''
    setupTurtle(t, coordTuple=coordTuple)
    box = [(30*scale,30*scale), (30*scale,-30*scale), (-30*scale,30*scale), (-30*scale,-30*scale)]
    drawCentredSquare(t, scale, ribbon_color)
    for i in box:
        t.goto(coordTuple)
        t.goto(t.pos() + i)
        drawCentredSquare(t, 0.4*scale, box_color)

    #Ribbon bows
    setupTurtle(t, "down", (t.pos() + (65*scale,100*scale)), pencolor=ribbon_color, width=12*scale)
    drawOval(t, 30*scale)
    setupTurtle(t, "down", (t.pos() + (-18*scale,7*scale)), pencolor=ribbon_color, heading=70, width=12*scale)
    drawOval(t, 30*scale)

def drawNStar(t, number, length, color):
    middle = ((length/2) * tan(radians(180/number)))/2 #Finds vertical distance from start to middle
    setupTurtle(t, "down", (t.pos() + (-length/2,middle)), fillcolor=color)
    t.begin_fill()
    for i in range(number):
        t.fd(length)
        t.rt(180-(180/number))
    t.end_fill()

def drawSpirograph(t, scale):
    setupTurtle(t, "down", width=3)
    for i in range (6):
        for colours in ["red", "magenta", "blue", "cyan", "green", "yellow", "black"]:
            t.color(colours)
            t.circle(50*scale)
            t.lt(10)

def drawPattern(t, x, y, number, sides, length, color):
    '''Draws a radial pattern of shapes around the point (x,y)'''
    setupTurtle(t, "down", (x,y), fillcolor=color)
    t.begin_fill()
    for i in range(number):
        for i in range(sides):
            t.fd(length)
            t.lt(360 / sides)
        t.lt(360 / number)
    t.end_fill()

def prediction(t, sides, length):
    '''Finds and returns the radius of the circle needed to fully enclose a pattern.'''
    pos_a = t.pos()
    t.speed(0) #Instant
    for i in range(sides // 2):
        t.fd(length)
        t.lt(360 / sides)
    radius = t.distance(pos_a)
    t.speed(0) #Returns speed to normal - DEBUG - do not forget to turn down later
    return radius

def getInput(message, type):
    while True:
        try:
            if type == "float":
                variable = float(input("Enter "+message+": "))
            else:
                variable = int(input("Enter "+message+": "))
            break

        except ValueError:
            print("Must be a valid",type,"!")
    return variable

def getColorInput(t, message, repeat):
    #For random colors - so we don't get ugly looking colors
    colorList = ["red", "green", "blue", "yellow", "purple", "cyan", "white"]
    while True:
        try:
            color = input("Enter "+str(message)+" color string (\"R\" for random, \"C\" for custom): ")
            if color == "r":
                color = colorList[random.randint(0,6)]
                break

            elif color == "c":
                while True:
                    print("Enter RGB values (max 255):")
                    color = (
                        int(input("Red: ")), int(input("Green: ")), int(input("Blue: "))
                    )
                    if (color[0] <= 255) and (color[1] <= 255) and (color[2] <= 255):
                        break

                    else:
                        print("Invalid color sequence!")
                break

            else:
                t.fillcolor(color) #Tests if color is valid
                break

        except:
            print("Please enter a valid color string!")

    if color == repeat:                         #If the chosen color is the same as the previous one;
        color = colorList[random.randint(0,6)]  #choose a new color

    return color

def decorate(t):
    '''Allows the user to specify an ornament and place it on the screen.'''
    running = True
    while running:
        setupTurtle(t, coordTuple=(0,0)) #Resets turtle to default
        t.screen.onscreenclick(t.goto)
        
        stop = input("Select a predefined shape by typing \"P\", type \"C\" to create a custom shape or stop by typing anything else: ")
        if stop == "p":
            while True:
                print("Available predefined shapes: \n1. present\n2. star\n3. spirograph")
                select = str(input("Enter name or number of shape exactly as shown, or type \"back\" to go back: "))
                if select == "back":
                    break

                elif select == "present" or select == "1":
                    scale = getInput("scale", "float")
                    box_color = getColorInput(t, "box", None)
                    ribbon_color = getColorInput(t, "ribbon", box_color)
                    setupTurtle(t, heading=0, fillcolor=box_color, shape="square", turtlesize=(5*scale,5*scale,1), width=1)
                    
                    stop = input("Move the ornament by clicking on the screen.\nType \"back\" to remake the ornament or type any other key to confirm position: ")
                    if stop == "back":
                        break
                    
                    t.screen.onscreenclick(None)
                    drawPresent(t, t.pos(), box_color, ribbon_color, scale)
                    break

                elif select == "star" or select == "2":
                    while True:
                        points = getInput("points (must be odd and minimum 3)", "integer")
                        if (points % 2 == 1) and (points >= 3):
                            break
                        else:
                            print("Must be an odd number and be >= 3!")
                    
                    length = getInput("width", "integer")
                    color = getColorInput(t, "star", None)
                    setupTurtle(t, fillcolor=color, shape="circle", turtlesize=(length/20,length/20,1))

                    stop = input("Move the ornament by clicking on the screen.\nType \"back\" to remake the ornament or type any other key to confirm position: ")
                    if stop == "back":
                        break

                    t.screen.onscreenclick(None)
                    drawNStar(t, points, length, color)
                    break

                elif select == "spirograph" or select == "3":
                    scale = getInput("scale", "float")
                    setupTurtle(t, shape="circle", turtlesize=(10*scale,10*scale,1))

                    stop = input("Move the ornament by clicking on the screen.\nType \"back\" to remake the ornament or type any other key to confirm position: ")
                    if stop == "back":
                        break

                    t.screen.onscreenclick(None)
                    drawSpirograph(t, scale)
                    break

                else:
                    print("No shape of that name!")
                break

        elif stop == "c":
            while True:
                sides = getInput("number of sides in each shape", "integer")
                length = getInput("length of sides", "integer")
                number = getInput("number of shapes", "integer")
                color = getColorInput(t, "ornament", None)

                radius = max(prediction(t, sides, length), 1) #Max function is used as a crash occurs if the turtle stretch factor is too small
                setupTurtle(t, shape="circle", turtlesize=((radius/10),(radius/10),1), fillcolor=color)

                stop = input("Move the ornament by clicking on the screen.\nType \"back\" to remake the ornament or type any other key to confirm position: ")
                if stop == "back":
                    break
                t.screen.onscreenclick(None)
                
                drawPattern(t, t.xcor(), t.ycor(), number, sides, length, color)
                break
        else:
            running = False
    t.hideturtle()

def main():
    t = Turtle(shape="turtle")
    t.screen.colormode(255)
    start = ((t.screen.window_height() * -0.5) + (t.screen.window_height() * 0.05)) #starts from the bottom of the screen with a 5% margin
    setupRoom(t)
    drawTree(t, 1, 0, start)
    decorate(t)

    bye = input("Enter anything to exit.")

main()