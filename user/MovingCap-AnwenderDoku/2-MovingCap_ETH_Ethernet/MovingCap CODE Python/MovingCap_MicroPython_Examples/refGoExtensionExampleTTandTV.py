#id refGoExtensionExampleTTandTV.py 2025-11-04 oh
# requires turnTRACK firmware v50.00.10.00_RE higher

# This example shows how to mimic the original XENAX protocol commands 
# TT (Tell Temperature) and TV (Tell Velocity) 
# TIP: This code is for demonstration purposes. For practical applications, 
# calling the text-based "refgo" interface 10 times per milliseconds is a waste
# of CPU time, but it demonstrates how fast MovingCap can run micropython code,
# even if it includes string processing. 

# NOTE: In earlier firmware versions (v50.00.09.xx and lower) the 
# functionality was provided by the mccom library. 
# Now refgo is the library to include and use.

import time
import refgo
import mcdrive as mc

# possible redirect modes:
# REFGO_REDIRECT_FORWARD_ALL = 1,
# REFGO_REDIRECT_FORWARD_UNPROCESSED = 2
# REFGO_REDIRECT_ONLY_PYTHON_PROCESSING = 3
refgo.open(2) 
cmd = ""

while (1): 
	cmd = refgo.read()
	if cmd is not None:
		if (cmd == "TT"):
			# Tell Temperature - return value of Movingcap-specific temperature object
			refgo.write("TT\r\n" + repr(mc.ReadObject(0x3401, 0x0a)) + "\r\n>")
		elif (cmd == "TV"): 
			# Tell Velocity - return value of DS402 standard object "Velocity actual value"
			refgo.write("TV\r\n"+ repr(mc.ReadObject(0x606c, 0x0)) + "\r\n>")
	time.sleep_ms(5)
