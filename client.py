#!/usr/bin/env python3
"""
Script for Tkinter GUI chat client.

Source:
https://gist.githubusercontent.com/schedutron/287324944d765ae0656eec6971ca40d8/raw/49695836956e8f202db88abf9198af0d95f427c1/chat_clnt.py

Blog:
https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170
"""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import process_fft as p_fft

image_id = '{%IMG%}'
image_id_bytes = p_fft.fft_send(image_id)
image_len_bytes_limit = 6

message_id = '{%MSG%}'
message_id_bytes = p_fft.fft_send(message_id)

id_length = max(len(image_id_bytes), len(message_id_bytes))

def sock_send(client, msg):
    client.send(message_id_bytes)
    send_bytes = p_fft.fft_send(msg)
    client.send(send_bytes)

def sock_recv(client):
    msg_id = client.recv(id_length)
    if msg_id == message_id_bytes:
        received_bytes = client.recv(BUFSIZ)
        msg = p_fft.fft_receive(received_bytes)
    elif msg_id == image_id_bytes:
        # For now, we save the image with a static name
        img_file = 'received.png'

        # Open the file to write the image
        img = open(img_file, 'wb')

        # Get the image size
        #
        # Currently, the implementation is limited by
        # the fact it can't handle the image sizes
        # dynamically. Yet to fix it. TODO.
        img_len_bytes = client.recv(image_len_bytes_limit)
        img_size = int(img_len_bytes.decode('utf-8'))
        print('Size: ', img_size)

        print('Receiving file')

        # We receive the image as 1024 byte chunks
        # until we receive it all
        while (img_size > 0):
            # The last chunk alone could be a little less
            # than 1024, so we use the minimum of img_size
            # and 1024 here.
            img_bytes = client.recv(min(img_size, 1024))

            # We write the image to the file as and when
            # we receive it.
            img.write(img_bytes)

            img_size = img_size - 1024

        img.close()

        print('Received file.')
        msg = 'image'
    else:
        msg = 'Skipped message!'
        print('Skipping something that is not a message')

    return msg

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = sock_recv(client_socket)
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break

def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    sock_send(client_socket, msg)
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()

#----Now comes the sockets part----
HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 102400
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

# Create the GUI container
top = tkinter.Tk()
top.title("Chatter")

# To show the messages
messages_frame = tkinter.Frame(top)

# For the messages to be sent.
my_msg = tkinter.StringVar()
my_msg.set("Type your messages here.")

# To navigate through past messages.
scrollbar = tkinter.Scrollbar(messages_frame)

# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)

scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

print("You can now start chatting using the GUI to chat.")

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.
