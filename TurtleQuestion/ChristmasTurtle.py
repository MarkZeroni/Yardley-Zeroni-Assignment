#TODO:
#Add more predefined shapes - stars, spirograph
#Remove debug code
#Optimise - remove redundant code i.e. multiple instances of setting speed when it hasn't changed
#   Possibly remove centred square function and add a generic draw (uncentred) shape function

import random
from turtle import *
from math import radians, tan

def setupRoom(t):
    '''Sets up the room background and draws windows.'''
    t.speed(10)
    #Floor
    hgt = t.screen.window_height()
    wdt = t.screen.window_width()
    t.up()
    t.goto((wdt * -0.5),(hgt * -0.3))
    t.down()
    t.begin_fill()
    t.fillcolor("brown")
    t.goto((wdt * 0.5),(hgt * -0.3))
    t.goto((wdt * 0.5),(hgt * -0.5))
    t.goto((wdt * -0.5),(hgt * -0.5))
    t.end_fill()
    #Wall
    t.goto((wdt * -0.5),(hgt * -0.3))
    t.begin_fill()
    t.fillcolor((50,50,70))
    t.goto((wdt * -0.5),(hgt * 0.5))
    t.goto((wdt * 0.5),(hgt * 0.5))
    t.goto((wdt * 0.5),(hgt * -0.3))
    t.end_fill()
    #Windows
    drawWindow(t, (wdt * -0.3, 0), 1)
    drawWindow(t, (wdt * 0.3, 0), 1)

def drawWindow(t, coordTuple, scale):
    '''Draws a window with 4 glass panes.'''
    t.up()
    t.goto(coordTuple)
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
    t.speed(0) #DEBUG - MUST CHANGE

    #Setup
    t.width(5)
    t.up()
    t.goto(x,y)
    t.down()

    #Trunk
    t.begin_fill()
    t.fillcolor(102,26,26)
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
    t.width(1)

def drawCentredSquare(t, scale, color):
    '''Draws a square centred at the current position.'''
    t.goto(t.pos() - (50*scale,50*scale))
    t.down()
    t.begin_fill()
    t.fillcolor(color)
    for i in range(4):
        t.fd(100*scale)
        t.lt(90)
    t.end_fill()
    t.up()

def drawPresent(t, coordTuple, box_color, ribbon_color, scale):
    '''Draws a present at the specified position, with the box and a ribbon.'''
    t.up()
    t.speed(0)
    t.goto(coordTuple)
    box = [(30*scale,30*scale), (30*scale,-30*scale), (-30*scale,30*scale), (-30*scale,-30*scale)]
    drawCentredSquare(t, scale, ribbon_color)
    for i in box:
        t.goto(coordTuple)
        t.goto(t.pos() + i)
        drawCentredSquare(t, 0.4*scale, box_color)

    #Ribbon bows
    t.seth(70)
    t.goto(t.pos() + (65*scale,120*scale))
    t.shape("circle")
    bg_color = (50,50,70) #Wall
    if t.ycor() < t.screen.window_height() * -0.3:
        bg_color = "brown" #Floor
    drawRibbon(t, scale, ribbon_color, bg_color)
    t.lt(50)
    t.goto(t.pos() + (-30*scale,-5*scale))
    drawRibbon(t, scale, ribbon_color, bg_color)

def drawRibbon(t, scale, ribbon_color, bg_color):
    '''Draws a ribbon at the turtle's current location and heading.'''
    t.fillcolor(ribbon_color)
    t.turtlesize(1.75*scale,2.75*scale,1)
    t.stamp()
    t.fillcolor(bg_color)
    t.turtlesize(0.875*scale,1.375*scale,1)
    t.stamp()

def drawNStar(t, number, length, color):
    middle = ((length/2) * tan(radians(180/number)))/2 #Finds vertical distance from start to middle
    t.up()
    t.goto(t.pos() + (-length/2,middle))
    t.down()
    t.begin_fill()
    t.fillcolor(color)
    for i in range(number):
        t.fd(length)
        t.rt(180-(180/number))
    t.end_fill()

def drawPattern(t, x, y, number, sides, length, color):
    '''Draws a radial pattern of shapes around the point (x,y)'''
    t.up()
    t.goto(x, y)
    t.setheading(0)
    t.width(1)
    t.pencolor("black")
    t.down()
    t.begin_fill()
    t.fillcolor(color)
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
            color = input("Enter "+str(message)+" color string (r for random, c for custom): ")
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

    if color == repeat:
        color = colorList[random.randint(0,6)]

    return color

def decorate(t):
    '''Allows the user to specify an ornament and place it on the screen.'''
    while True:
        t.up()
        t.speed(0)
        t.goto(0,0)
        
        stop = input("Select a predefined shape with \"p\", stop by typing \"exit\" or press any other key to create a custom shape: ")
        if stop == "exit":
            break
        elif stop == "p":
            while True:
                print("Available predefined shapes: \"present\", \"star\"")
                select = input("Enter name of predefined shape exactly as shown, or type \"back\" to go back: ")

                if select == "back":
                    break

                if select == "present":
                    scale = getInput("scale", "float")
                    box_color = getColorInput(t, "box", None)
                    ribbon_color = getColorInput(t, "ribbon", box_color)
                    t.screen.onscreenclick(t.goto)
                    t.shape("square")
                    t.seth(0)
                    t.turtlesize(5*scale,5*scale,1)
                    t.width(1)
                    t.fillcolor(box_color)
                    stop = input("Move the ornament by clicking on the screen.\nType \"stop\" to remake the ornament or type any other key to confirm position: ")
                    
                    t.screen.onscreenclick(None)
                    t.shape("turtle")
                    t.turtlesize(1,1,1)
                    t.speed(10)
                    
                    drawPresent(t, t.pos(), box_color, ribbon_color, scale)
                    t.shape("turtle")
                    t.turtlesize(1,1,1)
                    break

                if select == "star":
                    length = getInput("width", "integer")
                    points = getInput("points (must be odd)", "integer")
                    color = getColorInput(t, "star", None)

                    t.seth(0)
                    t.shape("circle")
                    t.turtlesize(length/20,length/20,1)
                    t.fillcolor(color)

                    t.screen.onscreenclick(t.goto)
                    stop = input("Move the ornament by clicking on the screen.\nType \"stop\" to remake the ornament or type any other key to confirm position: ")
                    t.screen.onscreenclick(None)
                    t.shape("turtle")
                    t.turtlesize(1,1,1)

                    drawNStar(t, points, length, color)
                    break

                else:
                    print("No shape of that name!")

        else:
            while True:
                sides = getInput("number of sides in each shape", "integer")
                length = getInput("length of sides", "integer")
                number = getInput("number of shapes", "integer")
                color = getColorInput(t, "ornament", None)

                t.screen.onscreenclick(t.goto)
                radius = max(prediction(t, sides, length), 1) #Max function is used as a crash occurs if the turtle stretch factor is too small
                t.shape("circle")
                t.turtlesize((radius/10),(radius/10),1)
                t.fillcolor(color)

                stop = input("Move the ornament by clicking on the screen.\nType \"back\" to remake the ornament or type any other key to confirm position: ")

                t.screen.onscreenclick(None)
                t.shape("turtle")
                t.turtlesize(1,1,1)

                if stop == "back":
                    break
                            
                t.speed(10)
                drawPattern(t, t.xcor(), t.ycor(), number, sides, length, color)
                break
    t.hideturtle()

def main():
    t = Turtle(shape="turtle")
    t.screen.colormode(255)
    #starts from the bottom of the screen with a 5% margin
    start = ((t.screen.window_height() * -0.5) + (t.screen.window_height() * 0.05))
    setupRoom(t)
    drawTree(t, 1, 0, start)
    decorate(t)

    print("Click the screen to exit.")
    t.screen.exitonclick()

main()