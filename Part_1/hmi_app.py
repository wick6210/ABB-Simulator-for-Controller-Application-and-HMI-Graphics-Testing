import time
from collections import deque

import plotly.graph_objects as go
import streamlit as st
from pymodbus.client import ModbusTcpClient

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
    0: " NONE",
    1: " HIGH LEVEL",
    2: " LOW LEVEL"
}

if "level_history" not in st.session_state:
    st.session_state.level_history = deque(maxlen=60)
if "time_history" not in st.session_state:
    st.session_state.time_history = deque(maxlen=60)

def read_all_registers() -> dict | None:
    """Connect, read HR[0..11], disconnect. Returns dict or None on failure."""
    client = ModbusTcpClient(MODBUS_HOST, port=MODBUS_PORT)
    try:
        if client.connect():
            result = client.read_holding_registers(address=0, count=12, slave=1)
            if not result.isError():
                r = result.registers
                return {
                    "level":      r[0],
                    "pump":       r[1],
                    "state":      r[2],
                    "alarm":      r[3],
                    "manual_mode": r[10],
                    "pump_cmd":   r[11],
                }
    except Exception:
        pass
    finally:
        client.close()
    return None


def write_register(address: int, value: int) -> None:
    client = ModbusTcpClient(MODBUS_HOST, port=MODBUS_PORT)
    try:
        if client.connect():
            client.write_register(address=address, value=value, slave=1)
    except Exception:
        pass
    finally:
        client.close()

with st.sidebar:
    st.title(" Control Panel")
    st.markdown("---")

    manual_mode = st.toggle(" Manual Override")

    if manual_mode:
        write_register(10, 1)   # HR[10] = manual enable
        st.markdown("**Pump Command:**")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button(" ON", use_container_width=True):
                write_register(11, 1)
        with col_b:
            if st.button(" OFF", use_container_width=True):
                write_register(11, 0)
        st.info("You have direct control of the pump.")
    else:
        write_register(10, 0)   # HR[10] = auto mode
        st.success("Controller running in AUTO mode.")

    st.markdown("---")
    st.markdown("** Register Map**")
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
    st.caption("ABB Simulator Project\nController ↔ HMI via Modbus TCP")

st.title(" ABB Tank Level Control System")
st.caption("HMI Graphics Testing Interface — Simulator for Controller Application")
st.markdown("---")

# Read live data
data = read_all_registers()

if data is None:
    st.error(
        " **Cannot connect to Controller Simulator.**  \n"
        "Run `python controller_sim.py` in another terminal first."
    )
    st.info("Retrying in 2 seconds...")
    time.sleep(2)
    st.rerun()

st.session_state.level_history.append(data["level"])
st.session_state.time_history.append(time.strftime("%H:%M:%S"))

if data["alarm"] > 0:
    st.error(
        f" **ALARM ACTIVE:** {ALARM_NAMES[data['alarm']]}  "
        f"— Tank at {data['level']}%"
    )

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label=" Tank Level",
        value=f"{data['level']}%",
    )
    # Visual level bar coloured by zone
    level_norm = data["level"] / 100
    if data["alarm"] > 0:
        bar_color = "red"
    elif data["level"] >= 85 or data["level"] <= 20:
        bar_color = "orange"
    else:
        bar_color = "normal"
    st.progress(level_norm)

with col2:
    pump_label = " ON" if data["pump"] else " OFF"
    st.metric(label=" Pump State", value=pump_label)

with col3:
    st.metric(
        label=" Controller FSM",
        value=STATE_NAMES.get(data["state"], "UNKNOWN")
    )

with col4:
    st.metric(
        label=" Alarm Status",
        value=ALARM_NAMES.get(data["alarm"], "?")
    )

st.markdown("---")

st.markdown("###  Tank Level Trend (Live — Last 60 ticks)")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=list(st.session_state.time_history),
    y=list(st.session_state.level_history),
    mode="lines",
    fill="tozeroy",
    name="Tank Level",
    line=dict(color="#0057A8", width=2),
    fillcolor="rgba(0, 87, 168, 0.15)"
))

# Setpoint reference lines
fig.add_hline(y=95, line_dash="dash", line_color="red",    annotation_text="High Alarm (95%)",    annotation_position="top left")
fig.add_hline(y=85, line_dash="dot",  line_color="orange", annotation_text="High Setpoint (85%)", annotation_position="top left")
fig.add_hline(y=20, line_dash="dot",  line_color="gold",   annotation_text="Low Setpoint (20%)",  annotation_position="bottom left")
fig.add_hline(y=5,  line_dash="dash", line_color="red",    annotation_text="Low Alarm (5%)",      annotation_position="bottom left")

fig.update_layout(
    yaxis=dict(range=[0, 100], title="Level (%)", gridcolor="#2a2a2a"),
    xaxis=dict(title="Time", gridcolor="#2a2a2a"),
    height=350,
    margin=dict(l=0, r=0, t=20, b=0),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#cccccc"),
)

st.plotly_chart(fig, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.caption(f" Last updated: {time.strftime('%H:%M:%S')}  |  Auto-refresh: 1s  |  Modbus TCP → localhost:{MODBUS_PORT}")

# ── Auto-refresh ──────────────────────────────────────────────────────────────
time.sleep(1)
st.rerun()
