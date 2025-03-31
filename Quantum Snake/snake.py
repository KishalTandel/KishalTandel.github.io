import turtle
import random

delay_snake = 100 #Snake moves every 100ms 
delay_food = 300   #Food moves every 300ms 
score = 0
high_score = 0
food_direction = random.choice(["horizontal", "vertical"])  #Initial food direction
food_velocity = 20 if random.choice([True, False]) else -20  #Initial food velocity

#Creating Game Window
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("#22222a")
wn.setup(width=600, height=600)
wn.tracer(0)  #For turning off auto-refresh for smooth motion

# Creating Snake Head
head = turtle.Turtle()
head.shape("square")
head.color("#FF9800")
head.penup()
head.goto(0, 0)
head.direction = "none"

# Creating Food
food = turtle.Turtle()
food.shape("circle")
food.shapesize(0.5)
food.color("#F01111")
food.penup()
food.goto(0, 100)

# Creating Potential Barriers
barriers = []
def spawn_barriers():
    global barriers
    for barrier in barriers:
        barrier.hideturtle() 
    barriers.clear()

    while len(barriers) < 4:
        x, y = random.randint(-270, 270), random.randint(-270, 200)
        
        #For ensuring barriers are not too close to the origin or each other
        if abs(x) > 50 and abs(y) > 50 and all(barrier.distance(x, y) > 100 for barrier in barriers):
            barrier = turtle.Turtle()
            barrier.shape("square")
            barrier.shapesize(4)
            barrier.color("#03A9B0")
            barrier.penup()
            barrier.goto(x, y)
            barriers.append(barrier)

spawn_barriers()

#Score Display
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 250)
pen.write("Score : 0  Highest Score : 0", align="center", font=("Roboto Condensed", 24, "bold"))

#Movement Controls
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    """Moves the snake in the current direction."""
    if head.direction == "up":
        head.sety(head.ycor() + 20)
    elif head.direction == "down":
        head.sety(head.ycor() - 20)
    elif head.direction == "left":
        head.setx(head.xcor() - 20)
    elif head.direction == "right":
        head.setx(head.xcor() + 20)
    
    check_collision()
    wn.update()
    wn.ontimer(move, delay_snake)

def move_food():
    """Moves the food in an oscillating manner, slower than the snake."""
    global food_velocity, food_direction

    if food_direction == "horizontal":
        new_x = food.xcor() + food_velocity
        if new_x >= 290 or new_x <= -290 or any(food.distance(segment)<20 for segment in segments):
            food_velocity *= -1  #Reverse direction
        food.setx(food.xcor() + food_velocity)
    else:
        new_y = food.ycor() + food_velocity
        if new_y >= 250 or new_y <= -290 or any(food.distance(segment)<20 for segment in segments):
            food_velocity *= -1  #Reverse direction
        food.sety(food.ycor() + food_velocity)

    for barrier in barriers:
        if food.distance(barrier)<60:
            if random.choice(['Reflect','Transmit'])=='Reflect':
                food_velocity*=-1

    wn.update()
    wn.ontimer(move_food, delay_food)

def check_collision():
    """Checks for collisions and resets the game immediately if needed."""
    global score, high_score

    #Collision with window border
    if abs(head.xcor()) > 290 or abs(head.ycor()) > 290:
        reset_game()

    #Collision with barriers
    for barrier in barriers:
        if head.distance(barrier) < 40:
            reset_game()

    #Collision with itself
    for segment in segments:
        if head.distance(segment) < 20:
            reset_game()

def reset_game():
    """Resets the game instantly upon collision."""
    global score, delay_snake, segments

    head.goto(0, 0)
    head.direction = "none"
    food.goto(0, 100)

    for segment in segments:
        segment.goto(1000, 1000)  #Move segments off-screen
    segments.clear()

    spawn_barriers()  #Reposition barriers

    score = 0
    pen.clear()
    pen.write(f"Score : {score} Highest Score : {high_score}", align="center", font=("Roboto Condensed", 24, "bold"))

def eat_food():
    """Handles food eating, increases score, and adds a new segment."""
    global food_direction, food_velocity, score, high_score

    if head.distance(food) < 20:
        x, y = random.randint(-270, 270), random.randint(-270, 270)
        food.goto(x, y)

        #Change Food Direction Randomly
        food_direction = random.choice(["horizontal", "vertical"])
        food_velocity = 20 if random.choice([True, False]) else -20

        #Add a new segment to the snake
        new_segment = turtle.Turtle()
        new_segment.shape("square")
        new_segment.color("#DDDDD5")
        new_segment.penup()
        new_segment.hideturtle()
        segments.append(new_segment)

        #Updating Score
        score += 10
        high_score = max(high_score, score)
        pen.clear()
        pen.write(f"Score : {score} Highest Score : {high_score}", align="center", font=("Roboto Condensed", 24, "bold"))

def move_segments():
    """Moves the snake's body segments."""
    for index in range(len(segments) - 1, 0, -1):
        segments[index].goto(segments[index - 1].pos())
        segments[index].showturtle()

    if segments:
        segments[0].goto(head.pos())
        segments[0].showturtle()

    eat_food()
    wn.ontimer(move_segments, delay_snake)


wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")

segments = []  #Snake body segments

#Start Movement Loops
move()
move_food()
move_segments()
wn.mainloop()