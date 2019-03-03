## FFT Chat
A GUI based chat room that applies uses FFT to encode/decode
messages sent by users. It is a client/server based application.

### Usage
* See if [Dependencies](#dependencies) have been installed.

* Start the server:

	`python3 server.py`

	By default, the server runs in port in port `33000`. Currently it can
	only be changed by editing the source of `server.py`.
	The `PORT` variable has to be changed.

* Start the client:

	`python3 client.py`

	The client asks for the HOST address and PORT to connect to. If
	both client and server run in the same machine, no need to enter
	the HOST. If server runs in port `33000` no need to enter it either.

* Then user can follow instructions in the GUI window that pops up.

### Dependencies
* numpy (for FFT)
* tkinter (for GUI)

#### Installing dependencies
* numpy

	```
	pip3 install numpy
	```

* tkinter
	For Ubuntu or Debian based distributions:
	```
	sudo apt install python3-tk
	```

	For other platforms refer to the [official Tk documentation](https://tkdocs.com/tutorial/install.html).

### Notes
* The maximum packet size is limited to 102400. It's a limitation which has to be fixed. References:
	- [socket.recv -- three ways to turn it into recvall (Python recipe)](https://code.activestate.com/recipes/408859/)
	- [Python socket receive - incoming packets always have a different size](https://stackoverflow.com/q/1708835/5614968)
	- [Socket Programming HOWTO](https://docs.python.org/3/howto/sockets.html)
