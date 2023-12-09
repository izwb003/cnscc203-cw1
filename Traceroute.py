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
import socket
import struct
import time
from ICMPChecksum import calculateChecksum

version = '0.1.0'


class TraceRoute4:
    """
    Define all the essential content for making a complete IPv4 Traceroute.
    """
    destinationAddress = ''
    timeout = 3
    icmpSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
    icmpID = 1
    icmpPacket = None

    def __init__(self, targetHost, timeout):
        self.destinationAddress = targetHost
        self.timeout = timeout
        self.icmpPacket = self.createICMPPacket()

    def sendICMPRequest(self, ttl):
        # Set TTL to IP header
        self.icmpSocket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)

        # Send ICMP packet
        # ICMP does not care about port, so 0 is OK.
        self.icmpSocket.sendto(self.icmpPacket, (self.destinationAddress, 0))

    def receiveICMPReply(self):
        # Set ICMP timeout
        self.icmpSocket.settimeout(self.timeout)

        try:
            # Try to receive ICMP reply
            data, address = self.icmpSocket.recvfrom(1024)  # 1024 as the buffer size.
            # Unpack the reply data
            # Byte 20 to 27 is where the ICMP header locates in a packet.
            icmp_header = struct.unpack("BBHHH", data[20:28])
            # address[0] is the sender's IP address, icmp_header[0] is the message type.
            return address[0], icmp_header[0]
        except socket.timeout:
            # If timeout return None
            return None, None

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

        icmp_header = struct.pack("BBHHH", icmp_echo_request, icmp_echo_code, icmp_checksum, icmp_id, icmp_sequence)
        icmp_checksum = calculateChecksum(icmp_header)
        # Add 4 bytes to fit the size (64 bytes) of a ICMP packet. Works as payload.
        icmp_packet = struct.pack("BBHHH", icmp_echo_request, icmp_echo_code, icmp_checksum, icmp_id, icmp_sequence) + b'\x00\x00\x00\x00'

        return icmp_packet


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
        traceRoute = TraceRoute4(destinationAddress, timeout, ttl)
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
            if icmpType == 0:   # ICMP Type 0 means the message reached the target host, so break.
                break
        else:
            print(f"{ttl}\t*\t{elapsedTime}ms")


if __name__ == '__main__':
    # Build command line process
    commandParser = argparse.ArgumentParser(
        description=f"Traceroute.py {version} Copyright (c) 2023 Steven Song. Coursework for CNSCC203 Computer Networks "
                    f"2023.")
    commandParser.add_argument('-j', metavar='maximum_hops', default=30, type=int,
                               help="The maximum number of hops for the search target.")
    commandParser.add_argument('-w', metavar='timeout', default=3, type=int,
                               help="Time out waiting for each reply (in milliseconds).")
    commandParser.add_argument('target_host', type=str,
                               help="target host to traceroute. (DNS name or IP address)")
    commandOptions = commandParser.parse_args()

    # Do traceroute
    traceroute(commandOptions.target_host, commandOptions.j, commandOptions.w)
