# The code is modified from https://github.com/Stanou01260/chessbot_python/blob/master/code/main.py

import tkinter as tk
import board_basics
from game_state_classes import *
from voice_to_chess_notation import Voice_to_chess_notation


def clear_logs():
    logs_text.delete('1.0', tk.END)


def add_log(log):
    logs_text.insert(tk.END, log + "\n")


def stop_playing():
    clear_logs()
    button_start = tk.Button(text="Start playing (s)", command=start_playing)
    button_start.grid(column=0, row=1)


def start_playing(ignore=None):
    pyautogui.click()
    print(ignore)
    game_state = Game_state(voice_to_chess_notation)
    add_log("Looking for a chessboard...")

    position, we_are_white = chessboard_detection.find_chessboard()

    add_log("Found the chessboard " + position.print_custom())
    game_state.board_position_on_screen = position

    button_start = tk.Button(text="Stop playing", command=stop_playing)
    button_start.grid(column=0, row=1)

    resized_chessboard = chessboard_detection.get_chessboard(game_state)

    game_state.previous_chessboard_image = resized_chessboard

    game_state.we_play_white = we_are_white
    if we_are_white:
        add_log("We are white")
        game_state.moves_to_detect_before_play = 0
    else:
        add_log("We are black")
        game_state.moves_to_detect_before_play = 1
        game_state.previous_chessboard_image = chessboard_detection.read_black_chessboard()

    while not game_state.board.is_game_over():
        window.update()
        if game_state.moves_to_detect_before_play == 0:
            game_state.play_next_move()

        if game_state.board.is_game_over():
            break

        found_move, move = game_state.register_move_if_needed()
        if found_move:
            clear_logs()
            add_log("The board :\n" + str(game_state.board) + "\n")
            add_log("\nAll moves :\n" + str(game_state.executed_moves))
        else:
            print(move)

    button_start = tk.Button(text="Start playing", command=start_playing)
    button_start.grid(column=0, row=1)


window = tk.Tk()
window.title("Voice to chess notation by Alper Karayaman")

label_title = tk.Label(text="Welcome on voice to chess notation, hope you will have fun with it", anchor="e",
                       wraplength=300)
label_title.grid(column=0, row=0)

voice_to_chess_notation = Voice_to_chess_notation()

button_start = tk.Button(text="Start playing (s)", command=start_playing)
button_start.grid(column=0, row=1)

logs_text = tk.Text(window, width=40, height=25, background='gray')
logs_text.grid(column=0, row=2)

window.geometry("+1000+100")
window.bind("s", start_playing)
window.mainloop()
