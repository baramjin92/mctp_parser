#!/usr/bin/python

import sys
import csv
import random

from io import StringIO

from test_packet import *
from mctp_util import *
from parser_nvme_mi import *
from parser_nvme_admin import *
from parser_control_primitive import *
from parser_pcie_command import *

TITLE_STR = "mctp_parser"

debug_option = {
    'physical_header'   : False,
    'mctp_header'       : False,
    'mctp_message'      : False,
    'message_body'      : False
}

class mctp_packet :
    def __init__(self, packet) :
        self.packet = packet 

    def check_som(self) :
        print('check som')

    def check_eom(self) :
        print('check eom')

if __name__ == '__main__' :
    print(TITLE_STR)
    
    f = StringIO(test_packet_str)
    reader = csv.reader(f, delimiter=' ')
    for rows in reader :
        packet = []
        for value in rows :
            packet.append(int(value, base=16))

        #print('\n\npacket : ', packet)

        physical_header = packet[0 : 4]

        address1 = physical_header[0]
        protocol_type = physical_header[1]
        length = physical_header[2]
        address2 = physical_header[3]

        if debug_option['physical_header'] :
            print('physical header : ', physical_header)
            print('address1 0x%02x address2 0x%02x length 0x%02x'%(address1, address2, length))
            if protocol_type == 0x0F :
                print('==== mctp packet ====')

        mctp_packet_header = packet[4 : 8]
        header_version = mctp_packet_header[0] & 0x0F
        dest_ep_id = mctp_packet_header[1]
        src_ep_id = mctp_packet_header[2]
        seq_no = (mctp_packet_header[3] >> 4) & 0x03
        eom = (mctp_packet_header[3] >> 6) & 0x01
        som = (mctp_packet_header[3] >> 7) &0x01

        if debug_option['mctp_header'] :
            print('mctp header : ', mctp_packet_header)
            print('ver : 0x%02x'%header_version)
            print('som : %d, eom : %d, seq_no : %d'%(som, eom, seq_no))

        pec = packet.pop()
        mctp_packet_payload = packet[8 : 8 + (length-4)]

        if som == 1 :
            print('\n\nstart message')
            message = []

        for data in mctp_packet_payload :
            message.append(data)

        if debug_option['mctp_message'] :
            print('mctp payload : ', mctp_packet_payload)
            print('pec : ', pec)

        if eom == 1 :
            ror, nmimt, csi = parser_nvme_mi_header(message)

            if debug_option['message_body'] :
                print('message : ', message)
                print('messsage length : 0x%02x'%len(message))
                print('parsing' + str_nmimt[nmimt])

            if nmimt == 0 : 
                parser_control_primitive(message, ror)
            elif nmimt == 1 :
                parser_nvme_mi(message, ror)
            elif nmimt == 2 :
                parser_nvme_admin(message, ror)
            elif nmimt == 4 :
                parser_pcie_command(message, ror)
            