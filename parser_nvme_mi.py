#!/usr/bin/python

import sys
import csv
import random

from mctp_util import *

DEBUG_NVME_MI = False

str_ror = [
    'Request Message',
    'Response Message'
]

str_nmimt = [
    'Control Primitive', 
    'NVMe-MI Command',
    'NVMe Admin Commnad',
    'Reserved',
    'PCIe Commmand'
]

str_csi = [
    'Command Slot 0',
    'Command Slot 1'
]

def parser_nvme_mi_header(message) :
    message_type = message[0]
    ror = (message[1] >> 7) & 0x01
    nmimt = (message[1] >> 3) & 0x0F
    csi = (message[1]) & 0x01

    if DEBUG_NVME_MI :
        print('ROR : %s'%(str_ror[ror]))
        print('NMIMT : %s'%(str_nmimt[nmimt]))
        print('CSI : %s'%(str_csi[csi]))

    return ror, nmimt, csi

str_mi_opcode = {
    # Figure 57
    0x00 : 'Read NVMe-MI Data Structure',
    0x01 : 'NVM Subsystem Health Status Poll',
    0x02 : 'Controller Health Status Poll',
    0x03 : 'Configuration Set',
    0x04 : 'Configuration Get',
    0x05 : 'VPD Read',
    0x06 : 'VPD Write',
    0x07 : 'Reset',
    0x08 : 'SES Receive',
    0x09 : 'SES Send',
    0x0A : 'Management Endpoint Buffer Read',
    0x0B : 'Management Endpoint Buffer Write',
    0x0C : 'Shutdown',       
}

def parser_mi_request(message) :
    message_length = len(message)

    opcode = message[4]
    controller_id = get_word(message[6 : 8])

    # Figure 55 & 56
    NMD0 = get_dword(message[8 : 12])
    NMD1 = get_dword(message[12 : 16])
    len_req_data = (message_length - 4) - 16
    MIC = get_dword(message[message_length - 4 : message_length])

    print('\n')
    print('opcode : 0x%02x [%s]'%(opcode, str_mi_opcode[opcode]))
    print('NMD0 : 0x%08x'%(NMD0))
    print('NMD1 : 0x%08x'%(NMD1))
    print('length of req data : %x'%(len_req_data))
    print('MIC = 0x%08x'%MIC)

def parser_mi_response(message) :
    message_length = len(message)

    # Figure 60
    status = message[4]
    # NMRESP = message[5 : 8]
    len_rsp_data = (message_length - 4) - 8
    MIC = get_dword(message[message_length - 4 : message_length])

    print('\n')
    print('STATUS = 0x%02x'%(status)) 
    print('length of rsp data : 0x%02x'%(len_rsp_data))
    print('MIC = 0x%08x'%MIC)

def parser_nvme_mi(message, ror) :
    if ror == ROR_REQUEST :
        parser_mi_request(message)
    elif ror == ROR_RESPONSE :
        parser_mi_response(message)

if __name__ == '__main__' :  
    print('parser nvme mi')