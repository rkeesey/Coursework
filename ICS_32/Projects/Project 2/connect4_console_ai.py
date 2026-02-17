# connect4_console_ai.py
#
# ICS 32 Winter 2022
# Project #2
#
# This executable module implements a console-only version of Connect Four.
# The second player is an AI player.

import connect4
import connect4_ui
import connect4_ui_ai



def run_console_ui() -> None:
    state = connect4_ui.make_new_game()
    print(state.board)
    prnt = connect4_ui.print_board(state)
    print(prnt)
    while True:
        board, turn = state
        if turn == 1: # Red turn (user)
            move = connect4_ui.choose_move(state)
            state_new = connect4_ui.make_move(state, move)
        elif turn == 2:
            move = connect4_ui_ai.ai_move(state)
            state_new = connect4_ui.make_move(state, move)
        
        prnt = connect4_ui.print_board(state_new)
        print(prnt)

        state = state_new



if __name__ == '__main__':
    run_console_ui()
