import turtle
import random
import time
import tkinter as tk
from tkinter import messagebox


FRAME_RATE = 30
TIME_FOR_1_FRAME = 1 / FRAME_RATE
CANNON_STEP = 10
LASER_LENGTH = 10
LASER_SPEED = 20
ALIEN_SPAWN_INTERVAL = 1.2
ALIEN_SPEED = 3.5


game_running = False
alien_timer = 0
game_timer = 0
score = 0


window = turtle.Screen()
window.tracer(0)
window.setup(0.5, 0.75)
window.bgcolor(0.2, 0.2, 0.2)
window.title("Tank Wars")

left = -window.window_width() / 2
right = window.window_width() / 2
top = window.window_height() / 2
bottom = -window.window_height() / 2
Floor_Level = 0.9 * bottom
GUTTER = 0.025 * window.window_width()


cannon = turtle.Turtle()
cannon.penup()
cannon.color(1, 1, 1)
cannon.shape("square")
cannon.setposition(0, Floor_Level)
cannon.cannon_movement = 0


text = turtle.Turtle()
text.penup()
text.hideturtle()
text.setposition(left * 0.8, top * 0.8)
text.color(1, 1, 1)

lasers = []
aliens = []

def draw_cannon():
    cannon.clear()
    cannon.turtlesize(1, 4)
    cannon.stamp()
    cannon.sety(Floor_Level + 10)
    cannon.turtlesize(1, 1.5)
    cannon.stamp()
    cannon.sety(Floor_Level + 20)
    cannon.turtlesize(0.8, 0.3)
    cannon.stamp()
    cannon.sety(Floor_Level)
    window.update()

def move_left():
    cannon.cannon_movement = -1

def move_right():
    cannon.cannon_movement = 1

def stop_cannon_movement():
    cannon.cannon_movement = 0

def create_laser():
    laser = turtle.Turtle()
    laser.penup()
    laser.color(1, 0, 0)
    laser.hideturtle()
    laser.setposition(cannon.xcor(), cannon.ycor())
    laser.setheading(90)
    laser.forward(20)
    laser.pendown()
    laser.pensize(5)
    lasers.append(laser)

def move_laser(laser):
    laser.clear()
    laser.forward(LASER_SPEED)
    laser.forward(LASER_LENGTH)
    laser.forward(-LASER_LENGTH)

def create_alien():
    alien = turtle.Turtle()
    alien.penup()
    alien.turtlesize(1.5)
    alien.setposition(
        random.randint(int(left + GUTTER), int(right - GUTTER)),
        top,
    )
    alien.shape("turtle")
    alien.setheading(-90)
    alien.color(random.random(), random.random(), random.random())
    aliens.append(alien)

def remove_sprite(sprite, sprite_list):
    sprite.clear()
    sprite.hideturtle()
    window.update()
    sprite_list.remove(sprite)
    turtle.turtles().remove(sprite)

def restart_game():
    global aliens, lasers, alien_timer, game_timer, score, game_running

    for laser in lasers:
        remove_sprite(laser, lasers)
    for alien in aliens:
        remove_sprite(alien, aliens)

    cannon.setposition(0, Floor_Level)
    cannon.cannon_movement = 0

    alien_timer = 0
    game_timer = time.time()
    score = 0
    game_running = True

    window.listen()
    game_loop(score_label)

def game_loop(score_label):
    global alien_timer, game_timer, score, game_running

    while game_running:
        timer_this_frame = time.time()

        time_elapsed = time.time() - game_timer
        text.clear()
        text.write(
            f"Time: {time_elapsed:5.1f}s\nScore: {score:5}",
            font=("Courier", 20, "bold"),
        )
        score_label.config(text=f"Score: {score}")

        new_x = cannon.xcor() + CANNON_STEP * cannon.cannon_movement
        if left + GUTTER <= new_x <= right - GUTTER:
            cannon.setx(new_x)
            draw_cannon()

        for laser in lasers.copy():
            move_laser(laser)
            if laser.ycor() > top:
                remove_sprite(laser, lasers)
                break
            for alien in aliens.copy():
                if laser.distance(alien) < 20:
                    remove_sprite(laser, lasers)
                    remove_sprite(alien, aliens)
                    score += 1
                    break

        if time.time() - alien_timer > ALIEN_SPAWN_INTERVAL:
            create_alien()
            alien_timer = time.time()

        for alien in aliens:
            alien.forward(ALIEN_SPEED)
            if alien.ycor() < Floor_Level:
                game_running = False
                break

        time_for_this_frame = time.time() - timer_this_frame
        if time_for_this_frame < TIME_FOR_1_FRAME:
            time.sleep(TIME_FOR_1_FRAME - time_for_this_frame)
        window.update()

    splash_text = turtle.Turtle()
    splash_text.hideturtle()
    splash_text.color(1, 1, 1)
    window.onkeypress(restart_game, "r")
    window.listen()

def setup_tkinter():
    root = tk.Tk()
    root.title("Tank Wars Control Panel")
    root.geometry("300x200")  

    start_button = tk.Button(root, text="Start Game", command=start_game)
    start_button.pack(pady=10)

    quit_button = tk.Button(root, text="Quit Game", command=quit_game)
    quit_button.pack(pady=10)

    score_label = tk.Label(root, text="Score: 0")
    score_label.pack(pady=10)

    return root, score_label

def start_game():
    global game_running
    if not game_running:
        game_running = True
        restart_game()

def quit_game():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        window.bye()
        root.quit()

if __name__ == "__main__":
    root, score_label = setup_tkinter()

    window.onkeypress(move_left, "Left")
    window.onkeypress(move_right, "Right")
    window.onkeyrelease(stop_cannon_movement, "Left")
    window.onkeyrelease(stop_cannon_movement, "Right")
    window.onkeypress(create_laser, "space")
    window.listen()

   
    root.mainloop()