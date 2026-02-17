# connect4_ui_ai.py
#
# ICS 32 
# Project #2
#
# This module contains utility functions to implement the AI player 
# for the console UI Connect Four game.
# 

import connect4
import random

DROP = 1
POP = 2

# New function
def ai_move(state: connect4.GameState) -> tuple[int, int]:
    '''
    Asks the AI to choose a move, returning a tuple whose first element
    is DROP or POP and whose second element is a valid column number.
    Hint: helper functions would use useful here.
    '''
    action = None
    col = None

    board, turn = state

    max_col = len(board)

    while True:
        choice = choose_action()
        if choice == 1:
            action = DROP
        elif choice == 2:
            action = POP
        else:
            continue
        while True:    
            colm = choose_col(max_col)
            try:
                if int(colm) <= max_col:
                    col = int(colm)
                else:
                    continue
            except ValueError:
                continue
 
            mv = (action, col)

            return mv

def choose_action():
    choice = random.randint(1, 2)
    return choice

def choose_col(max):
    choice = random.randint(1, max)
    return choice
