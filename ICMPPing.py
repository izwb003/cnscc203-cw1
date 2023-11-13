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

import sys

version = '0.1.0'


class CommandOptions:
    """Get command line options and make proper settings."""
    target_name = ""    # The target host name.
    nonstop_flag = False    # If true, ping the specified host until stopped.

    def __init__(self, argv):
        if len(argv) == 1:
            usage()
        for args in argv:
            if args is argv[0]:
                continue
            elif args == ("--help" or "-h"):
                usage()
                sys.exit(0)
            elif args == ("--version" or "-V"):
                show_version()
                sys.exit(0)
            elif args == "-t":
                self.nonstop_flag = True
            elif args is argv[len(argv) - 1]:
                if args.startswith('-') or args.startswith('--'):
                    print(f"Invalid argument {args}. Type \"--help\" or \"-h\" for help.")
                    sys.exit(1)
                self.target_name = args
            else:
                print(f"Invalid argument {args}. Type \"--help\" or \"-h\" for help.")
                sys.exit(1)


def usage():
    """Show help information."""
    global version
    print(f"""ICMPPing.py {version} Copyright (c) 2023 Steven Song.
Coursework for CNSCC203 Computer Networks 2023.

USAGE:
    ICMPPing [-h|--help] [-V|--version]
    ICMPPing [-t][-l size]

Options:
    -h | --help           - Show help.
    -V | --version        - Show version information.
    -t                    - Ping the specified host until stopped.""")


def show_version():
    """Show version information."""
    global version
    print(f"""ICMPPing.py {version} Copyright (c) 2023 Steven Song.
Coursework for CNSCC203 Computer Networks 2023.\n""")


if __name__ == '__main__':
    commandOptions = CommandOptions(sys.argv)
