
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
alternating_bit  = 1

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
			self.server_socket.bind(self.server_address) #binding is only done in case of server
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

class file_handler():

	file_name = None
	file_sequence_counter = None
	file_content = [] #{sequence:data}

	def __init__(self):
		self.file_sequence_counter = -1

	def increase_sequence_counter(self):
		self.file_sequence_counter += 1
		return self.file_sequence_counter

	def file_read(self,file_name,type='s'): #s=stats, d=data
		#first iteration get every info about file
		self.file_name = file_name
		try:
			file_size = os.stat('some_test_file').st_size
			temp_counter = 0
			with open(file_name,'r') as f:
				for line in f:
					for character in line:
						self.file_content.append(character)
						temp_counter += 1
			self.file_content.append("EOF")

		except Exception as e:
			exception_handler(e)
			file_size = e

		return {'file_size':file_size}


class server_packet():

	def calculate_checksum(self):
		pass



def connection_handler():

	global alternating_bit
	file_object = file_handler()
	connection_object = server_connection()
	connection_object.create_connection()
	print("Server socket created: " +str(connection_object.server_socket))
	print("Server waiting for request")

	#Binary counter
	counter = 0

	while True:
		message, address= connection_object.server_socket.recvfrom(1024)
		message = pickle.loads(message) #1=seq, 2=ack, 3=mes, 4=file_name, 5=type, 6=alternating_bit

		if message:
			if message[4] == 'd':
				print('Received message from the client: ' + str(message[2]) +
					  '\nRequest file name :' + str(message[3])+
					  '\nAnd from the address: '+ str(address))
				#Check if the request file exist on the server or not
				file_stat = file_object.file_read(message[3])
				file_stat = pickle.dumps([counter,file_stat,alternating_bit])

				#connection_object.send_response_to_client(connection_object.server_socket,file_stat,address)
				alternating_bit ^= 1
				file_object.file_sequence_counter = -1 #whenever you received 'd' request, its always the begnning of the process

			if message[4] == 'a':
				#start sending message to the client, but only send by checking the alternating bit received
				print("Received ACK from client" + " Alternative bit :" +str(message[5]))
				if alternating_bit == message[5]:
					data = file_object.file_content[file_object.increase_sequence_counter()]
				else:
					data = file_object.file_content[file_object.file_sequence_counter]
				content = pickle.dumps([counter,data,alternating_bit])
				connection_object.send_response_to_client(connection_object.server_socket, content, address)
				alternating_bit ^= 1

			if message[4] == 'c':
				print("Transmission completed !!")
				break


		counter += 1

def main():
	connection_handler()



if __name__=='__main__':
	main()










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





