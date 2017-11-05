
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
import os, sys
import pickle

sequence_counter = 0
ack_counter = 0

def exception_handler(e):
	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	print('Type: %s' % (exc_type), 'File name: %s' % (fname), exc_tb.tb_lineno, 'Error: %s' % (e))


class server_connection():

	server_ip = None
	server_port = None
	server_socket = None
	server_address = None
	def __init__(self,server_ip='127.0.0.1',server_port=12000):

		print("Initilizing ip address and port number")
		self.server_port = server_port
		self.server_ip = server_ip
		self.server_address = (self.server_ip, self.server_port)

	def create_connection(self):

		print("Creating server connection")
		try:
			self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.server_socket.bind(self.server_address) #binding is only done in case of server
		except socket.error as err:
			exception_handler(e)
			return False
		return True


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

	connection_object = server_connection()
	connection_object.create_connection()
	print("Server socket created: " +str(connection_object.server_socket))

	while True:
		print("Server waiting for request")
		message, address= connection_object.server_socket.recvfrom(1024)
		message = pickle.loads(message) #1=seq, 2=ack, 3=mes, 4=type
		for i in message:
			print(i)
		# print("Received message from the client: " + str(message.decode('utf-8')) + " and the address is :" + str(
		# 	address))


def main():
	connection_handler()



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




