# connect4_ui.py
#
# ICS 32 
# Project #2
#
# This module contains utility functions that can be called from a console-
# based UI for a Connect Four game.
# 
# The signatures for the four required functions are provided.
# Hint: It would be useful to create helper functions.

import connect4
from collections import namedtuple

DROP = 1
POP = 2


def make_new_game() -> connect4.GameState:
    '''Asks the user for a board size, then creates a new game and return connect4.GameState'''

    cols = int(input("Columns: "))
    rows = int(input("Rows: "))

    board, turn = connect4.new_game(cols, rows)

    return connect4.GameState(board, turn)

def print_board(state: connect4.GameState) -> str:
    '''Returns a string holding the contents of a game board, given a GameState'''

    board, turn = state

    board_string = ''
    for num in range(1, len(board) + 1):
        board_string += str(f'{num:<3}')
    board_string += '\n'
    
    for row in range(len(board[0])):
        for col in board:
            if col[row] == 1:
                board_string += 'R  '
            elif col[row] == 2:
                board_string += 'Y  '
            else:  
                board_string += '.  '
        board_string += '\n'

    winner = connect4.winner(state)
    if winner == 1:
        board_string += f'\nRED wins!\n'
    elif winner == 2:
        board_string += f'\nYELLOW wins!\n'
    elif turn == 1:
        board_string += f'\nRED\'s turn\n'
    elif turn == 2:
        board_string += f'\nYELLOW\'s turn\n'

    return board_string

def choose_move(state: connect4.GameState) -> tuple[int, int]:
    '''
    Asks the user to choose a move, returning a tuple whose first element
    is DROP or POP and whose second element is a valid column number.
    '''
    action = None
    col = None

    board, turn = state

    max_col = len(board)

    while True:
        choice = input("[D]rop or [P]op? ")
        if choice.casefold() == 'd':
            action = DROP
        elif choice.casefold() == 'p':
            action = POP
        else:
            continue
        while True:    
            colm = input("Column: ")
            try:
                if int(colm) <= max_col:
                    col = int(colm)
                else:
                    continue
            except ValueError:
                continue
 
            mv = (action, col)

            return mv


def make_move(state: connect4.GameState, move: tuple[int, int]) -> connect4.GameState:
    '''
    Makes the given move against the given state, returning the new state.
    For a valid move, return new state.
    
    Raise connect4.InvalidMoveError if invalid operation detected.
    Implement exception handler to catch this exceptions.
    If connect4.InvalidMoveError exception is caught, return original state inside the exception handler.
    '''

    try:
        action, col = move  
        if action == DROP: 
            state_new = connect4.drop(state, col - 1)
        elif action == POP:
            state_new = connect4.pop(state, col - 1)
        return state_new
    except connect4.InvalidMoveError:
        return state
