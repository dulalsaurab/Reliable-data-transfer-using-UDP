'''

'Client Program'
 Author: Saurab Dulal 
 Date. : October 16, 2017 
 Dependencies: Python 3+ 
 Description: Reliable data transfter using UDP  	

'''

import random
import socket
import time 
import os, sys
import pickle
import time
import hashlib 


#Some global variables 

sequence_counter =0
ack_counter  = 0
alternating_bit = 1
receiving_size = 2048
first_sent = True
type = 'd' #data request
total_packet_to_receive = None



def exception_handler(e):
	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	print('Type: %s' % (exc_type), 'On file: %s' % (fname), exc_tb.tb_lineno, 'Error: %s' % (e))


class file_handler():

	sequnceCount = [] #This will hold record of which chunk(seq) is written to a file
	global total_packet_to_receive

	def write_to_file(self, filename, data): #data {seq1:data, seq2:data }
			with open (filename, 'a+') as f: 
				for key in data.keys():
					
					if int(key) != 0 and int(key) != int(total_packet_to_receive):
						print(key,total_packet_to_receive)
						f.write(data[key])
					self.sequnceCount.append(key)


class _transport():
	
	#file is verified by the verify_packet method
	#once the packet is verified, its send to file handler to write
	#Only send those packet to file handler whose sequence is also verified 
	
	packet_received_sequence_number = 0 #this will remaing static 
	received_data = []  #we will hold ten packets at a time 

# 	#Receive response for the request send by client connection
# 	def receive_packet(self,packet):
# 		#verify the packet - checksum, sequence, and send response to client conn
# 		pass
#Disect packet and do the necessary stuffs

def verify_packet(packet): 
	

	checksum = packet[0]
	length = packet[1]
	seqNo = packet[2]
	msg = packet[3]

	if str(len(msg)) != packet[1]:
		return False
	else:
		received_checksum = hashlib.sha1(msg.encode('utf-8')).hexdigest()
		if received_checksum == checksum:
			return True	
	return False
	
#This class will create connection and will receive the response -
#After receiving the response it will send the response to transport for further verification

class _client_connection():

	#Create connection
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
		message, address = client_socket.recvfrom(receiving_size)
		return message, address


	def close_connection(self,client_socket):
		print("Closing socket connection")
		client_socket.close()


	def buffer_method(self):
		print("this is a buffer method")

	#also client connection will receive response from server and send it transport

#type - d=data, a=ack, r=retransmission
def create_packet(alternating_bit, protocol, message, file_name='', type='a',):

	global sequence_counter
	global ack_counter
	#create list for each message [seqnum,acknowledgement,data]

	#if Selective repeate is used, AB will always be equla to 1
	if protocol =='AB':
		packet = pickle.dumps([sequence_counter, ack_counter, message, file_name, type, alternating_bit])
		return packet

	else:
		packet = pickle.dumps([sequence_counter, ack_counter, message, file_name, type])
		return packet


def method_alternating_bit(packet,writeObject,chunk_received,address) : 
	
	global alternating_bit
	global first_sent 
	global type

	if alternating_bit == packet[2]:  

		#we have got the right packet, so lets write it to file
		alternating_bit ^= 1

		if first_sent:
			print("File is found on the server, now server will start transmitting the file")
			first_sent = False
			type = 'a'
		
		elif first_sent == False and packet[1][3]!='EOF' :
			try:
				writeObject.write_to_file('some_test_file_received', packet[1])
			except Exception as e:
				exception_handler(e)
				return False

			chunk_received.received_data.push(str(packet[1]))

		if packet[1][3]=='EOF':
			type = 'c'

		print("Received address :" +str(address)) 

	else:
		return False

	return True 

def missing_elements(L): #this will return missing sequence number
    start, end = L[0], L[-1]
    return sorted(set(range(start, end + 1)).difference(L))


def selective_repeate(packet_buffer,transport_object):
	
	#short the packet by sequence number, and find which sequence are missing 
	global type, total_packet_to_receive
	available_sequence  = [key for key in packet_buffer.keys()]
	
	if total_packet_to_receive == None:
		try:
			total_packet_to_receive = packet_buffer[0] #setting total packet to receive 
		except Exception as e:
			pass 
	missing_sequence = missing_elements(available_sequence)
	if not missing_sequence:
		transport_object.packet_received_sequence_number = max(available_sequence)
		if 'EOF' in packet_buffer.values():
			type = 'c'	
	
	return missing_sequence
	

def connection_handler_selective_repeate(file_name = None):
	
	global type, total_packet_to_receive
	protocol = 'SR' #selective repeate
	request_message = []
	file_name = 'some_test_file'
	connection_object = _client_connection() 
	transport = _transport()
	parallel_receive = 10 #default receive count 
	writeObject = file_handler()

	if connection_object.create_client_socket():
		print("Client socket created: " + str(connection_object.client_socket))
	else:
		print("Failled to create client socket, restart the client program")
		return
	counter = 0
	packet_buffer = {}
	while True: 
		sending_packet = create_packet(alternating_bit,protocol,request_message,file_name, type)
		try:
			connection_object.send_request_to_server(sending_packet, connection_object.address, connection_object.client_socket)

			if type == 'c':
				print("The transfer completed, process terminating !! ")
				break

			for x in range(0, parallel_receive):


				message, address = connection_object.receive_response_from_server(connection_object.client_socket)
				packet = pickle.loads(message)
				
				#[checksum, length of data, sequence number, msg]
				if packet:
					if verify_packet(packet):
						packet_buffer.update({packet[2]:packet[3]})#[{seqNo:message}]
							

			missing_sequence_number = selective_repeate(packet_buffer,transport) #check if any packets are not received 

			print("missing sequence number: "+ str(missing_sequence_number))
			
			if missing_sequence_number:
				request_message = missing_sequence_number #if some sequence are missing, ask these missing sequence from server
				parallel_receive = len(request_message)
			else:
				
				writeObject.write_to_file('some_test_file_received',packet_buffer)	

				if int(total_packet_to_receive) - int(transport.packet_received_sequence_number) <=10:
					parallel_receive = int(total_packet_to_receive) - int(transport.packet_received_sequence_number)
				else:
					parallel_receive = 10 #if all packets received, ask for next 10 packets
				print(parallel_receive)

				missing_sequence_number=[]
				packet_buffer = {}


		except Exception as e:
			exception_handler(e)
			print("Request timeout")



def connection_handler_alternating_bit(file_name='some_test_file_xputer'):

	global alternating_bit
	global first_sent
	global type
	chunk_received = _transport()
	writeObject = file_handler()
	file_name = file_name
	protocol = 'AB' #selective repeate
	request_message ='Innitial Request'
	file_name = file_name

	#create a conn object
	connection_object  = _client_connection()
	if connection_object.create_client_socket():
		print("Client socket created: " + str(connection_object.client_socket))
	else:
		print("Failled to create client socket, restart the client program")
		return

	counter = 0
	while True:
		sending_packet = create_packet(alternating_bit,'AB', request_message,file_name, type)

		try:
			
			connection_object.send_request_to_server(sending_packet, connection_object.address, connection_object.client_socket)
			
			''' The last message from client to server will be type=c i.e. complete, and server will close conn after receiving type 'c'''
			if type == 'c':
				print("The transfer process completed, process terminating !!")
				break

			message, address = connection_object.receive_response_from_server(connection_object.client_socket)

			packet = pickle.loads(message)  #0=counter, 1=data, 2=ALTbit
			if 'No such file or director' in packet[1][3]:
				print(packet[1][3])
				break
			if packet:
				#check if packet is ok or not
				if verify_packet(packet[1]):
			 	
			 		#Implementation of alternative bit 
					if method_alternating_bit(packet, writeObject, chunk_received, address) == False:
						continue 
			
				else:
					print("Packet not received or is corrupted")
					print("resending the request")
					continue

		except Exception as e:
			exception_handler(e)
			print('Request timeout') #This is a timeout case

	# print('The received message :' + chunk_received.received_data)



if __name__ == '__main__':

	#Input the file from the console
	# print("Enter the filename to download from the server: ")
	# file_name = input()
	connection_handler_selective_repeate()



