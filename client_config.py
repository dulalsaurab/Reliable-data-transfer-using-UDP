#!/bin/bash

class client_globals:
    #Client global variables 
    sequence_counter =0
    ack_counter  = 0
    alternating_bit = 1
    receiving_size = 2048
    first_sent = True
    type = 'd' #data request
    total_packet_to_receive = None