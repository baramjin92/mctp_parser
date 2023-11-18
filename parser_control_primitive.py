#!/usr/bin/python

import sys
import csv
import random

from mctp_util import *

str_control_opcode = {
    # Figure 35
    0x00 : 'Pause',
    0x01 : 'Resume',
    0x02 : 'Abort',
    0x03 : 'Get State',
}

def parser_control_primitive_request(message) :
    message_length = len(message)

    opcode = message[4]
    tag = message[5]
    CPSP = get_word(message[6 : 8])
    MIC = get_dword(message[message_length - 4 : message_length])

    print('\n')
    print('opcode : 0x%02x [%s]'%(opcode, str_control_opcode[opcode]))
    print('tag : 0x%08x'%(tag))
    print('CPSP : 0x%08x'%(CPSP))
    print('MIC = 0x%08x'%MIC)

def parser_control_primitive_response(message) :
    message_length = len(message)

    status = message[4]
    tag = message[5]
    CPSP = get_word(message[6 : 8])
    MIC = get_dword(message[message_length - 4 : message_length])

    print('\n')
    print('STATUS = 0x%02x'%(status)) 
    print('tag : 0x%08x'%(tag))
    print('CPSP : 0x%08x'%(CPSP))
    print('MIC = 0x%08x'%MIC)

def parser_control_primitive(message, ror) :
    if ror == ROR_REQUEST :
        parser_control_primitive_request(message)
    elif ror == ROR_RESPONSE :
        parser_control_primitive_response(message)

if __name__ == '__main__' :  
    print('parser control_primitive')