#id 3axis_shorttrack_axis3_z_vertical.py 2024-11-08 oh

import sys
import mcdrive as mc

# movement parameters
LOWSPEED_VELOCITY = 800000
LOWSPEED_ACCELERATION = 20000
HIGHSPEED_VELOCITY = 1000000
HIGHPEED_ACCELERATION = 50000
# (jerk is used as predefined)

# IN signal for (temporary) high speed operation
HIGHSPEED_IN = 7

# IN that controls this axis
CONTROLLER_CMD_IN = 8
# OUT that returns status of this axis
CONTROLLER_ACK_OUT = 1

def WaitDriveReady():
    """
    This function checks the status of the drive to ensure it is ready for operation.
    It continuously polls the drive's statusword for the "target reached" bit and waits until it is set.
    Additionally, it checks for any errors by continuously polling the drive's statusword for error bits.
    If an error is detected, it waits until the error is cleared.

    Parameters:
    None

    Returns:
    None
    """
    # make sure movement has started
    sys.wait(10)
    # Check statusword for "target reached"
    while(mc.ChkReady() == 0):
        sys.wait(1)
    # only continue if no error
    while(mc.ChkError() != 0):
        sys.wait(1)

def WaitForSignalFromController():
    # make sure the input is low first
    while (mc.ChkIn(CONTROLLER_CMD_IN) == 1):
        sys.wait(1)
    # wait for input high
    while (mc.ChkIn(CONTROLLER_CMD_IN) == 0):
        sys.wait(1)

# Determine soft limit positions (minimal and maximum positions) at startup
# end program, if there is no valid soft limit setup
softLimitMin = mc.ReadObject(0x607d, 1)
softLimitMax = mc.ReadObject(0x607d, 2)
if ((softLimitMin == 0 and softLimitMax == 0) or softLimitMax <= (softLimitMin + 1000)):
    print("flatTRACK demo abort. Check softlimit objects 607Dh.1h and 607D.2h!")
    sys.exit()

mc.ClearOut(CONTROLLER_ACK_OUT)

# initial wait, don't surprise me with immediate movement
sys.wait(5000)
# general init
mc.EnableDrive()
# go to startup position  
mc.SetPosVel(LOWSPEED_VELOCITY)
mc.SetAcc(LOWSPEED_ACCELERATION)
mc.GoPosAbs(softLimitMin)

while True:
    mc.SetOut(CONTROLLER_ACK_OUT)
    # LOW->HIGH slope starts the process
    WaitForSignalFromController()
    mc.ClearOut(CONTROLLER_ACK_OUT)
    if mc.ChkIn(HIGHSPEED_IN) == 0:
        mc.SetPosVel(LOWSPEED_VELOCITY)
        mc.SetAcc(LOWSPEED_ACCELERATION)
    else:
        mc.SetPosVel(HIGHSPEED_VELOCITY)
        mc.SetAcc(HIGHPEED_ACCELERATION)
    mc.GoPosAbs(softLimitMax)
    WaitDriveReady()
    if mc.ChkIn(HIGHSPEED_IN) == 0:
        sys.wait(500)
    mc.GoPosAbs(softLimitMin)
    WaitDriveReady()