#id driveSimplePosTest.py 2025-02-04 oh
# This is a simple positioning demo for a MovingCap turnTRACK 349 rotary drive.

import sys
import mcdrive as mc

def WaitTargetReached(): 
	# Check statusword for "target reached"
	while (mc.ChkReady() == 0):
		sys.wait(1)
	# only continue if no error 
	while (mc.ChkError() != 0):
		sys.wait(1)
	# check digital input IN2 - if low, add a second of pause/delay time
	if mc.ChkIn(2) == 0:
		sys.wait(1000)

# initial wait, don't surprise me with immediate movement
sys.wait(2000)

# Set 6092h.01h Feed constant to 360 --> one turn = 360°
mc.WriteObject(0x6092, 0x01, 360)

# general init
mc.EnableDrive()
mc.SetAcc(500)
mc.SetDec(500)
mc.SetPosVel(360)
# and go...
while(1):
	# set digital output OUT1 to high during move to position 0
	mc.SetOut(1)
	mc.GoPosAbs(0)
	WaitTargetReached()
	# reset OUT1 to low
	mc.ClearOut(1)
	mc.GoPosAbs(1000)
	WaitTargetReached()
	mc.GoPosAbs(180) 
	WaitTargetReached()
