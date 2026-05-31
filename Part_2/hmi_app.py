import time
from collections import deque

import plotly.graph_objects as go
import streamlit as st
from pymodbus.client.sync import ModbusTcpClient

st.set_page_config(
    page_title="ABB Tank HMI",
    layout="wide"
)

MODBUS_HOST = "localhost"
MODBUS_PORT = 5020

STATE_NAMES = {
    0: "FILLING",
    1: "DRAINING",
    2: "ALARM HIGH",
    3: "ALARM LOW",
    4: "MANUAL OVERRIDE"
}

ALARM_NAMES = {
    0: "NONE",
    1: "HIGH LEVEL",
    2: "LOW LEVEL"
}

if "level_history" not in st.session_state:
    st.session_state.level_history = deque(maxlen=60)

if "time_history" not in st.session_state:
    st.session_state.time_history = deque(maxlen=60)


def read_all_registers():
    client = ModbusTcpClient(MODBUS_HOST, port=MODBUS_PORT)

    try:
        if client.connect():

            result = client.read_holding_registers(
                0,
                12,
                unit=1
            )

            if not result.isError():

                r = result.registers

                return {
                    "level": r[0],
                    "pump": r[1],
                    "state": r[2],
                    "alarm": r[3],
                    "manual_mode": r[10],
                    "pump_cmd": r[11],
                }

    except Exception as e:
        print("Read error:", e)

    finally:
        client.close()

    return None


# Read controller data FIRST
data = read_all_registers()


# Sidebar
with st.sidebar:

    st.title("Control Panel")

    st.info(
        "Manual controls are provided by "
        "the ESP8266 hardware buttons."
    )

    st.markdown("---")

    if data is not None:

        st.metric(
            "Manual Mode",
            "ON" if data["manual_mode"] else "OFF"
        )

        st.metric(
            "Pump Command",
            "ON" if data["pump_cmd"] else "OFF"
        )

    else:

        st.warning("Controller Offline")

    st.markdown("---")

    st.markdown("### Register Map")

    st.code(
        "HR[0]  → Tank Level (%)\n"
        "HR[1]  → Pump State\n"
        "HR[2]  → FSM State\n"
        "HR[3]  → Alarm Code\n"
        "HR[10] ← Manual Enable\n"
        "HR[11] ← Pump Command",
        language=None
    )

    st.markdown("---")

    st.caption(
        "ABB Simulator Project\n"
        "Controller ↔ HMI via Modbus TCP"
    )


st.title("ABB Tank Level Control System")

st.caption(
    "HMI Graphics Testing Interface — "
    "Simulator for Controller Application"
)

st.markdown("---")


if data is None:

    st.error(
        "Cannot connect to Controller Simulator.\n\n"
        "Run simulator.py first."
    )

    time.sleep(2)

    st.rerun()


else:

    st.session_state.level_history.append(
        data["level"]
    )

    st.session_state.time_history.append(
        time.strftime("%H:%M:%S")
    )

    if data["alarm"] > 0:

        st.error(
            f"ALARM ACTIVE: "
            f"{ALARM_NAMES[data['alarm']]} "
            f"— Tank at {data['level']}%"
        )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Tank Level",
            f"{data['level']}%"
        )

        st.progress(
            data["level"] / 100.0
        )

    with col2:

        st.metric(
            "Pump State",
            "ON" if data["pump"] else "OFF"
        )

    with col3:

        st.metric(
            "Controller FSM",
            STATE_NAMES.get(
                data["state"],
                "UNKNOWN"
            )
        )

    with col4:

        st.metric(
            "Alarm Status",
            ALARM_NAMES.get(
                data["alarm"],
                "UNKNOWN"
            )
        )

    st.markdown("---")

    st.markdown(
        "### Tank Level Trend "
        "(Live — Last 60 Samples)"
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=list(st.session_state.time_history),
            y=list(st.session_state.level_history),
            mode="lines",
            fill="tozeroy",
            name="Tank Level"
        )
    )

    fig.add_hline(
        y=95,
        line_dash="dash",
        annotation_text="High Alarm"
    )

    fig.add_hline(
        y=85,
        line_dash="dot",
        annotation_text="High Setpoint"
    )

    fig.add_hline(
        y=20,
        line_dash="dot",
        annotation_text="Low Setpoint"
    )

    fig.add_hline(
        y=5,
        line_dash="dash",
        annotation_text="Low Alarm"
    )

    fig.update_layout(
        height=350,
        yaxis=dict(
            range=[0, 100],
            title="Level (%)"
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.caption(
        f"Last updated: {time.strftime('%H:%M:%S')} | "
        f"Modbus TCP → localhost:{MODBUS_PORT}"
    )

    time.sleep(1)

    st.rerun()
