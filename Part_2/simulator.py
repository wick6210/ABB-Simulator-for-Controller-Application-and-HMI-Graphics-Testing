import threading
import time
import serial

from pymodbus.server.sync import StartTcpServer
from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusSlaveContext,
    ModbusServerContext
)

FILL_RATE = 2
DRAIN_RATE = 1

HIGH_SETPOINT = 85
LOW_SETPOINT = 20

ALARM_HIGH_LVL = 95
ALARM_LOW_LVL = 5

TICK_S = 0.5

FILLING = 0
DRAINING = 1
ALARM_HIGH = 2
ALARM_LOW = 3
MANUAL = 4

SERIAL_PORT = "COM5"      # CHANGE THIS
BAUD = 115200


def serial_listener(context):
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD, timeout=1)

        print(f"Serial listening on {SERIAL_PORT}")

        while True:
            try:
                line = ser.readline().decode().strip()

                if not line:
                    continue

                print("RX:", line)

                if line.startswith("MODE:"):
                    value = int(line.split(":")[1])
                    context[0x00].setValues(3, 10, [value])

                elif line.startswith("PUMP:"):
                    value = int(line.split(":")[1])
                    context[0x00].setValues(3, 11, [value])

            except Exception as e:
                print("Serial error:", e)

    except Exception as e:
        print("Cannot open serial port:", e)


def run_fsm(context):

    state = FILLING
    level = 50.0

    while True:

        manual_mode = context[0x00].getValues(3, 10, 1)[0]
        manual_pump = context[0x00].getValues(3, 11, 1)[0]

        if manual_mode:
            state = MANUAL

        if state == MANUAL:

            pump = manual_pump
            alarm = 0

            if manual_mode == 0:
                state = (
                    FILLING
                    if level < HIGH_SETPOINT
                    else DRAINING
                )

        elif state == FILLING:

            pump = 1
            alarm = 0

            if level >= ALARM_HIGH_LVL:
                state = ALARM_HIGH

            elif level >= HIGH_SETPOINT:
                state = DRAINING

        elif state == DRAINING:

            pump = 0
            alarm = 0

            if level <= ALARM_LOW_LVL:
                state = ALARM_LOW

            elif level <= LOW_SETPOINT:
                state = FILLING

        elif state == ALARM_HIGH:

            pump = 0
            alarm = 1

            if level < HIGH_SETPOINT:
                state = DRAINING

        elif state == ALARM_LOW:

            pump = 1
            alarm = 2

            if level > LOW_SETPOINT:
                state = FILLING

        else:

            pump = 0
            alarm = 0

        if pump:
            level = min(100, level + FILL_RATE)
        else:
            level = max(0, level - DRAIN_RATE)

        context[0x00].setValues(3, 0, [int(level)])
        context[0x00].setValues(3, 1, [pump])
        context[0x00].setValues(3, 2, [state])
        context[0x00].setValues(3, 3, [alarm])

        time.sleep(TICK_S)


def main():

    block = ModbusSequentialDataBlock(0, [0] * 20)

    store = ModbusSlaveContext(hr=block)

    context = ModbusServerContext(
        slaves=store,
        single=True
    )

    context[0x00].setValues(3, 0, [50])

    threading.Thread(
        target=run_fsm,
        args=(context,),
        daemon=True
    ).start()

    threading.Thread(
        target=serial_listener,
        args=(context,),
        daemon=True
    ).start()

    print("Modbus TCP on localhost:5020")

    StartTcpServer(
        context=context,
        address=("localhost", 5020)
    )


if __name__ == "__main__":
    main()
