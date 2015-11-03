# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0, 0]
paddle1_pos = [PAD_WIDTH - 4, PAD_HEIGHT - 40] # LH; x, y
paddle2_pos = [WIDTH - 4, PAD_HEIGHT - 40] # RH; x, y
paddle1_vel = [0, 0]
paddle2_vel = [0, 0]
time = 0
init_pos = (WIDTH / 2, HEIGHT / 2)
DIRECTION = (LEFT, RIGHT)
score1 = 0
score2 = 0


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel, init_pos, DIRECTION # these are vectors stored as lists
    ball_pos = list(init_pos)
    #ball_vel = [2, 2] [h, v]
    time = 0

    if direction == RIGHT:
        ball_vel = [random.randrange(1, 2), random.randrange(1, 3)]
    if direction == LEFT:
        ball_vel = [random.randrange(-2, -1), random.randrange(1, 3)]


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, DIRECTION  # these are numbers
    global score1, score2  # these are ints
    direction = random.choice(DIRECTION)
    score1 = 0
    score2 = 0
    spawn_ball(direction)
    timer.start()

def restart ():
    global ball_pos, score1, score2
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    new_game()
    score1 = 0
    score2 = 0

def tick():
    global time, ball_pos, ball_vel
    time += 1

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, time
    global LEFT, RIGHT, paddle1_vel, paddle2_vel, HALF_PAD_WIDTH

    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # collide and reflect off of top of canvas
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    # collide and reflect off of bottom of canvas
    if ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]

    # restart in middle after ball hits gutter
    # LH side
    if ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        if ball_pos[1] <= paddle1_pos[1] + HALF_PAD_HEIGHT and ball_pos[1] >= paddle1_pos[1] - HALF_PAD_HEIGHT:
            ball_vel[0] = - ball_vel[0] * 1.1
        else:
            spawn_ball(RIGHT)
            score2 += 1
    # RH side
    if ball_pos[0] >= (WIDTH - PAD_WIDTH) - BALL_RADIUS:
        if ball_pos[1] <= paddle2_pos[1] + HALF_PAD_HEIGHT and ball_pos[1] >= paddle2_pos[1] - HALF_PAD_HEIGHT:
            ball_vel[0] = - ball_vel[0] * 1.1
        else:
            spawn_ball(LEFT)
            score1 += 1

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")

    # update paddle's vertical position, keep paddle on the screen
    # LH
    if paddle1_pos[1] > HEIGHT - HALF_PAD_HEIGHT and paddle1_vel[1] > 0:
        pass
    elif paddle1_pos[1] < 0 + HALF_PAD_HEIGHT and paddle1_vel[1] < 0:
        pass
    else:
         paddle1_pos[1] += paddle1_vel[1]
    # RH
    if paddle2_pos[1] > HEIGHT - HALF_PAD_HEIGHT and paddle2_vel[1] > 0:
        pass
    elif paddle2_pos[1] < 0 + HALF_PAD_HEIGHT and paddle2_vel[1] < 0:
        pass
    else:
         paddle2_pos[1] += paddle2_vel[1]

    # draw paddles
    # LH paddle
    canvas.draw_line([paddle1_pos[0], paddle1_pos[1] - HALF_PAD_HEIGHT], [paddle1_pos[0], paddle1_pos[1] + HALF_PAD_HEIGHT], PAD_WIDTH, "white")
    # RH paddle
    canvas.draw_line([paddle2_pos[0], paddle2_pos[1] - HALF_PAD_HEIGHT], [paddle2_pos[0], paddle2_pos[1] + HALF_PAD_HEIGHT], PAD_WIDTH, "white")

    # determine whether paddle and ball collide


    # draw scores
    canvas.draw_text(str(score1), (50, 25), 32, 'aqua')
    canvas.draw_text(str(score2), (470, 25), 32, 'aqua')

def keydown(key):
    global paddle1_vel, paddle2_vel
    # LH
    if key == simplegui.KEY_MAP["down"]:
        paddle1_vel = [0, 4]
    elif key == simplegui.KEY_MAP["up"]:
        paddle1_vel = [0, -4]
    # RH
    if key == simplegui.KEY_MAP["s"]:
        paddle2_vel = [0, 4]
    elif key == simplegui.KEY_MAP["w"]:
        paddle2_vel = [0, -4]

def keyup(key):
    global paddle1_vel, paddle2_vel
    # LH
    if key == simplegui.KEY_MAP["down"]:
        paddle1_vel = [0, 0]
    elif key == simplegui.KEY_MAP["up"]:
        paddle1_vel = [0, 0]
    # RH
    if key == simplegui.KEY_MAP["s"]:
        paddle2_vel = [0, 0]
    elif key == simplegui.KEY_MAP["w"]:
        paddle2_vel = [0, 0]

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
timer = simplegui.create_timer(1000, tick)

button1 = frame.add_button("New Game", new_game)
button2 = frame.add_button("Restart", restart)

# start frame
frame.start()