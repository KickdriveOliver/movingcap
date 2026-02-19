#id UsingRefGoCommandsFromPythonScript.py 2024-10-02 oh
# This example shows how to use the simplistic RefGo ASCII protocol commands
# for drive control, instead of the mcdrive library. 
# Both mcdrive and refgo can be used in combination, of course. 

import sys
import refgo

sys.wait(5000)

# go to absolute position 10000 
refgo.cmd("G10000")
# check if movement finished
while (refgo.cmd("TS") != 1):
	pass
while(1):
    # relative movement
    refgo.cmd("GW1000")
    # check if movement finished
    while (refgo.cmd("TS") != 1):
        pass
    sys.wait(1000)