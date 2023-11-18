#!/usr/bin/python

import sys
import csv
import random

ROR_REQUEST = 0
ROR_RESPONSE = 1

def get_word(data) :
    w_data = (data[1] << 8) | data[0]
    return w_data

def get_dword(data) :
    dw_data = (data[3] << 24) | (data[2] << 16) | (data[1] << 8) | data[0]
    return dw_data

if __name__ == '__main__' :  
    print('mctp utility')