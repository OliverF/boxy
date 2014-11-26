import sys
import socket
import threading
import status
import time

_kill = False
_relayport = 0
_remoteaddress = ""
_remoteport = 0

_clients = 0
_servers = 0

_socks = []

def acceptclients():
	global _socks

	clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientsock.bind(("0.0.0.0", _relayport))
	clientsock.listen(10)

	while True:
		clientconn, addr = clientsock.accept()

		if (_kill == True):
			clientsock.close()
			for sock in _socks:
				sock.close()
			return

		serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serversock.connect((_remoteaddress, _remoteport))

		_socks.append(clientconn)
		_socks.append(serversock)

		clientthread = threading.Thread(target = client, kwargs = {'client': clientconn, 'server': serversock})
		clientthread.start()

		serverthread = threading.Thread(target = server, kwargs = {'client': clientconn, 'server': serversock})
		serverthread.start()

def close(client, server):
	try:
		client.close()
	except socket.error:
		pass

	try:
		server.close()
	except socket.error:
		pass

def client(client, server):
	global _clients
	_clients += 1
	while True:
		try:
			data = client.recv(1)

			if (data == ""):
				close(client, server)
				break

			server.sendall(data)
			status.bytestoremote += sys.getsizeof(data)
		except socket.error:
			close(client, server)
			break
	_clients -= 1

def server(client, server):
	global _servers
	_servers += 1
	while True:
		try:
			data = server.recv(1)

			if (data == ""):
				close(client, server)
				break

			client.sendall(data)
			status.bytesfromremote += sys.getsizeof(data)
		except socket.error:
			close(client, server)
			break
	_servers -= 1

def start(relayport, remoteaddress, remoteport):
	global _relayport
	global _remoteaddress
	global _remoteport

	_relayport = relayport
	_remoteaddress = remoteaddress
	_remoteport = remoteport
	
	acceptthread = threading.Thread(target = acceptclients)
	acceptthread.start()

def stop():
	global _kill
	_kill = True
	#connect to the input port therefore allowing the thread to close
	quitsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	quitsock.connect(("127.0.0.1", _relayport))
	quitsock.close()