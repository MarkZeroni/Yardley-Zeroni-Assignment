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

def predictiveCircle(t, sides, length):
    '''Draws a circle that shows the maximum extent of the currently configured shape.'''
    pos_a = t.pos()
    t.speed(0)
    for i in range(sides // 2):
        t.fd(length)
        t.lt(360 / sides)
    radius = t.distance(pos_a)
    t.goto(pos_a + (0, -radius))
    t.seth(0)
    t.down()
    t.circle(radius)
    t.up()
    t.goto(pos_a)

def drawTree(t, scale, x, y):
    #Calculates the multiplier needed for 1x scale to take up 90% of the screen height. 649 is the true height of the tree.
    t.speed(10)
    scale = scale * ((t.screen.window_height() * 0.9) / 649)

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
    while True:
        t.up()
        t.speed(0)
        t.screen.onscreenclick(t.goto)
        stop = input("Click the screen where you want the ornament to be placed and then input any key, or stop by typing \"stop\": ")
        if stop == "stop":
            break
        t.screen.onscreenclick(None)
        y.goto(t.pos())
        
        sides = getIntInput("number of sides in each shape")
        length = getIntInput("length of sides")

        predictiveCircle(y, sides, length)

        number = getIntInput("number of shapes")

        #For random colors - so we don't get ugly looking colors
        colorList = [
        "red", "green", "blue", "yellow", "purple", "cyan", "white"
        ]

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
                    t.pencolor(color)
                    break

            except:
                print("Please enter a valid color string!")

        t.speed(10)
        y.clear()
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