#!/usr/bin/python

import sys
import csv
import random

from mctp_util import *

DEBUG_ADMIN = False

str_opcode = {
    # Figure 114
    0x00 : 'Abort',
    0x0C : 'Async Event Reqeust',
    0x20 : 'Capacity Management',
    0x05 : 'Create I/O Completion Queue',
    0x01 : 'Create I/O Submission Queue',
    0x04 : 'Delete I/O Completion Queue',
    0x00 : 'Delete I/O Submission Queue',
    0x14 : 'Device Self-test',
    0x1A : 'Directive Receive',
    0x19 : 'Directive Send',
    0x7C : 'Doorbell Buffer Config',
    0x10 : 'Firmware Commit',
    0x11 : 'Firmware Image Download',
    0x80 : 'Format NVM',
    0x0A : 'Get Features',
    0x86 : 'Get LBA Status',
    0x02 : 'Get Log Page',
    0x06 : 'Identify',
    0x18 : 'Keep Alive',
    0x24 : 'Lockdown',
    0x0D : 'Namespace Management',
    0x15 : 'Namespace Attachment',
    0x1D : 'NVMe-MI Receive',
    0x1E : 'NVMe-MI Send',
    0x84 : 'Sanitize',
    0x81 : 'Security Send',
    0x82 : 'Security Receive',
    0x09 : 'Set Features',
    0x1C : 'Virtualization Managment',
    0x7F : 'Fabrics Commands'
}

def parser_nvme_admin_request(message) :
    message_length = len(message)

    opcode = message[4]
    command_flag = message[5]
    controller_id = get_word(message[6 : 8])

    SQEDW1 = get_dword(message[8 : 12])
    SQEDW2 = get_dword(message[12 : 16])
    SQEDW3 = get_dword(message[16 : 20])
    SQEDW4 = get_dword(message[20 : 24])
    SQEDW5 = get_dword(message[24 : 28])
    DATA_OFFSET = get_dword(message[28 : 32])
    DATA_LENGTH = get_dword(message[32 : 36])
    SQEDW10 = get_dword(message[44 : 48])
    SQEDW11 = get_dword(message[48 : 52])
    SQEDW12 = get_dword(message[52 : 56])
    SQEDW13 = get_dword(message[56 : 60])
    SQEDW14 = get_dword(message[60 : 64])
    SQEDW15 = get_dword(message[64 : 68])
    len_req_data = (message_length - 4) - 68
    MIC = get_dword(message[message_length - 4 : message_length])

    print('\n')
    print('opcode : 0x%02x [%s], command_flag : 0x%02x, controller_id : 0x%04x'%(opcode, str_opcode[opcode], command_flag, controller_id))
    print('SQEDW1 : 0x%08x'%(SQEDW1))
    print('SQEDW2 : 0x%08x'%(SQEDW2))
    print('SQEDW3 : 0x%08x'%(SQEDW3))
    print('SQEDW4 : 0x%08x'%(SQEDW4))
    print('SQEDW5 : 0x%08x'%(SQEDW5))
    print('DATA_OFFSET : 0x%08x'%(DATA_OFFSET))
    print('DATA_LENGTH : 0x%08x'%(DATA_LENGTH))
    print('SQEDW10 : 0x%08x'%(SQEDW10))
    print('SQEDW11 : 0x%08x'%(SQEDW11))
    print('SQEDW12 : 0x%08x'%(SQEDW12))
    print('SQEDW13 : 0x%08x'%(SQEDW13))
    print('SQEDW14 : 0x%08x'%(SQEDW14))
    print('SQEDW15 : 0x%08x'%(SQEDW15))
    print('length of req data : %x'%(len_req_data))
    print('MIC = 0x%08x'%MIC)

def parser_nvme_admin_response(message) :
    message_length = len(message)

    status = message[4]
    CQED0 = get_dword(message[8 : 12])
    CQED1 = get_dword(message[12 : 16])
    CQED2 = get_dword(message[16 : 20])
    len_rsp_data = (message_length - 4) - 20
    MIC = get_dword(message[message_length - 4 : message_length])

    print('\n')
    print('STATUS = 0x%02x'%(status))
    print('CQED0 : 0x%08x'%(CQED0))
    print('CQED1 : 0x%08x'%(CQED1))
    print('CQED2 : 0x%08x'%(CQED2))    
    print('length of rsp data : 0x%02x'%(len_rsp_data))
    print('MIC = 0x%08x'%MIC)

def parser_nvme_admin(message, ror) :
    if ror == ROR_REQUEST :
        parser_nvme_admin_request(message)
    elif ror == ROR_RESPONSE :
        parser_nvme_admin_response(message)

if __name__ == '__main__' :  
    print('parser nvme admin')