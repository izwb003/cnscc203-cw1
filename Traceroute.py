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
    print("\n\n")


if __name__ == '__main__':
    # Build command line process
    commandParser = argparse.ArgumentParser(
        description=f"Traceroute.py {version} Copyright (c) 2023 Steven Song. Coursework for CNSCC203 Computer Networks "
                    f"2023.")
    commandParser.add_argument('-j', metavar='maximum_hops', default=30, type=int,
                               help="The maximum number of hops for the search target.")
    commandParser.add_argument('-w', metavar='timeout', default=3000, type=int,
                               help="Time out waiting for each reply (in milliseconds).")
    commandParser.add_argument('target_host', type=str, help="target host to traceroute. (DNS name or IP address)")
    commandOptions = commandParser.parse_args()

    # Do traceroute
    traceroute(commandOptions.target_host, commandOptions.j, commandOptions.w)

