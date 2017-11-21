
'''

'Server Program'
 Author: Saurab
 Date  : October 16, 2017 
 Dependencies: Python 3+ 
 Description:Reliable data transfer using UDP


'''

import random
import socket 
import datetime
import os, sys
import pickle
import hashlib 
import time 
receiving_size = 2048


sequence_counter = 0
ack_counter = 0
alternating_bit  = 1

# Don't forget
# 1. Every packet has got a sequence number, 
#	- and if some packet is lost, it can be asked again using that sequence number 
# 2. 


def exception_handler(e):
	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	print('Type: %s' % (exc_type), 'On file: %s' % (fname), exc_tb.tb_lineno, 'Error: %s' % (e))


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
			self.server_socket.bind(self.server_address) #Binding is only done in case of server
		except socket.error as err:
			exception_handler(e)
			return False
		return True


	def close_connection(self,server_socket):
		print("Closing server socket connection")
		server_socket.close()


	def send_response_to_client(self,server_socket,message,address):

		print("Sending request to the server")
		try:
			server_socket.sendto(message,address)  # message always needs to be in byte format
			print("Message sent sucessfull")

		except Exception as e:
			exception_handler(e)

class server_packet():
	checksum = 0
	length = 0
	seqNo = 0
	msg = 0
	total_packets = [] #this is a statis variable, this will hold the object of each packets
	
	@classmethod
	def increase_seqNumber(self):
		print(self.seqNo)
		self.seqNo += 1
		return self.seqNo

	def make_packet(self, data):
		self.total_packets.append(self)
		self.msg = data
		self.length = str(len(data))
		self.checksum=hashlib.sha1(data.encode('utf-8')).hexdigest()
		print ("Length: %s\n Sequence number: %s" % (self.length, self.increase_seqNumber()))
		return [self.checksum, self.length, self.seqNo, self.msg]

		


class file_handler(server_packet):

	file_name = None
	file_sequence_counter = None
	file_content = [] #{sequence:data}

	def __init__(self):
		self.file_sequence_counter = -1

	def increase_sequence_counter(self):
		self.file_sequence_counter += 1
		return self.file_sequence_counter

	
	def read_in_chunks(self, file_object, chunk_size=1024):
	
		'''Lazy function (generator) to read a file piece by piece.
		Default chunk size: 1k'''	
		while True:
			data = file_object.read(chunk_size)
			if not data:
				break
			yield data
	
	def file_read(self,file_name,type='s'): #s=stats, d=data
		#First iteration get every info about file
		self.file_name = file_name
		try:
			file_size = os.stat('some_test_file').st_size
			self.file_content.append(server_packet().make_packet(str(file_size)))

			temp_counter = 0
			with open(file_name,'r') as f:
				for piece in self.read_in_chunks(f):
					packet = server_packet()
					self.file_content.append(packet.make_packet(piece))
					temp_counter += 1
			
			self.file_content.append(server_packet().make_packet("EOF"))

		except Exception as e:
			exception_handler(e)
			file_size = e


def connection_handler():

	global alternating_bit

	file_object = file_handler()
	connection_object = server_connection()
	connection_object.create_connection()
	print("Server socket created: " +str(connection_object.server_socket))
	print("Server waiting for request")

	#Binary counter
	counter = 0
	AB_flag = False #only flip AB if AB_Client matches with AB server

	while True:
		# time.sleep(5)
		message, address= connection_object.server_socket.recvfrom(receiving_size)
		message = pickle.loads(message) #1=seq, 2=ack, 3=mes, 4=file_name, 5=type, 6=alternating_bit

		if message:
			if message[4] == 'd':
				print('Received message from the client: ' + str(message[2]) +
					  '\nRequest file name :' + str(message[3])+
					  '\nAnd from the address: '+ str(address))
				#Check if the request file exist on the server or not
				file_object.file_read(message[3])
				file_stat = file_object.file_content[file_object.increase_sequence_counter()]
				file_stat = pickle.dumps([counter,file_stat,alternating_bit])
				connection_object.send_response_to_client(connection_object.server_socket,file_stat,address)
				alternating_bit ^= 1
				file_object.file_sequence_counter = 0 #whenever you received 'd' request, its always the begnning of the process

			if message[4] == 'a':
				#start sending message to the client, but only send by checking the alternating bit received
				print("Received ACK from client" + " Alternative bit :" +str(message[5]) +"and type :" + str(message[4]))
				if alternating_bit == message[5]:
					data = file_object.file_content[file_object.increase_sequence_counter()]
					AB_flag = True
					
				else:
					data = file_object.file_content[file_object.file_sequence_counter]
					AB_flag = False

				content = pickle.dumps([counter,data,alternating_bit])
				connection_object.send_response_to_client(connection_object.server_socket, content, address)
				
				if AB_flag:
					alternating_bit ^= 1

			if message[4] == 'c':
				
				print("Transmission completed !!")
				connection_object.close_connection(connection_object.server_socket)
				break


		counter += 1

def main():
	connection_handler()



if __name__=='__main__':
	main()






