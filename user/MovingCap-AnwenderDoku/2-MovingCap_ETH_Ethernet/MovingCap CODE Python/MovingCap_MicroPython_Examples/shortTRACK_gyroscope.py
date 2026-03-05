#id rev6 shortTRACK_gyroscope.py demo
# MovingCap shortTRACK demo - detect horizontal/vertical orientation and adjust motion: 
# horizontal/flat - go back to default speed
# positive direction points to sky - increase speed
# positive direction points to ground - decrease speed
# precondition: 
# - Firmware v53.02.00.34_SRABBIT or higher 
# - Softlimit objects 607Dh.1h and 607D.2h set
import sys
import mcdrive as mc
		
# this determines the threshold for detecting left/right tilt
TILT_SENSITIVITY = 15

# Controller adjustments for the "hand-held" demo without payload:
# (shortTRACK can have much more dynamic velocity control, go for maximum stability)
CONTROLLER_PARAMETER_ADJUSTMENTS = """
050.6067h.00h,unsigned32,100 # Position window
050.6068h.00h,unsigned16,100 # Position window time
050.6081h.00h,unsigned32,100000 # Profile Velocity
050.6083h.00h,unsigned32,5000 # Profile acceleration
050.60a4h.00h,unsigned32,100000 # Profile Jerk
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


def GoPosAndCheckCurrent(targetPos):
    """
    This function moves the motor to a specified position and integrates the current 
    consumed during the movement. It waits until the target position is reached and then 
    adds a bit of standstill time to integrate the current.

    Parameters:
    targetPos (int): The target position to move the motor to. 

    Returns:
    int: The total current consumed during the movement and standstill time.
    """
    mc.GoPosAbs(targetPos)
    # wait until target reached and integrate current
    sum = 0
    while (mc.ChkReady() == 0):
        sum = sum + mc.ReadObject(0x6078,0)
        sys.wait(2)
    # always add a bit of standstill
    i = 0 
    while (i < 50):
        i = i + 1
        sum = sum + mc.ReadObject(0x6078,0)
        sys.wait(2)
    return sum

WriteObjectsFromKickdriveList(CONTROLLER_PARAMETER_ADJUSTMENTS)

# safety: only run this script if softlimit objects are set up properly
softLimitMin = mc.ReadObject(0x607d, 1) 
softLimitMax = mc.ReadObject(0x607d, 2)

if ((softLimitMin == 0 and softLimitMax == 0) or softLimitMax <= (softLimitMin + 20000)):
    print("flatTRACK demo abort. Check softlimit objects 607Dh.1h and 607Dh.2h!")
    while (1):
        sys.wait(1)
	
# initial wait, don't surprise me with immediate movement
sys.wait(5000)

# general init
mc.EnableDrive()
sys.wait(2000)

# initial movement to the center
mc.SetPosVel(100000)
mc.SetAcc(5000)
mc.WriteObject(0x60A4, 0, 100000)
# (note: for integer division, use "//" instead of "/"). Floats are not supported in the current MovingCap MircoPython engine. 
mc.GoPosAbs((softLimitMin + softLimitMax) // 2)
sys.wait(1000)

# and go...	
speed = 150000
while(1):
	# set new speed and acceleration
	mc.SetPosVel(speed)
	mc.SetAcc(speed // 20)
	# adjust jerk
	mc.WriteObject(0x60A4, 0, speed // 2)
	# perform movement sequence and integrate current
	startTime = sys.time()
	avg = GoPosAndCheckCurrent(softLimitMin + 5000)
	avg = avg + GoPosAndCheckCurrent(softLimitMin + 10000)
	avg = avg + GoPosAndCheckCurrent(softLimitMin + 20000)
	avg = avg + GoPosAndCheckCurrent(softLimitMax - 5000)
	duration = sys.time() - startTime
	avg = avg // duration
	# decision making / gyroscope: speed control using gravity
	if (avg < -TILT_SENSITIVITY):
		# assume positive direction points to ground
		if (speed > 20000):
			speed = speed // 2
			mc.WriteObject(0x3301, 0x0F, 1) # compensate for positive gravity
	elif (avg > TILT_SENSITIVITY):
		# assume positive direction points to sky
		if (speed < 1200000):
			speed = speed * 2
			mc.WriteObject(0x3301, 0x0F, -1) # compensate for positive gravity
	else:
		# assume vertical (again)
		speed = 100000 # reset speed
		mc.WriteObject(0x3301, 0x0F, 0) # reset compensation for gravity


