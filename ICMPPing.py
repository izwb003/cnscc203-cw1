#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Copyright (c) 2023 Steven Song

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import argparse
import random
import socket
import struct

version = '0.1.0'


class ICMPSocket4:
    destinationAddress = '127.0.0.1'
    icmpSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
    icmpPacket = None

    def __init__(self, targetHost, ID):
        self.destinationAddress = targetHost
        self.icmpPacket = self.createICMPPacket(ID)

    def connect(self, icmpPacket):
        self.icmpSocket.sendto(icmpPacket, (self.destinationAddress, 0))  # ICMP does not care about port, so 0 is OK.

    def createICMPPacket(self, ID):
        """
            Create ICMP Header as a "struct".
            Format:B as unsigned byte (8bit) for icmp_echo_request and icmp_echo_code;
                   H as unsigned short int (16bit) for icmp_checksum, icmp_id and icmp_sequence;
            [B:icmp_echo_request|B:icmp_echo_code|H:icmp_checksum|H:icmp_id|H:icmp_sequence][payload]
        """
        icmp_echo_request = 8
        icmp_echo_code = 0
        icmp_checksum = 0
        icmp_id = ID
        icmp_sequence = 1
        payload = b'qwertyuiopasdfghjklzxcvbnm'

        icmp_header = struct.pack('BBHHH', icmp_echo_request, icmp_echo_code, icmp_checksum, icmp_id, icmp_sequence)
        icmp_checksum = calculateChecksum(icmp_header + payload)
        icmp_header = struct.pack('BBHHH', icmp_echo_request, icmp_echo_code, socket.htons(icmp_checksum), icmp_id,
                                  icmp_sequence)

        return icmp_header + payload


def calculateChecksum(data):
    checksum = 0

    # Separate data into 16bit sub block and add them as sum
    for checkSumTime in range(0, len(data), 2):
        checksum += (data[checkSumTime] << 8) + (data[checkSumTime + 1])

    # Process with exceeded data
    checksum = (checksum >> 16) + (checksum & 0xFFFF)
    checksum += (checksum >> 16)

    # Get the checksum result by negation.
    return ~checksum & 0xFFFF


# def receiveOnePing(icmpSocket, destinationAddress, ID, timeout):

# def sendOnePing(icmpSocket, destinationAddress, ID):

# def doOnePing(destinationAddress, timeout):

# def ping(host, timeout):


if __name__ == '__main__':
    # Build command line process
    commandParser = argparse.ArgumentParser(
        description=f"ICMPPing.py {version} Copyright (c) 2023 Steven Song. Coursework for CNSCC203 Computer Networks "
                    f"2023.")
    commandParser.add_argument('-t', action='store_true', default=False,
                               help="ping the target host until stopped manually(Ctrl+C).")
    commandParser.add_argument('-c', metavar='count', default=4, type=int, help="stop after <count> times.")
    commandParser.add_argument('target_host', type=str, help="target host to ping. (DNS name or IP address)")
    commandOptions = commandParser.parse_args()

    # Do ping
    if commandOptions.t:
        while True:
            print("TODO: set ping command here")
            # ping(commandOptions.target_host)
    else:
        for pingTime in range(commandOptions.c):
            print("TODO: set ping command here")
            # ping(commandOptions.target_host)
