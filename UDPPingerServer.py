
'''
'Server Program'
@Author: Saurab
 Date. : October 16, 2017 
 Dependencies: Python 3+ 
 Description:


'''


import random
import socket 
import datetime

class server_connection():

	server_ip = None
	server_port = None
	client_socket = None

class file_handler():
	#read the file and create a chunk out of it
	pass

class server_packet():

	def calculate_checksum(self):
		pass




	# Create a UDP socket
	# Notice the use of SOCK_DGRAM for UDP packets 
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	# Assign IP address and port number to socket  
serverAddress = ('127.0.0.1',12000)
serverSocket.bind(serverAddress) #only used in case of server 


while True:
	
	print("Server waiting for new request")
	# Generate random number in the range of 0 to 10
	rand = random.randint(0, 10)
	message, address = serverSocket.recvfrom(1024)

	# Receive the client packet along with the address it is coming from 
	# Capitalize the message from the client
	# If rand is less is than 4, we consider the packet lost and do not respond 
	if rand < 4:			
		continue
	
	print(rand)
	print("Received message from the client: "+str(message.decode('utf-8'))+" and the address is :"+ str(address))

	if message:
		#Token is used to break the server message at client side
		message = message.upper()+b'token'+str(datetime.datetime.now()).encode('utf-8') 
		sent = serverSocket.sendto(message, address)
	




