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

"""
A NOTE TO USERS WHO ARE USING WINDOWS:
TURN OFF WINDOWS DEFENDER FIREWALL OR THIS PROGRAM WILL NOT WORK!
"""

import argparse
import secrets
import socket
import struct
import time
from ICMPChecksum import calculateChecksum

version = '0.1.0'


class ICMPTraceRoute4:
    """
    Define all the essential content for making a complete ICMP IPv4 Traceroute.
    """
    destinationAddress = ''
    timeout = 3
    ttl = 1
    icmpSocket = None
    icmpPacket = None

    def __init__(self, destinationAddress, timeout, ttl):
        self.destinationAddress = destinationAddress
        self.timeout = timeout
        self.ttl = ttl
        self.icmpSocket = self.createICMPSocket()
        self.icmpPacket = self.createICMPPacket()

    def createICMPSocket(self):
        # Create ICMP socket
        icmpSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
        # Set TTL in IP header
        icmpSocket.setsockopt(socket.getprotobyname("ip"), socket.IP_TTL, self.ttl)

        return icmpSocket

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
        icmp_id = 1
        icmp_sequence = 1

        payload = secrets.token_bytes(64)    # Build a random data which size as self.icmpDataSize.

        icmp_header = struct.pack('BBHHH', icmp_echo_request, icmp_echo_code, icmp_checksum, icmp_id, icmp_sequence)
        icmp_checksum = calculateChecksum(icmp_header + payload)
        icmp_header = struct.pack('BBHHH', icmp_echo_request, icmp_echo_code, socket.htons(icmp_checksum), icmp_id,
                                  icmp_sequence)

        return icmp_header + payload

    def sendICMPRequest(self):
        # Send ICMP request
        self.icmpSocket.sendto(self.icmpPacket, (self.destinationAddress, 0))

    def receiveICMPReply(self):
        self.icmpSocket.settimeout(self.timeout)

        try:
            data, address = self.icmpSocket.recvfrom(1024)
            icmp_header = struct.unpack("BBHHH", data[20:28])
            return address[0], icmp_header[0]
        except socket.timeout:
            return None, None


def traceroute(host, max_hops, timeout):
    """
    Full logic of traceroute a target host.
    :param host: Target host. IP or hostname accepted.
    :param max_hops: The maximum number of hops for the search target.
    :param timeout: Timeout waiting for response for each reply (in ms).
    :return:
    """
    destinationAddress = socket.gethostbyname(host)

    print(f"Tracking through up to {max_hops} hops")
    print(f"Routing to {host} [{destinationAddress}]:")

    for ttl in range(1, max_hops + 1):
        traceRoute = ICMPTraceRoute4(destinationAddress, timeout, ttl)
        # Send ICMP request
        traceRoute.sendICMPRequest()

        # Record start time
        startTime = time.time()

        # Receive ICMP reply
        address, icmpType = traceRoute.receiveICMPReply()

        # Record end time and calculate time
        endTime = time.time()
        elapsedTime = int((endTime - startTime) * 1000)

        # Close the socket
        traceRoute.icmpSocket.close()
        del traceRoute

        if address:
            print(f"{ttl}\t{address}\t{elapsedTime}ms")
            if icmpType == 0:
                print("Traceroute finished.")   # ICMP Type 0 means the message reached the target host, so break.
                break
        else:
            print(f"{ttl}\t*\ttimeout")


if __name__ == '__main__':
    # Build command line process
    commandParser = argparse.ArgumentParser(
        description=f"Traceroute.py {version} Copyright (c) 2023 Steven Song. Coursework for CNSCC203 Computer Networks "
                    f"2023.",
        epilog=f"Windows users shall make sure that you've turned off Windows Defender firewall.\n"
               f"Default firewall settings may block traceroute.")
    commandParser.add_argument('-j', metavar='maximum_hops', default=30, type=int,
                               help="The maximum number of hops for the search target.")
    commandParser.add_argument('-w', metavar='timeout', default=3000, type=int,
                               help="Time out waiting for each reply (in milliseconds).")
    commandParser.add_argument('target_host', type=str,
                               help="target host to traceroute. (DNS name or IP address)")
    commandOptions = commandParser.parse_args()

    # Do traceroute
    traceroute(commandOptions.target_host, commandOptions.j, commandOptions.w/1000)
