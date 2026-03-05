#id 3axis_flattrack_axis2_y_middle.py 2024-11-10 oh

import sys
import mcdrive as mc

# movement parameters
LOWSPEED_VELOCITY = 250000
LOWSPEED_ACCELERATION = 20000
HIGHSPEED_VELOCITY = 1000000
HIGHPEED_ACCELERATION = 20000
# (jerk is used as predefined)

# IN signal for (temporary) high speed operation
HIGHSPEED_IN = 7

# IN that controls this axis
CONTROLLER_CMD_IN = 8
# OUT that returns status of this axis
CONTROLLER_ACK_OUT = 1

# Multiplex IN signal: 
# supports two different pulse lengths to perform two different tasks
SHORT_PULSE_MS = 30
LONG_PULSE_MS = 150
PULSE_WINDOW_MS = 20

# OUT that handles the secondary handler axis
HANDLER_CMD_OUT = 2
# IN that receives the status of the secondary handler axis
HANDLER_ACK_IN = 10

# filter adjustments (only pre-v53.02.00.33_RABBIT)
CONTROLLER_PARAMETER_ADJUSTMENTS = """
050.3304h.01h,unsigned32,5000 # posInp bank0 filterFreq
050.3304h.03h,unsigned32,160 # velDisp bank2 filterFreq
050.3305h.03h,unsigned32,200 # velDisp bank2 milliQ
"""

def WriteObjectsFromKickdriveList(kickdriveTxtExportString):
    """
    This function takes a Kickdrive Object Editor text list and sets the parameters

    Parameters:
    kickdriveTxtExportString (str): A string containing KickDrive export data. 
    EEach line represents a CANopen object as comma seperated list  format "ID,Type,Value". 
    IDs contain NodeId, index and subindex in format 050.3401h.03h (for example) 
    Values are in decimal format. Everything after '#' is  a comment / ignored.

    Returns:
    None. The function prints a message for each object written to the drive.
    """
    # Create a list of parameters
    params = [line.split(',') for line in kickdriveTxtExportString.split('\n') if line.strip()]
    # Iterate through each parameter
    for param in params:
        # Skip lines without an ID
        if len(param) < 2:
            continue
        id = param[0].split('.')
        index = int(id[1].rstrip('h'), 16)
        subindex = int(id[2].rstrip('h'), 16)
        value = int(param[2].split('#')[0])
        mc.WriteObject(index, subindex, value)
        print ("Writing object " + hex(index) + "," + hex(subindex) + " = " + str(value))

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


def SendPulseToHandler(duration):
    mc.SetOut(HANDLER_CMD_OUT)
    sys.wait(duration)
    mc.ClearOut(HANDLER_CMD_OUT)

def WaitHandlerReady():
	# make sure the handler had time to acknowledge the new command
	sys.wait(10)
	while (mc.ChkIn(HANDLER_ACK_IN) == 0):
		sys.wait(1)

def WaitForPulseFromController():
    # make sure the input is low first
    while (mc.ChkIn(CONTROLLER_CMD_IN) == 1):
        sys.wait(1)
    # wait for input high
    while (mc.ChkIn(CONTROLLER_CMD_IN) == 0):
        sys.wait(1)
    # note start time and wait until low again
    startTime = sys.time() 
    while (mc.ChkIn(CONTROLLER_CMD_IN) == 1):
        sys.wait(1)
    endTime = sys.time()
    # return pulse duration in milliseconds
    pulseDuration = (endTime - startTime)
    if (pulseDuration >= SHORT_PULSE_MS - PULSE_WINDOW_MS) and (pulseDuration <= SHORT_PULSE_MS + PULSE_WINDOW_MS):
       return SHORT_PULSE_MS
    elif (pulseDuration >= LONG_PULSE_MS - PULSE_WINDOW_MS) and  (pulseDuration <= LONG_PULSE_MS + PULSE_WINDOW_MS):
       return LONG_PULSE_MS
    else:
       return 0


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
    WaitHandlerReady()
    WaitDriveReady()
    if mc.ChkIn(HIGHSPEED_IN) == 0:
        sys.wait(500)
    mc.SetOut(CONTROLLER_ACK_OUT)
    pulseDuration = WaitForPulseFromController()
    mc.ClearOut(CONTROLLER_ACK_OUT)
    if pulseDuration == LONG_PULSE_MS:
        # go to start position for the sequence
        if mc.ChkIn(HIGHSPEED_IN) == 0:
            mc.SetPosVel(LOWSPEED_VELOCITY)
            mc.SetAcc(LOWSPEED_ACCELERATION)
        else:
            mc.SetPosVel(HIGHSPEED_VELOCITY)
            mc.SetAcc(HIGHPEED_ACCELERATION)
        mc.GoPosAbs(softLimitMin)
    elif pulseDuration == SHORT_PULSE_MS:
        # do the sequence with 2x z axis movement
        SendPulseToHandler(SHORT_PULSE_MS)
        WaitHandlerReady()
        if mc.ChkIn(HIGHSPEED_IN) == 0:
            sys.wait(250)
            mc.SetPosVel(LOWSPEED_VELOCITY)
            mc.SetAcc(LOWSPEED_ACCELERATION)
        else:
            mc.SetPosVel(HIGHSPEED_VELOCITY)
            mc.SetAcc(HIGHPEED_ACCELERATION)
        mc.GoPosAbs(softLimitMax)
        WaitDriveReady()
        SendPulseToHandler(SHORT_PULSE_MS)