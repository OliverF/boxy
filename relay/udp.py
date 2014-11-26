import sys
import socket
import threading
import status

_kill = False
_relayport = 0
_remoteaddress = ""
_remoteport = 0

def relay():
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(("0.0.0.0", _relayport))

	incomingsetup = False
	clientport = 0
	clientip = ""

	while True:
		data, fromaddr = sock.recvfrom(1024)

		if (_kill == True):
			sock.close()
			return

		if (incomingsetup == False):
			clientport = fromaddr[1]
			clientip = fromaddr[0]
			incomingsetup = True

		if (fromaddr[0] == clientip):
			#forward from client to server
			sock.sendto(data, (_remoteaddress, _remoteport))
			status.bytestoremote += sys.getsizeof(data)
		else:
			#forward from server to client
			sock.sendto(data, (clientip, clientport))
			status.bytesfromremote += sys.getsizeof(data)

def start(relayport, remoteaddress, remoteport):
	global _relayport
	global _remoteaddress
	global _remoteport

	_relayport = relayport
	_remoteaddress = remoteaddress
	_remoteport = remoteport

	relaythread = threading.Thread(target = relay)
	relaythread.start()

def stop():
	_kill = True
	#send anything to the input port to trigger it to read, therefore allowing the thread to close
	quitsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	quitsock.sendto("killing", ("127.0.0.1", _relayport))
	quitsock.close()