'''
'Client Program'
@Author: Saurab Dulal 
 Date. : October 16, 2017 
 Dependencies: Python 3+ 
 Description: Simple UDPPingerClient program  	
'''

import random
import socket
import time 


class file_handler():

	# def file(self,file_name):
	# 	try:
	#read file_name
	#store received packet into the memory

	pass


#This class will create connection and will receive the response -
#After receiving the response it will send the response to transport for further verification

class _client_connection():
	# create connection
	server_ip = None
	server_port = None
	client_socket = None

	def __init__(self, server_ip = '127.0.0.1', server_port=12000): #default defined

		print("Initializing server ip address and port number")
		self.server_ip = server_ip
		self.server_port = server_port

	@staticmethod  #we don't want this value to be change
	def create_client_socket(self):

		print("Creating client socket")

		'''AF_INET refers to the Internet family of protocols, and
		it is of the SOCK_DGRAM datagram type, which means UDP -- Foundation of  Network Programming'''

		client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		#if required we can set_up time out condition for client_socket as well
		#clientSocket.settimeout(20) comment out if needed
		return client_socket

	def send_request_to_server(self, message, address, client_socket):
		print("sending request to the client")
		try:
			send = client_socket.sendto(message,address) #message always needs to be in byte format
		except Exception as e:
			print(e)


	def receive_response_from_server(self,client_socket):

		try:
			message, address = client_socket.recvfrom(1024)
		except Exception as e:
			return e

		if message:
			return message


	def close_connection(self,client_socket):
		print("Closing socket connection")
		client_socket.close()

	def buffer_method(self):
		print("this is a buffer method")

	#also client connection will receive response from server and send it transport





# class _transport(_client_connection.client_socket):
#
#
# 	client_socket = _client_connection.client_socket
#
# 	#receive response for the request send by client connection
# 	def receive_packet(self,packet):
# 		#verify the packet - checksum, sequence, and send response to client conn
# 		pass

	#Disect packet and do the necessary stuffs

def connection_handler():
	#this function will handle all the connections
	# will create a conn
	# wait in loop for packets
	# and send the received packet to transport for verification
	# if packet ok, send it to file handler who will write to the file,
	# stay in loop to receive packet
	# upon completion, close the connection
	# client_object.buffer_method()
	# print(client_object.server_p ort)
	# while True:

	pass


def main():
	connection_handler()



if __name__ == '__main__':
	main()

















#
# try:
#
# 	difftime = 0
# 	rcv_flag = False
#
# 	for apptempt in range(0,10):	#sending 10 sucessive message
#
# 		# message format, sequence number and time
# 		MESSAGE  = str("Sequence number :"+str(apptempt)+" and send at time :"+str(time.time()))
# 		MESSAGE = MESSAGE.encode('utf-8') #converting message to bytes
# 		sending_time = time.time()
#
# 		sent = clientSocket.sendto(MESSAGE, serverAddress)
#
# 		try:
# 			message, address = clientSocket.recvfrom(1024)
# 		except Exception as e:
# 			print("Connection time out")
# 			continue
# 		end_time = time.time()
#
# 		if message:
# 			message = message.decode('utf-8').split('token')
# 			print("Message from server: "+str(message[0]))
# 			print("Receved at :"+str(message[1]))
# 			print("Round trip time (RTT):"+str(end_time - sending_time))
# 			rcv_flag = False





