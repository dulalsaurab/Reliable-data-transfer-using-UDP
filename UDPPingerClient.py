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
import os, sys
import pickle
import time


sequence_counter =0
ack_counter  = 0
alternating_bit = 1

class file_handler():

	# def file(self,file_name):
	# 	try:
	#read file_name
	#store received packet into the memory

	pass

class _transport():

	received_data = ''


#
# 	#receive response for the request send by client connection
# 	def receive_packet(self,packet):
# 		#verify the packet - checksum, sequence, and send response to client conn
# 		pass
#Disect packet and do the necessary stuffs


def exception_handler(e):
	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	print('Type: %s' % (exc_type), 'On file: %s' % (fname), exc_tb.tb_lineno, 'Error: %s' % (e))


#This class will create connection and will receive the response -
#After receiving the response it will send the response to transport for further verification

class _client_connection():

	# create connection
	server_ip = None
	server_port = None
	client_socket = None
	address = None


	def __init__(self, server_ip = '127.0.0.1', server_port=12000): #default defined

		print("Initializing server ip address and port number")
		self.server_ip = server_ip
		self.server_port = server_port
		self.address = (self.server_ip, self.server_port)


	def create_client_socket(self):

		print("Creating client socket")

		'''AF_INET refers to the Internet family of protocols, and
		it is of the SOCK_DGRAM datagram type, which means UDP -- Foundation of Network Programming'''
		try:
			self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self.client_socket.settimeout(2)

		except socket.error as err:
			exception_handler(err)
			return False

		#if required we can set_up time out condition for client_socket as well
		#clientSocket.settimeout(20) comment out if needed

		return True


	def send_request_to_server(self, message, address, client_socket):

		print("Sending request to the server")

		try:
			send = client_socket.sendto(message,address) #message always needs to be in byte format

		except Exception as e:
			exception_handler(e)


	def receive_response_from_server(self,client_socket):

		try:
			message, address = client_socket.recvfrom(1024)
			return message, address
		except socket.timeout:
			return Exception



	def close_connection(self,client_socket):
		print("Closing socket connection")
		client_socket.close()


	def buffer_method(self):
		print("this is a buffer method")

	#also client connection will receive response from server and send it transport

#type - d=data, a=ack, r=retransmission
def create_packet(alternating_bit, message='', file_name='', type='a',):

	global sequence_counter
	global ack_counter
	#create list for each message [seqnum,acknowledgement,data]
	packet = pickle.dumps([sequence_counter, ack_counter, message, file_name, type, alternating_bit])
	return packet

def connection_handler(file_name=None):

	global alternating_bit
	chunk_received = _transport()

	file_name = file_name
	#create a conn object
	connection_object  = _client_connection()
	if connection_object.create_client_socket():
		print("Client socket created: " + str(connection_object.client_socket))
	else:
		print("Failled to create client socket, restart the client program")
		return

	first_sent = True
	type = 'd' #data request
	counter = 0
	while True:
		print(alternating_bit)
		packet = create_packet(alternating_bit,'Initial request','some_test_file', type)

		try:
			connection_object.send_request_to_server(packet, connection_object.address, connection_object.client_socket)
			if type == 'c':
				print("The transfer process completed, process terminating !!")
				break
			message, address = connection_object.receive_response_from_server(connection_object.client_socket)
			packet = pickle.loads(message)  #0=counter, 1=data, 2=ALTbit

			if packet:
				if alternating_bit == packet[2]:  #we got the right packet
					alternating_bit ^= 1
					if first_sent:
						print("File is found on the server, now server will start transmitting the file")
						first_sent = False
						type = 'a'
					elif first_sent == False and packet[1]!='EOF' :
						chunk_received.received_data+=str(packet[1])
					if packet[1] == 'EOF':
						type = 'c'
					print("Received address :" +str(address))

				else:
					continue 		#We didn't find ack for the first message

		except Exception as e:
			exception_handler(e)
			print('Request timeout') #This is a timeout case

	print('The received message :' + chunk_received.received_data)





if __name__ == '__main__':

	#Input the file from the console
	# print("Enter the filename to download from the server: ")
	# file_name = input()
	connection_handler()



