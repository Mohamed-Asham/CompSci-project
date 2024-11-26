import turtle

# Global variable to store the selected mood
selected_mood = None


def on_click(x, y):
    global selected_mood
    # Define the x positions for each mood
    x_positions = [-200, -100, 0, 100, 200]
    moods = ["Very Happy", "Happy", "Neutral", "Sad", "Angry"]

    # Check which mood was clicked based on x position
    for i, pos in enumerate(x_positions):
        if pos - 30 < x < pos + 30 and 20 < y < 80:  # Check if click is inside the circle
            selected_mood = moods[i]
            print(f"You selected: {selected_mood}")  # Print selected mood to the console
            return


def draw_mood_tracker():
    screen = turtle.Screen()
    screen.title("Interactive Mood Tracker")
    screen.setup(width=800, height=400)

    # Turtle setup
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)

    # Draw title
    pen.penup()
    pen.goto(0, 150)
    pen.write("Mood Tracker", align="center", font=("Arial", 24, "bold"))

    # Draw moods
    moods = ["Very Happy", "Happy", "Neutral", "Sad", "Angry"]
    colors = ["green", "lightgreen", "yellow", "orange", "red"]
    x_positions = [-200, -100, 0, 100, 200]

    for i, (mood, color, x) in enumerate(zip(moods, colors, x_positions)):
        # Draw circles for moods
        pen.goto(x, 50)
        pen.fillcolor(color)
        pen.begin_fill()
        pen.circle(30)
        pen.end_fill()
        pen.penup()

        # Write mood label inside the circle
        pen.goto(x, 50)
        pen.write(mood, align="center", font=("Arial", 10, "normal"))

    # Add description
    pen.goto(0, -150)
    pen.write("Click on a mood to select it!", align="center", font=("Arial", 12, "italic"))

    # Set up click detection
    screen.onclick(on_click)

    # Keep the window open
    screen.mainloop()


# Call the function
draw_mood_tracker()
