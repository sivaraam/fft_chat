#!/usr/bin/env python3
"""
Server for multithreaded (asynchronous) chat application.

Source:
https://gist.githubusercontent.com/schedutron/cd925247bfc4f8ae7930bbd99984a441/raw/754d98d3f90a86e3370378ef278ca7e25c4d1e05/chat_serv.py

Blog:
https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
"""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import process_fft as p_fft

# An ID to identify that an image is being sent
image_id = '{%IMG%}'
image_id_bytes = p_fft.fft_send(image_id)

message_id = '{%MSG%}'
message_id_bytes = p_fft.fft_send(message_id)

id_len = max(len(image_id_bytes), len(message_id_bytes))

def send(client, msg):
     client.send(message_id_bytes)
     msg_bytes = p_fft.fft_send(msg)
     client.send(msg_bytes)

def recv(client):
    msg_id = client.recv(id_len)
    if msg_id == message_id_bytes:
        msg_bytes = client.recv(BUFSIZ)
        msg = p_fft.fft_receive(msg_bytes)
    else:
        msg = 'Skipped message!'
        print('Skipping something that is not a message')

    return msg

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    greeting_msg = "Greetings from the cave! Now type your name and press enter!"
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        send(client, greeting_msg)
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = recv(client)
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    send(client, welcome)
    msg = "%s has joined the chat!" % name
    broadcast(msg)
    clients[client] = name

    while True:
        msg = recv(client)
        if msg != "{quit}":
            broadcast(msg, name+": ")
        else:
            send(client, "{quit}")
            client.close()
            del clients[client]
            broadcast("%s has left the chat." % name)
            break

def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        send(sock, prefix+msg)

clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 102400
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()

