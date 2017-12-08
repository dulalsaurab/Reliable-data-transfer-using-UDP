#!/bin/bash
'''
'Server Program'
 Author: Saurab Dulal 
 Date  : October 16, 2017 
 Dependencies: Python 3+ 
 Description:Reliable data transfer using UDP
 License: wtfpl 
'''
import random
import socket 
import datetime
import os, sys
import pickle
import hashlib 
import time 
import copy
from server_config import server_globals as gb

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
    print("Initializing ip address and port number")
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
      a = pickle.loads(message) #getting sequence number 
      server_socket.sendto(message,address)  # message always needs to be in byte format

      print("Message sent successful\n Sequence number : {}".format(a[2]))

    except Exception as e:
      exception_handler(e)

class server_packet():
  checksum = 0
  length = 0
  seqNo = 0
  msg = 0
  total_packets = [] #this is a static variable, this will hold the object of each packets
  total_number_of_packets = 0

  @classmethod
  def increase_seqNumber(self):
    self.seqNo += 1
    return self.seqNo

  def make_packet(self, data):

    
    self.total_packets.append(self)
    self.msg = data
    self.length = str(len(data))
    self.checksum=hashlib.sha1(data.encode('utf-8')).hexdigest()
    # print ("Length: %s\n Sequence number: %s" % (self.length, self.increase_seqNumber()))
    return [self.checksum, self.length, self.increase_seqNumber(), self.msg]

class file_handler(server_packet):
  file_name = None
  file_sequence_counter = -1
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
    self.file_name = file_name
    counter = 0
    packet = server_packet()
    
    try:
      file_size = os.stat(file_name).st_size
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
      self.file_content.append(server_packet().make_packet(str(e)))

    #update first packet with total no of packet info 
    packet.total_number_of_packets = len(self.file_content) #total number of packets available 
    self.file_content.insert(0,server_packet().make_packet(str(len(self.file_content)))) #insert at 0th position 
    self.file_content[0][2] = 0
    
def method_alternating_bit(message, connection_object, file_object, counter, address):
  AB_flag = False #only flip AB if AB_Client matches with AB server
  
  if gb.alternating_bit == message[5]:
    data = file_object.file_content[file_object.increase_sequence_counter()]
    AB_flag = True    
  else:
    data = file_object.file_content[file_object.file_sequence_counter]
    AB_flag = False

  content = pickle.dumps([counter,data,gb.alternating_bit])
  connection_object.send_response_to_client(connection_object.server_socket, content, address)

  if AB_flag:
    gb.alternating_bit ^= 1
  return

def get_packets(file_object, seq_list):
  packet_list = []
  loop_counter = copy.deepcopy(file_object.file_sequence_counter)
  #Determine no of packet to be send
  loop_range = 0 
  
  if len(file_object.file_content) - loop_counter <= 10: 
    loop_range = len(file_object.file_content) -1 
  else:
    loop_range = 10 + loop_counter

  if not seq_list:
    for x in range(loop_counter, loop_range):     
      packet_list.append(file_object.file_content[int(file_object.increase_sequence_counter())])
  else:
    for x in seq_list:   #x are all the missing sequence 
      packet_list.append(file_object.file_content[x])
  return packet_list

def selective_repeate(message, file_name, file_object): #2 message, #3 is filename 
  #First check if file is found or not, if not found send, just one message with file not found exception
  #send blocks of 10 packets at a time 
  if not file_object.file_content:
    file_object.file_read(file_name) #packets list will be created by this time 
    #send the desired message
  return get_packets(file_object, message)
    

def connection_handler_selective_repeat(file_object, connection_object):  
  counter = 0 
  while True:
    message, address = connection_object.server_socket.recvfrom(gb.receiving_size)
    message = pickle.loads(message)
    
    if message:
      if message[4] == 'd':
        print('Received request from the client: ' + str(message[2]) +
            '\nRequest file name :' + str(message[3])+
            '\nAnd from the address: '+ str(address))
        packets_to_be_send = selective_repeate(message[2], message[3], file_object)   #2 message, #3 is filename 
        #loop through and send all the available packets 
        for x in range(0,len(packets_to_be_send)):
          sending_packet = pickle.dumps(packets_to_be_send[x])
          connection_object.send_response_to_client(connection_object.server_socket,sending_packet,address)   
      elif message[4] == 'c':
        print("Transmission completed !!")
        connection_object.close_connection(connection_object.server_socket)
        break

def connection_handler_alternating_bit(file_object, connection_object):
  counter = 0
  while True:
    message, address= connection_object.server_socket.recvfrom(gb.receiving_size)
    message = pickle.loads(message) #1=seq, 2=ack, 3=mes, 4=file_name, 5=type, 6=alternating_bit
    
    if message:
    
      if message[4] == 'd':
        print('Received request from the client: ' + str(message[2]) +
            '\nRequest file name :' + str(message[3])+
            '\nAnd from the address: '+ str(address))
        #Check if the request file exist on the server or not
        file_object.file_read(message[3])
        file_stat = file_object.file_content[file_object.increase_sequence_counter()]
        file_stat = pickle.dumps([counter,file_stat,gb.alternating_bit])
        connection_object.send_response_to_client(connection_object.server_socket,file_stat,address)
        gb.alternating_bit ^= 1
        file_object.file_sequence_counter = 0 #whenever you received 'd' request, its always the beginning of the process

      if message[4] == 'a':
        #start sending message to the client, but only send by checking the alternating bit received
        print("Received ACK from client" + " Alternative bit : " +str(message[5]) +"and type :" + str(message[4]))    
        method_alternating_bit(message, connection_object, file_object, counter, address)
        
      if message[4] == 'c':
        print("Transmission completed !!")
        connection_object.close_connection(connection_object.server_socket)
        break
    counter += 1

if __name__=='__main__':

  file_object = file_handler()
  connection_object = server_connection()
  connection_object.create_connection()
  print("Server socket created: " +str(connection_object.server_socket))
  print("Server waiting for request")

  connection_handler_alternating_bit(file_object, connection_object)
  # connection_handler_selective_repeat(file_object, connection_object)





