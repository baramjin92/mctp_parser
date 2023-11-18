#!/usr/bin/python

import sys
import csv
import random

from mctp_util import *

from mctp_util import *

str_pcie_opcode = {
    # Figure 128
    0x00 : 'PCIe Configuration Read',
    0x01 : 'PCIe Configuration Write',
    0x02 : 'PCIe Memory Read',
    0x03 : 'PCIe Memroy Write',
    0x04 : 'PCIe I/O Read',
    0x05 : 'PCIe I/O Write',
}

def parser_pcie_command_request(message) :
    message_length = len(message)

    opcode = message[4]
    controller_id = get_word(message[6 : 8])

    # Figure 126
    PCIE_DW0 = get_dword(message[8 : 12])
    PCIE_DW1 = get_dword(message[12 : 16])
    PCIE_DW2 = get_dword(message[16 : 20])
    len_req_data = (message_length - 4) - 20
    MIC = get_dword(message[message_length - 4 : message_length])

    print('\n')
    print('opcode : 0x%02x [%s], controller_id : 0x%04x'%(opcode, str_pcie_opcode[opcode], controller_id))
    print('SQEDW1 : 0x%08x'%(PCIE_DW0))
    print('SQEDW2 : 0x%08x'%(PCIE_DW1))
    print('SQEDW3 : 0x%08x'%(PCIE_DW2))
    print('length of req data : %x'%(len_req_data))
    print('MIC = 0x%08x'%MIC)

def parser_pcie_command_response(message) :
    message_length = len(message)

    # Figure 129
    status = message[4]
    len_rsp_data = (message_length - 4) - 8
    MIC = get_dword(message[message_length - 4 : message_length])

    print('\n')
    print('STATUS = 0x%02x'%(status)) 
    print('length of rsp data : 0x%02x'%(len_rsp_data))
    print('MIC = 0x%08x'%MIC)

def parser_pcie_command(message, ror) :
    if ror == ROR_REQUEST :
        parser_pcie_command_request(message)
    elif ror == ROR_RESPONSE :
        parser_pcie_command_response(message)

if __name__ == '__main__' :  
    print('parser pcie command')