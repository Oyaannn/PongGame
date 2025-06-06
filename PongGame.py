from tkinter import *
import random

# Ukuran layar
WIDTH = 900
HEIGHT = 400

# Raket & bola
PAD_W = 10
PAD_H = 100
BALL_RADIUS = 30

# Pengaturan bola
INITIAL_SPEED = 8
BALL_SPEED_UP = 1.05
BALL_MAX_SPEED = 30
BALL_X_SPEED = INITIAL_SPEED
BALL_Y_SPEED = INITIAL_SPEED

# Skor dan batas kemenangan
PLAYER_1_SCORE = 0
PLAYER_2_SCORE = 0
WIN_SCORE = 5

right_line_distance = WIDTH - PAD_W
game_running = False  # status game
# Mode Single Player
mode_single_player = True
PLAYER_MOVE_SPEED = 20
AI_MOVE_SPEED = 4


# Inisialisasi Tkinter
root = Tk()
root.title("Pong Game")

c = Canvas(root, width=WIDTH, height=HEIGHT, bg="#1e1e1e")
c.pack()

# Garis lapangan
c.create_line(PAD_W, 0, PAD_W, HEIGHT, fill="white")
c.create_line(WIDTH - PAD_W, 0, WIDTH - PAD_W, HEIGHT, fill="white")
c.create_line(WIDTH / 2, 0, WIDTH / 2, HEIGHT, fill="white")

# Bola & Raket
BALL = c.create_oval(WIDTH / 2 - BALL_RADIUS / 2, HEIGHT / 2 - BALL_RADIUS / 2,
                     WIDTH / 2 + BALL_RADIUS / 2, HEIGHT / 2 + BALL_RADIUS / 2, fill="white", outline="#ccc")
LEFT_PAD = c.create_line(PAD_W / 2, 0, PAD_W / 2, PAD_H, fill="#00ffcc", width=PAD_W)
RIGHT_PAD = c.create_line(WIDTH - PAD_W / 2, 0, WIDTH - PAD_W / 2, PAD_H, fill="#00ffcc", width=PAD_W)

# Skor
p_1_text = c.create_text(WIDTH - WIDTH / 6, PAD_H / 4, text=PLAYER_1_SCORE, fill="white", font=("Arial", 20))
p_2_text = c.create_text(WIDTH / 6, PAD_H / 4, text=PLAYER_2_SCORE, fill="white", font=("Arial", 20))

# Tombol Start
start_button = start_button = Button(root, text="▶ Start Game", font=("Helvetica", 16, "bold"),
                      bg="#00b894", fg="white", activebackground="#55efc4", relief="flat", cursor="hand2", command=lambda: start_game())
start_button.pack(pady=10)

def move_paddle(event):
    if not game_running or not mode_single_player:
        return
    key = event.keysym
    if key == "w":
        c.move(LEFT_PAD, 0, -PLAYER_MOVE_SPEED)
    elif key == "s":
        c.move(LEFT_PAD, 0, PLAYER_MOVE_SPEED)

root.bind("<w>", move_paddle)
root.bind("<s>", move_paddle)


def reset_positions():
    # Reset posisi bola & paddle
    c.coords(BALL, WIDTH / 2 - BALL_RADIUS / 2, HEIGHT / 2 - BALL_RADIUS / 2,
             WIDTH / 2 + BALL_RADIUS / 2, HEIGHT / 2 + BALL_RADIUS / 2)
    c.coords(LEFT_PAD, PAD_W / 2, 0, PAD_W / 2, PAD_H)
    c.coords(RIGHT_PAD, WIDTH - PAD_W / 2, 0, WIDTH - PAD_W / 2, PAD_H)

def spawn_ball():
    global BALL_X_SPEED, BALL_Y_SPEED
    BALL_X_SPEED = random.choice([-INITIAL_SPEED, INITIAL_SPEED])
    BALL_Y_SPEED = random.choice([-INITIAL_SPEED, INITIAL_SPEED])
    reset_positions()

def update_score(player):
    global PLAYER_1_SCORE, PLAYER_2_SCORE
    if player == "left":
        PLAYER_1_SCORE += 1
        c.itemconfig(p_1_text, text=PLAYER_1_SCORE)
        flash_goal("YOU SCORED!")
    else:
        PLAYER_2_SCORE += 1
        c.itemconfig(p_2_text, text=PLAYER_2_SCORE)
        flash_goal("AI SCORED!")

def flash_goal(text):
    goal_text = c.create_text(WIDTH/2, HEIGHT/2 - 40, text=text, fill="white", font=("Arial", 24, "bold"))
    root.after(1000, lambda: c.delete(goal_text))

def bounce(action):
    global BALL_X_SPEED, BALL_Y_SPEED
    if action == "strike":
        BALL_Y_SPEED = random.randint(-10, 10)
        if abs(BALL_X_SPEED) < BALL_MAX_SPEED:
            BALL_X_SPEED *= -BALL_SPEED_UP
        else:
            BALL_X_SPEED = -BALL_X_SPEED
    else:
        BALL_Y_SPEED = -BALL_Y_SPEED

def check_winner():
    global game_running
    if PLAYER_1_SCORE >= WIN_SCORE:
        c.create_text(WIDTH / 2, HEIGHT / 2, text="🏆 Pemain 1 Menang!", fill="white", font=("Arial", 30))
        game_running = False
        start_button.config(state=NORMAL)
        return True
    elif PLAYER_2_SCORE >= WIN_SCORE:
        c.create_text(WIDTH / 2, HEIGHT / 2, text="🏆 Pemain 2 Menang!", fill="white", font=("Arial", 30))
        game_running = False
        start_button.config(state=NORMAL)
        return True
    return False

def auto_move_paddles():
    ball_coords = c.coords(BALL)
    ball_y = (ball_coords[1] + ball_coords[3]) / 2

    if mode_single_player:
        # AI untuk pemain kanan (RIGHT_PAD)
        right_coords = c.coords(RIGHT_PAD)
        right_y = (right_coords[1] + right_coords[3]) / 2

        if abs(ball_y - right_y) > 10:  # Tambah batas toleransi
            direction = AI_MOVE_SPEED if ball_y > right_y else -AI_MOVE_SPEED
            c.move(RIGHT_PAD, 0, direction)
    else:
        # Mode otomatis seperti sebelumnya
        left_coords = c.coords(LEFT_PAD)
        right_coords = c.coords(RIGHT_PAD)
        left_y = (left_coords[1] + left_coords[3]) / 2
        right_y = (right_coords[1] + right_coords[3]) / 2

        c.move(LEFT_PAD, 0, 10 if ball_y > left_y else -10)
        c.move(RIGHT_PAD, 0, 10 if ball_y > right_y else -10)

def move_ball():
    global BALL_X_SPEED, BALL_Y_SPEED
    if not game_running or check_winner():
        return

    auto_move_paddles()
    ball_left, ball_top, ball_right, ball_bottom = c.coords(BALL)

    if ball_top <= 0 or ball_bottom >= HEIGHT:
        bounce("wall")

    if ball_left <= PAD_W and c.coords(LEFT_PAD)[1] < ball_bottom and c.coords(LEFT_PAD)[3] > ball_top:
        bounce("strike")
    if ball_right >= right_line_distance and c.coords(RIGHT_PAD)[1] < ball_bottom and c.coords(RIGHT_PAD)[3] > ball_top:
        bounce("strike")

    if ball_right >= WIDTH:
        update_score("left")
        spawn_ball()
    elif ball_left <= 0:
        update_score("right")
        spawn_ball()

    c.move(BALL, BALL_X_SPEED, BALL_Y_SPEED)
    root.after(30, move_ball)

def start_game():
    global PLAYER_1_SCORE, PLAYER_2_SCORE, game_running
    # Reset segalanya
    c.delete("all")
    game_running = True
    PLAYER_1_SCORE = 0
    PLAYER_2_SCORE = 0
    start_button.config(state=DISABLED)

    # Lapangan & objek
    # Garis kiri
    c.create_line(PAD_W, 0, PAD_W, HEIGHT, fill="white")
    # Garis kanan
    c.create_line(WIDTH - PAD_W, 0, WIDTH - PAD_W, HEIGHT, fill="white")
    # Garis tengah
    c.create_line(WIDTH / 2, 0, WIDTH / 2, HEIGHT, fill="white")

    global BALL, LEFT_PAD, RIGHT_PAD, p_1_text, p_2_text

    BALL = c.create_oval(WIDTH / 2 - BALL_RADIUS / 2, HEIGHT / 2 - BALL_RADIUS / 2,
                         WIDTH / 2 + BALL_RADIUS / 2, HEIGHT / 2 + BALL_RADIUS / 2, fill="white")

    LEFT_PAD = c.create_line(PAD_W / 2, 0, PAD_W / 2, PAD_H, fill="yellow", width=PAD_W)
    RIGHT_PAD = c.create_line(WIDTH - PAD_W / 2, 0, WIDTH - PAD_W / 2, PAD_H, fill="yellow", width=PAD_W)

    p_1_text = c.create_text(WIDTH / 6, PAD_H / 4, text=PLAYER_2_SCORE, fill="white", font=("Arial", 20))
    p_2_text = c.create_text(WIDTH - WIDTH / 6, PAD_H / 4, text=PLAYER_1_SCORE, fill="white", font=("Arial", 20))

    spawn_ball()
    move_ball()

root.mainloop()