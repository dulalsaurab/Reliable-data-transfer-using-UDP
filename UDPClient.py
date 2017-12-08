#!/bin/bash
'''
'Client Program'
 Author: Saurab Dulal 
 Date. : October 16, 2017 
 Dependencies: Python 3+ 
 Description: Reliable data transfer using UDP
'''
import random
import socket
import time 
import os, sys
import pickle
import time
import hashlib 
from client_config import client_globals as gb

def exception_handler(e):
  exc_type, exc_obj, exc_tb = sys.exc_info()
  fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
  print('Type: %s' % (exc_type), 'On file: %s' % (fname), exc_tb.tb_lineno, 'Error: %s' % (e))

#This function will return missing sequence of number between consecutive numbers in a list 
def missing_elements(L): 
    start, end = L[0], L[-1]
    return sorted(set(range(start, end + 1)).difference(L))

#Transport method
class file_handler():
  sequnceCount = [] #This will hold record of which chunk(seq) is written to a file
  def write_to_file(self, filename, data): #data {seq1:data, seq2:data }
      with open (filename, 'a+') as f: 
        for key in data.keys(): 
          if int(key) != 0 and int(key) != 1 and int(key) != int(gb.total_packet_to_receive):
            print(key,gb.total_packet_to_receive)
            f.write(data[int(key)])
          self.sequnceCount.append(int(key))

#Transport method
def verify_packet(self, packet): 
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

#Transport method
#type - d=data, a=ack, r=retransmission
def create_packet(self, alternating_bit, protocol, message, file_name='', type='a',):
  #Create list for each message [sequence number, acknowledgment, data]
  #Note: if Selective repeat is used, AB will always be equal to 1
  
  if protocol =='AB':
    packet = pickle.dumps([gb.sequence_counter, gb.ack_counter, message, file_name, type, alternating_bit])
    return packet
  else:
    packet = pickle.dumps([gb.sequence_counter, gb.ack_counter, message, file_name, type])
    return packet

#Transport method
def method_alternating_bit(self, packet, writeObject, chunk_received, address) : 

  if gb.alternating_bit == packet[2]:  
    #we have got the right packet, so lets write it to file
    gb.alternating_bit ^= 1
    if gb.first_sent:
      print("File is found on the server, now server will start transmitting the file")
      gb.total_packet_to_receive = packet[1][3] #setting total packet to receive
      gb.first_sent = False
      gb.type = 'a'
    elif gb.first_sent == False and packet[1][3]!='EOF' :
      try:
        writeObject.write_to_file('some_test_file_received', {int(packet[0]):str(packet[1][3])})
      except Exception as e:
        exception_handler(e)
        return False
      chunk_received.received_data.append(str(packet[1]))
    if packet[1][3]=='EOF':
      gb.type = 'c'
    print("Received address :" +str(address)) 
  else:
    return False
  return True 

#Transport method
def selective_repeate(self, packet_buffer,transport_object):
  #sort the packet by sequence number, and find which sequence are missing 
  available_sequence  = [key for key in packet_buffer.keys()]
  if gb.total_packet_to_receive == None:
    try:
      gb.total_packet_to_receive = packet_buffer[0] #setting total packet to receive 
    except Exception as e:
      pass 
  missing_sequence = missing_elements(available_sequence)
  if not missing_sequence:
    transport_object.packet_received_sequence_number = max(available_sequence)
    if 'EOF' in packet_buffer.values():
      gb.type = 'c' 
  return missing_sequence
  

class _transport():
  packet_received_sequence_number = 0 #this will reaming static 
  received_data = []  #we will hold ten packets at a time 
  
  def __init__(self):
    _transport.verify_packet = verify_packet
    _transport.create_packet = create_packet
    _transport.method_alternating_bit = method_alternating_bit
    _transport.selective_repeate = selective_repeate
  
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
    try:
      self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      self.client_socket.settimeout(2)  #2 second time out set
    except socket.error as err:
      exception_handler(err)
      return False
    return True

  def send_request_to_server(self, message, address, client_socket):
    print("Sending request to the server")
    try:
      send = client_socket.sendto(message,address) #message always needs to be in byte format
    except Exception as e:
      exception_handler(e)

  def receive_response_from_server(self,client_socket):
    message, address = client_socket.recvfrom(gb.receiving_size)
    return message, address

  def close_connection(self,client_socket):
    print("Closing socket connection")
    client_socket.close()

def connection_handler_selective_repeate(transport, writeObject, connection_object, request_message=[], file_name = "some_test_file", protocol='SR'):
  parallel_receive = 10 #default receive count 
  counter = 0
  packet_buffer = {}

  while True: 
    sending_packet = transport.create_packet(gb.alternating_bit,protocol,request_message,file_name, gb.type)
    try:
      connection_object.send_request_to_server(sending_packet, connection_object.address, connection_object.client_socket)

      if gb.type == 'c':
        print("The transfer completed, process terminating !! ")
        break

      for x in range(0, parallel_receive):
        message, address = connection_object.receive_response_from_server(connection_object.client_socket)
        packet = pickle.loads(message)
        if 'No such file or director' in packet[3]:
          print(packet[3])
          return #return from the client program
        if packet:
          if transport.verify_packet(packet):
            packet_buffer.update({packet[2]:packet[3]})#[{seqNo:message}]

      missing_sequence_number = transport.selective_repeate(packet_buffer,transport) #check if any packets are not received 
      print("missing sequence number: "+ str(missing_sequence_number))

      if missing_sequence_number:
        request_message = missing_sequence_number #if some sequence are missing, ask these missing sequence from server
        parallel_receive = len(request_message)
      else:
        
        writeObject.write_to_file('some_test_file_received',packet_buffer)  
        if int(gb.total_packet_to_receive) - int(transport.packet_received_sequence_number) <=10:
          parallel_receive = int(gb.total_packet_to_receive) - int(transport.packet_received_sequence_number)
        else:
          parallel_receive = 10 #if all packets received, ask for next 10 packets
        print(parallel_receive)
        missing_sequence_number=[]
        packet_buffer = {}
    except Exception as e:
      exception_handler(e)
      print("Request timeout")

def connection_handler_alternating_bit(chunk_received, writeObject, connection_object, request_message, file_name='some_test_file', protocol='AB'):
  counter = 0
  while True:
    sending_packet = chunk_received.create_packet(gb.alternating_bit,'AB', request_message, file_name, gb.type)
    try:      
      connection_object.send_request_to_server(sending_packet, connection_object.address, connection_object.client_socket)
      ''' The last message from client to server will be type=c i.e. complete, and server will close conn after receiving type 'c'''
      if gb.type == 'c':
        print("The transfer process completed, process terminating !!")
        break
      message, address = connection_object.receive_response_from_server(connection_object.client_socket)
      packet = pickle.loads(message)  #0=counter, 1=data, 2=ALTbit
      if 'No such file or director' in packet[1][3]:
        print(packet[1][3])
        break
      if packet:
        #check if packet is ok or not
        if chunk_received.verify_packet(packet[1]):
          #Implementation of alternative bit 
          if transport.method_alternating_bit(packet, writeObject, chunk_received, address) == False:
            continue 
        else:
          print("Packet not received or is corrupted")
          print("resending the request")
          continue
    except Exception as e:
      exception_handler(e)
      print('Request timeout') #This is a timeout case


if __name__ == '__main__':

  print("Enter a file name to download from the server")
  file_name = input()
  print("File name :{}".format(file_name))
  transport = _transport()
  writeObject = file_handler()
  file_name = "some_test_file"
  request_message ='Initial Request'

  #Create connection object
  connection_object  = _client_connection()
  if connection_object.create_client_socket():
    print("Client socket created: " + str(connection_object.client_socket))
  else:
    print("Failed to create client socket, restart the client program")
    exit()
  
  connection_handler_alternating_bit(transport, writeObject, connection_object, "Initial Request", file_name, 'AB')
  # connection_handler_selective_repeate(transport, writeObject, connection_object, [], file_name, 'SR')



