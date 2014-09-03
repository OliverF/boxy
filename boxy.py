import socket
import threading
import sys
import getopt
import time
import signal
import os

inputport = 0
remoteport = 0 
remoteaddress = ""
kill = False

bytestoremote = 0
bytesfromremote = 0

help = "Invalid arguments, usage:\nboxy.py -i <input port> -p <remote port> -a <remote address>"

def relay():
	global bytestoremote
	global bytesfromremote

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind(("0.0.0.0", inputport))

	incomingsetup = False
	clientport = 0
	clientip = ""

	while True:
		data, fromaddr = sock.recvfrom(1024)

		if (kill == True):
			sock.close()
			return

		if (incomingsetup == False):
			clientport = fromaddr[1]
			clientip = fromaddr[0]
			incomingsetup = True

		if (fromaddr[0] == clientip):
			#forward from client to server
			sock.sendto(data, (remoteaddress, remoteport))
			bytestoremote += sys.getsizeof(data)
		else:
			#forward from server to client
			sock.sendto(data, (clientip, clientport))
			bytesfromremote += sys.getsizeof(data)

def reportbandwidth():
	global bytestoremote
	global bytesfromremote
	step = 0
	while True:
		time.sleep(1)
		if (sys.platform == "win32"):
			os.system('cls')
		else:
			os.system('clear')
		print "Relaying on port {0} to {1}:{2}".format(inputport, remoteaddress, remoteport)
		print "From remote: {0:.2f}MB/s | To remote: {1:.2f}MB/s".format(float(bytesfromremote)/1000000, float(bytestoremote)/1000000)
		if (step == 0):
			print "\\"
			step += 1
		elif (step == 1):
			print "|"
			step += 1
		elif (step == 2):
			print "/"
			step += 1
		elif (step == 3):
			print "-"
			step = 0
		bytesfromremote = 0
		bytestoremote = 0

def quit():
	global kill

	print "Quitting..."

	kill = True
	#send anything to the input port to trigger it to read, therefore allowing the thread to close
	quitsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	quitsock.sendto("killing", ("127.0.0.1", inputport))
	quitsock.close()
	os._exit(0)

#process args
try:
	options, args = getopt.getopt(sys.argv[1:], "i:p:a:")
except getopt.Getopterror:
	print help
	sys.exit(2)

try:
	for option, arg in options:
		if (option == "-i"):
			inputport = int(arg)
		elif (option == "-p"):
			remoteport = int(arg)
		elif (option == "-a"):
			remoteaddress = arg
except ValueError:
	print help
	sys.exit(2)

if ((0 < inputport <= 65535 and 0 < remoteport <= 65535 and remoteaddress != "") == False):
	print help
	sys.exit(2)

print "Relay starting on port " + str(inputport) + ", relaying UDP to", remoteaddress + ":" + str(remoteport)

#start relay
relaythread = threading.Thread(target=relay)
relaythread.start()

reportbandwidththread = threading.Thread(target = reportbandwidth)
reportbandwidththread.daemon = True
reportbandwidththread.start()

try:
	while raw_input() != "quit":
		continue
	quit()
except KeyboardInterrupt:
	quit()
except EOFError:
	#this exception is raised when ctrl-c is used to close the application on Windows, appears to be thrown twice?
	try:
		quit()
	except KeyboardInterrupt:
		os._exit(0)