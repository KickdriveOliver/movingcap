---
description: "Introduction to CANopen, CoE (CANopen over EtherCAT) and the CiA 402 device specification"
---
# Introduction to CANopen, CoE (CANopen over EtherCAT) and the CiA 402 device specification

2026-01-10 / www.kickdrive.de / www.fullmo.de

CANopen over EtherCAT (CoE) is a software interface that integrates the CiA 402 device profile framework of CANopen into EtherCAT networks. Within CoE, the CiA 402 device profile, defined according to IEC 61800-7-201:2015, plays a central role. CiA 402 defines standardized read-only or read/write parameter objects, together with a CiA 402 standard object number (index and subindex). CiA 402 defines device behavior and standard operating modes specifically developed for variable speed electric drive systems. 

CiA 301 defines the communication between controllers (master) and devices (devices/slaves) through clearly defined interaction patterns for configuring, controlling and monitoring devices at field level. Among other things, CANopen defines communication paradigms such as Service Data Objects / SDO, in which the controller actively sends information to connected devices ("SDO Download") or requests information from them ("SDO Upload"). 

## CANopen CiA 301 Overview of the communication profile

### Introduction
CiA 301 defines the CANopen application layer and the communication profile. It defines data types, coding rules, the object dictionary and all communication services and protocols - in particular NMT, SDO, PDO, SYNC, TIME and EMCY.

In typical CANopen networks, **NMT** controls the start-up of the nodes, state transitions and error monitoring, while **SDO** provides peer-to-peer access to parameters in the object dictionary.

### Network Management (NMT)

#### Controller device model
The CANopen NMT follows a controller-device model. One node acts as **NMT controller**, up to 127 nodes (node IDs 1-127) act as **NMT devices**. By sending unconfirmed NMT service messages to COB-ID 0x000, the controller can initialize, start, stop or reset individual or all devices.

### Node control services

These unconfirmed NMT services enable direct control of the devices:

- **Start Remote Node:** `01h` → Set device to Operational
- Stop Remote Node:** `02h` → Set device to Stopped
- Enter Pre-operational:** `80h` → Set device to Pre-operational
- Reset Node:** `81h` → Perform application reset
- **Reset Communication:** `82h` → Perform communication reset

#### Examples:
- `COB-ID=0h, Size=2, Data=81 00` → NMT Reset Node (all nodes)
- `COB-ID=0h, Size=2, Data=01 05` → NMT Start for Node-ID 5

#### Error control services
There are two error monitoring mechanisms - **Node Guarding** and **Heartbeat** - of which only one may be used per device. 

In **Node Guarding** mode, the device must respond to the **Guarding Request** of the controller within a specified timeout. 

In **Heartbeat** mode, each device periodically sends a one-byte status (0 = Boot-up, 4 = Stopped, 5 = Operational, 127 = Pre-operational) via COB-ID 0x700 + Node-ID; the controller monitors timeouts for error detection.

#### Boot-up service
Immediately after the **Reset Communication** sub-state, a device sends a one-byte **Boot-up** message (0x00) to **COB-ID 0x700 + Node-ID** to signal that it is ready for configuration.

#### NMT state machine
The NMT state machine comprises four main states with three initialization sub-states:

1. **Initialization** (automatically after power-on, divided into:  
   a. *Initializing* - basic initialization  
   b. *Reset Application* - resetting application-related parameters  
   c. *Reset Communication* - resetting communication-related parameters)  
2. **Pre-operational** - only SDO access, PDOs inactive  
3. **Operational** - all communication objects (PDO, SYNC, TIME, EMCY, SDO) active  
4. **Stopped** - communication stopped, except for error control  


Transitions are made via NMT services, hardware resets or local control.

##### State-object relationship
| NMT state | PDO | SDO | SYNC | TIME | EMCY | node control/error control |
|:---------------:|:---:|:---:|:----:|:----:|:----:|:---------------------------:|
| Pre-operational | | ✓ | ✓ | ✓ | ✓ | | ✓ |
| Operational | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Stopped | | | | | ✓ | ✓ |

This allows parameterization via SDO in **Pre-operational**, while PDO real-time transmission only takes place in **Operational**.

### Service Data Objects (SDO)

#### Client-server model
SDO implements a confirmed client-server protocol for accessing any entries in the object directory. 

The following applies to the standard SDO channel: Client requests (usually sent by the controller) are made to COB-ID 0x600 + NodeID; server/device responses to 0x580 + NodeID.

#### SDO services
SDO is divided into:
1. **SDO Download** (Client→Server): Write access  
   - **Initiate** (expedited): up to 4 bytes of data in one frame  
   - **Segment**: Toggle bit protocol for &gt;4 bytes  
2. **SDO Upload** (Server→Client): Read access  
   - **Initiate** (expedited): returns ≤4 bytes  
   - **Segment**: multi-part transfer for &gt;4 bytes  
3. **SDO Abort Transfer**: Abort on error  
4. **(Optional) Block Download/Upload**: optimized block transfer with CRC and sequence numbers

All SDO services are **confirmed**; responses contain a return code for success or error.

#### Expedited vs. Segmented vs. Block
- **Expedited** (≤4 B): one frame, no segmentation.  
- **Segmented** (&gt;4 B): several frames of 7 data bytes each with toggle bit.  
- **Block** (optional): numbered blocks, client confirms blocks, CRC possible.

#### Protocol details
- **Download Initiate**: Client sends `cs=0x20-0x23` in byte 0, index in bytes 1-2, sub-index byte 3, data in bytes 4-7.  
- **Upload Initiate**: Client sends `cs=0x40`, server responds with `cs=0x43` (expedited) or `cs=0x41` (segmented) plus length.  
- **Segments**: Client/Server use `cs=0x00/0x01` for download segments; `cs=0x60/0x61` for upload.  
- **Block**: `cs=0xA0...0xA4` for block download; `cs=0xC0...0xC2` for block upload.

### Summary
The CiA 301 communication profile ensures that CANopen devices can be configured, monitored and controlled in a standardized manner. **NMT** handles the entire device life cycle - boot-up, parameterization (via SDO in *Pre-operational*) and real-time communication (*Operational*). **SDO** offers flexible client-server access to any object dictionary entries, from individual parameters up to 4 bytes in length (expedited transfer) to entire data records (segmented or block transfer).

In combination with PDO for cyclical process data, SYNC for network-wide synchronization and EMCY for fast error alerting, CiA 301 forms the basis for interoperable, high-performance communication in automation networks.

## CiA 402 - General overview

### Introduction

CiA 402, alternatively referred to as DS 402 / Device Standard 402, is a device profile for drives and motion control defined by the CAN in Automation (CiA) organization. It specifies a universal interface and standardized behaviour for controlling electrical drives - such as servo drives, servo controllers, frequency converters and similar devices. As a "CANopen Device Profile", it is part of the CANopen protocol, but is also used in EtherCAT, POWERLINK and other application protocols such as TCP/IP. The CiA 402 device profile is specified in the IEC61800-7-201 standard as profile type 1 - CiA402 Drive Profile for power drive systems (PDS). 

This section provides an overview of the central aspects of CiA 402, with a focus on the drive states / "State Machine", the main **Controlword (6040h)** and **Statusword (6041h)**, common **Modes of Operation (6060h)** and a summary of other key standard objects in the Object Dictionary.

### The CiA 402 State Machine

At the center of the CiA 402 profile is the **State Machine (PDS FSA, Power Drive System - Finite State Automat)**, which defines the permissible states and transitions of a drive. By defining permitted actions and required reactions in different operating states, the state machine ensures safe and predictable control of motion axes.

#### Main states

- **Not Ready to Switch On**: Initial state after switching on. The drive is not ready to perform movements.
- **Switch On Disabled**: Drive may not be enabled (e.g. after error or during initialization).
- **Ready to Switch On**: Internal checks completed; drive can be enabled.
- **Switched On**: Drive is ready for Enable command.
- **Operation Enabled**: The drive can execute movement commands.
- **Quick Stop Active**: Quick Stop is activated, the drive stops as quickly as possible.
- **Fault Reaction Active**: The drive reacts to a detected fault-it performs appropriate safety measures.
- **Fault**: A fault condition has been detected; the operator must be reset.

#### Transitions

State transitions are controlled by bits in the **Controlword (6040h)**, which is sent to the device by the master. The drive reports back its current status via the **Statusword (6041h)**.

A simplified diagram:

![MovingCap CiA 402 State Machine](images/mc_cia402_web.svg)

Overview of the state transitions

|No. |Current state | Next state | Description | Control word bits (15...0) | Status word after transition (15...0) |
|--|------------------------|-------------------------|--------------------------------------|---------------------------------|--------------------------------------|
|1| Not ready to switch on | Switch on disabled | Automatic after initialization | xxxxxxxxxxxxxxxxxx (no ext. command)| xxxxxxxx x1xx0000 |
|2| Switch on disabled | Ready to switch on | Shutdown | xxxxxxxxxx000110 (0x0006) | xxxxxxxx x01x0001 |
|3| Ready to switch on | Switched on | Switch On | xxxxxxxxxx000111 (0x0007) | xxxxxxxx x01x0011 |
|4| Switched on | Operation enabled | Enable Operation | xxxxxxxxxx00111111 (0x000F) | xxxxxxxx x01x0111 |
|6| Switched on | Ready to switch on | Shutdown | xxxxxxxxxx000110 (0x0006) | xxxxxxxx x01x0001 |
|5| Operation enabled | Switched on | Disable Operation | xxxxxxxxxx000111 (0x0007) | xxxxxxxx x01x0011 |
|11| Operation enabled | Quick stop active | Quick stop | xxxxxxxxxx000010 (0x0002) | xxxxxxxx x00x0111 |
|12| Quick stop active | Switch on disabled | Disable Voltage | xxxxxxxxxx000000 (0x0000) | xxxxxxxx x1xx0000 |
|10| Switched on | Switch on disabled | Disable Voltage | xxxxxxxxxx000000 (0x0000) | xxxxxxxx x1xx0000 |
|7| Ready to switch on | Switch on disabled | Disable Voltage | xxxxxxxxxx000000 (0x0000) | xxxxxxxx x1xx0000 |
|13| Operation enabled | Fault reaction active | Fault detected (int. transition) | Automatic (no control word) | xxxxxxxx x0xx1111 |
|14| Fault reaction active | Fault | Internal after fault reaction | Automatic (no control word) | xxxxxxxx x0xx1000 |
|15| Fault | Switch on disabled | Fault Reset | xxxxxxxx1xxxxxxx (0x0080) | xxxxxxxx x1xx0000 |
|(16)| Quick stop active | Operation enabled | Enable Operation (1) | xxxxxxxxxx001111 (0x000F) | xxxxxxxx x01x0111 |

A detailed description can be found in the CiA 402 specification.

**Note:** 
(1) The CiA 402 specification recommends *not* implementing transition 16.

### Controlword (6040h object)

The control word (index 6040h) is the central control object with which the master controls the status and behavior of the drive. It is a 16-bit word, with each bit (or bit groups) triggering certain actions or requests on the drive, such as state changes or movement commands.

#### Important bit functions

| Bit | Name | Description |
|-------|-------------------------|-----------------------------------------------|
| 0 | Switch On | Requests the drive to be switched on |
| 1 | Enable Voltage | Enables the internal power supply |
| 2 | Quick Stop | Requests a quick stop of the movement |
| 3 | Enable Operation | Completely enables the axis |
| 7 | Fault Reset | Acknowledge/reset fault |
| 8 | Stop | Stop movement without deactivating the drive |
| 9 | Operation Mode Specific | Used in certain operating modes |
| 10 | Reserved | - |
| 11-15 | Manufacturer-specific | - |

The combination and timing of these bits determine exactly how the state machine switches between states. For example: To change from **Switch On Disabled** to **Operation Enabled**, bits 0, 1 and 2 must be set, followed by bit 3. See also the diagram above and the table of state transitions. 

### Statusword (6041h object)

The statusword (index 6041h) is a 16-bit word that is sent from the drive to the master and signals the current status. By reading the statusword, the master recognizes the current status of the drive in the CiA 402 state machine.

#### Representative bit meanings

| Bit | Name | Description |
|-------|-------------------------|-------------------------------------------------|
| 0 | Ready to Switch On | Drive is ready to be enabled |
| 1 | Switched On | Drive is enabled |
| 2 | Operation Enabled | Drive is enabled for movements |
| 3 | Fault | Fault present |
| 4 | Voltage Enabled | Power / voltage for drive output stage is present |
| 5 | Quick Stop | Reaction to Quick Stop function is active |
| 6 | Switch On Disabled | Drive is deactivated |
| 7 | Warning | Warning present (no error)
| 8 | Manufacturer Specific | (1) |
| 9 | Remote | (2) |
| 10 | target reached | Position is within target tolerance |
| 11 | internal limit active | Limit reached according to 607D objects |
| 12,13 | Operation Mode specific | - |
| 14,15 | Manufacturer Specific | - |


**Notes:** 
(1) MovingCap and Festo drives use this bit for the **Drive Moving** state.

(2) The remote bit has no meaning for MovingCap drives or is not set. The controlword is also evaluated when remote = 0. 

### Operating modes

Modes of Operation (Index 6060h) determines the operating mode in which the drive operates. Each mode supports a different control paradigm (e.g. position control, speed control, torque control).

#### 6060h Modes of Operation

| Value (decimal) | Mode Name | Application |
|------------------|---------------------------|---------------------------------------------------------|
| -128 to -1 | Manufacturer Specific | Manufacturer-specific |
| 0 | No mode assigned | - |
| 1 | Profile Position Mode | Moves position with defined profile |
| 2 | Velocity Mode | (obsolete, usually not supported, see Mode 3) |
| 3 | Profile Velocity Mode | Moves speed with profile acceleration |
| 4 | Profile Torque Mode | Controls torque according to profile |
| 6 | Homing Mode | Homing ("Home" position) |
| 7 | Interpolated Position Mode | Moves according to interpolated position points |
| 8 | Cyclic Synchronous Position | Synchronous position control (real-time) |
| 9 | Cyclic Synchronous Velocity| Synchronous speed control (real time) |
| 10 | Cyclic Synchronous Torque | Synchronous Torque (real time) |

A servo drive usually only supports some of the operating modes according to CiA 402. Frequently used modes are
- 1 = Profile Position Mode,
- 3 = Profile Velocity Mode,
- 6 = Homing Mode,
- 8 = Cyclic Synchronous Position Mode.

The current mode can be read out with **Modes of operation display** (6061h).

### Profile Position Mode

**Profile Position Mode** (PPM, 6060h = 1) is one of the basic position control modes in CiA 402. In this mode, the drive moves its load to a target position along a motion profile. Parameters such as speed, acceleration and deceleration can be set, enabling smooth and controlled movements. The mode is suitable for point-to-point positioning, sequential movements or indexing tasks.

#### Sequence

1. set **Modes of Operation** (6060h) to 1 (Profile Position Mode).
2. set **Target position** (607Ah) and desired profile parameters.
3. configure **Profile velocity** (6081h), **profile acceleration** (6083h) and **profile deceleration** (6084h).
4. start the movement with the **Controlword** (6040h) (e.g. by setting the new set-point bit in accordance with CiA 402).
5. monitor **Statusword** (6041h) and **Position actual value** (6064h) to confirm the processing.

#### Important objects for Profile Positioning

| Index | Name | Description |
|-------|----------------------|----------------------------------------------------------|
| 6060h | Modes of Operation | Set to 1 for Profile Position Mode |
| 607Ah | Target Position | Target Position |
| 6081h | Profile Velocity | Maximum Allowed Velocity |
| 6083h | Profile Acceleration | Acceleration Rate |
| 6084h | Profile Deceleration | Deceleration Rate |
| 6064h | Position Actual Value | Actual Position |
| 6040h | Controlword | Trigger Moving and Manage Status |
| 6041h | Statusword | Status feedback |

Optional/additional objects:
- 60F2h: Positioning Option Code (e.g. "relative" or "absolute")
- 6073h: Max Current - Max. Current/torque/force for the drive
- 607Dh.01h/607Dh.02h: Software Position Limit - Software limit switch

### Profile Velocity Mode

**Profile Velocity Mode** (PVM, 6060h = 3) enables the axis speed to be specified directly, whereby profiled acceleration and deceleration ramps can be maintained. Typical applications include conveyor belts, fans or other systems in which a constant speed is required.

#### Sequence

1. set **Modes of Operation** (6060h) to 3 (Profile Velocity Mode).
2. set **Target velocity** (60FFh) and desired **profile acceleration/deceleration** (6083h/6084h).
3. use **Controlword** (6040h) to trigger start, stop or speed changes.
4. read out **Velocity actual value** (606Ch) and **Statusword** (6041h) for monitoring.

#### Important objects for Profile Velocity

| Index | Name | Description |
|-------|--------------------------|-----------------------------------------------|
| 6060h | Modes of Operation | Set to 3 for Profile Velocity Mode |
| 60FFh | Target Velocity | Target Velocity |
| 6083h | Profile Acceleration | Acceleration Ramp |
| 6084h | Profile Deceleration | Deceleration Ramp |
| 606Ch | Velocity Actual Value | Actual Velocity |
| 6040h | Controlword | Control Start/Stop/Halt |
| 6041h | Statusword | Feedback and status monitoring |

### Important Object Dictionary Entries

The following table contains some important entries according to CiA 402 Device Profile, which are central for drive control and monitoring.

| Index | Name | Description | Type |
|--------|----------------------------|------------------------------------------------------|------------|
| 6040h | Controlword | Control and status change (master → drive) | unsigned16 |
| 6041h | Statusword | Status feedback (drive → master) | unsigned16 |
| 6060h | Modes of Operation | Sets the operating mode of the drive | integer8 |
| 6061h | Modes of Operation Display | Current operating mode | integer8 |
| 607Ah | Target Position | Target Position for Profile Position Mode | integer32 |
| 6064h | Position Actual Value | Position Feedback | integer32 |
| 606Ch | Velocity Actual Value | Velocity (actual value) | integer32 |
| 6081h | Profile Velocity | Max. Velocity in Profile Position Mode | unsigned32 |
| 6083h | Profile Acceleration | Acceleration ramp | unsigned32 |
| 6084h | Profile Deceleration | Deceleration Ramp | unsigned32 |
| 60FFh | Target Velocity | Target Velocity in Profile Velocity Mode | integer32 |
| 6098h | Homing Method | Homing Strategy Selection | integer8 |
| 607Dh.01h | Min position limit | Software limit switch minimum | integer32 |
| 607Dh.02h | Max position limit | Software limit switch maximum | integer32 |
| 6073h | Max Current | Max. Current/Torque/Force | unsigned16 |
| 6075h | Motor Rated Current | Rated current for drive/motor | unsigned32 |
| 6078h | Current Actual Value | Actual Motor Current | integer16 |

### Position scaling / User-Defined Units

Position scaling in CiA 402 combines configurable scaling parameters with fixed motor/encoder properties to convert internal position units (increments) into user-specific/technical units.

#### Motor/encoder system properties (608Fh)

- 608Fh: Position Encoder Resolution**
  - `608Fh.01 encoder_increments`: Increments per motor rotation
  - `608Fh.02 motor_revolutions`: Motor revolutions per encoder revolution
  - Example: For a 16-bit incremental encoder: `608Fh.01 = 65,536`, `608Fh.02 = 1` (usually 1, except for non 1:1 gearing between motor and encoder)

**Note:**  
These values reflect hardware properties and should only be changed when changing hardware.

#### Configurable scaling (6091h and 6092h)

- 6091h: Gear Ratio**
  - `6091h.01h motor_revolutions`: Number of motor revolutions
  - `6091h.02h shaft_revolutions`: Number of output revolutions
  - Example: 5 motor revolutions per 2 output revolutions → `6091h.01h = 5`, `6091h.02h = 2`

- 6092h: Feed Constant**
  - `6092h.01h feed`: Technical unit per output revolution (e.g. mm, μm)
  - `6092h.02h shaft_revolutions`: Number of output revolutions
  - Example: Toothed belt axis with 100 mm per revolution, scale μm: `6092h.01h feed = 100,000`, `6092h.02h = 1`


#### Formulas for position scaling

| size | formula (linguistic) | formula (with CiA 402 objects) |
|--------------------------------------------|--------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| Encoder resolution | Encoder_resolution = encoder_increments / motor_rev | 608Fh.01h / 608Fh.02h |
| Gear ratio | Gear_ratio = motor_revolutions / shaft_revolutions | 6091h.01h / 6091h.02h |
| Feed constant | Feed_constant = feed / shaft_revolutions | 6092h.01h / 6092h.02h |
| Internal position unit | Pos_internal = Pos_user × Encoder_resolution × Gear_ratio / Feed_constant| Pos_user × (608Fh.01h / 608Fh.02h) × (6091h.01h / 6091h.02h) / (6092h.01h / 6092h.02h) |
| | | or: Pos_user × (608Fh.01h × 6091h.01h × 6092h.02h) / (608Fh.02h × 6091h.02h × 6092h.01h) |
| Position as user variable | Pos_user = Pos_internal × Feed_constant / (Encoder_resolution × Gear_ratio) | Pos_internal × (6092h.01h / 6092h.02h) / [ (608Fh.01h / 608Fh.02h) × (6091h.01h / 6091h.02h) ] |
| | | or: Pos_internal × (608Fh.02h × 6091h.02h × 6092h.01h) / (608Fh.01h × 6091h.01h × 6092h.02h) |

#### Example

Given:
- Motor encoder = 65,536 increments per motor revolution (`608Fh.01h = 65536`, `608Fh.02h = 1`)
- Gear ratio: 1 output revolution per 5 motor revolutions (`6091h.01h = 5`, `6091h.02h = 1`)
- Feed constant: 100 mm per output revolution (`6092h.01h = 100`, `6092h.02h = 1`)

Calculated:

User unit / user-defined unit per internal encoder increment 
= (Feed constant) / (Gear ratio × Encoder resolution) 
= (100 mm/rev) / (5 × 65,536 increments/rev) 
= 0.00030517578125 [mm / increment]

Example: Position is at 80,000 internal increments
Pos_user = 80,000 × 0.00030517578125 ≈ 24.41 mm

**Note:**  
- The values in 608Fh reflect hardware properties and should only be adjusted if the hardware changes.
- The scaling parameters (6091h, 6092h) must match the application and the desired unit.
- The unit of the feed constant (e.g. μm, mm, degree) determines the technical size for all position values that are exchanged via the CiA 402 objects.


### Glossary

| Term | Description |
|-------------------------------|-----------------------------------------------------------------------------------------------------|
| **CiA 301** | Communication profile defined by CAN in Automation (CiA), which specifies essential CANopen application layer services, protocols and communication objects (including NMT, PDO, SDO, SYNC, EMCY). Originally developed for CAN-based embedded systems, CiA 301 forms the basis of numerous device profiles, including CiA 402. It is also used in other communication technologies, in particular as \"CANopen over EtherCAT\" (CoE) from Beckhoff in EtherCAT systems. Specified in EN 50325-4. |
| **CiA 402 (DS 402)** | Device profile for electrical drives defined by CAN in Automation (CiA). It offers a universal interface and standardized behaviour for controlling different electrical drives (e.g. servo drives, frequency inverters). Originally part of the CANopen protocol as the "CANopen Device Profile", it is now also frequently used for EtherCAT, POWERLINK and TCP/IP. Defined in IEC61800-7-201 as a standardized profile for Power Drive Systems (PDS). |
| **CAN (Controller Area Network)** | Robust communication bus system fieldbus in the vehicle sector and automation. |
| **CANopen** | Communication protocol and device specification for automation.    |
| **CiA (CAN in Automation)** | International user and manufacturer association for the development and support of CAN-based protocols. |
| **Object Dictionary (OD)** | Standardized table for organizing communication and device parameters of a CANopen device. |
| **SDO Service Data Object** | protocol for peer-to-peer communication and parameter access in CANopen networks.            |
| **PDO (Process Data Object)** | Time-critical object for data transmission of process data in real time.             |
| **NMT (Network Management)** | Protocol for managing states (Initialization, Pre-Operational, Operational, Stopped) in CANopen.
| **SYNC object** | Synchronization object for node actions in the network.                          |
| **EMCY (Emergency Message)** | Object for immediate reporting of errors/faults to a controller.                 |
| **Drive state machine** | Standardized state machine (CiA 402) for controlling drive states and transitions.  |
| **Modes of operation** | Operating modes for motion control (position, speed, homing).|
| **TPDO/RPDO (Transmit/Receive PDO)** | Process Data Object format specification for transmitting/receiving data (TPDO/RPDO). |
| **Heartbeat/Node Guarding** | Mechanisms for node monitoring and error detection in the network.  |                   |
| **Controller** | Network controlling node, e.g. machine controller. Controls other nodes; acts as NMT controller and SDO client. |
| **Device** | Controlled node, e.g. a servo drive. Controlled by the controller; acts as NMT device and SDO server. |
| **SDO Client** | Services requesting node / controller. Requests data from the SDO server. |
| **SDO Server** | Node / device providing services. Responds to requests from the SDO client. |

**Example for clarification**:  
CANopen PC software such as Kickdrive acts as an NMT controller and SDO client, while a CANopen node, e.g. a servo drive, acts as an NMT device and SDO server.