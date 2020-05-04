import turtle
import time
import random

#Screen
window = turtle.Screen()
window.title("Snake Game")
window.bgcolor("#ecf0f1")
window.setup(width=680, height=680)
window.tracer(0)

#Grid
grid = turtle.Turtle()
grid.penup()
grid.goto(-270,-270)
grid.pendown()
def square(side):
    for i in range(4):
        grid.forward(side)
        grid.left(90)

def row(n, side):
    for i in range(n):
        square(side)
        grid.forward(side)
    grid.left(180)
    grid.forward(n * side)
    grid.left(180)

def row_of_rows(m, n, side):
    for i in range(m):
        row(n, side)
        grid.left(90)
        grid.forward(side)
        grid.right(90)
    grid.right(90)
    grid.forward(m * side)
    grid.left(90)

row_of_rows(10,10, 60)
 
#head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.fillcolor("#27ae60")
head.penup()
x = random.randint(-4, 5)*60
y = random.randint(-4, 5)*60
head.shapesize(3)
head.goto(x, y)
head.direction = ""
body = []

# Snake food
food = turtle.Turtle()
food.speed(0)
food.shape("square")
food.fillcolor("#e74c3c")
food.shapesize(3)
food.penup()
x = random.randint(-4, 5)*60
y = random.randint(-4, 5)*60
food.goto(x,y)

# Name
name = turtle.Turtle()
name.speed(0)
name.shape("square")
name.color("black")
name.penup()
name.hideturtle()
name.goto(0,-300)
name.write("- Jovan Karuna Cahyadi -",align="center", font=("Courier", 14, "normal"))

#score
scoreboard = turtle.Turtle()
scoreboard.speed(0)
scoreboard.shape("square")
scoreboard.color("black")
scoreboard.penup()
scoreboard.hideturtle()
scoreboard.goto(220, -300)
scoreboard.write("Score: 0", font=("Courier", 14, "normal"))

def move(direction):
    if (direction == "up"):
        y = head.ycor()
        head.sety(y + 60)
    elif (direction == "down"):
        y = head.ycor()
        head.sety(y - 60)
    elif (direction == "left"):
        x = head.xcor()
        head.setx(x - 60)
    elif(direction == "right"):
        x = head.xcor()
        head.setx(x + 60)

#Return all move to make the snake going to all path
def greedyByLongestPath():
    moveset = []
    move = 0
    x = head.xcor()
    y = head.ycor()
    while(move < 100): # 10x10
        if(x < -180):
            if(y > 270):
                moveset.append("right")
                moveset.append("down")
                y -= 60
                x += 60
                move += 2
            else:
                moveset.append("up")
                y += 60
                move += 1
        elif(x > 270):
            if( y < -180):
                moveset.append("left")
                x -= 60
                move += 1
            else:
                moveset.append("down")
                y -= 60
                move += 1
        elif(y < -180):
            moveset.append("left")
            x -= 60
            move += 1
        else:
            if((x/60) % 2 == 0):
                if(y > 270):
                    moveset.append("right")
                    moveset.append("down")
                    y -= 60
                    x += 60
                    move += 2
                else:
                    moveset.append("up")
                    y += 60
                    move += 1
            else:
                if(y < -150):
                    moveset.append("right")
                    moveset.append("up")
                    y += 60
                    x += 60
                    move += 2
                else:
                    moveset.append("down")
                    y -= 60
                    move += 1
    return moveset


moveset = greedyByLongestPath()
delay = 0.05
score = 0
path = 0

while(True):

    window.update()
    #Going out of arena
    if (head.xcor() > 310 or head.xcor() < -250 or head.ycor() > 310 or head.ycor() <-250):
        print("lose")
        window.exitonclick()

    # Check for a collision with the food
    if head.distance(food) < 20:
        # Move the food to a random spot that is not occupied by snake
        while(True):
            check = True
            x_food = random.randint(-4, 5)*60
            y_food = random.randint(-4, 5)*60
            if(x_food == head.xcor() and y_food ==head.ycor()):
                continue
            else:
                for index in range(len(body)-1, 0, -1):
                    x_body = body[index-1].xcor()
                    y_body = body[index-1].ycor()
                    if(x_food == x_body and y_food == y_body):
                        check = False
                        break
                if(check == True):
                    break

        food.goto(x_food,y_food)

        # Add a body
        new_body = turtle.Turtle()
        new_body.speed(0)
        new_body.shape("square")
        new_body.fillcolor("#2ecc71")
        new_body.shapesize(3)
        new_body.penup()
        body.append(new_body)

        # Shorten the delay
        delay -= 0.00002

        # Increase the score
        score += 10

        scoreboard.clear()
        scoreboard.write("Score: {}".format(score), align="center", font=("Courier", 14, "normal")) 

    # Move the end segments first in reverse order
    for index in range(len(body)-1, 0, -1):
        x = body[index-1].xcor()
        y = body[index-1].ycor()
        body[index].goto(x, y)

    # Move segment 0 to where the head is
    if len(body) > 0:
        x = head.xcor()
        y = head.ycor()
        body[0].goto(x,y)

    if(score == 1000):
        print("win")
        win = turtle.Turtle()
        win.speed(0)
        win.shape("square")
        win.color("white")
        win.penup()
        win.hideturtle()
        win.goto(0, 0)
        win.write("You Win",align='center', font=("Courier", 50, "normal"))
        window.exitonclick()

    move(moveset[path])

    path += 1
    if(path == 100): #Use the first move in moveset
        path = 0

    time.sleep(delay)

window.mainloop()