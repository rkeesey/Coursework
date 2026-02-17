# echo_client.py
#
# ICS 32 
# Lab Code Example

import socket

def read_host() -> str:
    while True:
        host = input('Host: ').strip()

        if host == '':
            print('Please specify a host (either a name or an IP address)')
        else:
            return host

def read_port() -> int:
    while True:
        try:
            port = int(input('Port: ').strip())

            if 1 <= port <= 65535:
                return port

        except ValueError:
            pass
        
        print('Ports must be an integer between 1 and 65535')

def read_message() -> str:
    return input('Message: ')

def print_response(response: str) -> None:
    print('Response: ' + response)

def connect(host: str, port: int) -> 'connection':
    echo_socket = socket.socket()
    echo_socket.connect((host, port))

    echo_socket_input = echo_socket.makefile('r')
    echo_socket_output = echo_socket.makefile('w')

    return echo_socket, echo_socket_input, echo_socket_output

def close(connection: 'connection') -> None:
    echo_socket, echo_socket_input, echo_socket_output = connection

    echo_socket_input.close()
    echo_socket_output.close()
    echo_socket.close()

def send_message(connection: 'connection', message: str) -> None:
    echo_socket, echo_socket_input, echo_socket_output = connection

    echo_socket_output.write(message + '\r\n')
    echo_socket_output.flush()

def receive_response(connection: 'connection') -> None:
    echo_socket, echo_socket_input, echo_socket_output = connection
    return echo_socket_input.readline()[:-1]

def run() -> None:
    host = read_host()
    port = read_port()

    print(f'Connecting to {host} (port {port}) ...')
    connection = connect(host, port)
    print('Connected!')

    while True:
        message = read_message()

        if message == '':
            break
        else:
            send_message(connection, message)
            response = receive_response(connection)
            print_response(response)

    print('Closing connection...')
    close(connection)
    print('Closed!')


if __name__ == '__main__':
    run()
