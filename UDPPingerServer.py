
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
import os


class server_connection():

	server_ip = None
	server_port = None
	client_socket = None
	server_address = None
	def __init__(self,server_ip,server_port):

		print("Initilizing ip address and port number")
		self.server_port = server_port
		self.server_ip = server_ip
		self.server_address = (self.server_ip, self.server_port)

	def create_connection(self):

		print("creating server connection")
		server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		server_socket.bind(self.server_address) #binding is only done in case of server
		return server_socket


	def close_connection(self,server_socket):
		print("Closing server socket connection")
		server_socket.close()



def file_handler(file_name):
	#first iteration get every info about file
	file_stats = os.stat(file_name)
	print(file_stats)
	return file_stats


class server_packet():

	def calculate_checksum(self):
		pass



def connection_handler():
	pass


def main():
	pass



if __name__=='__main__':
	main()




#
# 	# Create a UDP socket
# 	# Notice the use of SOCK_DGRAM for UDP packets
# serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 	# Assign IP address and port number to socket
# serverAddress = ('127.0.0.1',12000)
# serverSocket.bind(serverAddress) #only used in case of server
#
#
# while True:
#
# 	print("Server waiting for new request")
# 	# Generate random number in the range of 0 to 10
# 	rand = random.randint(0, 10)
# 	message, address = serverSocket.recvfrom(1024)
#
# 	# Receive the client packet along with the address it is coming from
# 	# Capitalize the message from the client
# 	# If rand is less is than 4, we consider the packet lost and do not respond
# 	if rand < 4:
# 		continue
#
# 	print(rand)
# 	print("Received message from the client: "+str(message.decode('utf-8'))+" and the address is :"+ str(address))
#
# 	if message:
# 		#Token is used to break the server message at client side
# 		message = message.upper()+b'token'+str(datetime.datetime.now()).encode('utf-8')
# 		sent = serverSocket.sendto(message, address)
#




