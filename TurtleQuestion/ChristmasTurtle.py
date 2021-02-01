import random
from turtle import *

sides, length, number = 0, 0, 0

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

def drawTree(t, scale, x, y):
    #Calculates the multiplier needed for 1x scale to take up 90% of the screen height. 649 is the true height of the tree.
    scale = scale * ((t.screen.window_height() * 0.9) / 649)
    t.speed(10)

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

def decorate(t, y):

    #For random colors - so we don't get ugly looking colors
    colorList = [
        "red", "green", "blue", "yellow", "purple", "cyan", "white"
        ]

    while True:
        t.up()
        t.speed(0)
        t.goto(0,0)
        y.goto(0,0)
        
        # Will be used for predefined shapes
        stop = input("Select a predefined shape with \"p\", stop by typing \"exit\" or press any other key to create a custom shape: ")
        if stop == "exit":
            break
        elif stop == "p":
            #Add later
            print("Predefined shapes not yet supported! Enter a custom shape.")

        while True:
            sides = getIntInput("number of sides in each shape")
            length = getIntInput("length of sides")
            number = getIntInput("number of shapes")

            while True:
                try:
                    color = input("Enter color string (r for random, c for custom): ")
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
    y = Turtle()
    y.hideturtle()
    y.up()
    t.screen.colormode(255)

    #starts from the bottom of the screen with a 5% margin
    start = ((t.screen.window_height() * -0.5) + (t.screen.window_height() * 0.05))
    drawTree(t, 1, 0, start)
    decorate(t, y)

    print("Click the screen to exit.")
    t.screen.exitonclick()

main()