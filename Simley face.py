import turtle

selected_mood = None

def on_click(x, y):
    global selected_mood
    # Define the x positions for each mood
    x_positions = [-200, -100, 0, 100, 200]
    moods = ["Very Happy", "Happy", "Neutral", "Sad", "Angry"]

    # Check which mood was clicked based on x position
    for i, pos in enumerate(x_positions):
        if pos - 32 < x < pos + 32 and -20 < y < 65:  # Check if click is inside the circle
            selected_mood = moods[i]
            print(f"You selected: {selected_mood}")  # Print selected mood to the console
            return

def draw_smiley(pen, x, y, mood):
    """Draws a face inside the circle based on the mood."""
    # Eyes
    pen.penup()
    pen.goto(x - 10, y + 35)  # Left eye
    pen.dot(5, "black")  # Draw a small dot for the eye
    pen.goto(x + 10, y + 35)  # Right eye
    pen.dot(5, "black")  # Draw a small dot for the eye

    # Mouth
    pen.penup()
    pen.goto(x - 9, y + 17)  # Starting point for the mouth
    pen.pendown()
    pen.width(2)

    if mood == "Very Happy" or mood == "Happy":
        pen.setheading(-60)  # Start angle for a smile
        pen.circle(10, 120)  # Draw an upward arc for the smi
    elif mood == "Neutral":
        pen.setheading(0)  # Straight line for neutral mouth
        pen.forward(20)
    elif mood == "Sad" or mood == "Angry":
        pen.setheading(240)  # Start angle for a frown
        pen.circle(10, -120)  # Draw a downward arc for the frown

    # Reset orientation to ensure the circle shape isn't distorted
    pen.penup()
    pen.setheading(0)


def draw_mood_tracker():
    screen = turtle.Screen()
    screen.title("Interactive Mood Tracker")
    screen.setup(width=600, height=300)

    # Turtle setup
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)

    # Draw title
    pen.penup()
    pen.goto(0, 100)
    pen.write("Mood Tracker", align="center", font=("Arial", 24, "bold"))

    # Draw moods
    moods = ["Very Happy", "Happy", "Neutral", "Sad", "Angry"]
    colors = ["green", "lightgreen", "yellow", "orange", "red"]
    x_positions = [-200, -100, 0, 100, 200]

    for i, (mood, color, x) in enumerate(zip(moods, colors, x_positions)):
        # Draw circles for moods
        pen.goto(x, 0)
        pen.fillcolor(color)
        pen.begin_fill()
        pen.circle(30)
        pen.end_fill()
        pen.penup()

        draw_smiley(pen, x, 0, mood)

        # Write mood label inside the circle
        pen.goto(x, -20)
        pen.write(mood, align="center", font=("Arial", 10, "normal"))

    # Add description
    pen.goto(0, -70)
    pen.write("Click on a mood to select it!", align="center", font=("Arial", 12, "italic"))

    # Set up click detection
    screen.onclick(on_click)

    # Keep the window open
    screen.mainloop()


# Call the function
draw_mood_tracker()
