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

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    greeting_msg = "Greetings from the cave! Now type your name and press enter!"
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        greeting_bytes = p_fft.fft_send(greeting_msg)
        client.send(greeting_bytes)
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name_bytes = client.recv(BUFSIZ)
    name = p_fft.fft_receive(name_bytes)
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    welcome_bytes = p_fft.fft_send(welcome)
    client.send(welcome_bytes)
    msg = "%s has joined the chat!" % name
    broadcast(msg)
    clients[client] = name

    while True:
        msg_bytes = client.recv(BUFSIZ)
        msg = p_fft.fft_receive(msg_bytes)
        if msg != "{quit}":
            broadcast(msg, name+": ")
        else:
            quit_bytes = p_fft.fft_send("{quit}")
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast("%s has left the chat." % name)
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        broadcast_bytes = p_fft.fft_send(prefix+msg)
        sock.send(broadcast_bytes)

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

