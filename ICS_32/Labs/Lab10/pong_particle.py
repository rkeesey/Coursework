from graphics import Canvas
from tkinter import Tk
import random

import time
import sys


CANVAS_HEIGHT = 600
CANVAS_WIDTH = 800
BALL_SIZE = 30
PADDLE_WIDTH = 70
PADDLE_HEIGHT = 20
PADDLE_SPEED = 20

DELAY = 0.015
SPEED = 5

game_running = False

def hits_bottom(canvas, r):
    top_y = canvas.get_top_y(r)
    return top_y > CANVAS_HEIGHT - BALL_SIZE
    pass

def hits_right(canvas, r):
    left_x = canvas.get_left_x(r)
    return left_x > CANVAS_WIDTH - BALL_SIZE
    pass

def hits_left(canvas, r):
    left_x = canvas.get_left_x(r)
    # return left_x == 0
    return left_x < SPEED
    pass

def hits_top(canvas, r):
    top_y = canvas.get_top_y(r)
    # return top_y == 0
    return top_y < SPEED
    pass

def check_collision(canvas, obj1, obj2):
    '''
    Checks for collision between 2 objects
    Returns true if the 2 objects overlap
    False otherwise
    '''
    try:
        bbox1 = canvas.bbox(obj1)
        bbox2 = canvas.bbox(obj2)
    except (TypeError, ValueError, AttributeError):
        # If canvas.bbox returns a Mock or invalid result
        return False

    x_overlap = (bbox1[0] < bbox2[2]) and (bbox1[2] > bbox2[0])
    y_overlap = (bbox1[1] < bbox2[3]) and (bbox1[3] > bbox2[1])

    return x_overlap and y_overlap

def move(event, canvas, paddle):
    """Move the paddle based on the key pressed."""
    key = event.keysym
    left_x = canvas.get_left_x(paddle)
    if key == 'Left' and left_x > 0:
        canvas.move(paddle, -PADDLE_SPEED, 0)
    elif key == 'Right' and left_x < CANVAS_WIDTH - PADDLE_WIDTH:
        canvas.move(paddle, PADDLE_SPEED, 0)

def toggle_game(event):
    """Toggle the game state when the spacebar is pressed."""
    global game_running
    game_running = not game_running  # Switch between paused and running

def game_over():
    print("You lose!")
    exit()

def hits_paddle(canvas, velocity, ball, info):
    vx, vy = info[ball]

    info[ball] = (vx, -vy)

    new_vx = vx * (-1 + random.choice([-0.25, 0.25]))
    new_vy = vy * (-1 + random.choice([0, -0.25]))

    bbox = canvas.bbox(ball)

    create_ball(canvas, info, (new_vx,new_vy), start = (bbox[0], bbox[1])
)
    

def create_ball(canvas, info, velocity, start):
    x, y = start
    v_x, v_y = velocity
    
    ball = canvas.create_oval(x, y, x + BALL_SIZE, y + BALL_SIZE, color='black')
    info[ball] = (v_x, v_y)

    return ball



def main():
    global game_running

    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT, 'Move BALL') # Creates window for animation
    canvas.set_canvas_background_color('white')                 # Sets background white

    start_y = CANVAS_HEIGHT / 2 - BALL_SIZE / 2               
    end_y = start_y + BALL_SIZE
    
    og_ball = canvas.create_oval(10, 10, 10 + BALL_SIZE, 10 + BALL_SIZE, color='black')

    info = {og_ball: (1, 1)}

    paddle = canvas.create_rectangle(CANVAS_WIDTH // 2 - PADDLE_WIDTH // 2,
                                     CANVAS_HEIGHT - PADDLE_HEIGHT,
                                     CANVAS_WIDTH // 2 + PADDLE_WIDTH // 2,
                                     CANVAS_HEIGHT, color='black')
    x_speed = y_speed = 1

    def move_paddle(event):
        move(event, canvas, paddle)

    # Bind the arrow keys to the move_paddle callback function

    canvas.bind('<Left>', lambda event: move_paddle(event))
    canvas.bind('<Right>', lambda event: move_paddle(event))

    # A callback is a function passed as an argument to another function
    # Argument is the reference to the function 

    # Bind the spacebar to toggle the game state
    canvas.bind('<space>', lambda event: toggle_game('<space>'))
    
    # Focus on the canvas to capture key events
    canvas.focus_set()
   
    while True:
        if game_running:
            balls_hit_this_frame = set()
    
            for ball, velocity in list(info.items()):
                x_speed, y_speed = velocity

                # update world
                if hits_bottom(canvas,ball):
                    if ball == og_ball:
                        game_over()
                    else:
                        canvas.delete(ball)
                        del info[ball]
                        continue
                if hits_top(canvas,ball):
                    y_speed = abs(y_speed)
                if hits_left(canvas,ball):
                    x_speed = abs(x_speed)
                if hits_right(canvas,ball):
                    x_speed = -abs(x_speed)
                if check_collision(canvas, ball, paddle) and ball not in balls_hit_this_frame:
                    y_speed = -abs(y_speed)
                    hits_paddle(canvas, (x_speed, y_speed), ball, info)
                    balls_hit_this_frame.add(ball)

                info[ball] = (x_speed, y_speed)

                canvas.move(ball, x_speed*SPEED, y_speed*SPEED)    # moves object by the amounts specified for x and y

        canvas.update()
        # pause
        time.sleep(DELAY)

    canvas.mainloop()

if __name__ == "__main__":
    main()