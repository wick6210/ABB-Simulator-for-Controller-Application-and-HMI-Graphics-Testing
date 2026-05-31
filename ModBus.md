# ModBus

## Introduction

ModBus is a messaging structure that establishes master-slave configurations between various 'intelligent' devices. 
The message contains the slave ID, a command (R/W), the data and the checksum (LRC/CRC).
Since it is a messaging structure, it is independent of the underlying hardware.
It works on a Request/Response format.

### Request

The master communicates to the slave with a message/function code containing the slave ID, a command (R/W), data necessary to complete the command (data to write, or registers to read from), and a checksum to verify the integrity of the message.

### Response

The slave receives the message, and after verifying CRC/LRC, the slave executes the command. If the CRC/LRC is not verified then the slave changes the function code to indicate the error that has occured. Similarly, if during the command execution, there is an error in data / lack of data, the function code is changed to indicate the error that has occurred.

Controllers can be set up in ACSII or RTU Mode.

## ASCII Mode

ASCII stands for American Standard Code for Information Interchange.
When controllers are setup to communicate on ModBus in ASCII Mode, each 8-bit byte in a message is sent as 2 ASCII characters. This allows time intervals of up to 1 second to occur between characters without causing an error.  

Basically, in older radio systems and legacy hardware, sending the data in bit form was not so efficient, and caused errors, since there was no demarcation of start and end. Rather, it was just timing, and this timing would be just mere millisecond of silence for the receiver to determine the end of the message. However, when there was instances of jitter or noise or even a slight delay in transmission, this would result in the loss of data due to timing differences between the transmission and the reception stages.  

In contrast, ASCII Mode required every message to start with a colon, `:`, and to end with `CRLF`[Carriage Return Line Feed]. The Master would usually set the interval time of 1 second, which meant that any message could be delayed by up to 1 second before the receiver flags an error / end of reception.

## RTU Mode

RTU stands for Remote Terminal Unit.
When controllers are setup to communicate on ModBus in RTU Mode, each 8-bit byte in a message is sent as 2 4-bit hexadecimal characters. The main advantage is that with more bit density, there is better throughput than that of ASCII Mode at the same baud rate. However, each message must be transmitted in a continuous stream, without much delay. Let it be noted that the hexadecimal notation is what is represented for human readability, but that in real life, binary values are set as is on the communication line.  

Messages start with a silent interval of at least 3.5 character times. Similarly, a silence interval of around 3.5 character times is considered as the end of the message. If a message is received before 3.5 character times interval of delay, then it is considered as a continuation of the current message. If it is greater than 3.5 character times interval of delay, then it is considered as a new message.

## Example

Suppose we wish to send the code value of `4B`.

In ASCII Mode, we send `00110100` first [4], and then `01000010` next [B].  

In RTU Mode, we send `01001011` once, which translates to 4B in hexadecimal code.

As we can see, for every byte of data, ASCII Mode transmits 2 bytes of data, whereas RUT Mode transmits 1 byte of data. Hence, we sttribute character density, better throughput and lower bandwidth consumption to the ModBus RTU Mode over the ModBus ASCII Mode.

## Comparison

As seen above, RTU Mode is better than ASCII Mode in terms of throughput, speed and character density. In modern industrial automation, high-speed data cables allow for better use of the ModBus RTU Mode of message structure, and thus the ASCII Mode has been dropped off in the modern industry.
However, in legacy systems and older communication systems, the ModBus ASCII Mode is preferred due to its clear demarcation of the start and end of a message, allowing for better noise immunity than the ModBus RTU Mode.


## References

For an even more detailed explanation of the ModBus Protocol, please do refer to the link below.

https://www.modbustools.com/modbus.html
