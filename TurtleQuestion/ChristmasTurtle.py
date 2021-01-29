import random
from turtle import *

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

def drawTree(t, scale, x, y):
    #Calculates the multiplier needed for 1x scale to take up 90% of the screen height. 649 is the true height of the tree.
    t.speed(10)
    scale = scale * ((t.screen.window_height() * 0.9) / 649)

    #DEBUG - gets points
    treeLeaves = []
    #treeLeaves.append(t.pos())

    #Setup
    t.width(5)
    t.up()
    t.goto(x,y)
    t.down()

    #Trunk
    t.begin_fill()
    t.fillcolor(0.4,0.1,0.1)
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
    t.fillcolor(0,0.6,0)
    t.fd(180*scale)
    treeLeaves.append(t.pos())
    t.lt(120)
    t.fd(240*scale)
    treeLeaves.append(t.pos())
    t.rt(120)
    t.fd(80*scale)
    treeLeaves.append(t.pos())
    t.lt(120)
    t.fd(200*scale)
    treeLeaves.append(t.pos())
    t.rt(120)
    t.fd(60*scale)
    treeLeaves.append(t.pos())
    t.lt(120)
    t.fd(240*scale)
    treeLeaves.append(t.pos())
    t.lt(120)
    t.fd(240*scale)
    treeLeaves.append(t.pos())
    t.lt(120)
    t.fd(60*scale)
    treeLeaves.append(t.pos())
    t.rt(120)
    t.fd(200*scale)
    treeLeaves.append(t.pos())
    t.lt(120)
    t.fd(80*scale)
    treeLeaves.append(t.pos())
    t.rt(120)
    t.fd(240*scale)
    treeLeaves.append(t.pos())
    t.lt(120)
    t.fd(220*scale)
    treeLeaves.append(t.pos())
    t.end_fill()
    print(treeLeaves)

def decorate(t):
    while True:
        t.up()
        t.speed(0)
        t.screen.onscreenclick(t.goto)
        stop = input("Click the screen where you want the ornament to be placed and then input any key, or stop by typing \"stop\": ")
        if stop == "stop":
            break
        t.screen.onscreenclick(None)
        t.screen.window_height() # DEBUG - to catch if program closes
        number = getIntInput("number of shapes")
        sides = getIntInput("number of sides in each shape")
        length = getIntInput("length of sides")

        #For random colors - so we don't get ugly looking colors
        colorList = [
        "red", "green", "blue", "yellow", "purple", "cyan", "white"
        ]

        #If you can, try and make this work with tuples
        while True:
            try:
                color = input("Enter color string (r for random): ")
                if color == "r":
                    color = colorList[random.randint(0,6)]
                    break
                else:
                    t.pencolor(color)
                    break

            except:
                print("Please enter a valid color string!")

        t.speed(10)
        drawPattern(t, t.xcor(), t.ycor(), number, sides, length, color)
    t.hideturtle()

def getIntInput(message):
    while True:
        try:
            variable = int(input("Enter "+message+": "))
            break

        except ValueError:
            print("Must be a valid integer!")
    return variable

def main():
    t = Turtle(shape="turtle")
    print(t.screen.screensize())
    print(t.screen.window_height())

    #starts from the bottom of the screen with a 5% margin
    start = ((t.screen.window_height() * -0.5) + (t.screen.window_height() * 0.05))
    drawTree(t, 1, 0, start)
    decorate(t)

    print("Click the screen to exit.")
    t.screen.exitonclick()

main()






#Old Code - makes tree by connecting points. Not sure if it really fits the 'spirit' of using Turtle. If re-implemented, will need to make scalable.
"""
treeLeaves = [
    (225,-300),(90,-60),(180,-60),(70,130),(135,130),(0,365),(-135,130),(-70,130),(-180,-60),(-90,-60),(-225,-300)
    ]

treeTrunk = [
    (20,-240),(-20,-240),(-20,-300),(20,-300)
    ]

connectDots(t, treeLeaves, 5, (0,0,0), (0,0.6,0))
connectDots(t, treeTrunk, 5, (0,0,0), (0.4,0.1,0.1))

def connectDots(t, points, width, pencolor, fillcolor):
    '''Connects points with a line of customisable color and width, connecting the last point with the first. It then fills the enclosed area with a specified color.'''
    t.up()
    t.goto(points[0])
    t.down()
    t.width(width)
    t.pencolor(pencolor)
    t.begin_fill()
    t.fillcolor(fillcolor)

    for i in points:
        t.goto(i)

    t.goto(points[0])
    t.end_fill()
"""