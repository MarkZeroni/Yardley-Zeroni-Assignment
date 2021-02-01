import random
from turtle import *

def setupRoom(t):
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
    t.up()
    t.goto(coordTuple)
    glass = [(22.5*scale,22.5*scale), (22.5*scale,-22.5*scale), (-22.5*scale,22.5*scale), (-22.5*scale,-22.5*scale)]
    drawCentredSquare(t, scale, "brown")
    for i in glass:
        t.goto(coordTuple)
        t.goto(t.pos() + i)
        drawCentredSquare(t, 0.35*scale, "cyan")

def drawTree(t, scale, x, y):
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

def drawCentredSquare(t, scale, color):
    t.goto(t.pos() - (50*scale,50*scale))
    t.down()
    t.begin_fill()
    t.fillcolor(color)
    for i in range(4):
        t.fd(100*scale)
        t.lt(90)
    t.end_fill()
    t.up()

def drawPresent(t, y, coordTuple, scale):
    t.up()
    t.goto(coordTuple)
    box = [
        (30*scale,30*scale), (30*scale,-30*scale), (-30*scale,30*scale), (-30*scale,-30*scale)
        ]
    drawCentredSquare(t, scale, "red")
    for i in box:
        t.goto(coordTuple)
        t.goto(t.pos() + i)
        drawCentredSquare(t, 0.4*scale, "cyan")
    
    #Ribbon bows
    t.seth(0)
    t.shape("circle")
    t.fillcolor("red")
    t.turtlesize(2.75*scale,1.75*scale,1)
    t.up()
    t.goto(t.pos() + (15*scale,70*scale))
    t.rt(20)
    t.stamp()
    t.fillcolor("white")
    t.turtlesize(1.375*scale,0.875*scale,1)
    t.stamp()
    t.lt(50)
    t.goto(y.pos() + (-35*scale,-0*scale))
    t.fillcolor("red")
    t.turtlesize(2.75*scale,1.75*scale,1)
    t.stamp()
    t.fillcolor("white")
    t.turtlesize(1.375*scale,0.875*scale,1)
    t.stamp()

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
    t.speed(0)
    for i in range(sides // 2):
        t.fd(length)
        t.lt(360 / sides)
    radius = t.distance(pos_a)
    return radius

def getIntInput(message):
    while True:
        try:
            variable = int(input("Enter "+message+": "))
            break

        except ValueError:
            print("Must be a valid integer!")
    return variable

def getColorInput(t, message):
    #For random colors - so we don't get ugly looking colors
    colorList = [
        "red", "green", "blue", "yellow", "purple", "cyan", "white"
        ]
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
                t.pencolor(color) #Tests if color is valid
                break

        except:
            print("Please enter a valid color string!")

    return color

def decorate(t, y):
    while True:
        t.up()
        t.speed(0)
        t.goto(0,0)
        y.goto(0,0)
        
        stop = input("Select a predefined shape with \"p\", stop by typing \"exit\" or press any other key to create a custom shape: ")
        if stop == "exit":
            break
        elif stop == "p":
            while True:
                print("Available predefined shapes: \"present\"")
                select = input("Enter name of predefined shape exactly as shown, or type \"stop\" to exit: ")

                if select == "stop":
                    break

                if select == "present":
                    scale = getIntInput("scale")
                    box_color = getColorInput(t, "box")
                    ribbon_color = getColorInput(t, "ribbon")
                    t.screen.onscreenclick(t.goto)
                    t.shape("square")
                    t.turtlesize(scale,scale,1)
                    t.fillcolor(box_color)
                    stop = input("Move the ornament by clicking on the screen.\nType \"stop\" to remake the ornament or type any other key to confirm position: ")
                    
                    t.screen.onscreenclick(None)
                    t.shape("turtle")
                    t.turtlesize(1,1,1)
                    t.speed(10)

                    drawPresent(t, y, t.pos(), scale)




                else:
                    print("No shape of that name!")

        else:
            while True:
                sides = getIntInput("number of sides in each shape")
                length = getIntInput("length of sides")
                number = getIntInput("number of shapes")
                color = getColorInput(t, "ornament")

                t.screen.onscreenclick(t.goto)
                radius = max(prediction(y, sides, length), 1) #Max function is used as a crash occurs if the turtle stretch factor is too small
                t.shape("circle")
                t.turtlesize((radius/10),(radius/10),1)
                t.fillcolor(color)

                stop = input("Move the ornament by clicking on the screen.\nType \"stop\" to remake the ornament or type any other key to confirm position: ")

                t.screen.onscreenclick(None)
                t.shape("turtle")
                t.turtlesize(1,1,1)

                if stop == "stop":
                    break
                            
                t.speed(10)
                drawPattern(t, t.xcor(), t.ycor(), number, sides, length, color)
                break
    t.hideturtle()

def main():
    t = Turtle(shape="turtle")
    y = Turtle()
    y.hideturtle()
    y.up()
    t.screen.colormode(255)

    #delay = input("Adjust screen size and then press enter: ") # DEBUG

    #starts from the bottom of the screen with a 5% margin
    start = ((t.screen.window_height() * -0.5) + (t.screen.window_height() * 0.05))
    setupRoom(t)
    drawTree(t, 1, 0, start)
    decorate(t, y)

    print("Click the screen to exit.")
    t.screen.exitonclick()

main()



'''
y.showturtle()
    y.shape("circle")
    y.fillcolor("red")
    y.turtlesize(2.75*scale,1.75*scale,1)
    y.up()
    y.goto(t.pos() + (15*scale,70*scale))
    y.rt(20)
    y.stamp()
    y.fillcolor("white")
    y.turtlesize(1.375*scale,0.875*scale,1)
    y.stamp()
    y.lt(50)
    y.goto(y.pos() + (-35*scale,-0*scale))
    y.fillcolor("red")
    y.turtlesize(2.75*scale,1.75*scale,1)
    y.stamp()
    y.fillcolor("white")
    y.turtlesize(1.375*scale,0.875*scale,1)
    y.stamp()

'''