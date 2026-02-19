#id maxTRACK N23 demo rev8
# requirements: 
# - movement parameters in mm coordinates
# - zero position is top position
#
# use IN1=high or RefGo Command
# OW 3510H,1H,65536
# to switch to fast mode
#
# use IN1=low or RefGo Command
# OW 3510H,1H,0
# to switch back to slow mode

import drive
import sys

# wait until movement finished. Hold if error.
def moveAndWait(newPos):
    if drive.ChkIn(1) > 0:
        # IN1 high --> small pause, go fast
        sys.wait(1000)
        drive.SetAcc(1500)
        drive.SetDec(1500)
        drive.SetPosVel(750)
    else:
        # IN1 low --> large pause, go easy
        sys.wait(3000)
        drive.SetAcc(500)
        drive.SetDec(500)
        drive.SetPosVel(300)
    drive.GoPosAbs(newPos)
    drive.WriteControl(0x3F)
    timeout = sys.time() + 10000 
    while (drive.ChkReady() == 0 and sys.time() < timeout):
        sys.wait(1)
    # error recovery (e.g. stall error)
    if (drive.ChkError() == 1):
        drive.PowerQuit()
        sys.wait(10000)
        drive.EnableDrive()
        sys.wait(5000)

        
# initial wait, don't surprise with immediate movement 
sys.wait(5000)

while (1):
    # release brake
    drive.EnableDrive()
    sys.wait(2000)
    moveAndWait(20)
    moveAndWait(50)
    moveAndWait(300)
    moveAndWait(650)
    moveAndWait(10)
    sys.wait(1000)
    # engage brake
    drive.PowerQuit()
    # time for a break
    if drive.ChkIn(1) > 0:
        # IN1 high --> small pause
        sys.wait(2000)
    else:
        # IN1 low --> large pause
        sys.wait(5000)




