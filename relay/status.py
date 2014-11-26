import sys
import time
import os
import threading

bytestoremote = 0
bytesfromremote = 0

_relayport = 0
_remoteaddress = ""
_remoteport = 0

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
		print "Relaying on port {0} to {1}:{2}".format(_relayport, _remoteaddress, _remoteport)
		print "From remote: {0:.6f}MB/s | To remote: {1:.6f}MB/s".format(float(bytesfromremote)/1000000, float(bytestoremote)/1000000)
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

def start(relayport, remoteaddress, remoteport):
	global _relayport
	global _remoteaddress
	global _remoteport
	
	reportbandwidththread = threading.Thread(target = reportbandwidth)
	reportbandwidththread.daemon = True
	reportbandwidththread.start()

	_relayport = relayport
	_remoteaddress = remoteaddress
	_remoteport = remoteport