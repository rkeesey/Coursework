# connect4_network_client.py
#
# ICS 32 
# Project #2
#
# This executable module implements a networked console version of Connect Four.

from datetime import datetime
import connect4
import connect4_ui
import connect4_ui_ai
import client_short
import socket

# DROP: 1
# POP: 2
"""
1. client: Game num_rows num_cols
2. server: START
3. game starts when client recieves START
4. client prompts user for move and completes it
5. client sends server the user's move
6. server says user's move was received 
7. client sends MOVE to prompt server move
8. server sends interger string: "1" (DROP) or "2" POP
9. client sends COLUMN to prompt server column 
10. server sends integer string with column value
11. repeat process until one player wins
"""
def run_console_network() -> None:

    host = 'arcala-1.ics.uci.edu'
    port = 8000
    
    print(f'Connecting to {host} (port {port}) ...')
    connection = client_short.connect(host, port)
    print('Connected!')

    state = connect4_ui.make_new_game()
    prnt = connect4_ui.print_board(state)
    print(prnt)
    start_game = client_short.read_message() # GAME X Y
    client_short.send_message(connection, start_game) 
    response = client_short.receive_response(connection) # START
    client_short.print_response(response)

    my_IP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_IP.connect(("8.8.8.8", 80))  # Google's DNS server
    ip_address = my_IP.getsockname()[0]
    my_IP.close()
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("The client's IP address: ", ip_address)
    print("The game started at this time: ", start_time)

    while True:
        
        board, turn = state
        
        winner = connect4.winner(state)
        if winner != 0:
        
            print('Closing connection...')
            client_short.close(connection)
            print('Closed!')
            end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print("The client's IP address: ", ip_address)
            print("The game ended at this time: ", end_time)
            break

        elif turn == 1: # Red turn (user)
            move = connect4_ui.choose_move(state)
            state_new = connect4_ui.make_move(state, move)
            message = client_short.read_message() # USER X Y
            client_short.send_message(connection, message) # send move to server
            response = client_short.receive_response(connection)
            client_short.print_response(response) # RECEIVED
            prnt = connect4_ui.print_board(state_new)
            print(prnt)
            state = state_new
        
        elif turn == 2: # Yellow turn (server)
            
            message_1 = client_short.read_message() # MOVE
            client_short.send_message(connection, message_1) 
            response_1 = client_short.receive_response(connection) 
            client_short.print_response(response_1) # move choice

            message_2 = client_short.read_message() # COLUMN
            client_short.send_message(connection, message_2) 
            response_2 = client_short.receive_response(connection) 
            client_short.print_response(response_2) # column choice
            
            # make server move 
            move = connect4_ui.choose_move(state)
            state_new = connect4_ui.make_move(state, move)
            prnt = connect4_ui.print_board(state_new)
            print(prnt)
            state = state_new

if __name__ == '__main__':
    run_console_network()
