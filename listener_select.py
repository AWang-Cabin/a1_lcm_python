# This example demonstrates how to use LCM with the Python select module

import select
import lcm
from exlcm import aroundfeet_map_t

def my_handler(channel, data):
    msg = aroundfeet_map_t.decode(data)
    print("Received message on channel \"%s\"" % channel)
    print("   timestamp   = %s" % str(msg.aroundmap))

    print("")

lc = lcm.LCM()
lc.subscribe("EXAMPLE", my_handler)

try:
    timeout = 0.1  # amount of time to wait, in seconds
    while True:
        rfds, wfds, efds = select.select([lc.fileno()], [], [], timeout)
        if rfds:
            lc.handle()
        else:
            print("Waiting for message...")
except KeyboardInterrupt:
    pass