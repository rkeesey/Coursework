# echo_client.py
#
# ICS 32 
# Lab 7 Code 

import socket

class connection:
    def __init__(self, socket, inpt_str, otpt_str):
        self.socket = socket
        self.inpt_str = inpt_str
        self.otpt_str = otpt_str
    
    def __iter__(self): # make iterable
        yield self.socket
        yield self.inpt_str
        yield self.otpt_str

def read_host() -> str:
    '''
    Asks user for the host name or IP address until a valid one is provided
    Returns the valid host name/IP address 
    '''
    while True:
        inpt = input("Enter a host name or IP address: ")
        try:
            add = socket.inet_aton(inpt)
            return inpt
        except OSError:
            try:
                add = socket.gethostbyname(inpt)
                return inpt
            except OSError:
                print("\nInvalid host name or IP address!\n")


def read_port() -> int:
    '''
    Asks user for the port number until a valid one is provided
    Returns the valid port number between 1 and 65535
    '''
    while True:
        try:
            inpt = int(input("Enter a port number between 1-65535: "))
            if inpt >= 1 and inpt <= 65535:
                return inpt
            else:
                print("\nInvalid port number!\n")
        except ValueError:
            print("\nInvalid port number!\n")

def read_message() -> str:
    '''
    Asks user for a message to send
    returns message
    '''
    inpt = input("Enter a message: ")
    return inpt

def print_response(response: str) -> None:
    '''
    Prints reponse
    '''
    print(response)

def connect(host: str, port: int) -> 'connection':
    '''
    Create a socket 
    Connect to the host and port provided
    Create input and output streams for this socket
    return a connection consisting of the following:
    1) the socket, 2) the input stream, and 3) the output stream
    '''
    # socket object
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect host and port
    skt.connect((host, port))

    inpt_strm = skt.makefile('r')
    outpt_strm = skt.makefile('w')

    return connection(skt, inpt_strm, outpt_strm)

def close(connection: 'connection') -> None:
    '''
    Given a connection, consisting of 
    1) the socket, 2) the input stream, and 3) the output stream
    close all 3 components of the connection
    '''
    connection.inpt_str.close()
    connection.otpt_str.close()
    connection.socket.close()


def send_message(connection: 'connection', message: str) -> None:
    '''
    Given a connection and a message,
    send message to the output stream of the socket connection
    '''
    connection.otpt_str.write(message + '\n')
    connection.otpt_str.flush()


def receive_response(connection: 'connection') -> str:
    '''
    Receive message from socket input stream
    Return string
    '''
    data = connection.inpt_str.readline()
    if data:
        return data.strip()  # Remove the newline
    return ""


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