# PyModBus

## What It Is:

Implements modbus protocol, 1979, used a lot in industrial autmomation, PLC's functioning

## The Modbus Basics:

* Coils               -    Digital Outputs  :    Read/Write, Binary
* Discrete Inputs     -    Digital Inputs   :    Read, Binary
* Input Registers     -    Analog Inputs    :    Read, 16 bit numbers
* Holding Registers   -    Analog Outputs   :    Read/Write, 16 bit numbers

Manipulation can be done by network cables (Modbus TCP) or serial lines (Modbus RTU/ASCII)

## How It Works As A Controller (Client / Master):

* Initiation   :    Program opens a connection to a physical device via IP Address or Serial Port.
* Request      :    The script requests for data from the device by calling its device ID.
* Processing   :    PyModBus serialises the request into binary packet format that the device expects.
* Response     :    The device gets the request and sends the required data back to the program.

## How It Works As A Simulator (Server / Slave):

This simulates the conditions and working of an Industrial PLC to convert the laptop into a virtual PLC.

* Memory Setup         :    A virtual data store is defined in Python. PyModBus allocates virtual memory for Coils, Holding Registers, Input Registers, Discrete Inputs, etc.
* Starting The Server  :    Launch a background loop that listens on Modbus Port 502 (Using Pythons asyncio).
* Simulation Loop      :    A parallel Python thread simulates real-world behaviour.
* External Interaction :    Any external hardware can connect to the Python Script, and reads the registers.

## Why PyModBus?

Asynchronous Core :    Built on asyncio, meaning a single simulator can handle thousands of concurrent connections effortlessly.
Dual Role         :    A single Python script can act as both a client (gatherer) and a server (deliverer).
Abstraction       :    CRC and Checksums Are handled by the library, so no extra load on frame formatting.

## Further Technical Details

Please do reference this GitHub Repository for more information based on PyModBus.

https://github.com/pymodbus-dev/pymodbus