## repeater.py for 10.1.4
# This script reads from stdin and writes to stdout one line at a time until there is no more input.
# It also writes a message to stderr when it starts and stops, showing he lifetime of the process.

import sys

sys.stderr.write("10.1.4-subprocess_repeater.py: starting\n")
sys.stderr.flush()

while True:
    next_line = sys.stdin.readline()
    if not next_line:
        break
    sys.stdout.write(next_line)
    sys.stdout.flush()

sys.stderr.write("10.1.4-subprocess_repeater.py: exiting\n")
sys.stderr.flush()