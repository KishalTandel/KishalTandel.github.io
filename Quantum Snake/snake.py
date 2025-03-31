import turtle
import random

# Game Configurations
delay_snake = 100  # Snake moves every 100ms (faster)
delay_food = 300   # Food moves every 300ms (slower)
score = 0
high_score = 0
food_direction = random.choice(["horizontal", "vertical"])  # Initial food direction
food_velocity = 20 if random.choice([True, False]) else -20  # Initial food speed

# Create Game Window
wn = turtle.Screen()
wn.title("Snake Game")
wn.bgcolor("#22222a")
wn.setup(width=600, height=600)
wn.tracer(0)  # Turn off auto-refresh for smooth motion

# Create Snake Head
head = turtle.Turtle()
head.shape("square")
head.color("orange")
head.penup()
head.goto(0, 0)
head.direction = "Stop"

# Create Food
food = turtle.Turtle()
food.shape("circle")
food.shapesize(0.5)
food.color("red")
food.penup()
food.goto(0, 100)

# Create Barriers
barriers = []
def spawn_barriers():
    global barriers
    for barrier in barriers:
        barrier.hideturtle()  # Hide previous barriers instead of adding new ones
    barriers.clear()

    while len(barriers) < 3:
        x, y = random.randint(-270, 270), random.randint(-270, 270)
        
        # Ensure barriers are not too close to the origin or each other
        if abs(x) > 50 and abs(y) > 50 and all(barrier.distance(x, y) > 80 for barrier in barriers):
            barrier = turtle.Turtle()
            barrier.shape("square")
            barrier.shapesize(4)
            barrier.color("#ffffff")
            barrier.penup()
            barrier.goto(x, y)
            barriers.append(barrier)

spawn_barriers()

# Score Display
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 250)
pen.write("Score : 0  High Score : 0", align="center", font=("candara", 24, "bold"))

# Movement Controls
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
        if new_x >= 290 or new_x <= -290:
            food_velocity *= -1  # Reverse direction
        food.setx(food.xcor() + food_velocity)
    else:
        new_y = food.ycor() + food_velocity
        if new_y >= 290 or new_y <= -290:
            food_velocity *= -1  # Reverse direction
        food.sety(food.ycor() + food_velocity)

    wn.update()
    wn.ontimer(move_food, delay_food)

def check_collision():
    """Checks for collisions and resets the game immediately if needed."""
    global score, high_score

    # Collision with window border
    if abs(head.xcor()) > 290 or abs(head.ycor()) > 290:
        reset_game()

    # Collision with barriers
    for barrier in barriers:
        if head.distance(barrier) < 40:
            reset_game()

    # Collision with itself
    for segment in segments:
        if head.distance(segment) < 20:
            reset_game()

def reset_game():
    """Resets the game instantly upon collision."""
    global score, delay_snake, segments

    head.goto(0, 0)
    head.direction = "Stop"

    for segment in segments:
        segment.goto(1000, 1000)  # Move segments off-screen
    segments.clear()

    spawn_barriers()  # Reposition barriers

    score = 0
    pen.clear()
    pen.write(f"Score : {score} High Score : {high_score}", align="center", font=("candara", 24, "bold"))

def eat_food():
    """Handles food eating, increases score, and adds a new segment."""
    global food_direction, food_velocity, score, high_score

    if head.distance(food) < 20:
        x, y = random.randint(-270, 270), random.randint(-270, 270)
        food.goto(x, y)

        # Change Food Direction Randomly
        food_direction = random.choice(["horizontal", "vertical"])
        food_velocity = 20 if random.choice([True, False]) else -20

        # Add a new segment to the snake
        new_segment = turtle.Turtle()
        new_segment.shape("square")
        new_segment.color("white")
        new_segment.penup()
        segments.append(new_segment)

        # Update Score
        score += 10
        high_score = max(high_score, score)
        pen.clear()
        pen.write(f"Score : {score} High Score : {high_score}", align="center", font=("candara", 24, "bold"))

def move_segments():
    """Moves the snake's body segments."""
    for index in range(len(segments) - 1, 0, -1):
        segments[index].goto(segments[index - 1].pos())

    if segments:
        segments[0].goto(head.pos())

    eat_food()
    wn.ontimer(move_segments, delay_snake)

# Key Bindings
wn.listen()
wn.onkeypress(go_up, "w")
wn.onkeypress(go_down, "s")
wn.onkeypress(go_left, "a")
wn.onkeypress(go_right, "d")

segments = []  # Snake body segments

# Start Movement Loops
move()
move_food()
move_segments()

wn.mainloop()
