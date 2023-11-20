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
import secrets
import select
import socket
import struct
import time

version = '0.1.0'


class ICMPPing4:
    """
    Define all the essential content for making a complete IPv4 ICMPPing connection.
    """
    destinationAddress = '127.0.0.1'
    timeout = 2000
    icmpDataSize = 32
    icmpSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
    icmpID = 0
    icmpPacket = None

    def __init__(self, targetHost, ID, dataSize, timeout):
        self.destinationAddress = targetHost
        self.icmpDataSize = dataSize
        self.icmpID = ID
        self.icmpPacket = self.createICMPPacket()
        self.timeout = timeout/1000

    def sendOnePing(self):
        """
        Send a Ping request to the target host.
        :return: None.
        """

        # ICMP does not care about port, so 0 is OK.
        self.icmpSocket.sendto(self.icmpPacket, (self.destinationAddress, 0))

    def receiveOnePing(self):
        timeLeft = self.timeout

        while True:
            selectStartTime = time.time()
            selectMonitor = select.select([self.icmpSocket], [], [], timeLeft)
            elapsedTime = (time.time() - selectStartTime)

            if not selectMonitor[0]:
                return None, None, None

            receivedTime = time.time()
            receivedPacket, address = self.icmpSocket.recvfrom(1024)

            receivedICMPHeader = receivedPacket[20:28]
            receivedIPHeader = receivedPacket[:20]

            TTL = struct.unpack("!B", receivedIPHeader[8:9])[0]

            icmpType, code, checksum, packetID, sequence = struct.unpack("BBHHH", receivedICMPHeader)
            dataSize = len(receivedPacket) - 28

            timeLeft -= elapsedTime

            if packetID == self.icmpID:
                return dataSize, (receivedTime - selectStartTime)*1000, TTL

            if timeLeft <= 0:
                return None, None, None

    def createICMPPacket(self):
        """
            Create ICMP Header as a "struct", fill with payload data.
            Format:B as unsigned byte (8bit) for icmp_echo_request and icmp_echo_code;
                   H as unsigned short int (16bit) for icmp_checksum, icmp_id and icmp_sequence;
            [B:icmp_echo_request|B:icmp_echo_code|H:icmp_checksum|H:icmp_id|H:icmp_sequence][payload]
            :return: The created ICMP packet.
        """
        icmp_echo_request = 8
        icmp_echo_code = 0
        icmp_checksum = 0
        icmp_id = self.icmpID
        icmp_sequence = 1

        payload = secrets.token_bytes(self.icmpDataSize)    # Build a random data which size as self.icmpDataSize.

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


def doOnePing4(destinationAddress, timeout, dataSize):
    """
    Full logic of complete one ping request for IPv4.
    :param destinationAddress: Target host. IP only.
    :param timeout: Timeout waiting for response (in ms).
    :param dataSize: The size of the payload data.
    :return:
    """
    ID = random.randint(0, 65535)
    icmpPing = ICMPPing4(destinationAddress, ID, dataSize, timeout)
    icmpPing.sendOnePing()
    returnedDataSize, returnedDelay, returnedTTL = icmpPing.receiveOnePing()
    return returnedDataSize, returnedDelay, returnedTTL


def ping(host, timeout, dataSize, pingTime):
    """
    Full logic of pinging a target host.
    :param host: Target host. IP or hostname accepted.
    :param timeout: Timeout waiting for response (in ms).
    :param dataSize: Size of send data payload.
    :param pingTime: How many times to ping. -1 for non-stop.
    :return:
    """
    try:
        destinationAddress = socket.gethostbyname(host)
    except socket.gaierror:
        print("Error: Invalid hostname or IP address.")
        return

    if destinationAddress == host:
        print(f"Pinging {destinationAddress} with {dataSize} bytes of data:")
    else:
        print(f"Pinging {destinationAddress} [{host}] with {dataSize} bytes of data:")

    if pingTime == -1:
        while True:
            returnDataSize, delay, returnTTL = doOnePing4(destinationAddress, timeout, dataSize)
            if delay is not None:
                print(f"Reply from {destinationAddress}: Data size={returnDataSize}, Time={delay}ms, TTL={returnTTL}")
            else:
                print("Request timed out.")
    else:
        for loopTime in range(pingTime):
            returnDataSize, delay, returnTTL = doOnePing4(destinationAddress, timeout, dataSize)
            if delay is not None:
                print(f"Reply from {destinationAddress}: Data size={returnDataSize}, Time={delay}ms, TTL={returnTTL}")
            else:
                print("Request timed out.")


if __name__ == '__main__':
    # Build command line process
    commandParser = argparse.ArgumentParser(
        description=f"ICMPPing.py {version} Copyright (c) 2023 Steven Song. Coursework for CNSCC203 Computer Networks "
                    f"2023.")
    commandParser.add_argument('-t', action='store_true', default=False,
                               help="ping the target host until stopped manually(Ctrl+C).")
    commandParser.add_argument('-c', metavar='count', default=4, type=int, help="stop after <count> times.")
    commandParser.add_argument('-l', metavar='size', default=32, type=int, help="send buffer size.")
    commandParser.add_argument('-w', metavar='timeout', default=2000, type=int, help="timeout waiting for response(ms).")
    commandParser.add_argument('target_host', type=str, help="target host to ping. (DNS name or IP address)")
    commandOptions = commandParser.parse_args()

    # Do ping
    if not commandOptions.t:
        ping(commandOptions.target_host, commandOptions.w, commandOptions.l, commandOptions.c)
    else:
        ping(commandOptions.target_host, commandOptions.w, commandOptions.l, -1)
