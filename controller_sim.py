import threading
import time
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext

FILL_RATE       = 2     # % per tick when pump is ON
DRAIN_RATE      = 1     # % per tick (simulated process consumption)
HIGH_SETPOINT   = 85    # % → pump turns OFF (tank considered full)
LOW_SETPOINT    = 20    # % → pump turns ON  (tank considered low)
ALARM_HIGH_LVL  = 95    # % → high alarm triggered
ALARM_LOW_LVL   = 5     # % → low alarm triggered
TICK_S          = 0.5   # FSM update interval in seconds

FILLING         = 0
DRAINING        = 1
ALARM_HIGH      = 2
ALARM_LOW       = 3
MANUAL          = 4

def run_fsm(context):
    state = FILLING
    level = 50.0    # Start at 50% — middle of operating range

    while True:
        manual_mode     = context[0x00].getValues(3, 10, 1)[0]
        manual_pump_cmd = context[0x00].getValues(3, 11, 1)[0]

        if manual_mode == 1:
            state = MANUAL

        if state == MANUAL:
            pump  = manual_pump_cmd
            alarm = 0
            # Return to auto if HMI releases manual mode
            if manual_mode == 0:
                state = FILLING if level < HIGH_SETPOINT else DRAINING

        elif state == FILLING:
            pump  = 1
            alarm = 0
            if level >= ALARM_HIGH_LVL:
                state = ALARM_HIGH
            elif level >= HIGH_SETPOINT:
                state = DRAINING

        elif state == DRAINING:
            pump  = 0
            alarm = 0
            if level <= ALARM_LOW_LVL:
                state = ALARM_LOW
            elif level <= LOW_SETPOINT:
                state = FILLING

        elif state == ALARM_HIGH:
            pump  = 0
            alarm = 1   # High alarm code
            if level < HIGH_SETPOINT:
                state = DRAINING
                alarm = 0

        elif state == ALARM_LOW:
            pump  = 1
            alarm = 2   # Low alarm code
            if level > LOW_SETPOINT:
                state = FILLING
                alarm = 0

        else:
            # Fallback — should never hit this
            pump  = 0
            alarm = 0

        if pump == 1:
            level = min(100.0, level + FILL_RATE)
        else:
            level = max(0.0,   level - DRAIN_RATE)

        context[0x00].setValues(3, 0, [int(level)])   # HR[0] tank level
        context[0x00].setValues(3, 1, [pump])          # HR[1] pump state
        context[0x00].setValues(3, 2, [state])         # HR[2] FSM state
        context[0x00].setValues(3, 3, [alarm])         # HR[3] alarm code

        time.sleep(TICK_S)


def main():
    block   = ModbusSequentialDataBlock(0, [0] * 20)
    store   = ModbusSlaveContext(hr=block)
    context = ModbusServerContext(slaves=store, single=True)

    context[0x00].setValues(3, 0, [50])

    fsm_thread = threading.Thread(target=run_fsm, args=(context,), daemon=True)
    fsm_thread.start()

    print("=" * 55)
    print("  ABB Controller Simulator — Modbus TCP Server")
    print("  Listening on localhost:5020")
    print("  FSM running. Tank starts at 50%.")
    print("  Ctrl+C to stop.")
    print("=" * 55)

    # Blocking call — server runs until Ctrl+C
    StartTcpServer(context=context, address=("localhost", 5020))


if __name__ == "__main__":
    main()
