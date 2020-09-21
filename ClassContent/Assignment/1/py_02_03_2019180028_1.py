import turtle

####### funcsions #######
def moveTo(x, y):
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()

def drawIeung(scale = 1.0):
    turtle.circle(50 * scale)

def drawSiot():
    heading = turtle.heading()
    x, y = turtle.pos()

    turtle.right(135)
    turtle.forward(60)
    turtle.setheading(heading)
    moveTo(x, y)

    turtle.right(45)
    turtle.forward(60)
    turtle.setheading(heading)
    moveTo(x, y)

def drawI(scale = 1.0):
    heading = turtle.heading()
    x, y = turtle.pos()

    turtle.setheading(90)
    turtle.forward(100 * scale)

    turtle.setheading(heading)
    moveTo(x, y)

def drawU(scale = 1.0):
    heading = turtle.heading()
    x, y = turtle.pos()

    turtle.forward(100 * scale)
    moveTo(x + 100 * 0.5 * scale, y)
    turtle.setheading(270)

    turtle.forward(50 * scale)
    turtle.setheading(heading)
    moveTo(x, y)

def drawA(scale = 1.0):
    heading = turtle.heading()
    x, y = turtle.pos()

    turtle.forward(50 * scale)
    turtle.setheading(270)
    moveTo(x + 50 * scale, y + 50 * scale)

    turtle.forward(100 * scale)
    turtle.setheading(heading)
    moveTo(x, y)

def DrawNieun(scale = 1.0):
    heading = turtle.heading()
    x, y = turtle.pos()

    turtle.setheading(270)
    turtle.forward(50 * scale)

    turtle.setheading(0)
    turtle.forward(80 * scale)

    turtle.setheading(heading)
    moveTo(x, y)

####### logic #######
x = -200
y = 50

# 이
moveTo(x, y)
drawIeung()
moveTo(x + 70, y)
drawI()

# 수
moveTo(x + 150, y + 100)
drawSiot()
moveTo(x + 100, y + 50)
drawU()

# 원
moveTo(x + 260, y + 55)
drawIeung(0.5)
moveTo(x + 220, y + 50)
drawU(0.8)
moveTo(x + 280, y + 30)
drawA(0.7)
moveTo(x + 250, y + 20)
DrawNieun(0.8)
moveTo(x + 350, y + 50)

turtle.exitonclick()