#id flatTRACK_IO_left_right_Example_CODE.py 2025-05-06 oh

import sys
import mcdrive as mc

FLATTRACK_IO_LEFT_RIGHT_APP = """
050.3511h.01h,unsigned16,0 # IN1 function
050.3512h.01h,unsigned16,0 # IN2 function
050.3513h.01h,unsigned16,0 # IN3 function
050.3514h.01h,unsigned16,0 # IN4 function
050.3515h.01h,unsigned16,0 # IN5 function
050.3516h.01h,unsigned16,0 # IN6 function
050.3517h.01h,unsigned16,1024 # IN7 function
050.3517h.05h,integer32,0 # IN7 timer
050.3517h.06h,integer32,20000 # IN7 velocity
050.3517h.07h,integer32,5000 # IN7 acceleration
050.3517h.08h,integer32,0 # IN7 target pos
050.3517h.09h,integer32,0 # IN7 deceleration
050.3517h.0ah,integer32,1000 # IN7 max current / torque
050.3518h.01h,unsigned16,1024 # IN8 function
050.3518h.05h,integer32,0 # IN8 timer
050.3518h.06h,integer32,20000 # IN8 velocity
050.3518h.07h,integer32,5000 # IN8 acceleration
050.3518h.08h,integer32,450000 # IN8 target pos
050.3518h.09h,integer32,0 # IN8 deceleration
050.3518h.0ah,integer32,1000 # IN8 max current / torque
050.3519h.01h,unsigned16,0 # IN9 function
050.351ah.01h,unsigned16,0 # IN10 function
050.3611h.01h,unsigned16,6 # OUT1 function
050.3611h.02h,unsigned16,7 # OUT1 configuration
050.3611h.03h,integer32,0 # OUT1 right position
050.3611h.04h,integer32,0 # OUT1 left position
050.3611h.05h,integer32,1000 # OUT1 right pos. distance
050.3611h.06h,integer32,1000 # OUT1 left pos. distance
050.3612h.01h,unsigned16,6 # OUT2 function
050.3612h.02h,unsigned16,8 # OUT2 configuration
050.3612h.03h,integer32,0 # OUT2 right position
050.3612h.04h,integer32,0 # OUT2 left position
050.3612h.05h,integer32,1000 # OUT2 right pos. distance
050.3612h.06h,integer32,1000 # OUT2 left pos. distance
050.3613h.01h,unsigned16,0 # OUT3 function
050.3614h.01h,unsigned16,0 # OUT4 function
050.3614h.02h,unsigned16,0 # OUT4 configuration
050.6067h.00h,unsigned32,100 # Target Reached Window [user units]
050.6068h.00h,unsigned16,50 # Target Window Time [ms]
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
		
WriteObjectsFromKickdriveList(FLATTRACK_IO_LEFT_RIGHT_APP)
