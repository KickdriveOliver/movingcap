#id 3axis_flattrack_axis1_x_base.py 2024-11-10 oh

import sys
import mcdrive as mc

# movement parameters
LOWSPEED_VELOCITY = 250000
LOWSPEED_ACCELERATION = 6000
HIGHSPEED_VELOCITY = 600000
HIGHPEED_ACCELERATION = 12000
# (jerk is used as predefined)

# IN signal for (temporary) high speed operation
HIGHSPEED_IN = 7

# OUT that handles the secondary handler axis
HANDLER_CMD_OUT = 2
# IN that receives the status of the secondary handler axis
HANDLER_ACK_IN = 10

# Multiplex OUT signal: 
# use two different pulse lenghts to execute two different handler tasks
SHORT_PULSE_MS = 30
LONG_PULSE_MS = 150

# geometry
GRID_SIZE_MICROMETER = 40000

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
	sys.wait(20)
	while (mc.ChkIn(HANDLER_ACK_IN) == 0):
		sys.wait(1)


WriteObjectsFromKickdriveList(CONTROLLER_PARAMETER_ADJUSTMENTS)

# Determine soft limit positions (minimal and maximum positions) at startup
# end program, if there is no valid soft limit setup
softLimitMin = mc.ReadObject(0x607d, 1)
softLimitMax = mc.ReadObject(0x607d, 2)
if ((softLimitMin == 0 and softLimitMax == 0) or softLimitMax <= (softLimitMin + 1000)):
    print("flatTRACK demo abort. Check softlimit objects 607Dh.1h and 607D.2h!")
    sys.exit()

mc.ClearOut(HANDLER_CMD_OUT)

# initial wait, don't surprise me with immediate movement
sys.wait(5000)
# general init
mc.EnableDrive()
# go to startup position       
mc.SetPosVel(LOWSPEED_VELOCITY)
mc.SetAcc(LOWSPEED_ACCELERATION)
mc.GoPosAbs(softLimitMin)

# and go...
currentPosition = softLimitMin
nextPosition = currentPosition
stepSize = 40000
direction = 1
while True:    
    WaitHandlerReady()
    WaitDriveReady()
    # long pulse to Y -> go to start position
    SendPulseToHandler(LONG_PULSE_MS)

    if mc.ChkIn(HIGHSPEED_IN) == 0:
        mc.SetPosVel(LOWSPEED_VELOCITY)
        mc.SetAcc(LOWSPEED_ACCELERATION)
    else:
        mc.SetPosVel(HIGHSPEED_VELOCITY)
        mc.SetAcc(HIGHPEED_ACCELERATION)

    mc.GoPosAbs(nextPosition)		
    # wait until Y and X in position
    WaitHandlerReady()
    WaitDriveReady()
    currentPosition = nextPosition
    # now let the handler do its sequence
    SendPulseToHandler(SHORT_PULSE_MS)
    # and prepare next round
    nextPosition = currentPosition + direction * stepSize
    if nextPosition > softLimitMax:
        direction = -1
        nextPosition = currentPosition + direction * stepSize
    elif nextPosition < softLimitMin:
        direction = 1
        nextPosition = currentPosition + direction * stepSize

    if mc.ChkIn(HIGHSPEED_IN) == 0:
         sys.wait(500)