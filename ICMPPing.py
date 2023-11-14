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

version = '0.1.0'

# class ICMPSocket:

# def receiveOnePing(icmpSocket, destinationAddress, ID, timeout):

# def sendOnePing(icmpSocket, destinationAddress, ID):

# def doOnePing(destinationAddress, timeout):

# def ping(host, timeout):


if __name__ == '__main__':
    # Build command line process
    commandParser = argparse.ArgumentParser(description=f"ICMPPing.py {version} Copyright (c) 2023 Steven Song. Coursework for CNSCC203 Computer Networks 2023.")
    commandParser.add_argument('-t', action='store_true', default=False, help="ping the target host until stopped manually(Ctrl+C).")
    commandParser.add_argument('-c', metavar='count', default=4, type=int, help="stop after <count> times.")
    commandParser.add_argument('target_host', type=str, help="target host to ping. (DNS name or IP address)")
    commandOptions = commandParser.parse_args()

    # Do ping
    if commandOptions.t:
        while True:
            print("TODO: set ping command here")
            # ping(commandOptions.target_host)
    else:
        for i in range(0, commandOptions.c):
            print("TODO: set ping command here")
            # ping(commandOptions.target_host)
