'''
'Client Program'
@Author: Saurab Dulal 
 Date. : October 16, 2017 
 Dependencies: Python 3+ 
 Description: Simple UDPPingerClient program  	
'''

#ea

import random
import socket
import time 

#since we need to send a ping message to specific ip and port 
#we need to specify servers IP and port number 

UDP_IP = '127.0.0.1' #local host 
UDP_PORT = 12000 #server listening at port 

serverAddress = (UDP_IP,UDP_PORT)
clientSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP

clientSocket.settimeout(20) #wait for 20 seconds before time out 

try:

	difftime = 0 
	rcv_flag = False
	
	for apptempt in range(0,10):	#sending 10 sucessive message 

		# message format, sequence number and time 
		MESSAGE  = str("Sequence number :"+str(apptempt)+" and send at time :"+str(time.time()))
		MESSAGE = MESSAGE.encode('utf-8') #converting message to bytes
		sending_time = time.time()

		sent = clientSocket.sendto(MESSAGE, serverAddress)
		
		try:
			message, address = clientSocket.recvfrom(1024)
		except Exception as e:
			print("Connection time out")
			continue 
		end_time = time.time()

		if message:
			message = message.decode('utf-8').split('token')
			print("Message from server: "+str(message[0]))
			print("Receved at :"+str(message[1]))
			print("Round trip time (RTT):"+str(end_time - sending_time))
			rcv_flag = False

finally:
	clientSocket.close()



