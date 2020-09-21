import turtle

def moveTo(x, y):
    turtle.penup()
    turtle.goto(x, y)
    turtle.pendown()

lineCount = 3
boardX = -turtle.window_width() * 0.25
boardY = -turtle.window_height() * 0.25

# 가로선을 그립니다.
for i in range(lineCount):
    moveTo(boardX, boardY + i * 100)
    turtle.forward((lineCount - 1) * 100)

# 세로선을 그립니다.
turtle.setheading(90)
for i in range(lineCount):
    moveTo(boardX + i * 100, boardY)
    turtle.forward((lineCount - 1) * 100)
turtle.setheading(0)

# 과제 요구 사항에는 없었지만 그래도 호출하도록 했습니다.
turtle.exitonclick()