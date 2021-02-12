# HIT137 - Assignment 2 Keith Yardley & Mark Zeroni
#                       ******   Christmas Turtle   ******

import random
from turtle import *
from math import radians, tan #Needed to calculate center of some ornaments

def setupTurtle(t, pen_state="up", coordTuple=None, heading=0, speed=0, pencolor="black", fillcolor="black", shape="turtle", turtlesize=(1,1,1), width=1):
    '''Sets up the turtle with a variety of attributes. Only Turtle (t) is mandatory.'''
    t.speed(0) #For teleporting to coords
    t.up()
    if coordTuple is not None: t.goto(coordTuple)   #Only goto if coords are given
    t.speed(speed) #Goes back to designated speed
    if pen_state == "down": t.down() #Defaults to being up
    t.seth(heading)
    t.fillcolor(fillcolor)
    t.pencolor(pencolor)
    t.shape(shape)
    t.turtlesize(turtlesize[0],turtlesize[1],turtlesize[2]) #Goes through the given tuple
    t.width(width)

def setupRoom(t):
    '''Sets up the room background and draws windows.'''
    hgt = t.screen.window_height()
    wdt = t.screen.window_width()
    #Floor
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
    drawCentredSquare(t, scale, "brown") #Draw the window frame as a square
    for i in glass:
        t.goto(coordTuple)
        t.goto(t.pos() + i) #Directly adding coordTuple + i does not work
        drawCentredSquare(t, 0.35*scale, "cyan") #Draw the window glass over the frame

def drawPoints(t, list, scale):
    '''Moves the turtle through the given list of points, and then fills in the enclosed area.'''
    t.begin_fill()
    for i in list:
        t.goto(i[0]*scale,i[1]*scale)
    t.end_fill()

def drawTree(t, scale, x, y):
    '''Draws the Christmas tree.'''
    scale = (t.screen.window_height() * 0.9) / 728.88 #Calculates the multiplier needed for 1x scale to take up 90% of the screen height.

    setupTurtle(t, "down", (x,y), width=5, speed=0, fillcolor=(102,26,26))
    points_trunk = [(0.00,-364.50), (22.47,-364.50), (22.47,-297.10), (-22.47,-297.10), (-22.47,-364.50), (22.47,-364.50)]
    points_leaves = [(22.47,-297.10), (224.65,-297.10), (89.86,-63.64), (89.86,-63.64), (179.72,-63.64), (67.40,130.92),
                    (134.79,130.92), (0.00,364.38), (-134.79,130.92), (-67.40,130.92), (-179.72,-63.64), (-89.86,-63.64),
                    (-224.65,-297.10),(22.47,-297.10)]  #Lists were made by drawing the tree normally using t.fd and t.seth through trial and error.
    
    drawPoints(t, points_trunk, scale)  #Draws tree trunk
    t.fillcolor(0,153,0)                #Sets color to green
    drawPoints(t, points_leaves, scale) #Draws tree leaves

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
    ''''Draws an oval, initially drawn 45 degrees to the right.'''
    for i in range(2):
        t.circle(radius, 90)
        t.circle(radius/2, 90)

def drawPresent(t, coordTuple, box_color, ribbon_color, scale):
    '''Draws a present at the specified position, with the box and a ribbon.'''
    setupTurtle(t, coordTuple=coordTuple)
    box = [(30*scale,30*scale), (30*scale,-30*scale), (-30*scale,30*scale), (-30*scale,-30*scale)]
    drawCentredSquare(t, scale, ribbon_color) #Draws the ribbon as the background
    for i in box:
        t.goto(coordTuple)
        t.goto(t.pos() + i)
        drawCentredSquare(t, 0.4*scale, box_color)  #Draws the box parts over the ribbon to make the ribbon into a cross.

    #Ribbon bows
    setupTurtle(t, "down", (t.pos() + (65*scale,100*scale)), pencolor=ribbon_color, width=12*scale)
    drawOval(t, 30*scale)
    setupTurtle(t, "down", (t.pos() + (-18*scale,7*scale)), pencolor=ribbon_color, heading=70, width=12*scale)
    drawOval(t, 30*scale)

def drawNStar(t, number, length, color):
    '''Draws a star with an odd number (N) of points.'''
    middle = ((length/2) * tan(radians(180/number)))/2 #Finds vertical distance from start to middle
    setupTurtle(t, "down", (t.pos() + (-length/2,middle)), fillcolor=color)
    t.begin_fill()
    for i in range(number):
        t.fd(length)
        t.rt(180-(180/number))
    t.end_fill()

def drawSpirograph(t, scale):
    '''Draws a colorful spirograph (circle of circles)'''
    setupTurtle(t, "down", width=3)
    for i in range (6):
        for colours in ["red", "magenta", "blue", "cyan", "green", "yellow"]:
            t.color(colours)
            t.circle(25*scale)  #Arbitrary scale - scale of 1 makes it not too big or small
            t.lt(10)

def drawPattern(t, x, y, number, sides, length, color):
    '''Draws a radial pattern of shapes around the point (x,y)'''
    setupTurtle(t, "down", (x,y), fillcolor=color)
    t.begin_fill()
    for i in range(number):     #Draws the radial pattern
        for i in range(sides):  #Draws a shape
            t.fd(length)
            t.lt(360 / sides)   #Draws the lines in the shape
        t.lt(360 / number)
    t.end_fill()

def prediction(t, sides, length):
    '''Finds and returns the radius of the circle needed to fully enclose a pattern.'''
    pos_a = t.pos()
    t.speed(0) #Instant
    for i in range(sides // 2): #Shapes with an odd number of sides have their max distance on the corners
        t.fd(length)            #just before and after the halfway point.
        t.lt(360 / sides)
    radius = t.distance(pos_a) #Radius of the prediction circle is equal to the diameter of the chosen shape
    t.speed(0) #Returns speed to normal - DEBUG - do not forget to turn down later
    return radius

def getInput(message, type):
    '''Gets an input of the specified type and catches the error if the input is invalid.'''
    while True:
        try:
            if type == "float": #Avoids making seperate functions to get int and float inputs while catching errors
                variable = float(input("Enter "+message+": "))
            else:
                variable = int(input("Enter "+message+": "))
            if variable == 0 or variable == float(0):   #Prevents crashes if scale is set to 0
                raise ValueError
            break

        except ValueError:
            print("Must be a valid",type,"and must be >0!")
    return variable

def getColorInput(t, message, repeat):
    '''Gets a color input from the user, allowing color strings and rgb values.'''
    colorList = ["red", "green", "blue", "yellow", "purple", "cyan", "white"] #For random colors - so there are no ugly looking colors
    while True:
        color = input("Enter "+str(message)+" color string or RGB tuple (max 255) or type \"R\" for random: ")
        print(color)
        if color == "r":
            while True:
                color = colorList[random.randint(0,6)]
                if color != repeat: #If the chosen color is the same as the previous one, choose a new color
                    break
            break

        else:
            try:
                t.fillcolor(color) #Tests if color string is valid
                break
            except:
                try: #Convert to tuple if string doesn't work
                    color = color.strip(" ").strip("(").strip(")").split(",") #Strips all whitespace and parenthesis and then splits parts seperated by commas.
                    for i in range(len(color)): color[i] = int(color[i]) #Converts elements into integers
                    t.fillcolor(tuple(color)) #Tests if color tuple is valid
                    break
                except:
                    print("Invalid color string or tuple, please re-enter.")
    return color

def decorate(t):
    '''Allows the user to specify an ornament and place it on the screen.'''
    running = True
    while running:
        setupTurtle(t, coordTuple=(0,0)) #Resets turtle to default
        t.screen.onscreenclick(t.goto)   #Allows the user to place the ornament where clicked
        
        stop = input("Select a predefined shape by typing \"P\", type \"C\" to create a custom shape or hide the turtle and then exit by typing anything else: ")
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
                    
                    t.screen.onscreenclick(None) #Stops the user from relocating the cursor when halfway through as it would cause parts of the shape to be drawn elsewhere.
                    drawPresent(t, t.pos(), box_color, ribbon_color, scale)
                    break

                elif select == "star" or select == "2":
                    while True:
                        points = getInput("points (must be odd and minimum 3)", "integer")
                        if (points % 2 == 1) and (points >= 3): #The star function can only handle stars with an odd number of points
                            break                               #and it must have >=3 sides as less does not form a shape.
                        else:
                            print("Must be an odd number and be >= 3!")
                    
                    length = getInput("width", "integer")
                    color = getColorInput(t, "star", None)
                    setupTurtle(t, fillcolor=color, shape="circle", turtlesize=(length/20,length/20,1))

                    stop = input("Move the ornament by clicking on the screen.\nType \"back\" to remake the ornament or type any other key to confirm position: ")
                    if stop == "back":
                        break

                    t.screen.onscreenclick(None)    #Stops the user from relocating the cursor when halfway through as it would cause parts of the shape to be drawn elsewhere.
                    drawNStar(t, points, length, color)
                    break

                elif select == "spirograph" or select == "3":
                    scale = getInput("scale", "float")
                    setupTurtle(t, shape="circle", turtlesize=(5*scale,5*scale,1))

                    stop = input("Move the ornament by clicking on the screen.\nType \"back\" to remake the ornament or type any other key to confirm position: ")
                    if stop == "back":
                        break

                    t.screen.onscreenclick(None)    #Stops the user from relocating the cursor when halfway through as it would cause parts of the shape to be drawn elsewhere.
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

                t.screen.onscreenclick(None)    #Stops the user from relocating the cursor when halfway through as it would cause parts of the shape to be drawn elsewhere.
                drawPattern(t, t.xcor(), t.ycor(), number, sides, length, color)
                break
        else:
            pause = input("Press \"P\" to continue drawing or press any other button to quit.")
            if pause != "p":
                running = False
    t.hideturtle()

def main():
    t = Turtle(shape="turtle")
    t.screen.colormode(255)
    start = ((t.screen.window_height() * -0.5) + (t.screen.window_height() * 0.05)) #starts from the bottom of the screen with a 5% margin
    setupRoom(t)
    drawTree(t, 1, 0, start)
    decorate(t) #Main loop of the program

main()